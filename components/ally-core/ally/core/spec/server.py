'''
Created on Jun 28, 2011

@package: ally core
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Module containing specifications for the server processing.
'''

from ally.core.spec.codes import Code
from ally.core.spec.resources import Path
from ally.design.processor import Classes
from ally.support.util_sys import validateTypeFor
from inspect import isclass
from types import GeneratorType
import abc
import logging

# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class IStream(metaclass=abc.ABCMeta):
    '''
    The specification for a linked stream.
    '''
    __slots__ = ()

    @abc.abstractclassmethod
    def read(self, nbytes=None):
        '''
        To read a file's contents, call f.read(size), which reads some quantity of data and returns it as a string.
        @param nbytes: integer
            Is an optional numeric argument. When size is omitted or negative, the entire contents of the file will be
            read and returned; it's your problem if the file is twice as large as your machine's memory.
            Otherwise, at most size bytes are read and returned. If the end of the file has been reached, f.read()
            will return an empty string ('').
        @return: bytes
            The content.
        '''

    @abc.abstractclassmethod
    def close(self):
        '''
        Closes the stream.
        '''

    @classmethod
    def __subclasshook__(cls, C):
        if cls is IStream:
            if (any('read' in B.__dict__ for B in C.__mro__) and
                any('close' in B.__dict__ for B in C.__mro__)):
                return True
        return NotImplemented

# --------------------------------------------------------------------

class Content:
    '''
    Container for content.
    
    @ivar type: string
        The content type.
    @ivar length: integer
        The length in bytes of the source.
    @ivar source: IStream|GeneratorType
        The source for the content.
    '''
    __slots__ = ('type', 'length', 'source')

    def __init__(self):
        '''
        Construct the content.
        '''
        self.type = None
        self.length = None
        self.source = None

if __debug__:
    # Used to validate the values for the container in debug mode.
    validateTypeFor(Content, 'contentType', str)
    validateTypeFor(Content, 'length', int)
    validateTypeFor(Content, 'source', (IStream, GeneratorType))

class Linked:
    '''
    The specification for a linked source.
    
    @ivar next: callable
        The callable used for getting the next content.
    '''
    __slots__ = ('next',)
    de continuat cu multipart.

    @abc.abstractclassmethod
    def next(self):
        '''
        Closes the current source and provide the next content.
        
        @return: Content|None
            The next content block or None if there is no more available.
        '''

class Request:
    '''
    Container for request data.
    
    @ivar method: integer
        The method of the request, can be one of GET, INSERT, UPDATE or DELETE constants.
    @ivar path: Path
        The path to the resource node.
    '''
    __slots__ = ('method', 'path')

    def __init__(self):
        '''
        Construct the request.
        '''
        self.method = None
        self.path = None

if __debug__:
    # Used to validate the values for the container in debug mode.
    validateTypeFor(Request, 'method', int)
    validateTypeFor(Request, 'path', Path)

class Response:
    '''
    Container for response data.
    
    @ivar code: Code
        The code of the response.
    @ivar text: string
        A small text message for the code.
    @ivar message: object
        A message for the code, can be any object that can be used by the framework for reporting an error.
    @ivar allows: integer
        Contains the allow flags for the methods.
    @ivar content: Content
        A content of the response.
    '''
    __slots__ = ('code', 'text', 'message', 'allows')

    def __init__(self):
        '''
        Constructs the response.
        '''
        self.code = None
        self.text = None
        self.message = None
        self.allows = 0

if __debug__:
    # Used to validate the values for the container in debug mode.
    validateTypeFor(Response, 'code', Code)
    validateTypeFor(Response, 'text', str)
    validateTypeFor(Response, 'allows', int, False)

class ClassesServer(Classes):
    '''
    The processing argument classes.
    '''

    def __init__(self, request=Request, response=Response, requestCnt=Content, responseCnt=Content):
        '''
        Construct the classes used for the server processing.
        
        @param request: class
            The class for the 'request' argument
        @param response: class
            The class for the 'response' argument
        @param requestCnt: class
            The class for the 'request content' argument
        @param responseCnt: class
            The class for the 'response requestCnt' argument
        '''
        assert isclass(request), 'Invalid request class %s' % request
        assert isclass(response), 'Invalid response class %s' % response
        assert isclass(requestCnt), 'Invalid content request class %s' % requestCnt
        assert isclass(responseCnt), 'Invalid content response class %s' % responseCnt

        self.request = request
        self.response = response
        self.requestCnt = requestCnt
        self.responseCnt = responseCnt
