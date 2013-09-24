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
from ally.design.processor.attribute import attribute, requires, defines
from ally.design.processor.execution import Chain
import os
import io
from ally.design.processor.handler import HandlerProcessor
from ally.design.processor.context import Context
from ally.support.util_spec import IDo
import logging

# --------------------------------------------------------------------
log = logging.getLogger(__name__)
PATH_SEP = os.path.sep
# --------------------------------------------------------------------

class FItem(Context):
    '''
    The file system item context.
    '''
    # ---------------------------------------------------------------- Defined
    parent = attribute(Context, doc='''
    @rtype: Context
    The parent item.
    ''')
    name = attribute(str, doc='''
    @rtype: string
    The item name.
    ''')
    children = attribute(dict, doc='''
    @rtype: dictionary{string: Context}
    The children items.
    ''')
    path = attribute(list, doc='''
    @rtype: list[string]
    The path of the item.
    ''')
    URIType = attribute(str, doc='''
    @rtype: string
    The item URI type (e.g. file://, http://, fttp:// ...).
    ''')
#     doGetStream = attribute(IDo, doc='''
#     @rtype: callable() -> IInputStream
#     Provides the input stream for item.
#     ''')
    lastModified = attribute(int, doc='''
    @rtype: integer
    The time of the modification.
    ''')
    hash = attribute(str, doc='''
    @rtype: datetime
    The item status hash.
    ''')
    listeners = attribute(list, doc='''
    @rtype: list[Context]
    The list of listeners for this item.
    ''')

class FListener(Context):
    # ---------------------------------------------------------------- Defined
    path = attribute(list, doc='''
    @rtype: list[string]
    The path of the listener.
    ''')
    doMatch = defines(IDo, doc='''
    @rtype: callable(listenerPath, itemPath) -> boolean
    Matches the item path against the paths accepted by the listener.
    @param listenerPath: list[string]
        Pattern for paths accepted by the listener.
    @param itemPath: list[string]
        Path of the item.
    ''')
    doOnContentCreated = defines(IDo, doc='''
    @rtype: callable(URI, content)
    Is called when an item for this listener is created.
    @param URI: string
        Pattern for paths accepted by the listener.
    @param content: stream
        Stream with the content of the resource.
    ''')
    doOnContentChanged = defines(IDo, doc='''
    @rtype: callable(URI, content)
    Is called when an item for this listener is changed.
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
    
class Solicit(Context):
    '''
    The solicit context.
    '''
    # ---------------------------------------------------------------- Requires
    registerPaths = requires(list, doc='''
    @rtype: list[str]
    The list of paths to scan.
    ''')
    
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
    
    def process(self, chain, solicit:Solicit, Item:FItem, Listener:FListener, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Builds the listeners.
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(solicit, Solicit), 'Invalid solicit %s' % solicit
        assert solicit.registerPaths, 'Invalid register paths %s' % solicit.registerPaths
        
        self._chain = chain
        
        listeners = []
        for path in solicit.registerPaths:
            pathList = [e for e in path.split(PATH_SEP) if e]
            # create the listener
            listener = chain.arg.Listener()
            assert isinstance(listener, FListener), 'Invalid listener %s' % listener
            listener.path = pathList
            listener.doMatch = match
            listener.doOnContentCreated = doOnContentCreated
            listener.doOnContentChanged = doOnContentChanged
            listener.doOnContentRemoved = doOnContentRemoved
            listeners.append(listener)
        
        solicit.listeners = listeners


#------------------------------------------------------------------Methods for listeners     
def match(listenerPath, itemPath):
    assert isinstance(itemPath, list) and itemPath, 'Invalid item path %s' % itemPath
    assert isinstance(listenerPath, list) and listenerPath, 'Invalid path %s' % listenerPath
    
    if len(itemPath) > len(listenerPath): return False
    for item1, item2 in zip(itemPath, listenerPath):
        if item1 != item2 and item2 != '*': return False
    return True

def doOnContentCreated(URI, content):
    '''
    Parse the file or whatever.
    '''
    assert log.debug('Parse file: %s' % URI) or True
    #print(content.read())
    
def doOnContentChanged(URI, content):
    '''
    Parse the file (again) or whatever.
    '''
    assert log.debug('Parse file: %s' % URI) or True

def doOnContentRemoved(URI):
    '''
    Do nothing for now.
    '''
    assert log.debug('Deleted item: %s' % URI) or True
    
