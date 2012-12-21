'''
Created on Jan 9, 2012

@@package: development support
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the services for the development support.
'''

from ..ally_core.resources import services, resourcesRoot
from ..ally_core_http.processor import converterPath
from ..ally_gateway.security import scheme
from ally.api.security import SchemeRepository
from ally.container import ioc
from development.request.api.request import IRequestService
from development.request.impl.request import RequestService

# --------------------------------------------------------------------

@ioc.config
def publish_development():
    '''
    If true the development services will be published.
    '''
    return True

@ioc.entity
def requestService() -> IRequestService:
    b = RequestService(); yield b
    b.root = resourcesRoot()
    b.converterPath = converterPath()

# --------------------------------------------------------------------

@ioc.before(services)
def publishServices():
    if publish_development(): services().append(requestService())

@ioc.before(scheme)
def updateSchemeForIntrospection():
    if publish_development():
        s = scheme(); assert isinstance(s, SchemeRepository), 'Invalid scheme %s' % s
        
        s['Introspection access'].doc('''
        Allows for the introspection of the application requests.
        ''').addAll(IRequestService)
