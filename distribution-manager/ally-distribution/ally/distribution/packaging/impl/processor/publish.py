'''
Created on Feb 14, 2014

@package: ally distribution
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Publish a package to an egg.
'''

import logging
import os

from ally.design.processor.attribute import requires
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
from distutils.core import run_setup
from shutil import rmtree


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

# --------------------------------------------------------------------

class PublishHandler(HandlerProcessor):
    '''
    Implementation for a processor that provides the package egg publish.
    '''
    
    def __init__(self):
        super().__init__(Package=Package)

    def process(self, chain, distribution:Distribution, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Provides the package publish.
        '''
        assert isinstance(distribution, Distribution), 'Invalid distribution %s' % distribution
        if not distribution.packages: return
            
        savedCwd = os.getcwd()
             
        for package in distribution.packages:
            assert isinstance(package, Package), 'Invalid package %s' % package
            
            os.chdir(package.path)
            
            run_setup(package.pathSetupPy, ('register', 'sdist', 'bdist_egg', 'upload'))
            
            # Cleaning setup directories.
            rmtree('build')
            rmtree('dist')
            rmtree('%s.egg-info' % package.name.replace('-', '_'))
        
        # Restoring environment. 
        os.chdir(savedCwd)
