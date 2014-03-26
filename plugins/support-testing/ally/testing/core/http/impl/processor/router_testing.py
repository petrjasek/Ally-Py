'''
Created on Mar 25, 2014

@package: support testing
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides a processor that triggers the testing environment.
'''

import logging

from ally.container.ioc import injected
from ally.core.spec.codes import UPDATE_SUCCESS
from ally.design.processor.attribute import requires
from ally.design.processor.execution import Chain, Processing
from ally.http.spec.codes import CodedHTTP
from ally.http.spec.server import HTTP_PUT
from ally.http.impl.processor import router_by_path
from ally.testing.container.switcher import Switcher


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Request(router_by_path.Request):
    '''
    Context for request. 
    '''
    # ---------------------------------------------------------------- Required
    method = requires(str)

# --------------------------------------------------------------------

@injected
class RouterTestingHandler(router_by_path.RoutingByPathHandler):
    '''
    Implementation for a handler that triggers the testing environment.
    '''
    
    create = None
    # The create call to be used.
    switcher = Switcher
    # The database switcher.
    
    def __init__(self):
        assert isinstance(self.rootURI, str), 'Invalid root URI %s' % self.rootURI
        assert callable(self.create), 'Invalid create call %s' % self.create
        assert isinstance(self.switcher, Switcher), 'Invalid switcher %s' % self.switcher
        super().__init__()
        
    def process(self, chain, processing, request:Request, response:CodedHTTP, **keyargs):
        '''
        @see: HandlerBranching.process
        
        Process the testing.
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(processing, Processing), 'Invalid processing %s' % processing
        assert isinstance(request, Request), 'Invalid request %s' % request
        assert isinstance(response, CodedHTTP), 'Invalid response %s' % response

        if request.method == HTTP_PUT and request.uri.strip('/') == self.rootURI:
            self.create()
            UPDATE_SUCCESS.set(response)
            response.status = 200
            assert log.debug('Successful re/created testing environment') or True
            chain.cancel()
            
        else:
            match = self._regex.match(request.uri)
            if match:
                request.uri = ''.join(match.groups())
                if Request.rootURI in request: request.rootURI = self.rootURI
                self.switcher.switchToAlternate()
                chain.route(processing)
                chain.onFinalize(self.switchBack)
                
    def switchBack(self, final, **keyargs):
        self.switcher.switchToMain()
            