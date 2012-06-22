'''
Created on Jun 11, 2012

@package: ally core http
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the decoding/encoding for the content length header.
'''

from ally.container.ioc import injected
from ally.core.http.spec.codes import INVALID_HEADER_VALUE
from ally.core.http.spec.server import IEncoderHeader, IDecoderHeader
from ally.core.spec.codes import Code
from ally.core.spec.server import IStream
from ally.design.context import Context, requires, defines
from ally.design.processor import HandlerProcessorProceed

# --------------------------------------------------------------------

class Request(Context):
    '''
    The request context.
    '''
    # ---------------------------------------------------------------- Required
    decoderHeader = requires(IDecoderHeader)

class RequestContent(Context):
    '''
    The response content context.
    '''
    # ---------------------------------------------------------------- Defined
    length = defines(int, doc='''
    @rtype: integer
    The content source length in bytes. 
    ''')
    # ---------------------------------------------------------------- Required
    source = requires(IStream)

class ResponseDecode(Context):
    '''
    The response context.
    '''
    # ---------------------------------------------------------------- Defined
    code = defines(Code)
    text = defines(str)
    message = defines(str)

# --------------------------------------------------------------------

@injected
class ContentLengthDecodeHandler(HandlerProcessorProceed):
    '''
    Implementation for a processor that provides the decoding of content length HTTP response header.
    '''

    nameContentLength = 'Content-Length'
    # The name for the content length header

    def __init__(self):
        assert isinstance(self.nameContentLength, str), 'Invalid content length name %s' % self.nameContentLength
        super().__init__()

    def process(self, request:Request, requestCnt:RequestContent, response:ResponseDecode, **keyargs):
        '''
        @see: HandlerProcessorProceed.process
        
        Decodes the request content length also wraps the content source if is the case.
        '''
        assert isinstance(request, Request), 'Invalid request %s' % request
        assert isinstance(requestCnt, RequestContent), 'Invalid request content %s' % requestCnt
        assert isinstance(response, ResponseDecode), 'Invalid response %s' % response
        assert isinstance(request.decoderHeader, IDecoderHeader), \
        'Invalid header decoder %s' % request.decoderHeader

        value = request.decoderHeader.retrieve(self.nameContentLength)
        if value:
            try: requestCnt.length = int(value)
            except ValueError:
                if ResponseDecode.code in response and not response.code.isSuccess: return
                response.code, response.text = INVALID_HEADER_VALUE, 'Invalid %s' % self.nameContentLength
                response.message = 'Invalid value \'%s\' for header \'%s\''\
                ', expected an integer value' % (value, self.nameContentLength)
                return
            else: requestCnt.source = StreamLengthLimited(requestCnt.source, requestCnt.length)

class StreamLengthLimited(IStream):
    '''
    Provides a class that implements the @see: IStream that limits the reading from another stream based on the
    provided length.
    '''

    def __init__(self, stream, length):
        '''
        Constructs the length limited stream.
        
        @param stream: IStream
            The stream to wrap and provide limited reading from.
        @param length: integer
            The number of bytes to allow the read from the wrapped stream.
        '''
        assert isinstance(stream, IStream), 'Invalid stream %s' % stream
        assert isinstance(length, int), 'Invalid length %s' % length

        self._stream = stream
        self._length = length
        self._closed = False
        self._offset = 0

    def read(self, nbytes=None):
        '''
        @see: IStream.read
        '''
        if self._closed: raise ValueError('I/O operation on a closed content file')
        count = nbytes
        if self._length is not None:
            if self._offset >= self._length:
                return b''
            delta = self._length - self._offset
            if count is None:
                count = delta
            elif count > delta:
                count = delta
        bytes = self._stream.read(count)
        self._offset += len(bytes)
        return bytes

    def close(self):
        '''
        @see: IStream.close
        '''
        self._closed = True

# --------------------------------------------------------------------

class ResponseEncode(Context):
    '''
    The response context.
    '''
    # ---------------------------------------------------------------- Required
    encoderHeader = requires(IEncoderHeader)

class ResponseContent(Context):
    '''
    The response content context.
    '''
    # ---------------------------------------------------------------- Required
    length = requires(int)

# --------------------------------------------------------------------

@injected
class ContentLengthEncodeHandler(HandlerProcessorProceed):
    '''
    Implementation for a processor that provides the encoding of content length HTTP response header.
    '''

    nameContentLength = 'Content-Length'
    # The name for the content length header

    def __init__(self):
        assert isinstance(self.nameContentLength, str), 'Invalid content length name %s' % self.nameContentLength
        super().__init__()

    def process(self, response:ResponseEncode, responseCnt:ResponseContent, **keyargs):
        '''
        @see: HandlerProcessorProceed.process
        
        Encodes the content length.
        '''
        assert isinstance(response, ResponseEncode), 'Invalid response %s' % response
        assert isinstance(responseCnt, ResponseContent), 'Invalid response content %s' % responseCnt
        assert isinstance(response.encoderHeader, IEncoderHeader), \
        'Invalid response header encoder %s' % response.encoderHeader

        if ResponseContent.length in responseCnt:
            response.encoderHeader.encode(self.nameContentLength, str(responseCnt.length))
