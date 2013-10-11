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
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.execution import Chain
from ally.design.processor.handler import HandlerProcessor, Handler
from ally.support.util_context import listBFS
import logging
from acl.api.access import generateId
from acl.api.group import IGroupService
from security.api.right import IRightService

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
    groupName = requires(str)
    
class WithTracking(Context):
    '''
    Container for the tracking information.
    '''
    lineNumber = requires(int)
    colNumber = requires(int)
    
class AccessData(Context):
    '''
    The access container context.
    '''
    filters = defines(list)
    methods = defines(list)
    urls = defines(list)

class AccessDefinition(AccessData, WithTracking):
    '''
    The access container context with tracking info.
    '''

@injected
@setup(Handler, name='synchronizeAccesses')
class SynchronizeActionHandler(HandlerProcessor):
    '''
    Implementation for a processor that synchronizes the accesses in the configuration file with the database.
    '''
    
    groupService = IGroupService; wire.entity('groupService')
    rightService = IRightService; wire.entity('rightService')
    
    def __init__(self):
        assert isinstance(self.groupService, IGroupService), \
        'Invalid group service %s' % self.groupService
        super().__init__(Repository=Repository)
        
        # will keep a track of the warnings displayed to avoid displaying the same warning multiple times
        self._warnings = set()
        
    def process(self, chain, solicit:Solicit, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Synchronize the accesses in the configuration file with the accesses in the database.
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(solicit, Solicit), 'Invalid solicit %s' % solicit
        assert isinstance(solicit.repository, Repository), 'Invalid repository %s' % solicit.repository
        
        repositories = listBFS(solicit.repository, Repository.children, Repository.accesses)
        self.syncEntityAccessesWithDb(self.groupService, repositories)
        
        rightsDb = {r.Name: r.Id for r in [self.rightService.getById(id) for id in self.rightService.getAll()]}
        self.syncEntityAccessesWithDb(self.rightService, repositories, rightsDb)
    
    def syncEntityAccessesWithDb(self, service, repositories, entitiesDb=None):
        '''
        Method to synchronize entity accesses from the configuration file with the database.
        @param service: the service for the entity to be synchronized 
        @param repositories: list of repositories containing the entity data from the configuration files
        @param entitiesDb: mapping entityName : entityId; if it's not provided, will assume entityName = entityId 
        '''
        if entitiesDb is None: entitiesDb = {}
        
        for repository in repositories:
            assert isinstance(repository, Repository), 'Invalid repository %s' % repository
            
            accessesFromDb = set(service.getAccesses(entitiesDb.get(repository.groupName, repository.groupName)))
            
            for accessData in repository.accesses:
                assert isinstance(accessData, AccessData), 'Invalid access data %s' % accessData
                
                if not accessData.urls: continue
                if not accessData.methods: accessData.methods = ['GET'] 
                #a list of tuples containing all combinations of methods and urls
                urlsMethods = [(url, method) for url in accessData.urls for method in accessData.methods]
                
                filters = accessData.filters
                if not filters: filters = [None]
                 
                for filter in filters:
                    for (url, method) in urlsMethods:
                            accessId = generateId(url.replace('#', '*'), method)
                            accessesFromDb.discard(accessId)
                            
                            try:
                                service.remAcl(entitiesDb.get(repository.groupName, repository.groupName), accessId)
                                service.addAcl(entitiesDb.get(repository.groupName, repository.groupName), accessId)
                                if filter:
                                    service.registerFilter(entitiesDb.get(repository.groupName, repository.groupName), 
                                                           accessId, filter)
                            except: log.warning('Invalid filter access: %s, %s, %s, %s, %s',
                                              repository.groupName, filter, url, method, accessId)
                            
            #now remove from db the accesses that are no longer present in the configuration files
            for accessId in accessesFromDb:
                service.remAcl(entitiesDb.get(repository.groupName, repository.groupName), accessId)
