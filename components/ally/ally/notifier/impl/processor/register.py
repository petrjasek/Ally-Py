'''
Created on Sep 12, 2013

@author: mihaigociu

@package: ally base
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Gociu

Registering the listeners for the file notifier.
'''

from ally.container.ioc import injected
from ally.design.processor.attribute import defines
from ally.design.processor.handler import HandlerProcessor
from ally.design.processor.context import Context
from ally.support.util_spec import IDo
import logging
from urllib.parse import urlsplit

# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class ListenerRegister(Context):
    '''
    The file system item context.
    '''
    # ---------------------------------------------------------------- Defined
    uri = defines(str, doc='''
    @rtype: string
    Pattern for the paths that this listener is interested in.
    ''') 
    doMatch = defines(IDo, doc='''
    @rtype: callable(item) -> boolean
    Matches the item path against the paths accepted by the listener.
    @param item: Context
        The item to match.
    ''')
    doOnContentCreated = defines(IDo, doc='''
    @rtype: callable(URI, content)
    Is called when an item for this listener is created. Should handle stream closing.
    @param URI: string
        Pattern for paths accepted by the listener.
    @param content: stream
        Stream with the content of the resource.
    ''')
    doOnContentChanged = defines(IDo, doc='''
    @rtype: callable(URI, content)
    Is called when an item for this listener is changed. Should handle stream closing.
    @param URI: string
        Pattern for paths accepted by the listener.
    @param content: stream
        Stream with the content of the resource.
    ''')
    doOnContentRemoved = defines(IDo, doc='''
    @rtype: callable(URI)
    Is called when an item for this listener is deleted.
    @param URI: string
        Pattern for paths accepted by the listener.
    @param content: stream
        Stream with the content of the resource.
    ''')
    
class Register(Context):
    '''
    The register context.
    '''
    # ---------------------------------------------------------------- Defines
    listeners = defines(list, doc='''
    @rtype: list[Context]
    The listeners for the items tree.
    ''')
    
# --------------------------------------------------------------------

@injected
class RegisterListeners(HandlerProcessor):
    '''
    Implementation that provides the file system polling and notifying.
    '''
    
    patterns = list
    # The URI patterns that this register is providing listeners for.
    
    def __init__(self):
        assert isinstance(self.patterns, list), 'Invalid patterns %s' % self.patterns
        super().__init__()
    
    def process(self, chain, register:Register, Listener:ListenerRegister, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Register the listeners.
        '''
        assert isinstance(register, Register), 'Invalid register %s' % register
        
        if register.listeners is None: register.listeners = []
        for pattern in self.patterns:
            assert isinstance(pattern, str), 'Invalid pattern %s' % pattern
            # create the listener
            
            listener = Listener()
            assert isinstance(listener, ListenerRegister), 'Invalid listener %s' % listener
            
            listener.uri = pattern
            listener.doMatch = self.createMatch(urlsplit(pattern))
            listener.doOnContentCreated = self.doOnContentCreated
            listener.doOnContentChanged = self.doOnContentChanged
            listener.doOnContentRemoved = self.doOnContentRemoved
            register.listeners.append(listener)

    def createMatch(self, uriListener):
        '''
        Create the match for the provided items.
        '''
        pathListener = uriListener.path.split('/')
        def doMatch(uri):
            '''
            Process the match of the pattern URI with the provided URI.
            '''
            uriItem = urlsplit(uri)
            if uriListener.scheme != uriItem.scheme: return False
            pathItem = uriItem.path.split('/')
            if not pathItem or not pathListener: return False
            
            if len(pathItem) > len(pathListener): return False
            for item1, item2 in zip(pathItem, pathListener):
                if item1 != item2 and item2 != '*': return False
            return True
        
        return doMatch

#------------------------------------------------------------------Methods for listeners   

    def doOnContentCreated(self, uri, content):
        '''
        Parse the file or whatever.
        '''
        self.doOnContentChanged(uri, content)
        
    def doOnContentChanged(self, uri, content):
        '''
        Parse the file (again) or whatever.
        '''
        assert log.debug('Content changed for URI: %s' % uri) or True
    
    def doOnContentRemoved(self, uri):
        '''
        Do nothing for now.
        '''
        assert log.debug('Content deleted for URI: %s' % uri) or True
        self.doOnContentChanged(uri, None)
    
