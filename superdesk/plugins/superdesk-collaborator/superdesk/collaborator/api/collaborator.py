'''
Created on May 2, 2012

@package: superdesk collaborator
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

API specifications for collaborators.
'''

from ally.api.config import service, call
from ally.api.type import Iter
from ally.support.api.entity import Entity, IEntityGetCRUDService
from internationalization.api.source import QSource
from superdesk.api.domain_superdesk import modelSuperDesk
from superdesk.person.api.person import Person, QPerson
from superdesk.source.api.source import Source

# --------------------------------------------------------------------

@modelSuperDesk
class Collaborator(Entity):
    '''
    Provides the collaborator model.
    '''
    Person = Person
    Source = Source

# --------------------------------------------------------------------

# No query

# --------------------------------------------------------------------

@service((Entity, Collaborator))
class ICollaboratorService(IEntityGetCRUDService):
    '''
    Provides the service methods for the collaborators.
    '''

    @call
    def getAll(self, personId:Person.Id=None, sourceId:Source.Id=None, offset:int=None, limit:int=None,
               qp:QPerson=None, qs:QSource=None) -> Iter(Collaborator):
        '''
        Provides all the collaborators.
        '''

