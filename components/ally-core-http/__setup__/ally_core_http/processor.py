'''
Created on Nov 24, 2011

@package: ally core http
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the configurations for the processors used in handling the request.
'''

from . import server_pattern_rest
from ..ally_core.converter import contentNormalizer, converterPath
from ..ally_core.processor import decoding, handlersResources, methodInvoker, \
    converter, handlersExplainError, requestTypes, invokingHandler
from ..ally_core.resources import resourcesLocator
from .meta_service import parameterMetaService
from ally.container import ioc
from ally.core.http.impl.processor.formatting import FormattingProviderHandler
from ally.core.http.impl.processor.header import HeaderStandardHandler
from ally.core.http.impl.processor.meta_filter import MetaFilterHandler
from ally.core.http.impl.processor.method_override import MethodOverrideHandler
from ally.core.http.impl.processor.parameter import ParameterHandler
from ally.core.http.impl.processor.uri import URIHandler
from ally.core.spec.server import IProcessor, Processors
import re
from ..ally_core.processor import handlersRedirect

# --------------------------------------------------------------------
# Creating the processors used in handling the request

@ioc.config
def read_from_params():
    '''If true will also read header values that are provided as query parameters'''
    return True

@ioc.config
def allow_method_override():
    '''
    If true will allow the method override by using the header 'X-HTTP-Method-Override', the GET can be override with
    DELETE and the POST with PUT.
    '''
    return True

# --------------------------------------------------------------------

@ioc.entity
def methodOverride() -> IProcessor:
    b = MethodOverrideHandler()
    b.readFromParams = read_from_params()
    return b

@ioc.entity
def uri() -> IProcessor:
    b = URIHandler()
    b.resourcesLocator = resourcesLocator()
    b.converterPath = converterPath()
    return b

@ioc.entity
def parameter() -> IProcessor:
    b = ParameterHandler()
    b.converterPath = converterPath()
    b.parameterMetaService = parameterMetaService()
    return b

@ioc.entity
def headerStandard() -> IProcessor:
    b = HeaderStandardHandler()
    b.readFromParams = read_from_params()
    return b

@ioc.entity
def metaFilter() -> IProcessor:
    b = MetaFilterHandler()
    b.normalizer = contentNormalizer()
    b.fetching = Processors(*handlersFetching())
    b.readFromParams = read_from_params()
    return b

@ioc.entity
def formattingProvider() -> IProcessor:
    b = FormattingProviderHandler()
    b.readFromParams = read_from_params()
    return b

@ioc.entity
def pathHandlers():
    return [(server_pattern_rest(), handlersResources())]

# --------------------------------------------------------------------

@ioc.entity
def handlersFetching():
    '''
    The specific handlers to be used for an actual invoking procedure, used by the meta filter to actually fetch 
    entities whenever the X-Filter is used and there is no compound method available.
    '''
    return [methodInvoker(), requestTypes(), invokingHandler()]

# --------------------------------------------------------------------

@ioc.before(handlersExplainError)
def updateHandlersExplainError():
    handlersExplainError().insert(0, headerStandard())

@ioc.before(handlersRedirect)
def updateHandlersRedirect():
    handlersRedirect().insert(handlersRedirect().index(decoding()), parameter())

@ioc.before(handlersResources)
def updateHandlersResources():
    handlers = [headers(), uri(), formattingProvider()]
    if allow_method_override(): handlers.insert(0, methodOverride()) # Add also the method override if so configured
    for proc in handlers: handlersResources().insert(handlersResources().index(methodInvoker()), proc)

    handlersResources().insert(handlersResources().index(converter()), metaFilter())
    handlersResources().insert(handlersResources().index(decoding()), parameter())
