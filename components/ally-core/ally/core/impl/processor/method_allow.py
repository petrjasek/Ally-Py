'''
Created on Mar 6, 2014

@package: ally core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the allowed methods handler.
'''

from ally.container.ioc import injected
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor


# --------------------------------------------------------------------
class Node(Context):
    '''
    The node context.
    '''
    # ---------------------------------------------------------------- Required
    invokers = requires(dict)

class Request(Context):
    '''
    The request context.
    '''
    # ---------------------------------------------------------------- Required
    node = requires(Context)

class Response(Context):
    '''
    The response context.
    '''
    # ---------------------------------------------------------------- Defined
    allows = defines(set, doc='''
    @rtype: set(string)
    The allowed methods.
    ''')
    # ---------------------------------------------------------------- Optional
    isSuccess = requires(bool)
    
# --------------------------------------------------------------------

@injected
class MethodAllowHandler(HandlerProcessor):
    '''
    Implementation for a processor that provides the allowed methods.
    '''
    
    def __init__(self):
        super().__init__(Node=Node)

    def process(self, chain, request:Request, response:Response, **keyargs):
        '''
        Provide the allowed mehtods.
        '''
        assert isinstance(request, Request), 'Invalid request %s' % request
        assert isinstance(response, Response), 'Invalid response %s' % response
        if response.isSuccess is False: return  # Skip in case the response is in error

        assert isinstance(request.node, Node), 'Invalid request node %s' % request.node
        assert isinstance(request.node.invokers, dict) and request.node.invokers, \
        'Invalid request node invokers %s' % request.node.invokers
        if response.allows is None: response.allows = set()
        response.allows.update(request.node.invokers)
