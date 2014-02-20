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

from ally.container import ioc
from ally.distribution.packaging.impl.processor.arg_setup import ArgSetupHandler
from ally.distribution.packaging.impl.processor.build import BuildHandler
from ally.distribution.packaging.impl.processor.publish import PublishHandler
from ally.distribution.packaging.impl.processor.scanner import Scanner
from ally.distribution.packaging.impl.processor.write_setup import \
    WriteSetupHandler


# --------------------------------------------------------------------
@ioc.config
def sources():
    ''' The location(s) path where the packages sources are located, this configuration can be overridden 
    with command line arguments, the paths are relative from where the distribution is executed.'''
    return []

@ioc.config
def path_build() -> str:
    ''' The location path where the packages are placed, this configuration can be overridden 
    with command line arguments, this path is relative from where the distribution is executed.'''
    return None

# --------------------------------------------------------------------

@ioc.entity
def assemblyBuild() -> Assembly:
    '''
    The assembly used for building packages.
    '''
    return Assembly('Packaging Build')

@ioc.entity
def assemblyPublish() -> Assembly:
    '''
    The assembly used for publishing packages.
    '''
    return Assembly('Packaging Publish')

# --------------------------------------------------------------------

@ioc.entity
def packages() -> list: return ['__setup__', '__plugin__']

@ioc.entity
def scanner() -> Handler:
    b = Scanner()
    b.locations = sources()
    b.packages = packages()
    return b

@ioc.entity
def argSetup() -> Handler: return ArgSetupHandler()

@ioc.entity
def writeSetup() -> Handler: return WriteSetupHandler()

@ioc.entity
def build() -> Handler:
    b = BuildHandler()
    b.pathBuild = path_build()
    return b

@ioc.entity
def publish() -> Handler: return PublishHandler()

# --------------------------------------------------------------------

@ioc.before(assemblyBuild)
def updateAssemblyBuild():
    assemblyBuild().add(scanner(), argSetup(), writeSetup(), build())
    
@ioc.before(assemblyPublish)
def updateAssemblyPublish():
    assemblyPublish().add(scanner(), argSetup(), writeSetup(), publish())

