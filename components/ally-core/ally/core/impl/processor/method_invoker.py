'''
Created on Jul 14, 2011

@package: Newscoop
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the requested method validation handler.
'''

from ally.api.config import GET, INSERT, UPDATE, DELETE
from ally.container.ioc import injected
from ally.core.spec.codes import METHOD_NOT_AVAILABLE
from ally.core.spec.resources import Path, Node
from ally.core.spec.server import Request, Response
from ally.design.processor import Handler, processor, Chain, ext
from ally.core.spec.extension import Invoke

# --------------------------------------------------------------------

class MethodInvokerHandler(Handler):
    '''
    Implementation for a processor that validates if the request method (GET, INSERT, UPDATE, DELETE) is compatible
    with the resource node of the request, basically checks if the node has the invoke for the requested method.
    If the node has no invoke than this processor will stop the execution chain and provide an error response also
    providing the allows methods for the resource path node.
    '''

    @processor
    def process(self, chain, request:(Request, ext(Invoke)), response:Response, **keyargs):
        '''
        @see: IProcessor.process
        '''
        assert isinstance(chain, Chain), 'Invalid processors chain %s' % chain
        assert isinstance(request, Request), 'Invalid request %s' % request
        assert isinstance(request, Invoke), 'Invalid request %s' % request
        assert isinstance(response, Response), 'Invalid response %s' % response
        assert isinstance(request.path, Path), 'Invalid request path %s' % request.path
        node = request.path.node
        assert isinstance(node, Node), 'Invalid request path node %s' % node

        if request.method == GET: # Retrieving
            request.invoker = node.get
            if request.invoker is None:
                self._sendNotAvailable(node, rsp, 'Path not available for get')
                return
        elif req.method == INSERT: # Inserting
            req.invoker = node.insert
            if req.invoker is None:
                self._sendNotAvailable(node, rsp, 'Path not available for post')
                return
        elif req.method == UPDATE: # Updating
            req.invoker = node.update
            if req.invoker is None:
                self._sendNotAvailable(node, rsp, 'Path not available for put')
                return
        elif req.method == DELETE: # Deleting
            req.invoker = node.delete
            if req.invoker is None:
                self._sendNotAvailable(node, rsp, 'Path not available for delete')
                return
        else:
            self._sendNotAvailable(node, rsp, 'Path not available for this method')
            return
        ConstructMetaModel(req.invoker.output, self=rsp)
        chain.proceed()

    def _processAllow(self, node, rsp):
        '''
        Set the allows for the response based on the provided node.
        '''
        assert isinstance(node, Node)
        assert isinstance(rsp, Response)
        if node.get is not None:
            rsp.addAllows(GET)
        if node.insert is not None:
            rsp.addAllows(INSERT)
        if node.update is not None:
            rsp.addAllows(UPDATE)
        if node.delete is not None:
            rsp.addAllows(DELETE)

    def _sendNotAvailable(self, node, rsp, message):
        self._processAllow(node, rsp)
        rsp.setCode(METHOD_NOT_AVAILABLE, message)
