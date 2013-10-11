'''
Created on Oct 10, 2013

@package: gui core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Gociu

Provides the synchronization with the database for rights.
'''

from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.design.processor.attribute import requires
from ally.design.processor.context import Context
from ally.design.processor.execution import Chain
from ally.design.processor.handler import HandlerProcessor, Handler
import logging
from ally.support.util_context import listBFS

# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------
class Repository(Context):
    '''
    The repository context.
    '''
    # ---------------------------------------------------------------- Required
    groupName = requires(str)
    children = requires(list)

class SynchronizeGroupsRightsHandler(HandlerProcessor):
    '''
    Base for a processors that synchronize the groups and the rights in the configuration file with the database.
    '''
    
    def __init__(self, Repository):
        super().__init__(Repository=Repository)
        
    def syncWithDatabase(self, service, entitiesRepository, entitiesDb, createEntityArgs=None):
        '''
        Generic method to synchronize entities from configuration file with the database.
        @param service: the service for the entity to be synchronized 
        @param entitiesRepository: list of repositories containing the entity data from the configuration files 
        @param entitiesDb: mapping entityName : entityId 
        @param createEntityArgs: optional dictionary of arguments for creating the entities
        '''
        assert isinstance(entitiesDb, dict), 'Invalid entities mapping %s' % entitiesDb
        
        for repository in entitiesRepository:
            assert isinstance(repository, Repository), 'Invalid entity %' % repository
            if not repository.groupName in entitiesDb:
                entity = self.createEntity(repository, createEntityArgs)
                try:
                    service.insert(entity)
                except Exception as e:
                    log.warning('Error adding %s to database' % entity)
            else: entitiesDb.pop(repository.groupName)
        
        # remove the remaining entities that are only in the db and not in the configuration file
        for entityId in entitiesDb.values(): service.delete(entityId)
        
    def createEntity(self, entityRepository, args):
        '''
        Should be overwritten by the child class to return the type of entity that it needs.
        '''
        