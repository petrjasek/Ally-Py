'''
Created on Feb 10, 2014

@package: ally distribution
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Builds a package to an egg.
'''

import logging

from ally.container.ioc import injected
from ally.design.processor.attribute import requires
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
import os
from shutil import rmtree
from distutils.core import run_setup


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Package(Context):
    '''
    The package context.
    '''
    # ---------------------------------------------------------------- Required
    path = requires(str)
    pathSetupPy = requires(str)
    name = requires(str)

# --------------------------------------------------------------------

@injected
class BuildHandler(HandlerProcessor):
    '''
    Implementation for a processor that provides the package egg build.
    '''
    
    pathBuild = str
    # The location where the builds are placed. 
    
    def __init__(self):
        assert isinstance(self.pathBuild, str), 'Invalid build path %s' % self.pathBuild
        super().__init__()

    def process(self, chain, package:Package, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Provides the package build.
        '''
        assert isinstance(package, Package), 'Invalid package %s' % package
        
        savedCwd = os.getcwd()
        os.chdir(package.path)
        
        buildPath = os.path.join(savedCwd, self.pathBuild)
        run_setup(package.pathSetupPy, ('sdist', '--dist-dir', buildPath, 'bdist_egg', '--dist-dir', buildPath))
        # run_setup(package.pathSetupPy, ('--help', 'sdist'))
        
        # Cleaning setup directories.
        rmtree('build')
        rmtree('%s.egg-info' % package.name)
        
        # Restoring environment. 
        os.chdir(savedCwd)
