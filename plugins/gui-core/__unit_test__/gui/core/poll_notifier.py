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

from ally.container.ioc import initialize
from ally.design.processor.assembly import Assembly
from ally.design.processor.execution import Processing, FILL_ALL
from ally.notifier.impl.processor.scanner_file_system import FileSystemScanner
from ally.xml.digester import RuleRoot, Node
from gui.core.config.impl.processor.configuration_notifier import \
    ConfigurationListeners
from gui.core.config.impl.processor.xml.parser import ParserHandler
from gui.core.config.impl.rules import URLRule, ActionRule, MethodRule, \
    AccessRule, GroupRule, DescriptionRule

# --------------------------------------------------------------------
logging.basicConfig()
logging.getLogger('ally.design.processor').setLevel(logging.INFO)
logging.getLogger('ally.notifier').setLevel(logging.DEBUG)

# --------------------------------------------------------------------

class TestConfigurationParsing(unittest.TestCase):

    def testConfigurationParser(self):
        ''' '''
        parser = ParserHandler()
        parser.rootNode = RuleRoot()
        
        anonymous = parser.rootNode.addRule(GroupRule(), 'Config/Anonymous')
        captcha = parser.rootNode.addRule(GroupRule(), 'Config/Captcha')
        right = parser.rootNode.addRule(GroupRule(), 'Config/Right')
        right.addRule(DescriptionRule(), 'Description')
        
        # allows = anonymous.addRule(AccessRule(), 'Allows')
        allows = Node('Allows')
        allows.addRule(AccessRule())
        # allows.addRule(MethodRule(fromAttributes=True))
        allows.addRule(URLRule(), 'URL')
        allows.addRule(MethodRule(), 'Method')
        
        action = Node('Action')
        action.addRule(ActionRule())
        action.childrens['Action'] = action
        
        actions = Node('Actions')
        actions.childrens['Action'] = action
        
        anonymous.childrens['Actions'] = actions
        anonymous.childrens['Action'] = action
        anonymous.childrens['Allows'] = allows
        
        # no actions for captcha
        captcha.childrens['Allows'] = allows
        
        right.childrens['Actions'] = actions
        right.childrens['Action'] = action
        right.childrens['Allows'] = allows
        
        assemblyParsing = Assembly('Parsing XML')
        assemblyParsing.add(initialize(parser))
        
        assemblyScanning = Assembly('Files scanner')
        registerListeners = ConfigurationListeners()
        registerListeners.assemblyConfiguration = assemblyParsing
        registerListeners.patterns = ['file:///home/mihaigociu/Work/notifier_test/config_test.xml',
                                      'file:///home/mihaigociu/Work/*/config_test.xml']
        
        assemblyScanning.add(initialize(registerListeners), initialize(FileSystemScanner()))
        # assemblyScanning.add(initialize(RegisterListeners()))
        
        proc = assemblyScanning.create()
        assert isinstance(proc, Processing)
        
        proc.execute(FILL_ALL)

if __name__ == '__main__': unittest.main()
        
