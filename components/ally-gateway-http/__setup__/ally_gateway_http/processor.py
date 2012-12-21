'''
Created on Nov 24, 2011

@package: ally gateway http
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the configurations for the authentication processors.
'''

from ..ally_core.processor import assemblyResources, methodInvoker
from ..ally_core_http.processor import pathAssemblies
from ally.container import ioc
from ally.core.authentication.impl.processor.authentication import \
    AuthenticationHandler
from ally.design.processor import Handler, Assembly

# --------------------------------------------------------------------

@ioc.config
def server_pattern_authenticated():
    ''' The pattern used for matching the REST authenticated resources paths in HTTP URL's'''
    return '^resources\/my(/|(?=\\.)|$)'

@ioc.config
def always_authenticate():
    '''
    Flag indicating that the authentication should not be made only when there is a authentication data type required,
    but the authentication should be made for all requests
    '''
    return False

# --------------------------------------------------------------------

@ioc.entity
def authentication() -> Handler:
    b = AuthenticationHandler()
    b.alwaysAuthenticate = always_authenticate()
    b.authenticators = authenticators()
    return b

# --------------------------------------------------------------------

@ioc.entity
def assemblyResourcesAuthentication() -> Assembly:
    '''
    The assembly containing the handlers that will be used in processing a REST request.
    '''
    return Assembly()

@ioc.entity
def authenticators(): return []

# --------------------------------------------------------------------

@ioc.before(assemblyResourcesAuthentication)
def updateAssemblyResourcesAuthentication():
    assemblyResourcesAuthentication().add(assemblyResources())
    assemblyResourcesAuthentication().add(authentication(), after=methodInvoker())

@ioc.before(pathAssemblies)
def updatePathAssemblies():
    pathAssemblies().insert(0, (server_pattern_authenticated(), assemblyResourcesAuthentication()))

