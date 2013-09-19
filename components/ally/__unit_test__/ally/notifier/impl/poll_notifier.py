'''
Created on Sep 11, 2013

@author: mihaigociu

@package: ally base
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Gociu

Tests the notifier.

'''
# Required in order to register the package extender whenever the unit test is run.
if True:
    import package_extender
    package_extender.PACKAGE_EXTENDER.setForUnitTest(True)

# --------------------------------------------------------------------
import logging
import unittest

from ally.design.processor.attribute import requires, defines
from ally.design.processor.execution import Processing, FILL_ALL
from ally.design.processor.context import Context
from ally.design.processor.assembly import Assembly
from ally.container.ioc import initialize
from ally.notifier.impl.register import RegisterListeners
from ally.notifier.impl.scanner import ScannerHandler

# --------------------------------------------------------------------

logging.basicConfig()
logging.getLogger('ally.design.processor').setLevel(logging.INFO)

# --------------------------------------------------------------------

class TestSolicit(Context):
    '''
    The solicit context.
    '''
    # ---------------------------------------------------------------- Defines
    registerPaths = defines(list, doc='''
    @rtype: list[str]
    The list of paths to scan.
    ''')

# --------------------------------------------------------------------

class TestConfigurationParsing(unittest.TestCase):

    def testConfigurationParser(self):
        ''' '''
        assemblyScanning = Assembly('Files scanner')
        assemblyScanning.add(initialize(RegisterListeners()), initialize(ScannerHandler()))
        #assemblyScanning.add(initialize(RegisterListeners()))
        
        proc = assemblyScanning.create(solicit=TestSolicit)
        assert isinstance(proc, Processing)
        
        solicit = proc.ctx.solicit(registerPaths=['/home/mihaigociu/Work/notifier_test/test1.txt', \
                                                  '/home/mihaigociu/Work/*/test1.txt'])
        arg = proc.execute(FILL_ALL, solicit=solicit)
        assert isinstance(arg.solicit, TestSolicit)

if __name__ == '__main__': unittest.main()
        