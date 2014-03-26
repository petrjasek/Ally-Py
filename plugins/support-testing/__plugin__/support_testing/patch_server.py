'''
Created on Mar 25, 2014

@package: ally core http
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the server configuration patch.
'''

from __setup__.ally_core_http.processor import assemblyResources
from __setup__.ally_core_http.server import root_uri_resources, \
    resourcesRouter, updateAssemblyServerForError
from __setup__.ally_http.server import assemblyServer
from ally.container import ioc
from ally.design.processor.handler import Handler
from ally.testing.core.http.impl.processor.router_testing import RouterTestingHandler

from .processor import SWITCHER_TESTING
from .processor import creator, testing_allowed

# --------------------------------------------------------------------

@ioc.config
def root_uri_test_resources():
    ''' The prefix used for matching the test resources paths in HTTP URL's.'''
    return '%s-test' % root_uri_resources()

# --------------------------------------------------------------------
@ioc.entity
def routerTesting() -> Handler:
    b = RouterTestingHandler()
    b.rootURI = root_uri_test_resources()
    b.switcher = SWITCHER_TESTING
    b.assembly = assemblyResources()
    b.create = creator()
    return b

# --------------------------------------------------------------------

@ioc.after(updateAssemblyServerForError)
def updateAssemblyServerForTesting():
    if testing_allowed(): assemblyServer().add(routerTesting(), after=resourcesRouter())
