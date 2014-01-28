'''
Created on May 31, 2013

@package: ally core http
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Finds all get invokers that can be directly accessed without the need of extra information, basically all paths that can be
directly related to a node.
'''

from ally.api.operator.extract import inheritedTypesFrom
from ally.api.operator.type import TypeModel, TypeProperty
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
from ally.http.spec.server import HTTP_GET
from collections import deque
from ally.support.util_context import findFirst

# --------------------------------------------------------------------

class Register(Context):
    '''
    The register context.
    '''
    # ---------------------------------------------------------------- Required
    nodes = requires(list)
    polymorphs = requires(dict)
    
class Invoker(Context):
    '''
    The invoker context.
    '''
    # ---------------------------------------------------------------- Required
    node = requires(Context)
    target = requires(TypeModel)
    isModel = requires(bool)
    path = requires(list)
    
class Element(Context):
    '''
    The element context.
    '''
    # ---------------------------------------------------------------- Required
    property = requires(TypeProperty)

class Node(Context):
    '''
    The node context.
    '''
    # ---------------------------------------------------------------- Required
    parent = requires(Context)
    invokers = requires(dict)
    nodesByProperty = requires(dict)
    child = requires(Context)
    childByName = requires(dict)
    properties = requires(set)
    # ---------------------------------------------------------------- Defined
    invokersAccessible = defines(list, doc='''
    @rtype: list[tuple(string, Context)]
    The list of invokers tuples that are accessible for this node, the first entry in tuple is a generated invoker name.
    ''')
    invokersAccessiblePolymorph = defines(dict, doc='''
    @rtype: dict{TypeModel:[tuple(string, Context)]}
    The list of invokers tuples that are accessible for this node, the first entry in tuple is a generated invoker name.
    ''')
    
# --------------------------------------------------------------------

