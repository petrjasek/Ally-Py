'''
Created on Oct 9, 2013

@package: gui core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Gociu

Provides the synchronization with the database for accesses.
'''
from functools import reduce

from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.design.processor.attribute import requires, defines
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
    # ---------------------------------------------------------------- Defines
    syncAccesses = defines(dict)
    
    # ---------------------------------------------------------------- Required
    repository = requires(Context)

class Repository(Context):
    '''
    The repository context.
    '''
    # ---------------------------------------------------------------- Required
    children = requires(list)
    accesses = requires(list)

#TODO: separate db sync for accesses and compensates
class SyncAccess(Context):
    # ---------------------------------------------------------------- Defines
    #category info
    categoryName = defines(str)
    
    #access info
    accessId = defines(int)
    url = defines(str)
    method = defines(str)
    filter = defines(str)
    
    #compensates info
    compensates = defines(dict)
    
    #tracking info
    uri = defines(str)
    line = defines(int)
    column = defines(int)


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

class URL(Context):
    # ---------------------------------------------------------------- Required
    url = requires(str)
    compensates = requires(list)

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
    #TODO: make sure accessCategoryService is also ICompensatePrototype
    
    def __init__(self, Repository):
        super().__init__(Repository=Repository, Access=Access, URL=URL, SyncAccess=SyncAccess)
    
    def createSyncAccesses(self, SyncAccess, entityAccesses, entityIdNameMapping=None):
        if entityIdNameMapping is None: entityIdNameMapping = {}
        
        return {entityId: self.filterSyncAccesses(self.categorySyncAccesses(SyncAccess, entityIdNameMapping.get(entityId, entityId), accesses))
                for entityId, accesses in entityAccesses.items()}
    
    def categorySyncAccesses(self, SyncAccess, categoryName, accesses):
        if not accesses: return []
        return [self.createSyncAccess(SyncAccess, categoryName, filter, url, method, compensates, 
                                          (access.uri, access.lineNumber, access.colNumber))
                    for access in accesses
                    for filter,url,method,compensates in self.getFiltersUrlsMethods(access)]
        
    def createSyncAccess(self,SyncAccess, categoryName, filter, url, method, compensates, trackingInfo):
        accessId = generateId(url.strip('/').replace('#', '*'), method)
        if compensates:
            compensateIds = {generateId(compensate.strip('/').replace('#', '*'), method):compensate for compensate in compensates}
        else: compensateIds = None
        
        access = SyncAccess()
        assert isinstance(access, SyncAccess), 'Invalid sync access context %s' % access
        access.categoryName = categoryName
        access.accessId = accessId
        access.url = url; access.method = method; access.filter = filter
        access.compensates = compensateIds
        uri, line, column = trackingInfo
        access.uri = uri; access.line = line; access.column = column
        return access
    
    def getFiltersUrlsMethods(self, access):
        assert isinstance(access, Access), 'Invalid access context %s' % access
            
        if not access.urls: return []
        if not access.methods: access.methods = self.default_access_methods
        
        filters = access.filters if access.filters else [None]
        #a list of tuples containing all combinations of filters, methods and urls
        return [(filter, url.url, method, url.compensates) for filter in filters for url in access.urls 
                for method in access.methods]

    
    def syncAccessesWithDb(self, syncAccesses):
        for categoryId, accesses in syncAccesses.items():
            self.syncCategoryAccesses(categoryId, accesses)
            
    def syncCategoryAccesses(self, categoryId, accesses):
        accessesFromDb = set(str(accessId) for accessId in self.accessCategoryService.getAccesses(categoryId))
        accessesFromConfig = set(access.accessId for access in accesses)
        
        toAdd = [access for access in accesses if access.accessId in accessesFromConfig.difference(accessesFromDb)]
        toDelete = [access for access in accesses if access.accessId in accessesFromDb.difference(accessesFromConfig)]
        
        addedFilters = set(access.filter for access in toAdd if self.addCategoryAccess(categoryId, access) and 
                        self.addAccessFilter(categoryId, access))
        unusedFilters = set(access.filter for access in toAdd if access.filter).difference(addedFilters)
        
        if unusedFilters:
            urls = set([access.url for access in toAdd])
            categoryName, uri, line, column = accesses[0].categoryName, accesses[0].uri, accesses[0].line, accesses[0].column 
            log.warning('Filters (%s) do not apply to any of the access URLs (%s) defined in category \'%s\' in file \'%s\' at line \'%s\' column \'%s\' ',
                        reduce(lambda x, y: '\'%s\',\'%s\'' % (x,y), unusedFilters), 
                        reduce(lambda x, y: '\'%s\',\'%s\'' % (x,y), urls),
                        categoryName, uri, line, column)
        
        for access in toDelete: self.accessCategoryService.remAcl(categoryId, access.accessId)
        
    def addCategoryAccess(self, categoryId, access):
        try:
            self.accessCategoryService.remAcl(categoryId, access.accessId)
            self.accessCategoryService.addAcl(categoryId, access.accessId)
            return True
        except:
            #TODO: there is a bug here, for Anonymous accesses
            log.warning('Unknown access \'%s\' for method \'%s\' defined in category \'%s\' in file \'%s\' at line \'%s\' column \'%s\' ',
                        access.url, access.method, access.categoryName, access.uri, access.line, access.column)
            return False
    
    def addAccessFilter(self, categoryId, access):
        try:
            if access.filter:
                return self.accessCategoryService.registerFilter(categoryId, access.accessId, access.filter, access.url)
            return False
        except:
            log.warning('Unknown filter \'%s\' in category \'%s\' in file \'%s\' at line \'%s\' column \'%s\'', 
                        access.filter, access.categoryName, access.uri, access.line, access.column)
            return False
    
    
    def syncCompensatesWithDb(self, syncAccesses):
        for categoryId, accesses in syncAccesses.items():
            for access in accesses: self.syncAccessCompensates(categoryId, access)
    
    def syncAccessCompensates(self, category, access):
        '''
        Method to synchronize access compensates from the configuration file with the database.
        '''
        if not access.compensates: return
        
        compensatesDb = set(compensate.Access for compensate in self.accessCategoryService.getCompensates(category, access.accessId))
        compensatesConfig = set(cid for cid in access.compensates.keys())
        
        toAdd = compensatesConfig.difference(compensatesDb)
        toDelete = compensatesDb.difference(compensatesConfig)
        
        for compensateId in toAdd:
            try:
                self.accessCategoryService.addCompensate(category, access.accessId, compensateId)
            except:
                log.warning('Unknown compensate \'%s\' for method \'%s\' defined in category \'%s\' in file \'%s\' at line \'%s\' column \'%s\' ',
                           access.compensates.get(compensateId), access.method, access.categoryName, access.uri, access.line, access.column)
        
        #remove the remaining compensates
        for compensateId in toDelete:
            self.accessCategoryService.remCompensate(category, access.accessId, compensateId)
        
    
    def syncEntityAccessesWithDb_old(self, entityAccesses, entityIdNameMapping=None):
        '''
        Method to synchronize entity accesses from the configuration file with the database.
        @param entityAccesses: mapping entityId : list of accesses 
        '''
        if entityIdNameMapping is None: entityIdNameMapping = {}
        for entityId, accesses in entityAccesses.items():
            if not accesses: continue
            accessesFromDb = set(self.accessCategoryService.getAccesses(entityId))
            
            #keep a record of Acls added so far to avoid adding the same acl twice or adding a different filter for a acl
            #this can happen due to right inheritance
            addedAccesses = set()
            
            for accessData in accesses:
                assert isinstance(accessData, Access), 'Invalid access data %s' % accessData
                
                if not accessData.urls: continue
                if not accessData.methods: accessData.methods = self.default_access_methods
                #a list of tuples containing all combinations of methods and urls
                urlsMethods = [(url.url, method, url.compensates) for url in accessData.urls for method in accessData.methods]
                
                filters = accessData.filters
                if not filters: filters = [None]
                unusedFilters = set(f for f in filters if f)
                
                for filter in filters:
                    for url, method, compensates in urlsMethods:
                        accessId = generateId(url.rstrip('/').strip('/').replace('#', '*'), method)
                        if compensates:
                            compensateIds = {generateId(compensate.rstrip('/').strip('/').replace('#', '*'), method):compensate for compensate in compensates}
                        else: compensateIds = {}
                        
                        if accessId in addedAccesses:
                            unusedFilters.clear() #avoid displaying unnecessary filter errors for inherited accesses
                            continue
                        
                        accessesFromDb.discard(accessId)
                        
                        try:
                            self.accessCategoryService.remAcl(entityId, accessId)
                            self.accessCategoryService.addAcl(entityId, accessId)
                            addedAccesses.add(accessId)
                            #also sync compensates for this access (if any)
                            trackingInfo = (method, entityIdNameMapping.get(entityId, entityId), accessData.uri, \
                                            accessData.lineNumber, accessData.colNumber)
                            self.syncCompensates(entityId, accessId, compensateIds, trackingInfo)
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

    def filterSyncAccesses(self, accesses):
        '''
        Will discard duplicates (comparing accessId attribute) from a list of SyncAccess contexts 
        '''
        filtered = []
        existing = set()
        for access in accesses:
            if access.accessId in existing: continue
            filtered.append(access)
            existing.add(access.accessId)
            
        return filtered
    
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
        
        if not solicit.syncAccesses: solicit.syncAccesses = {}
        solicit.syncAccesses.update(self.createSyncAccesses(chain.arg.SyncAccess, groupAccesses))


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
        
        if not solicit.syncAccesses: solicit.syncAccesses = {}
        solicit.syncAccesses.update(self.createSyncAccesses(chain.arg.SyncAccess, rightAccesses, idNameMapping))
        
        #TODO: move this to another processor
        self.syncAccessesWithDb(solicit.syncAccesses)
        self.syncCompensatesWithDb(solicit.syncAccesses)
        
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
        
    