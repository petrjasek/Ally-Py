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
from ally.core.spec.server import IInputStream
from ally.design.context import Context, requires, defines
from ally.design.processor import HandlerProcessorProceed

# --------------------------------------------------------------------

class RequestDecode(Context):
    '''
    The request context.
    '''
    # ---------------------------------------------------------------- Required
    decoderHeader = requires(IDecoderHeader)
    source = requires(IInputStream)
    # ---------------------------------------------------------------- Defined
    length = defines(int, doc='''
    @rtype: integer
    The content source length in bytes. 
    ''')

class ResponseDecode(Context):
    '''
    The response context.
    '''
    # ---------------------------------------------------------------- Defined
    code = defines(Code)
    text = defines(str)
    errorMessage = defines(str)

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

    def process(self, request:RequestDecode, response:ResponseDecode, **keyargs):
        '''
        @see: HandlerProcessorProceed.process
        
        Decodes the request content length also wraps the content source if is the case.
        '''
        assert isinstance(request, RequestDecode), 'Invalid request %s' % request
        assert isinstance(response, ResponseDecode), 'Invalid response %s' % response
        assert isinstance(request.decoderHeader, IDecoderHeader), \
        'Invalid header decoder %s' % request.decoderHeader

        value = request.decoderHeader.retrieve(self.nameContentLength)
        if value:
            try: request.length = int(value)
            except ValueError:
                if ResponseDecode.code in response and not response.code.isSuccess: return
                response.code, response.text = INVALID_HEADER_VALUE, 'Invalid %s' % self.nameContentLength
                response.errorMessage = 'Invalid value \'%s\' for header \'%s\''\
                ', expected an integer value' % (value, self.nameContentLength)
                return
            else: request.source = StreamLengthLimited(request.source, request.length)

#TODO: maybe place this in an input content handler that uses length for handling the input.
class StreamLengthLimited(IInputStream):
    '''
    Provides a class that implements the @see: IInputStream that limits the reading from another stream based on the
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
        assert isinstance(stream, IInputStream), 'Invalid stream %s' % stream
        assert isinstance(length, int), 'Invalid length %s' % length

        self._stream = stream
        self._length = length
        self._closed = False
        self._offset = 0

    def read(self, nbytes=None):
        '''
        @see: IInputStream.read
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
        @see: IInputStream.close
        '''
        self._closed = True

# --------------------------------------------------------------------

class ResponseEncode(Context):
    '''
    The response context.
    '''
    # ---------------------------------------------------------------- Required
    encoderHeader = requires(IEncoderHeader)
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

    def process(self, response:ResponseEncode, **keyargs):
        '''
        @see: HandlerProcessorProceed.process
        
        Encodes the content length.
        '''
        assert isinstance(response, ResponseEncode), 'Invalid response %s' % response
        assert isinstance(response.encoderHeader, IEncoderHeader), \
        'Invalid response header encoder %s' % response.encoderHeader

        if ResponseEncode.length in response:
            response.encoderHeader.encode(self.nameContentLength, str(response.length))
