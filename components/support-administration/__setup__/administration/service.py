'''
Created on Jan 9, 2012

@@package: ally core administration
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the services for the administration support.
'''

from ..ally_core.resources import services
from ..ally_gateway.security import scheme
from admin.introspection.api.component import IComponentService
from admin.introspection.api.plugin import IPluginService
from admin.introspection.impl.component import ComponentService
from admin.introspection.impl.plugin import PluginService
from ally.api.security import SchemeRepository
from ally.container import ioc

# --------------------------------------------------------------------

@ioc.config
def publish_introspection():
    '''
    If true the introspection services will be published and available, otherwise they will only be accessible inside
    the application.
    '''
    return True

@ioc.entity
def componentService() -> IComponentService: return ComponentService()

@ioc.entity
def pluginService() -> IPluginService:
    b = PluginService()
    b.componentService = componentService()
    return b

# --------------------------------------------------------------------

@ioc.before(services)
def publishServices():
    if publish_introspection():
        services().append(componentService())
        services().append(pluginService())

@ioc.before(scheme)
def updateSchemeForIntrospection():
    if publish_introspection():
        s = scheme(); assert isinstance(s, SchemeRepository), 'Invalid scheme %s' % s
        
        s['Introspection access'].doc('''
        Allows for the introspection of the application distribution meaning that the components and plugins that 
        compose the distribution are visible
        ''').addAll(IComponentService, IPluginService)
