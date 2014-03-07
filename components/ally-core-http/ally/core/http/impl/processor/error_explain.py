'''
Created on Jun 28, 2011

@package: ally core http
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Balaceanu

Provides support for explaining the errors in the content of the request.
'''

from collections import Callable
import logging

from ally.api.type import typeFor
from ally.container.ioc import injected
from ally.core.spec.resources import Converter
from ally.core.spec.transform import IRender
from ally.design.processor.attribute import requires
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Request(Context):
    '''
    The request context.
    '''
    # ---------------------------------------------------------------- Required
    converterContent = requires(Converter)

class Response(Context):
    '''
    The response context.
    '''
    # ---------------------------------------------------------------- Required
    isSuccess = requires(bool)
    errors = requires(list)
    renderFactory = requires(Callable)

# --------------------------------------------------------------------

@injected
class ErrorExplainHandler(HandlerProcessor):
    '''
    Implementation for a processor that provides on the response a form of the error that can be extracted from 
    the response code and error message, this processor uses the code status (success) in order to trigger the error
    response.
    '''
    def __init__(self):
        super().__init__()
    
    def process(self, chain, request:Request, response:Response, responseCnt:Context, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Process the error into a response content.
        '''
        assert isinstance(request, Request), 'Invalid request %s' % request
        assert isinstance(response, Response), 'Invalid response %s' % response
        
        if response.isSuccess is not False or not response.errors: return  # Not in error.
        
        errors = {}
        
        for code, decoding, message, data in response.errors:
            if decoding.name not in errors: errors[decoding.name] = {}
            errors[decoding.name][code] = dict(msg=message)
            assert isinstance(data, dict), 'Invalid data %' % data
            errors[decoding.name][code].update(self.convertData(data, request.converterContent))
        
        renderer = response.renderFactory(responseCnt)
        assert isinstance(renderer, IRender), 'Invalid render %s' % renderer
        
        renderer.beginObject('errors')
        for prop, codes in errors.items():
            assert isinstance(codes, dict), 'Invalid codes %s' % codes
            renderer.beginObject(prop)
            for code, msgs in codes.items():
                assert isinstance(msgs, dict), 'Invalid messages %s' % msgs
                renderer.beginObject(code)
                for msgKey, msg in msgs.items():
                    renderer.property(msgKey, msg)
                renderer.end()
            renderer.end()
        renderer.end()
    
    # ----------------------------------------------------------------
    
    def convertData(self, data, converter):
        assert isinstance(data, dict), 'Invalid data %s' % data
        assert isinstance(converter, Converter), 'Invalid converter %s' % converter
        cData = dict()
        for k, v in data.items():
            cData[k] = converter.asString(v, typeFor(type(v)))
        return cData
