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

from ally.container.ioc import injected
from ally.design.processor.attribute import requires
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
from distutils.core import run_setup
from shutil import rmtree


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Package(Context):
    '''
    The package context.
    '''
    # ---------------------------------------------------------------- Required
    path = requires(str)
    name = requires(str)

# --------------------------------------------------------------------

@injected
class PublishHandler(HandlerProcessor):
    '''
    Implementation for a processor that provides the package egg publish.
    '''
    
    def __init__(self):
        super().__init__()

    def process(self, chain, package:Package, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Provides the package publish.
        '''
        assert isinstance(package, Package), 'Invalid package %s' % package
        
        savedCwd = os.getcwd()
        os.chdir(package.path)
        
        run_setup(package.pathSetupPy, ('sdist', 'bdist_egg', 'upload'))
        
        # Cleaning setup directories.
        rmtree('build')
        rmtree('%s.egg-info' % package.name)
        
        # Restoring environment. 
        os.chdir(savedCwd)
