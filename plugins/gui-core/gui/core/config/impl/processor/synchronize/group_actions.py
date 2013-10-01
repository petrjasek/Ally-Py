'''
Created on Sept 04, 2013

@package: gui core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Gociu

Provides the synchronization with the database for actions.
'''

from acl.api.access import IAccessService
from acl.api.group import IGroupService, Group
from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.design.processor.attribute import requires
from ally.design.processor.context import Context
from ally.design.processor.execution import Chain
from ally.design.processor.handler import HandlerProcessor, Handler
from gui.action.api.category_group import IActionGroupService
import logging
from ally.support.util_context import listBFS

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
    groupName = requires(str, doc='''
    @rtype: string
    The name of the group (e.g. "Anonymous").
    ''')
    children = requires(list, doc='''
    @rtype: list[Context]
    The list of children created.
    ''')
    actions = requires(list, doc='''
    @rtype: list[Action]
    The list of actions created.
    ''')
    
class ActionData(Context):
    '''
    The action container context.
    '''
    # ---------------------------------------------------------------- Required
    path = requires(str)

@injected
@setup(Handler, name='synchronizeGroupActions')
class SynchronizeGroupActionsHandler(HandlerProcessor):
    '''
    Implementation for a processor that synchronizes the actions of the groups in the configuration file with
    the database.
    '''
    
    actionGroupService = IActionGroupService; wire.entity('actionGroupService')
    groupService = IGroupService; wire.entity('groupService')
    
    anonymousGroups = set
    # The set with the anonymous groups names
    
    def __init__(self):
        assert isinstance(self.actionGroupService, IActionGroupService), \
        'Invalid action group service %s' % self.actionGroupService
        assert isinstance(self.groupService, IGroupService)
        'Invalid group service %s' % self.groupService
        assert isinstance(self.anonymousGroups, set), 'Invalid anonymous groups %s' % self.anonymousGroups
        super().__init__(Repository=Repository)
        
    def process(self, chain, solicit:Solicit, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Synchronize the actions of the groups in the configuration file with the database.
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(solicit, Solicit), 'Invalid solicit %s' % solicit
        assert isinstance(solicit.repository, Repository), 'Invalid repository %s' % solicit.repository
        
        groups = listBFS(solicit.repository, Repository.children, Repository.groupName)
        #first group the actions by group name: groupName -> [actions]
        groupActions = {}
        for group in groups:
            actions = groupActions.get(group.groupName)
            if not actions: groupActions[group.groupName] = group.actions
            else: actions.extend(group.actions)
        
        for groupName, actions in groupActions.items():
            actionsDb = set(self.actionGroupService.getActions(groupName))
            if actions:
                actionsSet = set(action.path for action in actions)
                toDelete = actionsDb.difference(actionsSet)
                toAdd = actionsSet.difference(actionsDb)
            else:
                toDelete = actionsDb
                toAdd = None
                
            if toDelete:
                for path in toDelete:
                    self.actionGroupService.remAction(groupName, path)
            
            if toAdd:
                for path in toAdd:
                    self.actionGroupService.addAction(groupName, path)
            
            actionsDb = set(self.actionGroupService.getActions(groupName))
            actions