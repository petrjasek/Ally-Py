'''
Created on Oct 9, 2013

@package: gui core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Gociu

Provides the synchronization with the database for accesses.
'''
from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.design.processor.attribute import requires
from ally.design.processor.context import Context
from ally.design.processor.execution import Chain
from ally.design.processor.handler import HandlerProcessor, Handler
from ally.support.util_context import listBFS, hasAttribute
import logging
from acl.api.access import generateId
from acl.api.group import IGroupService
from security.api.right import IRightService
from acl.api.acl import IAclPrototype

from functools import reduce

# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Solicit(Context):
    '''
    The solicit context.
    '''
    # ---------------------------------------------------------------- Required
    repository = requires(Context)

class Repository(Context):
    '''
    The repository context.
    '''
    # ---------------------------------------------------------------- Required
    children = requires(list)
    accesses = requires(list)
    
class Access(Context):
    '''
    The access container context.
    '''
    # ---------------------------------------------------------------- Required
    filters = requires(list)
    methods = requires(list)
    urls = requires(list)
    lineNumber = requires(int)
    colNumber = requires(int)
    uri = requires(str)

# --------------------------------------------------------------------

@injected
class SynchronizeCategoryAccessHandler(HandlerProcessor):
    '''
    Base implementation for a processor that synchronizes the accesses in the configuration file with the database.
    '''
    
    default_access_methods = ['GET']; wire.config('default_access_methods', doc='''
    The default access methods (will be used if no methods are provided for an access). 
    ''')
    accessCategoryService = IAclPrototype; wire.entity('accessCategoryService')
    
    def __init__(self, Repository):
        super().__init__(Repository=Repository, Access=Access)
    
    def syncEntityAccessesWithDb(self, entityAccesses, entityIdNameMapping=None):
        '''
        Method to synchronize entity accesses from the configuration file with the database.
        @param entityAccesses: mapping entityId : list of accesses 
        '''
        if entityIdNameMapping is None: entityIdNameMapping = {}
        for entityId, accesses in entityAccesses.items():
            accessesFromDb = set(self.accessCategoryService.getAccesses(entityId))
            
            #keep a record of Acls added so far to avoid adding the same acl twice or adding a different filter for a acl
            #this can happen due to right inheritance
            addedAccesses = set()
            
            for accessData in accesses:
                assert isinstance(accessData, Access), 'Invalid access data %s' % accessData
                
                if not accessData.urls: continue
                if not accessData.methods: accessData.methods = self.default_access_methods
                #a list of tuples containing all combinations of methods and urls
                urlsMethods = [(url, method) for url in accessData.urls for method in accessData.methods]
                
                filters = accessData.filters
                if not filters: filters = [None]
                unusedFilters = set(f for f in filters if f)
                
                for filter in filters:
                    for url, method in urlsMethods:
                            accessId = generateId(url.replace('#', '*'), method)
                            if accessId in addedAccesses:
                                unusedFilters.clear() #avoid displaying unnecessary filter errors for inherited accesses
                                continue
                            accessesFromDb.discard(accessId)
                            
                            try:
                                self.accessCategoryService.remAcl(entityId, accessId)
                                self.accessCategoryService.addAcl(entityId, accessId)
                                addedAccesses.add(accessId)
                            except:
                                log.warning('Unknown access \'%s\' for method \'%s\' defined in category \'%s\' in file \'%s\' at line \'%s\' column \'%s\' ',
                                            url, method, entityIdNameMapping.get(entityId, entityId), accessData.uri, accessData.lineNumber, accessData.colNumber)
                            else:
                                try:
                                    if filter and self.accessCategoryService.registerFilter(entityId, accessId, filter, url):
                                        unusedFilters.discard(filter)
                                except:
                                    log.warning('Unknown filter \'%s\' in category \'%s\' in file \'%s\' at line \'%s\' column \'%s\'', 
                                                filter, entityIdNameMapping.get(entityId, entityId), accessData.uri, accessData.lineNumber, accessData.colNumber)
                if unusedFilters:
                    log.warning('Filters (%s) do not apply to any of the access URLs (%s) defined in category \'%s\' in file \'%s\' at line \'%s\' column \'%s\' ',
                                reduce(lambda x, y: '\'%s\',\'%s\'' % (x,y), unusedFilters), 
                                reduce(lambda x, y: '\'%s\',\'%s\'' % (x,y), accessData.urls),
                                entityIdNameMapping.get(entityId, entityId), 
                                accessData.uri, accessData.lineNumber, accessData.colNumber)
                
            #now remove from db the accesses that are no longer present in the configuration files
            for accessId in accessesFromDb:
                self.accessCategoryService.remAcl(entityId, accessId)
    
    def groupAccesses(self, repositories, Repository, idAttr):
        '''
        For a list of repositories, groups the accesses by some Id attribute.
        @return: mapping Id : list of actions
        '''
        groupAccesses = {}
        for repository in repositories:
            assert isinstance(repository, Repository), 'Invalid repository %s' % repository
            assert hasAttribute(Repository, idAttr.__name__), 'Invalid repository %s' % repository
            accesses = groupAccesses.get(getattr(repository, idAttr.__name__))
            if not accesses: groupAccesses[getattr(repository, idAttr.__name__)] = repository.accesses
            else: accesses.extend(repository.accesses)
        
        return groupAccesses

