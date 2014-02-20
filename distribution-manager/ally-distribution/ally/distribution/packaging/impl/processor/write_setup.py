'''
Created on Feb 17, 2014

@package: ally distribution
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Writes the setup file.
'''

import os
from os.path import join

from ally.container.ioc import injected
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.execution import Chain
from ally.design.processor.handler import HandlerProcessor


# --------------------------------------------------------------------
SETUP = '''
from setuptools import setup, find_packages

# --------------------------------------------------------------------

setup(%s
      )
'''

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
    pathSetupPy = defines(str, doc='''
    @rtype: string
    The setup.py path.
    ''')
    # ---------------------------------------------------------------- Required
    path = requires(str)
    arguments = requires(dict)

# --------------------------------------------------------------------

@injected
class WriteSetupHandler(HandlerProcessor):
    '''
    Implementation for a processor that provides the setup.py file writing.
    '''
    
    defaultEntries = [
                      ('platforms', '[\'all\']'),
                      ('zip_safe', 'True'),
                      ('license', '\'GPL v3\''),
                      ('url', '\'http://www.sourcefabric.org/en/superdesk/\''),
                      ('packages', 'find_packages(\'.\')'),
                      ]
    # The default entries to put in setup if not present in the arguments.
    
    def __init__(self):
        assert isinstance(self.defaultEntries, list), 'Invalid default entries %s' % self.defaultEntries
        super().__init__(Package=Package)

    def process(self, chain, distribution:Distribution, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Provides the setup.py file.
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(distribution, Distribution), 'Invalid distribution %s' % distribution
        if not distribution.packages: return
            
        for package in distribution.packages:
            assert isinstance(package, Package), 'Invalid package %s' % package
            assert isinstance(package.path, str), 'Invalid path %s' % package.path
            assert isinstance(package.arguments, dict), 'Invalid arguments %s' % package.arguments
            
            entries = []
            for name, value in self.defaultEntries:
                if name in package.arguments: continue
                entries.append('%s=%s' % (name, value))
                
            for name in sorted(package.arguments.keys()):
                entries.append('%s=%r' % (name, package.arguments[name]))
            
            package.pathSetupPy = join(package.path, 'setup.py')
            with open(package.pathSetupPy, 'w') as f:
                print(SETUP % ',\n      '.join(entries), file=f)
            
        chain.onFinalize(self.clear)
        
    # ----------------------------------------------------------------
    
    def clear(self, final, distribution, **keyargs):
        ''' Clears the setup.py files after finalization.'''
        assert isinstance(distribution, Distribution), 'Invalid distribution %s' % distribution
        if not distribution.packages: return
            
        for package in distribution.packages:
            assert isinstance(package, Package), 'Invalid package %s' % package
            assert isinstance(package.pathSetupPy, str), 'Invalid path %s' % package.pathSetupPy
            
            os.remove(package.pathSetupPy)
