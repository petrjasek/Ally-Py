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
    rightName = requires(str)
    
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
class SynchronizeAccessHandler(HandlerProcessor):
    '''
    Base implementation for a processor that synchronizes the accesses in the configuration file with the database.
    '''
    def __init__(self):
        super().__init__(Repository=Repository)
    
    #TODO: don't send service as parameter; add it to this class and overwrite it in child classes
    def syncEntityAccessesWithDb(self, service, entityAccesses):
        '''
        Method to synchronize entity accesses from the configuration file with the database.
        @param service: the service for the entity to be synchronized 
        @param entityAccesses: mapping entityId : list of accesses 
        '''
        for entity, accesses in entityAccesses.items():
            accessesFromDb = set(service.getAccesses(entity))
            
            for accessData in accesses:
                assert isinstance(accessData, AccessData), 'Invalid access data %s' % accessData
                
                if not accessData.urls: continue
                #TODO: add GET to a list of configurations and get it with wire
                #defaults_methods = wire.config...
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
                                service.remAcl(entity, accessId)
                                service.addAcl(entity, accessId)
                                if filter:
                                    service.registerFilter(entity, accessId, filter)
                            except: log.warning('Invalid filter access: %s, %s, %s, %s, %s',
                                              entity, filter, url, method, accessId)
                            
            #now remove from db the accesses that are no longer present in the configuration files
            for accessId in accessesFromDb:
                service.remAcl(entity, accessId)

@injected
@setup(Handler, name='synchronizeGroupAccesses')
class SynchronizeGroupAccessHandler(SynchronizeAccessHandler):
    '''
    Implementation for a processor that synchronizes the group accesses in the configuration file with the database.
    '''
    
    groupService = IGroupService; wire.entity('groupService')
    
    def __init__(self):
        assert isinstance(self.groupService, IGroupService), \
        'Invalid group service %s' % self.groupService
        super().__init__()
        
    def process(self, chain, solicit:Solicit, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Synchronize the group accesses in the configuration file with the accesses in the database.
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(solicit, Solicit), 'Invalid solicit %s' % solicit
        assert isinstance(solicit.repository, Repository), 'Invalid repository %s' % solicit.repository
        
        groups = listBFS(solicit.repository, Repository.children, Repository.groupName)
        groupAccesses = {}
        for group in groups:
            assert isinstance(group, Repository), 'Invalid group %s' % group
            accesses = groupAccesses.get(group.groupName)
            if not accesses: groupAccesses[group.groupName] = group.accesses
            else: accesses.extend(group.accesses)
            
        self.syncEntityAccessesWithDb(self.groupService, groupAccesses)

@injected
@setup(Handler, name='synchronizeRightAccesses')
class SynchronizeRightAccessHandler(SynchronizeAccessHandler):
    '''
    Implementation for a processor that synchronizes the right accesses in the configuration file with the database.
    '''
    
    rightService = IRightService; wire.entity('rightService')
    
    def __init__(self):
        assert isinstance(self.rightService, IRightService), \
        'Invalid right service %s' % self.rightService
        super().__init__()
        
    def process(self, chain, solicit:Solicit, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Synchronize the accesses in the configuration file with the accesses in the database.
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(solicit, Solicit), 'Invalid solicit %s' % solicit
        assert isinstance(solicit.repository, Repository), 'Invalid repository %s' % solicit.repository
        
        #maps the right.Name : right.Id
        rightsDb = {r.Name: r.Id for r in [self.rightService.getById(id) for id in self.rightService.getAll()]}
        rights = listBFS(solicit.repository, Repository.children, Repository.rightName)
        #TODO: duplicate logic for rights and groups - fix it (add method to parent class)
        rightAccesses = {}
        for right in rights:
            assert isinstance(right, Repository), 'Invalid right %s' % right
            accesses = rightAccesses.get(rightsDb.get(right.rightName))
            if not accesses: rightAccesses[rightsDb.get(right.rightName)] = right.accesses
            else: accesses.extend(right.accesses)
        
        self.syncEntityAccessesWithDb(self.rightService, rightAccesses)
    