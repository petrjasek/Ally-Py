'''
Created on Aug 6, 2013

@package: gateway acl
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

API specifications for service access.
'''

from .domain_acl import modelACL
from ally.api.config import service, call
from ally.support.api.entity_named import Entity, IEntityGetService, IEntityFindService

# --------------------------------------------------------------------

@modelACL
class Access(Entity):
    '''
    Defines an access entry based on a URI pattern.
    '''
    Pattern = str

# --------------------------------------------------------------------

@service((Entity, Access))
class IAccessService(IEntityGetService, IEntityFindService):
    '''
    The ACL access service provides the means of setting up the access control layer for services.
    '''
    
    #TODO: Gabriel: remove
    @call(filter='Dummy filter')
    def isDummyFilter(self, access:Access) -> bool:
        '''
        '''