class PathGetAccesibleHandler(HandlerProcessor):
    '''
    Implementation for a processor that provides the accessible invokers for a node.
    '''
    
    def __init__(self):
        super().__init__(Invoker=Invoker, Element=Element, Node=Node)

    def process(self, chain, register:Register, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Provides the accessible invokers.
        '''
        assert isinstance(register, Register), 'Invalid register %s' % register
        if not register.nodes: return  # No nodes to process
        
        for current in register.nodes:
            assert isinstance(current, Node), 'Invalid node %s' % current
            
            if current.invokers and HTTP_GET in current.invokers:
                # The available paths are compiled only for nodes that have a get invoker that can use them.
                target = None
                invoker = current.invokers[HTTP_GET]
                assert isinstance(invoker, Invoker)
                if invoker.isModel and invoker.target: target = invoker.target
                
                for name, node in self.iterAvailable(current, invoker.isModel, target):
                    if not node.invokers or HTTP_GET not in node.invokers: continue
                    if current.invokersAccessible is None: current.invokersAccessible = []
                    
                    current.invokersAccessible.append((name, node.invokers[HTTP_GET]))
                
            elif register.polymorphs and current.properties:
                for prop in current.properties:
                    assert isinstance(prop, TypeProperty)
                    target = prop.parent
                    if target not in register.polymorphs: continue

                    for name, node in self.iterAvailable(current, True, target):
                        if not node.invokers and HTTP_GET not in node.invokers: continue
                        if current.invokersAccessiblePolymorph is None: current.invokersAccessiblePolymorph = dict()
                        accessible = current.invokersAccessiblePolymorph.get(target)
                        if accessible is None: accessible = current.invokersAccessiblePolymorph[target] = []
                        
                        accessible.append((name, node.invokers[HTTP_GET]))
    
    # ----------------------------------------------------------------
    
    def iterAvailable(self, node, isModel, target):
        '''
        Iterates all the available nodes for node.
        '''
        assert isinstance(node, Node), 'Invalid node %s' % node
        assert target is None or isinstance(target, TypeModel), 'Invalid model %s' % target
        
        if target:
            for cname, cnode in self.iterTarget('', node, target):
                yield cname, cnode
        
        for cname, cnode in self.iterChildByName('', node):
            if isModel:
                if cnode.parent and findFirst(cnode.parent, Node.parent, Node.child): yield cname, cnode
            else: yield cname, cnode
            if target:
                for cname, cnode in self.iterTarget(cname, cnode, target): yield cname, cnode
        
        if target and node.nodesByProperty:
            for parent in inheritedTypesFrom(target.clazz, TypeModel):
                assert isinstance(parent, TypeModel), 'Invalid parent %s' % parent
                if not parent.propertyId: continue
                pnode = node.nodesByProperty.get(parent.propertyId)
                if pnode:
                    for cname, cnode in self.iterTarget('', pnode, parent): yield cname, cnode
    
    def iterTarget(self, name, node, target):
        '''
        Iterates all the nodes that are made available by properties in the target.
        '''
        assert isinstance(target, TypeModel), 'Invalid target model %s' % target
        assert isinstance(node, Node), 'Invalid node %s' % node
        tnode = node.child or node
        assert isinstance(tnode, Node), 'Invalid node %s' % tnode
        
        for cname, cnode in self.iterAccessibleByName(name, tnode):
            assert isinstance(cnode, Node), 'Invalid node %s' % cnode

            if not cnode.invokers or not HTTP_GET in cnode.invokers:
                if cnode.child and cnode.child.invokers and HTTP_GET in cnode.child.invokers: cnode = cnode.child
                else: continue

            invoker = cnode.invokers[HTTP_GET]
            assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
            for el in reversed(invoker.path):
                assert isinstance(el, Element), 'Invalid element %s' % el
                if not el.property: continue
                assert isinstance(el.property, TypeProperty), 'Invalid property %s' % el.property
                
                if el.property.parent == target and el.property.name in target.properties:
                    yield cname, cnode
                    for ccname, ccnode in self.iterChildByName(cname, cnode): yield ccname, ccnode
                else:
                    if not tnode.invokers or HTTP_GET not in tnode.invokers: continue
                    ninvoker = tnode.invokers[HTTP_GET]
                    assert isinstance(ninvoker, Invoker), 'Invalid invoker %s' % ninvoker
                    if not ninvoker.path: continue
                    for el in reversed(ninvoker.path):
                        if el.property: break
                    
                    if cnode.properties and el.property in cnode.properties and cnode.child:
                        yield cname, cnode.child
                        for ccname, ccnode in self.iterChildByName(cname, cnode.child):
                            yield ccname, ccnode

                break
    
    def iterChildByName(self, name, node, exclude=None, nameComposer=lambda name, cname, node: ''.join((name, cname))):
        '''
        Iterates all the nodes that are directly available under the child by name attribute in the node.
        '''
        assert isinstance(name, str), 'Invalid name %s' % name
        stack = deque()
        stack.append((name, node))
        while stack:
            name, node = stack.popleft()
            assert isinstance(node, Node), 'Invalid node %s' % node
            if exclude and exclude == node: continue
            if not node.childByName: continue
            for cname, cnode in node.childByName.items():
                cname = nameComposer(name, cname, cnode)
                yield cname, cnode
                stack.append((cname, cnode))
    
    def iterAccessibleByName(self, name, node):
        '''
        Iterates over nodes accessible from the given node.
        '''
        assert isinstance(node, Node), 'Invalid node %s' % node
        for cname, cnode in self.iterChildByName(name, node): yield cname, cnode
        
        current = node
        while current:
            assert isinstance(current, Node)
            if not current.parent: return
            parent = current.parent
            if not parent.childByName:
                current = parent.parent
                continue
            
            for pname, pnode in self.iterChildByName('', parent, node, lambda name, cname, cnode: self.nodeName(cnode)):
                yield pname, pnode
            
            current = parent

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
