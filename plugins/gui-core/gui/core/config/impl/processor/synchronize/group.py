'''
Created on Sept 04, 2013

@package: gui core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Gociu

Provides the synchronization with the database for actions.
'''

from acl.api.group import IGroupService, Group
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

@injected
@setup(Handler, name='synchronizeGroups')
class SynchronizeGroupsHandler(HandlerProcessor):
    '''
    Implementation for a processor that synchronizes the groups in the configuration file with the database.
    '''
    
    groupService = IGroupService; wire.entity('groupService')
    
    anonymousGroups = set
    # The set with the anonymous groups names
    
    def __init__(self):
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
        
        groupsDb = set(self.groupService.getAll())
        groups = listBFS(solicit.repository, Repository.children, Repository.groupName)
        
        for group in groups:
            assert isinstance(group, Repository), 'Invalid repository %' % group
            
            if not group.groupName in groupsDb:
                groupNew = Group()
                groupNew.Name = group.groupName
                groupNew.IsAnonymous = group.groupName in self.anonymousGroups
                self.groupService.insert(groupNew) 
            else: groupsDb.remove(group.groupName)
        
        # remove the remaining groups that are only in the db and not in the configuration file
        for group in groupsDb: self.groupService.delete(group)
    
        
