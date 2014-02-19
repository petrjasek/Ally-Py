'''
Created on Feb 17, 2014

@package: ally distribution
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Writes the setup file.
'''

from os.path import join

from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
import os
from ally.design.processor.execution import Chain


# --------------------------------------------------------------------
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

class WriteSetupHandler(HandlerProcessor):
    '''
    Implementation for a processor that provides the setup.py file writing.
    '''

    def process(self, chain, package:Package, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Provides the setup.py file.
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(package, Package), 'Invalid package %s' % package
        assert isinstance(package.path, str), 'Invalid path %s' % package.path
        assert isinstance(package.arguments, dict), 'Invalid arguments %s' % package.arguments
        
        package.pathSetupPy = join(package.path, 'setup.py')
        with open(package.pathSetupPy, 'w') as f:
            print('''
from setuptools import setup, find_packages

# --------------------------------------------------------------------

setup(packages=find_packages('.'),
      platforms=['all'],
      zip_safe=True,
      license='GPL v3',
      url='http://www.sourcefabric.org/en/superdesk/',
''', file=f)
            for name in sorted(package.arguments.keys()):
                print('      %s=%r,' % (name, package.arguments[name]), file=f)
            
            print('      )', file=f)
            
        chain.onFinalize(self.clear)
        
    # ----------------------------------------------------------------
    
    def clear(self, final, package, **keyargs):
        ''' Clears the setup.py files after finalization.'''
        assert isinstance(package, Package), 'Invalid package %s' % package
        assert isinstance(package.pathSetupPy, str), 'Invalid path %s' % package.pathSetupPy
        
        os.remove(package.pathSetupPy)
