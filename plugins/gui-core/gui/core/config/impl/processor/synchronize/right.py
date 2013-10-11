'''
Created on Oct 10, 2013

@package: gui core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Gociu

Provides the synchronization with the database for rights.
'''

from security.api.right import IRightService, Right, RightType
from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.design.processor.attribute import requires, optional
from ally.design.processor.context import Context
from ally.design.processor.execution import Chain
from ally.design.processor.handler import Handler
import logging
from ally.support.util_context import listBFS
from gui.core.config.impl.processor.synchronize.group_right_base import SynchronizeGroupsRightsHandler
from security.api.right_type import IRightTypeService

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
    groupName = requires(str)
    children = requires(list)
    description = optional(str)

@injected
@setup(Handler, name='synchronizeRights')
class SynchronizeRightsHandler(SynchronizeGroupsRightsHandler):
    '''
    Implementation for a processor that synchronizes the rights in the configuration file with the database.
    '''
    
    rightService = IRightService; wire.entity('rightService')
    rightTypeService = IRightTypeService; wire.entity('rightTypeService')
    
    def __init__(self):
        assert isinstance(self.rightService, IRightService)
        'Invalid right service %s' % self.rightService
        super().__init__(Repository=Repository)
        
    def process(self, chain, solicit:Solicit, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Synchronize the rights of the groups in the configuration file with the database.
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(solicit, Solicit), 'Invalid solicit %s' % solicit
        assert isinstance(solicit.repository, Repository), 'Invalid repository %s' % solicit.repository
        
        try: self.rightTypeService.getById('GUIAccess')
        except:
            rightType = RightType()
            rightType.Name = 'GUIAccess'
            self.rightTypeService.insert(rightType)
        
        rightsDb = {e.Name: e.Id for e in [self.rightService.getById(id) for id in self.rightService.getAll()]}    
        self.syncWithDatabase(self.rightService, listBFS(solicit.repository, Repository.children, Repository.groupName), rightsDb,
                              {'rightType':'GUIAccess'})
    
    def createEntity(self, repository, args):
        assert isinstance(repository, Repository), 'Invalid group repository %s' % repository
        assert isinstance(args, dict), 'Invalid rightType for createEntity %s' % args
        right = Right()
        right.Name = repository.groupName
        right.Type = args.get('rightType')
        right.Description = repository.description if Repository.description in repository else ''
        return right
