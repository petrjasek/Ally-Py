'''
Created on Feb 10, 2014

@package: ally distribution
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the package scanner.
'''

import logging
import os
from os.path import join, isdir

from ally.container.ioc import injected
from ally.design.processor.assembly import Assembly
from ally.design.processor.attribute import defines
from ally.design.processor.context import Context
from ally.design.processor.execution import FILL_ALL


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Package(Context):
    '''
    The package context.
    '''
    # ---------------------------------------------------------------- Defined
    path = defines(str, doc='''
    @rtype: string
    The path where the package is found.
    ''')
    pathSetup = defines(str, doc='''
    @rtype: string
    The path where the setups are found.
    ''')
    packageSetup = defines(str, doc='''
    @rtype: string
    The package where the package setups are found.
    ''')
    name = defines(str, doc='''
    @rtype: string
    The package name.
    ''')
    
# --------------------------------------------------------------------

@injected
class ScannerPackage:
    '''
    Provides the package scanning and processing through an assembly.
    '''
    
    location = str
    # The location where to scan for packages.
    packages = list
    # The target packages (folders) that identifies a package in the location.
    assembly = Assembly
    # The assembly used for processing the scanned package.
    
    def __init__(self):
        assert isinstance(self.location, str), 'Invalid location %s' % self.location
        assert isinstance(self.packages, list), 'Invalid packages %s' % self.packages
        assert isinstance(self.assembly, Assembly), 'Invalid assembly %s' % self.assembly
        self._processing = self.assembly.create(package=Package)

    def scan(self):
        ''' Scan the packages.'''
        if not os.path.isdir(self.location): return
        
        for folder in os.listdir(self.location):
            fullPath = join(self.location, folder)
            if not isdir(fullPath): continue
            
            packageName = name = None
            for current in self.packages:
                packagePath = join(fullPath, current)
                if not isdir(packagePath): continue
                
                packages = [name for name in os.listdir(packagePath) if isdir(join(packagePath, name))
                            and not name.startswith('__')]
                if len(packages) != 1:
                    log.info('Not a package \'%s\' for \'%s\' because found to many root setup packages \'%s\'',
                             fullPath, current, ', '.join(packages))
                else:
                    packageName = current
                    name = packages[0]
                break  # We stop for the first found setup folder.
            
            if name is None: continue
            
            package = self._processing.ctx.package()
            assert isinstance(package, Package), 'Invalid package %s' % package
            package.name = folder.replace('-', '_')
            package.packageSetup = '%s.%s' % (packageName, name)
            package.path = fullPath
            package.pathSetup = join(packagePath, name)
            self._processing.execute(FILL_ALL, package=package)
