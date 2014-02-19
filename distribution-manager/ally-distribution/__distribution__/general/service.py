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

from ally.container import ioc, deploy
from ally.distribution.packaging.impl.processor.arg_setup import ArgSetupHandler
from ally.distribution.packaging.impl.processor.build import BuildHandler
from ally.distribution.packaging.impl.scanner_package import ScannerPackage
from ally.distribution.packaging.impl.processor.write_setup import WriteSetupHandler

# --------------------------------------------------------------------

@deploy.start
def performBuild():
    scanner().scan()

# --------------------------------------------------------------------

@ioc.config
def path_sources():
    ''' The location path where the packages sources are located, this configuration can be overridden 
    with command line arguments, this path is relative from where the distribution is executed.'''
    return ''

@ioc.config
def path_build():
    ''' The location path where the packages are placed, this configuration can be overridden 
    with command line arguments, this path is relative from where the distribution is executed.'''
    return ''

# --------------------------------------------------------------------

@ioc.entity
def assemblyPackage() -> Assembly:
    '''
    The assembly used for packaging.
    '''
    return Assembly('Packaging')

# --------------------------------------------------------------------

@ioc.entity
def buildPackages() -> list: return ['__setup__', '__plugin__']

@ioc.entity
def scanner() -> ScannerPackage:
    b = ScannerPackage()
    b.location = path_sources()
    b.packages = buildPackages()
    b.assembly = assemblyPackage()
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

# --------------------------------------------------------------------

@ioc.before(assemblyPackage)
def updateAssemblyPackage():
    assemblyPackage().add(argSetup(), writeSetup(), build())

