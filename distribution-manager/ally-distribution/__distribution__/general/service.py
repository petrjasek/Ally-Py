'''
Created on Oct 3, 2013

@package: ally distribution
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the services setup for distribution.
'''

from ally.container import ioc, deploy
from ally.distribution.packaging.broker import Broker

# --------------------------------------------------------------------

@ioc.config
def package_location():
    ''' The location path where the components/plugins eggs will be placed'''
    return 'packaged-eggs'

@ioc.config
def path_components():
    ''' The location path where the components sources are located'''
    return '../../components'

@ioc.config
def path_plugins():
    ''' The location path where the plugins sources are located'''
    return '../../plugins'

@ioc.config
def path_ui():
    ''' The location path where the UI plugins sources are located'''
    return '../../ui'

@ioc.config
def path_plugins_ui():
    ''' The location path to the build folder of UI plugins '''
    return '../../plugins-ui'

@ioc.config
def setup_folder_names():
    '''The name of the folderin which information about plugin/component is located'''
    return {'plugins'    : '__plugin__',
            'components' : '__setup__'}
    
@ioc.config 
def actions_bucket():
    '''Actions to be performed by distribution manager'''
    return {}
# --------------------------------------------------------------------

@deploy.start
def runBroker():
    b = Broker()
    b.actions = actions_bucket()
    b.plugins_ui_path = path_plugins_ui()
    b.process()
