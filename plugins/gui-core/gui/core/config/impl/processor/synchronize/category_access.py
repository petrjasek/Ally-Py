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
    
class AccessData(Context):
    '''
    The access container context.
    '''
    # ---------------------------------------------------------------- Required
    filters = requires(list)
    methods = requires(list)
    urls = requires(list)
    lineNumber = requires(int)
    colNumber = requires(int)

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
        super().__init__(Repository=Repository)
    
    def syncEntityAccessesWithDb(self, entityAccesses):
        '''
        Method to synchronize entity accesses from the configuration file with the database.
        @param entityAccesses: mapping entityId : list of accesses 
        '''
        for entity, accesses in entityAccesses.items():
            accessesFromDb = set(self.accessCategoryService.getAccesses(entity))
            
            for accessData in accesses:
                assert isinstance(accessData, AccessData), 'Invalid access data %s' % accessData
                
                if not accessData.urls: continue
                if not accessData.methods: accessData.methods = self.default_access_methods
                #a list of tuples containing all combinations of methods and urls
                urlsMethods = [(url, method) for url in accessData.urls for method in accessData.methods]
                
                filters = accessData.filters
                if not filters: filters = [None]
                 
                for filter in filters:
                    for (url, method) in urlsMethods:
                            accessId = generateId(url.replace('#', '*'), method)
                            accessesFromDb.discard(accessId)
                            
                            try:
                                self.accessCategoryService.remAcl(entity, accessId)
                                self.accessCategoryService.addAcl(entity, accessId)
                                if filter:
                                    self.accessCategoryService.registerFilter(entity, accessId, filter)
                            except: log.warning('Invalid filter access: %s, %s, %s, %s, %s',
                                              entity, filter, url, method, accessId)
                            
            #now remove from db the accesses that are no longer present in the configuration files
            for accessId in accessesFromDb:
                self.accessCategoryService.remAcl(entity, accessId)
    
    def groupAccesses(self, repositories, Repository, idName):
        '''
        For a list of repositories, groups the accesses by some Id attribute.
        @return: mapping Id : list of actions
        '''
        groupAccesses = {}
        for repository in repositories:
            assert isinstance(repository, Repository), 'Invalid repository %s' % repository
            assert hasAttribute(Repository, idName), 'Invalid repository %s' % repository
            accesses = groupAccesses.get(getattr(repository, idName))
            if not accesses: groupAccesses[getattr(repository, idName)] = repository.accesses
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
        groupAccesses = self.groupAccesses(groups, RepositoryGroup, 'groupName')
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
        
        rights = listBFS(solicit.repository, RepositoryRight.children, RepositoryRight.rightName)
        #first group the accesses by right id: rightId -> [accesses]
        rightAccesses = self.groupAccesses(rights, RepositoryRight, 'rightId')
        self.syncEntityAccessesWithDb(rightAccesses)
    