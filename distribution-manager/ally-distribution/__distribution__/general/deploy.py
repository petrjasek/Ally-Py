'''
Created on Oct 2, 2013

@package: ally distribution
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the setup for general resources.
'''

from .service import path_components, package_location, path_plugins, path_plugins_ui
from ally.container import support, deploy
from distribution import parser, options
from pydoc import getdoc
import logging
from .service import actions_bucket
from ally.design.priority import PRIORITY_FIRST

# --------------------------------------------------------------------

logging.basicConfig(format='%(asctime)s %(levelname)-7s %(message)s')
logging.getLogger('ally.distribution').setLevel(logging.INFO)

FLAG_PACKAGE = 'package'
# Flag indicating the packaging action.
FLAG_BUILD_EGGS = 'build'
# Flag indicating the build eggs action.
FLAG_SCAN_INT = 'scan'
# Flag indicating scanning for internationalization messages.
FLAG_PUBLISH = 'publish'
# Flag indicating publishing on pypi repository.
FLAG_COMPONENTS = 'components'
FLAG_PLUGINS = 'plugins'
FLAG_PLUGINS_UI = 'plugins-ui'

actionFlags = [FLAG_PACKAGE, FLAG_BUILD_EGGS, FLAG_PUBLISH, FLAG_SCAN_INT]
targetFlags = [FLAG_COMPONENTS, FLAG_PLUGINS, FLAG_PLUGINS_UI]

# --------------------------------------------------------------------

@deploy.prepare
def prepare():
    
    destComponents = options.registerConfiguration(path_components)
    destPlugins    = options.registerConfiguration(path_plugins)
    destPluginsUI  = options.registerConfiguration(path_plugins_ui)
    
    options.location = None
    
    #Action flags    
    options.registerFlag(FLAG_PACKAGE)
    options.registerFlag(FLAG_SCAN_INT)
    options.registerFlag(FLAG_BUILD_EGGS)
    options.registerFlag(FLAG_PUBLISH)
    
    #Target flags
    options.registerFlag(FLAG_COMPONENTS)
    options.registerFlag(FLAG_PLUGINS)
    options.registerFlag(FLAG_PLUGINS_UI)
    
    options.registerFlagLink(destComponents, FLAG_COMPONENTS)
    options.registerFlagLink(destPlugins, FLAG_PLUGINS)
    options.registerFlagLink(destPluginsUI, FLAG_PLUGINS_UI)
    
    parser.add_argument('--location', metavar='folder', dest='location', help='The location where '
                        'the distribution results should be placed, if none provided it will default to '
                        'a location based on the performed action, if packaging is performed it will default to "packaged-eggs" '
                        'in current folder')
    parser.add_argument('--components', nargs='?', dest=destComponents, help=getdoc(path_components))
    parser.add_argument('--plugins', nargs='?', dest=destPlugins, help=getdoc(path_plugins))
    parser.add_argument('--plugins-ui', nargs='?', dest=destPluginsUI, help=getdoc(path_plugins_ui))
    parser.add_argument('--package', action='store_true', dest=FLAG_PACKAGE)
    parser.add_argument('--publish', action='store_true', dest=FLAG_PUBLISH)
    parser.add_argument('--build', action='store_true', dest=FLAG_BUILD_EGGS)
    parser.add_argument('--scan', action='store_true', dest=FLAG_SCAN_INT)
    
@deploy.start(priority=PRIORITY_FIRST)
def deploy():
    if options.location: support.force(package_location, options.location)
    for action in actionFlags:
        if options.isFlag(action):
            actions_bucket()[action] = []
            if options.isFlag(FLAG_COMPONENTS) or \
               options.isFlag(FLAG_PLUGINS) or \
               options.isFlag(FLAG_PLUGINS_UI):
                if options.isFlag(FLAG_COMPONENTS):
                    actions_bucket()[action].append({'path' : path_components(),
                                                  'type' : FLAG_COMPONENTS})
                if options.isFlag(FLAG_PLUGINS):
                    actions_bucket()[action].append({'path' : path_plugins(),
                                                  'type' : FLAG_PLUGINS})
                if options.isFlag(FLAG_PLUGINS_UI):
                    actions_bucket()[action].append({'path' : path_plugins_ui(),
                                                  'type' : FLAG_PLUGINS_UI})
            else:
                actions_bucket[action] = [{'path' : path_components(),
                                                  'type' : FLAG_COMPONENTS},
                                         {'path' : path_plugins(),
                                                  'type' : FLAG_PLUGINS},
                                         {'path' : path_plugins_ui(),
                                                  'type' : FLAG_PLUGINS_UI},
                                         ]