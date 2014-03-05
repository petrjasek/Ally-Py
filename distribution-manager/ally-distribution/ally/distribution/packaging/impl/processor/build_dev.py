'''
Created on Mar 5, 2014

@package: ally distribution
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides development build installation.
'''

from distutils.core import run_setup
import logging
import os
import re
from shutil import rmtree

from ally.container.ioc import injected
from ally.design.processor.attribute import requires
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
import json


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Distribution(Context):
    '''
    The distribution context.
    '''
    # ---------------------------------------------------------------- Required
    packages = requires(list)
    versions = requires(dict)
    
class Package(Context):
    '''
    The package context.
    '''
    # ---------------------------------------------------------------- Required
    path = requires(str)
    name = requires(str)

# --------------------------------------------------------------------

@injected
class BuildDevHandler(HandlerProcessor):
    '''
    Implementation for a processor that provides development build installation.
    '''
    
    pathBuild = str
    # The location where the builds are placed. 
    exclude = '(__pycache__)|(\.\w+)'
    # The regex used for excluding folder or files from the timestamp search.
    attributeVersion = 'version'
    # The name for the version attribute.
    
    def __init__(self):
        assert isinstance(self.pathBuild, str), 'Invalid build path %s' % self.pathBuild
        assert isinstance(self.exclude, str), 'Invalid exclude %s' % self.exclude
        assert isinstance(self.attributeVersion, str), 'Invalid version attribute %s' % self.attributeVersion
        super().__init__(Package=Package)
        
        self._exc = re.compile(self.exclude)

    def process(self, chain, distribution:Distribution, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Build development packages.
        '''
        assert isinstance(distribution, Distribution), 'Invalid distribution %s' % distribution
        if not distribution.packages: return
        
        savedCwd, pathBuild = os.getcwd(), os.path.abspath(self.pathBuild)
        for package in distribution.packages:
            assert isinstance(package, Package), 'Invalid package %s' % package
            meta = distribution.versions[package.name]
            meta['dist'] = self.buildDist(package, pathBuild)
                
        # Restoring environment. 
        os.chdir(savedCwd)
        with open(os.path.join(self.pathBuild, 'versions.json'), 'w') as f: json.dump(distribution.versions, f)

    # ----------------------------------------------------------------
    
    def buildDist(self, package, buildPath):
        ''' Build the distribution package.'''
        assert isinstance(package, Package), 'Invalid package %s' % package
        
        os.chdir(package.path)
            
        with open('setup.py', 'w') as f: print(package.setup, file=f)
        
        log.info('%s Building: %s', '=' * 50, package.name)
        try: distr = run_setup('setup.py', ('-q', 'sdist', '--dist-dir', buildPath))
        except: log.exception('Cannot publish \'%s\'', package.path)
        
        # Cleaning setup directories.
        os.remove('setup.py')
        if os.path.exists('build'): rmtree('build')
        eggInfo = '%s.egg-info' % package.name.replace('-', '_')
        if os.path.exists(eggInfo): rmtree(eggInfo)
        
        return os.path.basename(distr.dist_files[0][2])
