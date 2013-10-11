'''
Created on Oct 3, 2013

@package: ally distribution
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the services setup for distribution.
'''

from ally.container import ioc
from ally.distribution.packaging.packager import Packager

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

# --------------------------------------------------------------------

@ioc.entity
def packagerComponents():
    b = Packager()
    b.pathSource = path_components()
    b.folderType = '__setup__'
    b.destFolder = package_location()
    return b

@ioc.entity
def packagerPlugins():
    b = Packager()
    b.pathSource = path_plugins()
    b.folderType = '__plugin__'
    b.destFolder = package_location()
    return b
