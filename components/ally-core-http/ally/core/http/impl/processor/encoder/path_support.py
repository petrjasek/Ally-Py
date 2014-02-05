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

# --------------------------------------------------------------------

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
    
# --------------------------------------------------------------------

pathUpdaterSupportEncodeExport = ExportingSupport(Support)
# The path updater support export.

class PathUpdaterSupportEncode(HandlerProcessor):
    '''
    Implementation for a handler that provides the models paths update when in a collection.
    '''
    
    def __init__(self):
        super().__init__(Invoker=Invoker, Element=Element)
        
    def process(self, chain, create:Create, node:Node, invoker:Invoker, **keyargs):
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
        
        if isinstance(create.objType, TypeModel) and node.invokersAccessible and create.objType in node.invokersAccessible:
            invokersAccessible = node.invokersAccessible[create.objType]
            assert isinstance(invokersAccessible, list), 'Invalid accessible invokers %s' % invokersAccessible
            for _name, invoker in invokersAccessible:
                assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
                for el in reversed(invoker.path):
                    assert isinstance(el, Element), 'Invalid element %s' % el
                    if el.property in properties:
                        elements.append(el)
                        break
        
        if elements:
            create.encoder = EncoderPathUpdater(create.encoder, elements, isinstance(create.objType, TypeModel))

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

class EncoderPathUpdater(ITransfrom):
    '''
    Implementation for a @see: ITransfrom that updates the path before encoding .
    '''
    
    def __init__(self, encoder, elements, isModel):
        '''
        Construct the path updater.
        '''
        assert isinstance(encoder, ITransfrom), 'Invalid property encoder %s' % encoder
        assert isinstance(elements, list), 'Invalid elements %s' % elements
        assert isinstance(isModel, bool), 'Invalid is model flag %s' % isModel
        
        self.encoder = encoder
        self.elements = elements
        self.isModel = isModel
        
    def transform(self, value, target, support):
        '''
        @see: ITransfrom.transform
        '''
        assert isinstance(support, Support), 'Invalid support %s' % support
        if support.nodesValues is None: support.nodesValues = {}

        for el in self.elements:
            assert isinstance(el, Element), 'Invalid element %s' % el
            assert isinstance(el.property, TypeProperty), 'Invalid property %s' % el.property
            if self.isModel: support.nodesValues[el.node] = getattr(value, el.property.name)
            else: support.nodesValues[el.node] = value
        
        self.encoder.transform(value, target, support)
