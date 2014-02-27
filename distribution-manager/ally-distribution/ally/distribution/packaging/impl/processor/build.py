'''
Created on Feb 10, 2014

@package: ally distribution
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Builds a package to an egg.
'''

from distutils.core import run_setup
import logging
import os
from shutil import rmtree

from ally.container.ioc import injected
from ally.design.processor.attribute import requires
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Distribution(Context):
    '''
    The distribution context.
    '''
    # ---------------------------------------------------------------- Required
    packages = requires(list)
    
class Package(Context):
    '''
    The package context.
    '''
    # ---------------------------------------------------------------- Required
    path = requires(str)
    name = requires(str)
    setup = requires(str)

# --------------------------------------------------------------------

@injected
class BuildHandler(HandlerProcessor):
    '''
    Implementation for a processor that provides the package egg build.
    '''
    
    cmds = list
    # The setup util distribution commands.
    pathBuild = str
    # The location where the builds are placed. 
    
    def __init__(self):
        assert isinstance(self.cmds, list), 'Invalid commands %s' % self.cmds
        assert isinstance(self.pathBuild, str), 'Invalid build path %s' % self.pathBuild
        super().__init__(Package=Package)

    def process(self, chain, distribution:Distribution, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Provides the package build.
        '''
        assert isinstance(distribution, Distribution), 'Invalid distribution %s' % distribution
        if not distribution.packages: return
        if not self.cmds: return
            
        savedCwd = os.getcwd()
             
        for package in distribution.packages:
            assert isinstance(package, Package), 'Invalid package %s' % package

            os.chdir(package.path)
            
            with open('setup.py', 'w') as f: print(package.setup, file=f)
            
            buildPath = os.path.join(savedCwd, self.pathBuild)
            log.info('%s Building %s', '=' * 50, package.name)
            
            commands = []
            for cmd in self.cmds:
                commands.append(cmd)
                commands.append('--dist-dir')
                commands.append(buildPath)
            
            try: run_setup('setup.py', commands)
            except: log.exception('Cannot publish \'%s\'', package.path)
            
            # Cleaning setup directories.
            os.remove('setup.py')
            if os.path.exists('build'): rmtree('build')
            eggInfo = '%s.egg-info' % package.name.replace('-', '_')
            if os.path.exists(eggInfo): rmtree(eggInfo)
            
        # Restoring environment. 
        os.chdir(savedCwd)
