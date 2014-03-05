'''
Created on Oct 3, 2013

@package: ally distribution
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the services setup for distribution.
'''

from ally.design.processor.assembly import Assembly
from ally.design.processor.handler import Handler
from ally.support.util_spec import IDo

from ally.container import ioc
from ally.distribution.packaging.impl.index_pip import IndexPip
from ally.distribution.packaging.impl.processor.arg_setup import ArgSetupHandler
from ally.distribution.packaging.impl.processor.build import BuildHandler
from ally.distribution.packaging.impl.processor.build_dev import BuildDevHandler
from ally.distribution.packaging.impl.processor.generate_setup import GenerateSetupHandler
from ally.distribution.packaging.impl.processor.publish import PublishHandler
from ally.distribution.packaging.impl.processor.scanner import Scanner
from ally.distribution.packaging.impl.processor.dev_versioner import VersionerDevHandler


# --------------------------------------------------------------------
@ioc.config
def sources():
    ''' The location(s) path where the packages sources are located. If the path ends with '*' (ex: '../components/*')
    then all the folders found in components will be considered as packages. This configuration can be overridden with
    command line arguments, the paths are relative from where the distribution is executed.'''
    return []

@ioc.config
def path_build() -> str:
    ''' The location path where the packages are placed, this configuration can be overridden 
    with command line arguments, this path is relative from where the distribution is executed.'''
    return None

@ioc.config
def build_cmds() -> list:
    ''' The commands used for build.'''
    return []

@ioc.config
def root_uri() -> str:
    ''' The index root URI that can be used for fetching the files, for instance on git something like
    'https://raw.github.com/superdesk/ally-py-common/tree/master/packages'.'''
    return None

# --------------------------------------------------------------------

@ioc.entity
def assemblyBuild() -> Assembly:
    '''
    The assembly used for building packages.
    '''
    return Assembly('Packaging Build')

@ioc.entity
def assemblyBuildDev() -> Assembly:
    '''
    The assembly used for building development packages.
    '''
    return Assembly('Packaging Build for Development')

@ioc.entity
def assemblyPublish() -> Assembly:
    '''
    The assembly used for publishing packages.
    '''
    return Assembly('Packaging Publish')

# --------------------------------------------------------------------

@ioc.entity
def packages() -> list: return ['__setup__', '__plugin__', '__distribution__']

@ioc.entity
def scanner() -> Handler:
    b = Scanner()
    b.locations = sources()
    b.packages = packages()
    return b

@ioc.entity
def argSetup() -> Handler: return ArgSetupHandler()

@ioc.entity
def versionerDev() -> Handler:
    b = VersionerDevHandler()
    b.pathBuild = path_build()
    return b

@ioc.entity
def generateSetup() -> Handler: return GenerateSetupHandler()

@ioc.entity
def build() -> Handler:
    b = BuildHandler()
    b.pathBuild = path_build()
    b.cmds = build_cmds()
    return b

@ioc.entity
def buildDev() -> Handler:
    b = BuildDevHandler()
    b.pathBuild = path_build()
    return b

@ioc.entity
def publish() -> Handler: return PublishHandler()

@ioc.entity
def indexPip() -> IDo:
    b = IndexPip()
    b.locations = sources()
    b.rootURI = root_uri()
    return b

# --------------------------------------------------------------------

@ioc.before(assemblyBuild)
def updateAssemblyBuild():
    assemblyBuild().add(scanner(), argSetup(), generateSetup(), build())

@ioc.before(assemblyBuildDev)
def updateAssemblyBuildDev():
    assemblyBuildDev().add(scanner(), argSetup(), versionerDev(), generateSetup(), buildDev())

@ioc.before(assemblyPublish)
def updateAssemblyPublish():
    assemblyPublish().add(scanner(), argSetup(), generateSetup(), publish())

