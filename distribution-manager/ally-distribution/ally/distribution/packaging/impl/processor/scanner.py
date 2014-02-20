'''
Created on Feb 10, 2014

@package: ally distribution
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the distribution scanner.
'''

import logging
import os
from os.path import join, isdir

from ally.container.ioc import injected
from ally.design.processor.attribute import defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------
    
class PackageScan(Context):
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

class Distribution(Context):
    '''
    The distribution context.
    '''
    # ---------------------------------------------------------------- Defined
    packages = defines(list, doc='''
    @rtype: list[Context]
    The list of found packages.
    ''')
   
# --------------------------------------------------------------------

@injected
class Scanner(HandlerProcessor):
    '''
    Provides the distribution scanner.
    '''
    
    locations = list
    # The locations where to scan for packages.
    packages = list
    # The target packages (folders) that identifies a package in the location.
    
    def __init__(self):
        assert isinstance(self.locations, list), 'Invalid locations %s' % self.locations
        assert isinstance(self.packages, list), 'Invalid packages %s' % self.packages
        super().__init__()

    def process(self, chain, distribution:Distribution, Package:PackageScan, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Scan the distribution.
        '''
        assert isinstance(distribution, Distribution), 'Invalid distribution %s' % distribution
        
        if distribution.packages is None: distribution.packages = []
        for location in self.locations:
            if not os.path.isdir(location): continue
            
            for folder in os.listdir(location):
                fullPath = join(location, folder)
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
                
                package = Package()
                assert isinstance(package, PackageScan), 'Invalid package %s' % package
                package.packageSetup = '%s.%s' % (packageName, name)
                package.path = fullPath
                package.pathSetup = join(packagePath, name)
                distribution.packages.append(package)
