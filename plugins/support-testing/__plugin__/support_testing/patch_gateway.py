'''
Created on Mar 25, 2014

@package: support testing
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the gateway patch.
'''

import logging

from __setup__.ally_core_http.server import server_provide_errors, \
    root_uri_errors
from ally.container import ioc
from ally.http.spec.codes import PATH_NOT_FOUND, UNAUTHORIZED_ACCESS, \
    INVALID_AUTHORIZATION, FORBIDDEN_ACCESS, METHOD_NOT_AVAILABLE
from ally.http.spec.server import HTTP_OPTIONS, HTTP_PUT

from .processor import SWITCHER_TESTING
import re


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

try: from .. import gateway  # @UnusedImport
except ImportError: log.info('No Gateway plugin available to patch.')
else:
    from ..gateway.service import defaultGateways
    from ..gateway.service import asPattern
    from ..support_testing.patch_server import root_uri_test_resources
    from ..gateway_acl.service import rootURI, root_uri_acl
    from ally.testing.core.http.impl.processor.root_testing_uri import RootTestingURIHandler

    @SWITCHER_TESTING.switch(defaultGateways)
    @ioc.entity
    def defaultTestGateways() -> list: return []
    
    @ioc.replace(rootURI)
    def rootTestURI():
        b = RootTestingURIHandler()
        b.switcher = SWITCHER_TESTING
        b.rootURIMain = root_uri_acl()
        b.rootURIAlternate = root_uri_test_resources()
        return b

    @ioc.before(defaultTestGateways)
    def updateGatewayWithTestResourcesOptions():
        defaultTestGateways().extend([
        {
         'Name': 'allow_test_resources_OPTIONS',
         'Pattern': asPattern(root_uri_test_resources()),
         'Methods': [HTTP_OPTIONS],
         },
        {
         'Name': 'allow_test_reset',
         'Pattern': '^%s(?:[/]?)$' % re.escape(root_uri_test_resources()),
         'Methods': [HTTP_PUT],
         },
                                   ])
    
    @ioc.before(defaultTestGateways)
    def updateGatewayWithTestResourcesErrors():
        if server_provide_errors():
            defaultTestGateways().extend([
            # If path is not found then we try to dispatch a unauthorized access if the path is not
            # found in REST the default error will have priority over the unauthorized access
            {
             'Name': 'error_test_unauthorized_vs_not_found',
             'Pattern': asPattern(root_uri_test_resources()),
             'Errors': [PATH_NOT_FOUND.status],
             'Navigate': '%s/{1}?status=%s' % (root_uri_errors(), UNAUTHORIZED_ACCESS.status),
             },
            {
             'Name': 'error_test_unauthorized',
             'Pattern': asPattern(root_uri_test_resources()),
             'Errors': [INVALID_AUTHORIZATION.status, FORBIDDEN_ACCESS.status, METHOD_NOT_AVAILABLE.status],
             'Navigate': '%s/{1}' % root_uri_errors(),
             },
                                       ])
