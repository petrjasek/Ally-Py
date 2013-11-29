'''
Created on Oct 14, 2013

@package: support mongoengine
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the mongo engine connection proxy binding.
'''

from collections import deque
import logging
from mongoengine.connection import connect, disconnect
from threading import current_thread

from ally.container.impl.proxy import IProxyHandler, Execution, \
    registerProxyHandler, hasProxyHandler
from ally.container.ioc import injected
from ally.design.processor.attribute import requires
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Bind(Context):
    '''
    The bind context.
    '''
    # ---------------------------------------------------------------- Required
    proxy = requires(object)
    
# --------------------------------------------------------------------

@injected
class BindConnectionHandler(HandlerProcessor, IProxyHandler):
    '''
    Implementation for a processor that provides the mongo engine connection proxy binding.
    '''
    
    url = None
    # The mongo datbase URL.
    database = None
    # The database to use.
    
    def __init__(self):
        assert isinstance(self.url, str), 'Invalid database URL %s' % self.url
        assert isinstance(self.database, str), 'Invalid database %s' % self.database
        super().__init__()

    def process(self, chain, bind:Bind, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Binds a connection wrapping for the provided proxy.
        '''
        assert isinstance(bind, Bind), 'Invalid bind %s' % bind
        assert not hasProxyHandler(BindConnectionHandler, bind.proxy), 'Proxy already has a connection %s' % bind.proxy

        registerProxyHandler(self, bind.proxy)

    # ----------------------------------------------------------------

    def handle(self, execution):
        '''
        @see: IProxyHandler.handle
        '''
        assert isinstance(execution, Execution), 'Invalid execution %s' % execution

        try: connections = current_thread()._ally_mongo_connection
        except AttributeError: connections = current_thread()._ally_mongo_connection = deque()
        
        if connections and connections[0] == self: return execution.invoke()
        
        connections.appendleft(self)
        connect(self.database, host=self.url)
        
        try: return execution.invoke()
        finally: disconnect()
