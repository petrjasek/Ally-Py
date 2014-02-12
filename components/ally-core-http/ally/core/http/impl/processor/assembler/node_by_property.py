'''
Created on Jan 17, 2014

@package: ally core http
@copyright: 2014 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mugur Rus

Indexes nodes by id property.
'''

from ally.api.operator.type import TypeProperty
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
from collections import deque
import logging

# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Register(Context):
    '''
    The register context.
    '''
    # ---------------------------------------------------------------- Required
    root = requires(Context)

class Node(Context):
    '''
    The node context.
    '''
    # ---------------------------------------------------------------- Defined
    nodesByProperty = defines(dict, doc='''
    @rtype: dictionary{TypeProperty: set(Context)}
    The nodes contexts indexed by the identifier property model.
    ''')
    # ---------------------------------------------------------------- Required
    child = requires(Context)
    childByName = requires(dict)
    properties = requires(set)
    parent = requires(Context)

# --------------------------------------------------------------------

class NodeByPropertyHandler(HandlerProcessor):
    '''
    Implementation for a processor that provides all nodes indexed by the identifier property.
    '''
    
    def __init__(self):
        super().__init__(Node=Node)

    def process(self, chain, register:Register, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Provides the nodes indexed by the identifier property.
        '''
        assert isinstance(register, Register), 'Invalid register %s' % register
        if register.root is None: return  # No root context to process
        assert isinstance(register.root, Node), 'Invalid node %s' % register.node
        
        stack = deque()
        stack.append((register.root, {}))
        while stack:
            current, previous = stack.popleft()
            # First we search the first level node properties.
            nodesByProperty = {prop:set(nodes) for prop, nodes in previous.items()}
            nstack, k = [current], 0
            while len(nstack) > k:
                node = nstack[k]
                k += 1
                
                assert isinstance(node, Node), 'Invalid node %s' % node
                if node.childByName: nstack.extend(node.childByName.values())
                elif node.child:
                    assert isinstance(node.child, Node), 'Invalid node %s' % node.child
                    for prop in node.properties:
                        assert isinstance(prop, TypeProperty), 'Invalid property %s' % prop
                        nodes = nodesByProperty.get(prop)
                        if nodes is None: nodes = nodesByProperty[prop] = set()
                        nodes.add(node.child)
                    
                    if node.child.childByName:
                        stack.extend((nod, nodesByProperty) for nod in node.child.childByName.values())
                    elif node.child.child:
                        stack.append((node.child.child, nodesByProperty))
                    
            for node in nstack:
                node.nodesByProperty = nodesByProperty
            for nodes in nodesByProperty.values():
                for node in nodes: node.nodesByProperty = nodesByProperty
