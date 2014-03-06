'''
Created on Nov 24, 2011

@package: ally core http
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the processors for handling Cross-Origin Resource Sharing.
'''

from itertools import chain

from ally.container import ioc
from ally.design.processor.handler import Handler
from ally.http.impl.processor.cors import CrossOriginResourceSharingHandler
from ally.http.impl.processor.method_deliver_ok import DeliverOkForMethodHandler
from ally.http.spec.headers import PARAMETERS_AS_HEADERS
from ally.http.spec.server import HTTP_OPTIONS

from ..ally_core.processor import methodAllow
from .processor import headersCorsAllow, updateAssemblyResources, assemblyResources, parametersAsHeaders, read_from_params


# --------------------------------------------------------------------
@ioc.config
def allow_origin() -> list:
    '''The allow origin to dispatch for responses'''
    return ['*']

@ioc.config
def allow_headers() -> list:
    '''The allow headers to dispatch for OPTIONS, to this headers the custom headers will be added'''
    return []

# --------------------------------------------------------------------
    
@ioc.entity
def crossOriginOthersOptions() -> dict:
    return {}
    
@ioc.entity
def crossOriginResourceSharing() -> Handler:
    b = CrossOriginResourceSharingHandler()
    b.allowOrigin = allow_origin()
    b.allowHeaders = sorted(set(chain(allow_headers(), headersCorsAllow())))
    b.othersOptions = crossOriginOthersOptions()
    return b

@ioc.entity
def deliverOkForOptionsHandler() -> Handler:
    b = DeliverOkForMethodHandler()
    b.forMethod = HTTP_OPTIONS
    return b

# --------------------------------------------------------------------

@ioc.before(crossOriginOthersOptions)
def updateCrossOriginOthersOptionsForParams():
    if read_from_params():
        crossOriginOthersOptions()[PARAMETERS_AS_HEADERS] = parametersAsHeaders()

@ioc.after(updateAssemblyResources)
def updateAssemblyResourcesForOptions():
    assemblyResources().add(crossOriginResourceSharing(), deliverOkForOptionsHandler(),
                            after=methodAllow())
