'''
Created on Oct 8, 2013
 
@package: ally.distribution
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Cristian Domsa
 
Functionality for building eggs.
'''
import logging
from ally.distribution.util import SETUP_FILENAME, PYTHON_CLI, BUILD_EGG, runCmd
from ally.container.ioc import injected

# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Builder:
    
    packagePath = str
    #path to the current package
    packageName = str
    #name of the package
    
    def __init__(self):
        '''
        do nothing
        '''
                
    def build(self):
        '''
        builds egg for current package
        '''
        assert logging.info('*** BUILD egg *** {0}'.format(self.packageName)) or True
        
        cmd = ' '.join([PYTHON_CLI, SETUP_FILENAME, BUILD_EGG]) 
        runCmd(self.packagePath, cmd)