class RepositoryGroup(Repository):
    '''
    The repository context.
    '''
    # ---------------------------------------------------------------- Required
    groupName = requires(str)
    
@injected
@setup(Handler, name='synchronizeGroupAccesses')
class SynchronizeGroupAccessHandler(SynchronizeCategoryAccessHandler):
    '''
    Implementation for a processor that synchronizes the group accesses in the configuration file with the database.
    '''
    
    accessCategoryService = IGroupService; wire.entity('accessCategoryService')
    
    def __init__(self):
        assert isinstance(self.accessCategoryService, IGroupService), \
        'Invalid group service %s' % self.accessCategoryService
        super().__init__(RepositoryGroup)
        
    def process(self, chain, solicit:Solicit, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Synchronize the group accesses in the configuration file with the accesses in the database.
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(solicit, Solicit), 'Invalid solicit %s' % solicit
        assert isinstance(solicit.repository, RepositoryGroup), 'Invalid repository %s' % solicit.repository
        
        groups = listBFS(solicit.repository, RepositoryGroup.children, RepositoryGroup.groupName)
        #first group the accesses by group name: groupName -> [accesses]
        groupAccesses = self.groupAccesses(groups, RepositoryGroup, RepositoryGroup.groupName)
        self.syncEntityAccessesWithDb(groupAccesses)


class RepositoryRight(Repository):
    '''
    The repository context.
    '''
    # ---------------------------------------------------------------- Required
    rightName = requires(str)
    rightId = requires(int)

@injected
@setup(Handler, name='synchronizeRightAccesses')
class SynchronizeRightAccessHandler(SynchronizeCategoryAccessHandler):
    '''
    Implementation for a processor that synchronizes the right accesses in the configuration file with the database.
    '''
    
    accessCategoryService = IRightService; wire.entity('accessCategoryService')
    
    def __init__(self):
        assert isinstance(self.accessCategoryService, IRightService), \
        'Invalid right service %s' % self.accessCategoryService
        super().__init__(RepositoryRight)
        
    def process(self, chain, solicit:Solicit, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Synchronize the accesses in the configuration file with the accesses in the database.
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(solicit, Solicit), 'Invalid solicit %s' % solicit
        assert isinstance(solicit.repository, RepositoryRight), 'Invalid repository %s' % solicit.repository
        
        rights = listBFS(solicit.repository, RepositoryRight.children, RepositoryRight.rightId)
        #first group the accesses by right id: rightId -> [accesses]
        idNameMapping = self.getIdNameMapping(rights, RepositoryRight, RepositoryRight.rightId, RepositoryRight.rightName)
        rightAccesses = self.groupAccesses(rights, RepositoryRight, RepositoryRight.rightId)
        self.syncEntityAccessesWithDb(rightAccesses, idNameMapping)
    
    def getIdNameMapping(self, repositories, Repository, idAttr, nameAttr):
        '''
        Creates mapping rightId : rightName for the given repositories. 
        '''
        idNameMapping = {}
        for repository in repositories:
            assert isinstance(repository, Repository), 'Invalid repository %s' % repository
            assert hasAttribute(Repository, idAttr.__name__), 'Invalid repository %s' % repository
            assert hasAttribute(Repository, nameAttr.__name__), 'Invalid repository %s' % repository
            idNameMapping[getattr(repository, idAttr.__name__)] = getattr(repository, nameAttr.__name__)
        
        return idNameMapping
        
    