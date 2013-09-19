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
from collections import deque
import os
import datetime
from ally.design.processor.handler import HandlerProcessor
from ally.design.processor.context import Context

# --------------------------------------------------------------------

PATH_SEPARATOR = os.path.sep

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
    @rtype: list[str]
    The path of the item.
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
    path = attribute(list, doc='''
    @rtype: list[str]
    The path of the listener.
    ''')

class Solicit(Context):
    '''
    The solicit context.
    '''
    # ---------------------------------------------------------------- Required
    registerPaths = requires(list, doc='''
    @rtype: list[str]
    The list of paths to scan.
    ''')
    
    # ---------------------------------------------------------------- Defines
    itemTree = defines(Context, doc='''
    @rtype: Context
    The root of the item tree structure
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
        
        Builds the items tree and registers listeners for items.
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(solicit, Solicit), 'Invalid solicit %s' % solicit
        assert solicit.registerPaths, 'Invalid register paths %s' % solicit.registerPaths
        
        self._chain = chain
        if not solicit.itemTree: solicit.itemTree = createItem('ROOT', chain)
        if not solicit.itemTree.children: solicit.itemTree.children = dict()
        
        listeners = []
        for path in solicit.registerPaths:
            pathList = [e for e in path.split(PATH_SEPARATOR) if e]
            #create the listener
            listener = chain.arg.Listener()
            assert isinstance(listener, FListener), 'Invalid listener %s' % listener
            listener.path = pathList
            listeners.append(listener)
            
        item = self.createItems(listeners)
        assert isinstance(item, FItem), 'Invalid item %s' % item
        solicit.itemTree.children[item.name] = item
        
    def createItems(self, listeners):
        '''
        Creates a tree structure of items that matches the given path.
        
        '''
        chain = self._chain
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        
        root = createItem('ROOT', chain)
        
        for listener in listeners:
            assert isinstance(listener, FListener), 'Invalid listener %s' % listener
            assert listener.path, 'Invalid listener path %s' % listener.path
            assert os.path.isdir(buildPath(listener.path[:1], PATH_SEPARATOR)), 'Invalid root directory %s' % listener.path[:1]
            
            startName = listener.path[0]
            queue = deque()
            queue.append((startName, root)) #name, parent
            while queue:
                name, parent = queue.popleft()
                assert isinstance(name, str), 'Invalid item name %s' % name
                assert isinstance(parent, FItem), 'Invalid item parent %s' % parent
                
                item = parent.children.get(name)
                if item==None:
                    path = parent.path + [name]
                    if not matchPaths(path, listener.path): continue
                    #if the item does not exist, create it and add it to the tree
                    item = createItem(name, chain, path, parent)
                    assert isinstance(item, FItem), 'Invalid item %s' % item
                    #add the new item to the tree (by linking the parent to it)
                    if item.parent.children == None: item.parent.children = dict() 
                    item.parent.children[item.name] = item
                    #set last modified time for the new item
                    try:
                        item.lastModified = int(os.path.getmtime(buildPath(item.path, PATH_SEPARATOR)))
                        item.hash = str(datetime.datetime.fromtimestamp(item.lastModified))
                    except: continue
                
                if not matchPaths(item.path, listener.path): continue
                #add the listener
                item.listeners.append(listener)
                
                #get the children of this node and add them to the queue
                pathStr = buildPath(item.path, PATH_SEPARATOR)
                if os.path.isdir(pathStr):
                    for child in [f for f in os.listdir(pathStr) if not f.startswith('.')]:
                        queue.append((child, item))
        
        return root.children.get(startName)

def createItem(name, chain, path = [], parent = None):
    assert isinstance(chain, Chain), 'Invalid chain %s' % chain
    item = chain.arg.Item()
    item.name = name
    item.path = path
    item.parent = parent
    item.listeners = []
    item.children = dict()
    return item

def matchPaths(itemPath, path):
    assert isinstance(itemPath, list) and itemPath, 'Invalid item path %s' % itemPath
    assert isinstance(path, list) and path, 'Invalid path %s' % path
    
    if len(itemPath) > len(path): return False
    
    for i in range(len(itemPath)):
        if itemPath[i] != path[i] and path[i] != '*': return False
    
    return True
    
def buildPath(path, separator):
    assert isinstance(path, list), 'Invalid path list %s' % path
    assert isinstance(separator, str), 'Invalid separator %s' % separator
    return '%s%s' % (separator, separator.join(path))
        
    