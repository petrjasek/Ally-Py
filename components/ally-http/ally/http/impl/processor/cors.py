'''
Created on Apr 29, 2013

@package: ally http
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the cross origin resource sharing delivering.
'''

from ally.container.ioc import injected
from ally.design.processor.attribute import requires, optional
from ally.design.processor.handler import HandlerProcessor
from ally.http.spec.headers import ALLOW_ORIGIN, ALLOW_METHODS, HeaderCmx, \
    HeadersDefines, ALLOW_REQUEST_HEADERS, HeadersRequire, ALLOW_HEADERS
from ally.http.spec.server import HTTP_OPTIONS


# --------------------------------------------------------------------
class Request(HeadersRequire):
    '''
    The request context.
    '''
    # ---------------------------------------------------------------- Required
    method = requires(str)

class Response(HeadersDefines):
    '''
    The response context.
    '''
    # ---------------------------------------------------------------- Optional
    isSuccess = requires(bool)
    allows = optional(set)

# --------------------------------------------------------------------

@injected
class CrossOriginResourceSharingHandler(HandlerProcessor):
    '''
    Handler for delivering cross origin resource sharing, based on http://www.w3.org/TR/cors/.
    '''
    
    allowOrigin = None
    # The value to set for allow origin.
    allowMethods = None
    # The method names that are allowed.
    allowHeaders = None
    # The headers that are allowed.
    othersOptions = None
    # Other cross origin resource sharing headers for options, this is a dictionary having as a key the HeaderCmx
    # and as a value the values to push for that header.

    def __init__(self):
        assert self.allowOrigin is None or isinstance(self.allowOrigin, list), \
        'Invalid allow origin %s' % self.allowOrigin
        assert self.allowMethods is None or isinstance(self.allowMethods, list), \
        'Invalid allow methods %s' % self.allowMethods
        self._allowed = set()
        if self.allowHeaders:
            assert isinstance(self.allowHeaders, list), \
            'Invalid allow headers %s' % self.allowHeaders
            self._allowed.update(name.lower() for name in self.allowHeaders)
        assert self.othersOptions is None or isinstance(self.othersOptions, dict), \
        'Invalid other options %s' % self.othersOptions
                
        super().__init__()

    def process(self, chain, request:Request, response:Response, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Process the cross origin data.
        '''
        assert isinstance(request, Request), 'Invalid request %s' % request
        assert isinstance(response, Response), 'Invalid response %s' % response
        if response.isSuccess is False: return  # Skip in case the response is in error

        if self.allowOrigin: ALLOW_ORIGIN.encode(response, *self.allowOrigin)

        if request.method == HTTP_OPTIONS:
            current = ALLOW_METHODS.decode(response)
            if current: allows = set(current)
            else: allows = set()
            
            allows.add(HTTP_OPTIONS)
            if Response.allows in response and response.allows: allows.update(response.allows)
            if self.allowMethods: allows.update(self.allowMethods)
            if allows: ALLOW_METHODS.encode(response, *sorted(allows))
            
            if self._allowed:
                allowed = []
                current = ALLOW_REQUEST_HEADERS.decode(request)
                if current:
                    for name in current:
                        if name.lower() in self._allowed: allowed.append(name)
                if allowed: ALLOW_HEADERS.extend(response, *allowed)
            
            if self.othersOptions:
                for header, values in self.othersOptions.items():
                    assert isinstance(header, HeaderCmx), 'Invalid header %s' % header
                    header.extend(response, *values)
