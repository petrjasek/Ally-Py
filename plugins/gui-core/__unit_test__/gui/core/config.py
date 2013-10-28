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

from gui.core.config.impl.processor.synchronize.category import RepositoryGroup, RepositoryRight,\
    SynchronizeRightsHandler

from pkg_resources import get_provider, ResourceManager

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
        assemblyParsing = self.createAssemplyParsing()
        result = self.executeProcess(assemblyParsing)
        
        groupRepos = listBFS(result.solicit.repository, RepositoryGroup.children, RepositoryGroup.groupName)
        rightRepos = listBFS(result.solicit.repository, RepositoryGroup.children, RepositoryRight.rightName)
        
        #make sure the number of groups and rights is correct
        self.assertTrue(len(groupRepos) == 2 and len(rightRepos) == 5, 'Wrong number of groups and rights: %s groups, %s rights' \
                                                                        % (len(groupRepos), len(rightRepos))) 
        
        groups = {group.groupName:group for group in groupRepos}
        #make sure Anonymous and Captcha groups have been parsed
        self.assertTrue('Anonymous' in groups and 'Captcha' in groups, 'Missing groups: Anonymous and Captcha')
        
        rights = {right.rightName:right for right in rightRepos}
        #make sure Requests_inspection right has been parsed
        self.assertTrue('Requests_inspection' in rights and 'Requests_inspection_2' in rights, 'Missing rights: Requests_inspection, Requests_inspection_2')
        #check if description has been parsed
        for right in rights.values():
            self.assertIsNotNone(right.description, 'Missing description for %s' % right.description) 
        
        #check actions for group Anonymous
        self.checkActions(groups, 'Anonymous', ['menu', 'menu.request', 'menu.request.blob', 'menu.mucu', 'menu.cucu'])
        
        #check actions for right Requests_inspection
        self.checkActions(rights, 'Requests_inspection', ['menu_2', 'menu_2.request', 'menu_2.mucu'])
        
        #check accesses for group Anonymous
        toCheck = [(filter, url, method) for filter in ['FilterDummy','Authent','lala'] for method in ['GET'] 
                   for url in ['User/*', 'User/*/Blog', 'User/#/SubUser/*']]
        self.checkAccesses(groups, 'Anonymous', toCheck)
        
        #check accesses for right Requests_inspection
        toCheck = [(filter, url, method) for filter in ['userAuth'] for method in ['GET'] 
                   for url in ['User/*', 'User/*/Blog', 'User/#/SubUser/*']]
        self.checkAccesses(rights, 'Requests_inspection', toCheck)
        
        #check right inheritance attribute
        self.assertTrue('Requests_inspection' in rights['Requests_inspection_2'].rightInherits, 'Inheritance not detected for Requests_inspection_2 and Requests_inspection') 
    
    def testSyncRights(self):
        '''
        Will test parts of the Right Synchronization assemblers (the parts that don't interact with the database)
        '''
        assemblyParsing = self.createAssemplyParsing()
        result = self.executeProcess(assemblyParsing)
        
        rightRepos = listBFS(result.solicit.repository, RepositoryGroup.children, RepositoryRight.rightName)
        syncRigthsAssembler = SynchronizeRightsHandler()
        
        rights = {right.rightName:right for right in rightRepos}
        
        #test cyclic inheritance first
        cyclicInheritance = ['Right_1', 'Right_2', 'Right_3']
        rightsCyclicTest = {right.rightName:[right] for right in rightRepos}
        
        self.assertTrue(syncRigthsAssembler.isCyclicInheritance('Right_1', rightsCyclicTest), 'Cyclic inheritance not detected for %s' % rightsCyclicTest)
        self.assertFalse(syncRigthsAssembler.isCyclicInheritance('Requests_inspection', rightsCyclicTest), 'Non-existing cyclic inheritance detected for Requests_inspection') 
        
        #test rights inheritance - discard the cyclic inheritance rights
        syncRigthsAssembler.doInheritance([right for right in rightRepos if right.rightName not in cyclicInheritance])
        #check if actions have been inherited correctly from Requests_inspection
        self.checkActions(rights, 'Requests_inspection_2', ['menu_2', 'menu_2.request', 'menu_2.mucu'])
        
        #check if accesses have been inherited correctly from Requests_inspection
        toCheck = [(filter, url, method) for filter in ['userAuth'] for method in ['GET'] 
                   for url in ['User/*', 'User/*/Blog', 'User/#/SubUser/*']]
        self.checkAccesses(rights, 'Requests_inspection_2', toCheck)
        
        
    def checkAccesses(self, categories, categoryName, toCheck):
        filtersUrlsMethods = set((filter, url, method) for access in categories[categoryName].accesses for url in access.urls 
                       for method in access.methods for filter in access.filters)
        missing = []
        for t in toCheck:
            if not t in filtersUrlsMethods: missing.append(t)
        self.assertFalse(missing, 'Missing accesses from category %s: %s' % (categoryName, missing)) 
    
    def checkActions(self, categories, categoryName, toCheck):
        actions = {action.path: action for action in categories[categoryName].actions}
        missing = []
        for action in toCheck:
            if not action in actions: missing.append(action)
        self.assertFalse(missing, 'Missing actions from category %s: %s' % (categoryName, missing))
    
    def executeProcess(self, assembly):
        proc = assembly.create(solicit=TestSolicit)
        assert isinstance(proc, Processing)
        
        #use packageProvider (not os package) to access files from inside the package (like config_test.xml)
        packageProvider = get_provider(__name__)
        manager = ResourceManager()
        self.assertTrue(packageProvider.has_resource('config_test.xml'), 'Xml Config file missing')
        
        content = packageProvider.get_resource_stream(manager, 'config_test.xml')
        solicit = proc.ctx.solicit(stream=content, uri = 'file://%s' % 'config_test.xml')
        
        arg = proc.execute(FILL_ALL, solicit=solicit)
        assert isinstance(arg.solicit, TestSolicit)
        content.close()
        return arg
    
    def createAssemplyParsing(self):
        parser = ParserHandler()
        parser.rootNode = RuleRoot()
        
        anonymous = parser.rootNode.addRule(GroupRule(), 'Config/Anonymous')
        captcha = parser.rootNode.addRule(GroupRule(), 'Config/Captcha')
        right = parser.rootNode.addRule(RightRule('name', 'inherits'), 'Config/Right')
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
        return assemblyParsing
    
# --------------------------------------------------------------------

if __name__ == '__main__': unittest.main()