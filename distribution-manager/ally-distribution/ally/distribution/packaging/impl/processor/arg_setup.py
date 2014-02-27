'''
Created on Feb 10, 2014

@package: ally distribution
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the setup distutils arguments for building the egg.
'''

import logging
import os

from ally.container.ioc import injected
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
import re


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
    # ---------------------------------------------------------------- Defined
    name = defines(str, doc='''
    @rtype: string
    The package name.
    ''')
    arguments = defines(dict, doc='''
    @rtype: dictionary{string: object}
    The arguments to be used by setup distutils for building the eggs.
    ''')
    # ---------------------------------------------------------------- Required
    packageSetup = requires(str)
    path = requires(str)
    pathSetup = requires(str)

# --------------------------------------------------------------------

@injected
class ArgSetupHandler(HandlerProcessor):
    '''
    Implementation for a processor that provides the arguments extracted from setup file.
    '''
    
    attributes = {'NAME'            : 'name',
                  'VERSION'         : 'version',
                  'AUTHOR'          : 'author',
                  'AUTHOR_EMAIL'    : 'author_email',
                  'KEYWORDS'        : 'keywords',
                  'INSTALL_REQUIRES': 'install_requires',
                  'DESCRIPTION'     : 'description',
                  'LONG_DESCRIPTION': 'long_description',
                  'TEST_SUITE'      : 'test_suite',
                  'CLASSIFIERS'     : 'classifiers',
                 }
    # The attributes mapping from module constants to distutils setup argument.
    attributeExtra = '__extra__'
    # The extra attribute.
    argumentName = 'name'
    # The name argument.

    def __init__(self):
        assert isinstance(self.attributes, dict), 'Invalid attributes %s' % self.attributes
        assert isinstance(self.attributeExtra, str), 'Invalid attribute extra %s' % self.attributeExtra
        assert isinstance(self.argumentName, str), 'Invalid name argument %s' % self.argumentName
        super().__init__(Package=Package)

    def process(self, chain, distribution:Distribution, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Provides the package build arguments.
        '''
        assert isinstance(distribution, Distribution), 'Invalid distribution %s' % distribution
        if not distribution.packages: return
        
        packages = distribution.packages
        distribution.packages = []
        for package in packages:
            assert isinstance(package, Package), 'Invalid package %s' % package
            assert isinstance(package.packageSetup, str), 'Invalid package setup %s' % package.packageSetup
            assert isinstance(package.pathSetup, str), 'Invalid setup path %s' % package.pathSetup
            
            arguments = {}
            setupPath = os.path.join(package.pathSetup, '__init__.py')
            if os.path.isfile(setupPath):
                g, l = {}, {}
                with open(setupPath, 'rb') as f: exec(f.read(), g, l)
                
                for name, attr in self.attributes.items():
                    if name not in l: continue
                    arguments[attr] = l[name]
                
                if self.attributeExtra in l: arguments.update(l[self.attributeExtra])
                
            if self.argumentName not in arguments:
                log.info('Discarded \'%s\' because no package name found', package.path)
            else:
                package.name = arguments[self.argumentName]
                if re.findall('\s+', package.name):
                    log.info('Discarded \'%s\' because the package name \'%s\' contains white spaces',
                             package.path, package.name)
                else:
                    if package.arguments is None: package.arguments = arguments
                    else: package.arguments.update(arguments)
                    distribution.packages.append(package)
