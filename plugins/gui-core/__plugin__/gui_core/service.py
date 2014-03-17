'''
Created on Jan 9, 2012

@package: gui core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the services for the gui core.
'''

from __setup__.ally.notifier import registersListeners
from ally.container import ioc, support, app
from ally.design.processor.assembly import Assembly
from ally.design.processor.handler import Handler
from ally.xml.digester import Node, RuleRoot
from ally.xml.parser import ParserHandler
from ally.xml.rules import AccessRule, MethodRule, URLRule, ActionRule, DescriptionRule, GroupRule, RightRule
from ally.notifier.impl.processor.configuration_notifier import ConfigurationListeners
from ally.xml.uri_repository_caching import UriRepositoryCaching
import logging

# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# The synchronization processors
synchronizeAction = synchronizeGroups = synchronizeRights = synchronizeGroupActions = synchronizeRightActions = \
prepareGroupAccesses = prepareRightAccesses = syncCategoryAccesses = syncGroupAccesses = syncRightAccesses = support.notCreated  # Just to avoid errors
support.createEntitySetup('gui.core.config.impl.processor.synchronize.**.*')

# --------------------------------------------------------------------

@ioc.config
def access_group():
    '''
    Contains the names of the access groups that are expected in the configuration file. Expected properties are name and
    optionally a flag indicating if actions are allowed.
    '''
    return {
            'Anonymous': dict(hasActions=True, isAnonymous=True),
            'Captcha': dict(hasActions=False),
            'Right': dict(hasActions=True, isRight=True)
            }
    
@ioc.config
def gui_configuration():
    ''' The URI pattern (can have * for dynamic path elements) where the XML configurations can be found.'''
    return []

# --------------------------------------------------------------------

@ioc.entity
def assemblyGUIConfiguration() -> Assembly:
    return Assembly('GUI Configurations')

@ioc.entity
def configurationStreams() -> list:
    '''
    The configurations streams, this entries are processed at application start.
    The list entries need to be tuples having on the first position a stream URL and on the second
    position the configuration stream. 
    '''
    return []

@ioc.entity
def nodeRootXML() -> Node: return RuleRoot()

@ioc.entity
def parserXML() -> Handler:
    b = ParserHandler()
    b.rootNode = nodeRootXML()
    return b

@ioc.entity
def uriRepositoryCaching() -> Handler:
    b = UriRepositoryCaching()
    return b

@ioc.entity
def configurationListeners() -> Handler:
    configGui = ConfigurationListeners()
    configGui.assemblyConfiguration = assemblyGUIConfiguration()
    configGui.patterns = gui_configuration()
    return configGui

# --------------------------------------------------------------------

@ioc.before(synchronizeGroupActions)
def updateAccessGroup():
    synchronizeGroupActions().anonymousGroups = set(name for name, spec in access_group().items()
                                                    if spec.get('isAnonymous', False))

@ioc.before(synchronizeGroups)
def updateGroup():
    synchronizeGroups().anonymousGroups = set(name for name, spec in access_group().items()
                                                    if spec.get('isAnonymous', False))

@ioc.before(nodeRootXML)
def updateRootNodeXMLForGroups():
    for name, spec in access_group().items():
        assert isinstance(name, str), 'Invalid name %s' % name
        assert isinstance(spec, dict), 'Invalid specifications %s' % spec
        if spec.get('isRight', False): node = nodeRootXML().addRule(RightRule('name', 'inherits'), 'Config/%s' % name)
        else: node = nodeRootXML().addRule(GroupRule(), 'Config/%s' % name)
        addNodeAccess(node)
        addNodeDescription(node)
        if spec.get('hasActions', False): addNodeAction(node)

@ioc.before(assemblyGUIConfiguration)
def updateAssemblyConfiguration():
    assemblyGUIConfiguration().add(parserXML(), uriRepositoryCaching(), synchronizeAction(), synchronizeGroups(), synchronizeRights(),
                                synchronizeGroupActions(), synchronizeRightActions(),
                                prepareGroupAccesses(), prepareRightAccesses(), syncGroupAccesses(), syncRightAccesses())

@ioc.before(registersListeners)
def updateRegistersListenersForConfiguration():
    if gui_configuration(): registersListeners().append(configurationListeners())
    else: log.info('There are no GUI rights configuration files to be scanned.')

@app.deploy
def processConfigurationStreams():
    ''' Process the configurations streams.'''
    if not configurationStreams():
        log.info('There are no GUI rights configuration streams to be processed.')
        return
    
    for uri, content in configurationStreams(): configurationListeners().doOnContentCreated(uri, content)
    

# --------------------------------------------------------------------

def addNodeDescription(node):
    assert isinstance(node, Node), 'Invalid node %s' % node
    node.addRule(DescriptionRule(), 'Description')

def addNodeAccess(node):
    assert isinstance(node, Node), 'Invalid node %s' % node
    
    access = node.addRule(AccessRule(), 'Allows')
    access.addRule(MethodRule(fromAttributes=True))
    access.addRule(URLRule(), 'URL')
    access.addRule(MethodRule(), 'Method')

def addNodeAction(node):
    assert isinstance(node, Node), 'Invalid node %s' % node
    
    action = Node('Action')
    action.addRule(ActionRule())
    action.childrens['Action'] = action
    
    actions = Node('Actions')
    actions.childrens['Action'] = action
    
    node.childrens['Actions'] = actions
    node.childrens['Action'] = action
