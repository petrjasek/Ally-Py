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
from ally.distribution.packaging.builder import Builder

# --------------------------------------------------------------------

@ioc.config
def path_components():
    ''' The location path where the components sources are located'''
    return '../../components'

@ioc.config
def path_plugins():
    ''' The location path where the components sources are located'''
    return '../../plugins'

# --------------------------------------------------------------------

@ioc.entity
def packager_components():
    b = Packager()
    b.pathSource = path_components()
    b.folderType = '__setup__'
    return b

@ioc.entity
def packager_plugins():
    b = Packager()
    b.pathSource = path_plugins()
    b.folderType = '__plugin__'
    return b
