'''
Created on Feb 14, 2014

@package: ally core http
@copyright: 2014 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mugur Rus

Builds a parsing tree for polymorph models 
'''

import logging
from ally.api.operator.type import TypeModel
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
from ally.http.spec.server import HTTP_POST, HTTP_PUT

# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Register(Context):
    '''
    The register context.
    '''
    # ---------------------------------------------------------------- Required
    invokers = requires(list)
    polymorphed = requires(dict)
    
class Invoker(Context):
    '''
    The invoker context.
    '''
    # ---------------------------------------------------------------- Defined
    polymorphRoutes = defines(dict, doc='''
    @rtype: dictionary{TypeModel: Context}
    The polymorph routes indexed by the polymorphed model type.
    ''')
    # ---------------------------------------------------------------- Required
    node = requires(Context)
    target = requires(TypeModel)
    methodHTTP = requires(str)
    decodingContent = requires(Context)

class Node(Context):
    '''
    The node context.
    '''
    # ---------------------------------------------------------------- Required
    invokersPost = requires(dict)
    invokersPut = requires(dict)

class Polymorph(Context):
    '''
    The polymorph context.
    '''
    # ---------------------------------------------------------------- Required
    target = requires(TypeModel)
    values = requires(dict)

class PolymorphDecodingModel(Context):
    '''
    The polymorph decoding context.
    '''
    # ---------------------------------------------------------------- Required
    invoker = defines(Context, doc='''
    @rtype: Context
    The invoker for the specialized model.
    ''')
    values = defines(dict, doc='''
    @rtype: dictionary{string: object}
    A dictionary containing the polymorphic values.
    ''')
    decodingContent = defines(Context, doc='''
    @rtype: Context
    The decoding to be used in decoding the content values.
    ''')

# --------------------------------------------------------------------

class PolymorphPersistHandler(HandlerProcessor):
    '''
    Implementation for a processor that provides the dictionary of decodings/invokers corresponding
    to each specialized model.
    '''
    
    def __init__(self):
        super().__init__(Invoker=Invoker, Node=Node)
    
    def process(self, chain, register:Register, PolymorphDecoding:PolymorphDecodingModel, **keyargs):
        '''
        @see: PolymorphTreeHandler.process
        
        Provides the invoker, decoding tuples indexed by the polymorphed model type.
        '''
        assert isinstance(register, Register), 'Invalid register %s' % register
        if not register.invokers: return
        
        for invoker in register.invokers:
            assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
            assert isinstance(invoker.node, Node), 'Invalid node %s' % invoker.node
            
            if not invoker.target: continue
            assert isinstance(invoker.target, TypeModel), 'Invalid target %s' % invoker.target
            
            if invoker.methodHTTP == HTTP_POST: invokers = invoker.node.invokersPost
            elif invoker.methodHTTP == HTTP_PUT: invokers = invoker.node.invokersPut
            else: continue
            if not invokers: continue
            
            if invoker.target not in register.polymorphed: continue
            for polymorph in register.polymorphed[invoker.target]:
                assert isinstance(polymorph, Polymorph)
                if not polymorph.target in invokers: continue
                
                decoding = invoker.polymorphRoutes[polymorph.target] = PolymorphDecoding()
                decoding.invoker = invokers[polymorph.target]
                decoding.values = polymorph.values
                decoding.decodingContent = invoker.decodingContent
                
                print('set', decoding.invoker.id, decoding.values, 'to', invoker.id)
