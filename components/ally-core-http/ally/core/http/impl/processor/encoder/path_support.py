'''
Created on Mar 15, 2013

@package: ally core http
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the path support.
'''

from ally.api.operator.type import TypeModel, TypeProperty
from ally.core.spec.transform import ITransfrom
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
from ally.core.impl.processor.encoder.base import ExportingSupport
from ally.api.operator.extract import inheritedTypesFrom
from collections import OrderedDict

# --------------------------------------------------------------------

class Register(Context):
    '''
    The register context.
    '''
    # ---------------------------------------------------------------- Required
    nodes = requires(list)
    polymorphs = requires(dict)
    polymorphed = requires(dict)

class Node(Context):
    '''
    The node context.
    '''
    # ---------------------------------------------------------------- Required
    invokersGet = requires(dict)
    invokersAccessible = requires(dict)
    
class Invoker(Context):
    '''
    The invoker context.
    '''
    # ---------------------------------------------------------------- Required
    path = requires(list)
 
class Element(Context):
    '''
    The element context.
    '''
    # ---------------------------------------------------------------- Required
    node = requires(Context)
    property = requires(TypeProperty)

class Create(Context):
    '''
    The create item encoder context.
    '''
    # ---------------------------------------------------------------- Required
    encoder = requires(ITransfrom)
       
class Support(Context):
    '''
    The support context.
    '''
    # ---------------------------------------------------------------- Defined
    nodesValues = defines(dict, doc='''
    @rtype: dictionary{Context: object}
    The values used in constructing the paths indexed by corresponding node.
    ''')

class Polymorph(Context):
    '''
    The polymorph context.
    '''
    # ---------------------------------------------------------------- Required
    target = requires(TypeModel)
    parents = requires(list)
    values = requires(dict)

# --------------------------------------------------------------------

pathUpdaterSupportEncodeExport = ExportingSupport(Support)
# The path updater support export.

class PathUpdaterSupportEncode(HandlerProcessor):
    '''
    Implementation for a handler that provides the models paths update when in a collection.
    '''
    
    def __init__(self):
        super().__init__(Invoker=Invoker, Element=Element)
        
    def process(self, chain, create:Create, node:Node, register:Register, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Create the update model path encoder.
        '''
        assert isinstance(create, Create), 'Invalid create %s' % create
        assert isinstance(node, Node), 'Invalid node %s' % node
        
        if create.encoder is None: return 
        # There is no encoder to provide path update for.
        if not node.invokersAccessible and not node.invokersGet: return
        # No get invokers to support.
        
        if isinstance(create.objType, TypeModel):
            assert isinstance(create.objType, TypeModel)
            properties = set(create.objType.properties.values())
        elif isinstance(create.objType, TypeProperty):
            properties = set()
            properties.add(create.objType)
        else: return  # The type is not for a path updater, nothing to do, just move along
        
        elements = []
        if node.invokersGet:
            assert isinstance(node.invokersGet, dict), 'Invalid get invokers %s' % node.invokersGet
            for prop in properties:
                ninvoker = node.invokersGet.get(prop)
                if not ninvoker: continue
                assert isinstance(ninvoker, Invoker), 'Invalid invoker %s' % ninvoker
                
                for el in reversed(ninvoker.path):
                    assert isinstance(el, Element), 'Invalid element %s' % el
                    if el.property == prop:
                        elements.append(el)
                        break

        if isinstance(create.objType, TypeModel):

            typeElements = {create.objType: elements}
            types = [create.objType]
            if register.polymorphed and create.objType in register.polymorphed:
                for polymorph in register.polymorphed[create.objType]:
                    assert isinstance(polymorph, Polymorph), 'Invalid polymorph %s' % polymorph
                    assert isinstance(polymorph.target, TypeModel)
                    types.append(polymorph.target)
            
            if node.invokersAccessible:
                for objType in types:
                    if objType not in node.invokersAccessible: continue
                    invokersAccessible = node.invokersAccessible[objType]
                    
                    assert isinstance(invokersAccessible, OrderedDict), 'Invalid accessible invokers %s' % invokersAccessible
                    for _name, invoker in invokersAccessible.items():
                        assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
                        
                        for el in reversed(invoker.path):
                            assert isinstance(el, Element), 'Invalid element %s' % el
                            if el.property:
                                elements = typeElements.get(objType)
                                if not elements: elements = typeElements[objType] = []
                                elements.append(el)
                                break
    
            if typeElements:
                create.encoder = EncoderPathUpdaterModel(create.encoder, typeElements)
        
        elif elements:
            create.encoder = EncoderPathUpdaterProperty(create.encoder, elements)

    def nodeName(self, node):
        '''
        Return the node name based on the nodes that contain the name:node correspondence dictionary
        '''
        if not node.parent: return ''
        elif node.parent.childByName:
            for cname, cnode in node.parent.childByName.items():
                if cnode == node: return cname
        elif node.parent.child: return self.nodeName(node.parent)
        return None
    
# --------------------------------------------------------------------

class EncoderPathUpdaterModel(ITransfrom):
    '''
    Implementation for a @see: ITransfrom that updates the path before encoding .
    '''
    
    def __init__(self, encoder, typeElements):
        '''
        Construct the path updater for model value.
        '''
        assert isinstance(encoder, ITransfrom), 'Invalid property encoder %s' % encoder
        assert isinstance(typeElements, dict), 'Invalid elements %s' % typeElements
        
        self.encoder = encoder
        self.typeElements = typeElements
        
    def transform(self, value, target, support):
        '''
        @see: ITransfrom.transform
        '''
        assert isinstance(support, Support), 'Invalid support %s' % support
        if support.nodesValues is None: support.nodesValues = {}

        types = inheritedTypesFrom(type(value), TypeModel, inDepth=True)
        for typeElement in types:
            elements = self.typeElements.get(typeElement)
            if elements: 
                for el in elements:
                    assert isinstance(el, Element), 'Invalid element %s' % el
                    assert isinstance(el.property, TypeProperty), 'Invalid property %s' % el.property
                    support.nodesValues[el.node] = getattr(value, el.property.name)
                break
        
        self.encoder.transform(value, target, support)

class EncoderPathUpdaterProperty(ITransfrom):
    '''
    Implementation for a @see: ITransfrom that updates the path before encoding .
    '''
    
    def __init__(self, encoder, elements):
        '''
        Construct the path updater for property value.
        '''
        assert isinstance(encoder, ITransfrom), 'Invalid property encoder %s' % encoder
        assert isinstance(elements, list), 'Invalid elements %s' % elements
        
        self.encoder = encoder
        self.elements = elements
        
    def transform(self, value, target, support):
        '''
        @see: ITransfrom.transform
        '''
        assert isinstance(support, Support), 'Invalid support %s' % support
        if support.nodesValues is None: support.nodesValues = {}
        
        for el in self.elements:
            assert isinstance(el, Element), 'Invalid element %s' % el
            assert isinstance(el.property, TypeProperty), 'Invalid property %s' % el.property
            support.nodesValues[el.node] = value
        
        self.encoder.transform(value, target, support)
