'''
Created on Aug 22, 2013

@package: gui core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Gociu

GUI core configuration XML testing.
'''
# Required in order to register the package extender whenever the unit test is run.
if True:
    import package_extender
    package_extender.PACKAGE_EXTENDER.setForUnitTest(True)

# --------------------------------------------------------------------

import logging
import unittest
import os

from ally.support.util_io import IInputStream
from ally.container.ioc import initialize
from ally.design.processor.assembly import Assembly
from ally.design.processor.attribute import defines, requires
from ally.design.processor.context import Context
from ally.design.processor.execution import Processing, FILL_ALL
from ally.xml.digester import RuleRoot, Node
from gui.core.config.impl.processor.xml.parser import ParserHandler
from gui.core.config.impl.rules import URLRule, ActionRule, MethodRule, \
    AccessRule, GroupRule, DescriptionRule, RightRule
from ally.support.util_context import listBFS

from gui.core.config.impl.processor.synchronize.group import Repository as RepositoryGroup
from gui.core.config.impl.processor.synchronize.right import Repository as RepositoryRight

# --------------------------------------------------------------------

logging.basicConfig()
logging.getLogger('ally.design.processor').setLevel(logging.INFO)

# --------------------------------------------------------------------
    
class TestSolicit(Context):
    '''
    The solicit context.
    '''
    # ---------------------------------------------------------------- Defined
    stream = defines(IInputStream)
    uri = defines(str)
    # ---------------------------------------------------------------- Required
    repository = requires(Context)

# --------------------------------------------------------------------
    
class TestConfigurationParsing(unittest.TestCase):

    def testConfigurationParser(self):
        
        parser = ParserHandler()
        parser.rootNode = RuleRoot()
        
        anonymous = parser.rootNode.addRule(GroupRule(), 'Config/Anonymous')
        captcha = parser.rootNode.addRule(GroupRule(), 'Config/Captcha')
        right = parser.rootNode.addRule(RightRule('name'), 'Config/Right')
        right.addRule(DescriptionRule(), 'Description')
        
        #allows = anonymous.addRule(AccessRule(), 'Allows')
        allows = Node('Allows')
        allows.addRule(AccessRule())
        #allows.addRule(MethodRule(fromAttributes=True))
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
        
        #no actions for captcha
        captcha.childrens['Allows'] = allows
        
        right.childrens['Actions'] = actions
        right.childrens['Action'] = action
        right.childrens['Allows'] = allows
        
        assemblyParsing = Assembly('Parsing XML')
        assemblyParsing.add(initialize(parser))
        
        # ------------------------------------------------------------
        
        proc = assemblyParsing.create(solicit=TestSolicit)
        assert isinstance(proc, Processing)
        
        uri = 'file://%s' % os.path.abspath('config_test.xml')
        content = open('config_test.xml', 'rb')
        solicit = proc.ctx.solicit(stream=content, uri = uri)
        
        arg = proc.execute(FILL_ALL, solicit=solicit)
        assert isinstance(arg.solicit, TestSolicit)
        content.close()
        
        groups = listBFS(arg.solicit.repository, RepositoryGroup.children, RepositoryGroup.groupName)
        rights = listBFS(arg.solicit.repository, RepositoryGroup.children, RepositoryRight.rightName)
        for entity in groups+rights:
            print('Group: %s' % entity.groupName if entity.groupName else entity.rightName )
            if entity.description: print('Description: %s' % entity.description)
            
            print('Actions: ')
            if entity.actions:
                for action in entity.actions:
                    print('Action at line %s: ' % action.lineNumber, action.path, action.label, action.script, action.navBar)
                 
            print("Accesses: ")
            if entity.accesses:
                for access in entity.accesses:
                    print('Access at line %s: ' % access.lineNumber, access.filters, access.methods, access.urls)
            
            print()

# --------------------------------------------------------------------

if __name__ == '__main__': unittest.main()