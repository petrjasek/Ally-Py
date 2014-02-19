'''
Created on Feb 17, 2014

@package: ally distribution
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Writes the setup configuration file.
'''

import os
from os.path import join

from ally.container.ioc import injected
from ally.design.processor.attribute import requires, attribute
from ally.design.processor.context import Context
from ally.design.processor.execution import Chain
from ally.design.processor.handler import HandlerProcessor


# --------------------------------------------------------------------
class Package(Context):
    '''
    The package context.
    '''
    # ---------------------------------------------------------------- Defined
    pathSetupCfg = attribute(str, doc='''
    @rtype: string
    The setup.cfg path.
    ''')
    # ---------------------------------------------------------------- Required
    path = requires(str)
    arguments = requires(dict)

# --------------------------------------------------------------------

@injected
class WriteConfigHandler(HandlerProcessor):
    '''
    Implementation for a processor that provides the setup.cfg file writing.
    '''
    
    configurations = dict
    # The configurations dictionary, as a key the configuration group and and as a value a dictionary
    # having as a key the configuration name.
    
    def __init__(self):
        assert isinstance(self.configurations, dict), 'Invalid configurations %s' % self.configurations
        super().__init__()

    def process(self, chain, package:Package, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Provides the setup.cfg file.
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(package, Package), 'Invalid package %s' % package
        assert isinstance(package.path, str), 'Invalid path %s' % package.path
        assert isinstance(package.arguments, dict), 'Invalid arguments %s' % package.arguments
        
        package.pathSetupCfg = join(package.path, 'setup.cfg')
        with open(package.pathSetupCfg, 'w') as f:
            for group in sorted(self.configurations.keys()):
                print('[%s]' % group, file=f)
                configs = self.configurations[group]
                for name in sorted(configs.keys()):
                    print('%s=%s' % (name, configs[name]), file=f)
            
        chain.onFinalize(self.clear)
        
    # ----------------------------------------------------------------
    
    def clear(self, final, package, **keyargs):
        ''' Clears the setup.cfg files after finalization.'''
        assert isinstance(package, Package), 'Invalid package %s' % package
        assert isinstance(package.pathSetupCfg, str), 'Invalid path %s' % package.pathSetupCfg
        
        os.remove(package.pathSetupCfg)
