'''
Created on Feb 17, 2014

@package: ally distribution
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Generate the setup file.
'''

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
    setup = defines(str, doc='''
    @rtype: string
    The setup text content.
    ''')
    # ---------------------------------------------------------------- Required
    path = requires(str)
    arguments = requires(dict)

# --------------------------------------------------------------------

@injected
class GenerateSetupHandler(HandlerProcessor):
    '''
    Implementation for a processor that provides the setup.py file generator.
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
            
            package.setup = SETUP % ',\n      '.join(entries)
            
