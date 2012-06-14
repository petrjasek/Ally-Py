'''
Created on Jun 5, 2012

@package: ally core http
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides support for setting fixed headers on responses.
'''

from ally.container.ioc import injected
from ally.core.http.spec.server import IEncoderHeader
from ally.design.processor import Handler, processor, Chain
import logging
from ally.design.context import Context, requires

# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Response(Context):
    '''
    The response context.
    '''
    # ---------------------------------------------------------------- Required
    encoderHeader = requires(IEncoderHeader)

# --------------------------------------------------------------------

@injected
class HeaderSetHandler(Handler):
    '''
    Provides the setting of static header values.
    '''

    headers = dict
    # The static header values to set on the response.

    def __init__(self):
        assert isinstance(self.headers, dict), 'Invalid header dictionary %s' % self.header
        if __debug__:
            for name, value in self.headers.items():
                assert isinstance(name, str), 'Invalid header name %s' % name
                assert isinstance(value, str), 'Invalid header value %s' % value

    @processor
    def encode(self, chain, response:Response, **keyargs):
        '''
        Set the fixed header values on the response.
        '''
        assert isinstance(chain, Chain), 'Invalid processors chain %s' % chain
        assert isinstance(response, Response), 'Invalid response %s' % response
        assert isinstance(response.encoderHeader, IEncoderHeader), \
        'Invalid header encoder %s' % response.encoderHeader

        for name, value in self.headers.items(): response.encoderHeader.encode(name, value)

        chain.proceed()
