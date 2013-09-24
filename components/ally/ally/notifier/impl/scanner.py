'''
Created on Sep 13, 2013

@author: mihaigociu

@package: ally base
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Gociu

Scanning the items tree.
'''

from ally.container.ioc import injected
from ally.design.processor.attribute import attribute, requires, defines
from ally.design.processor.execution import Chain
from collections import deque
import os
import datetime
from ally.design.processor.handler import HandlerProcessor
from ally.design.processor.context import Context
from threading import Thread
from time import sleep
import logging
from ally.support.util_spec import IDo

# --------------------------------------------------------------------

log = logging.getLogger(__name__)
PATH_SEP = os.path.sep

# --------------------------------------------------------------------
class Solicit(Context):
    '''
    The solicit context.
    '''
    # ---------------------------------------------------------------- Requires
    listeners = requires(list, doc='''
    @rtype: list[Context]
    The listeners for the items tree.
    ''')
    
    # ---------------------------------------------------------------- Defines
    itemTree = defines(Context, doc='''
    @rtype: Context
    The root of the item tree structure
    ''')

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
    #---------------------------------------------------Defined
    path = attribute(list, doc='''
    @rtype: list[str]
    The path of the listener.
    ''')
    #----------------------------------------------------Requires
    doMatch = requires(IDo, doc='''
    @rtype: callable(listenerPath, itemPath) -> boolean
    Matches the item path against the paths accepted by the listener.
    @param listenerPath: list[string]
        Pattern for paths accepted by the listener.
    @param itemPath: list[string]
        Path of the item.
    ''')
    doOnContentCreated = requires(IDo, doc='''
    @rtype: callable(URI, content)
    Is called when an item for this listener is created.
    @param URI: string
        Pattern for paths accepted by the listener.
    @param content: stream
        Stream with the content of the resource.
    ''')
    doOnContentChanged = requires(IDo, doc='''
    @rtype: callable(URI, content)
    Is called when an item for this listener is changed.
    @param URI: string
        Pattern for paths accepted by the listener.
    @param content: stream
        Stream with the content of the resource.
    ''')
    doOnContentRemoved = requires(IDo, doc='''
    @rtype: callable(URI)
    Is called when an item for this listener is deleted.
    @param URI: string
        Pattern for paths accepted by the listener.
    @param content: stream
        Stream with the content of the resource.
    ''')
    
# --------------------------------------------------------------------
@injected
class ScannerHandler(HandlerProcessor):
    '''
    Scans the item tree for modified items.
    '''
    def process(self, chain, solicit:Solicit, Item:FItem, Listener:FListener, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        First creates the items tree and adds the listeners.
        Then it scans the items tree and launches notifications.
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(solicit, Solicit), 'Invalid solicit %s' % solicit
        
        self._chain = chain
        if not solicit.itemTree: solicit.itemTree = createItem('ROOT', chain, [])
        if not solicit.itemTree.children: solicit.itemTree.children = dict()
        
        item = self.createItems(solicit.listeners)
        assert isinstance(item, FItem), 'Invalid item %s' % item
        solicit.itemTree.children[item.name] = item
        
        scanThread = ScannerThread(target=self.scanItems, name='Scanner thread', args=(solicit.itemTree,))
        scanThread.start()
    
    def createItems(self, listeners):
        '''
        Creates a tree structure of items that matches the given path.
        '''
        chain = self._chain
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(listeners, list), 'Invalid listeners %s' % listeners 
        
        root = createItem('ROOT', chain, [])
        
        for listener in listeners:
            assert isinstance(listener, FListener), 'Invalid listener %s' % listener
            assert listener.path, 'Invalid listener path %s' % listener.path
            assert os.path.isdir(buildPath(listener.path[:1], PATH_SEP)), 'Invalid root directory %s' % listener.path[:1]
            
            startName = listener.path[0]
            queue = deque()
            queue.append((startName, root))  # name, parent
            while queue:
                name, parent = queue.popleft()
                assert isinstance(name, str), 'Invalid item name %s' % name
                assert isinstance(parent, FItem), 'Invalid item parent %s' % parent
                
                item = parent.children.get(name)
                if item is None:
                    path = parent.path + [name]
                    if not listener.doMatch(listener.path, path): continue
                    # if the item does not exist, create it and add it to the tree
                    item = createItem(name, chain, path, parent)
                    assert isinstance(item, FItem), 'Invalid item %s' % item
                    # add the new item to the tree (by linking the parent to it)
                    if item.parent.children is None: item.parent.children = {} 
                    item.parent.children[item.name] = item
                    
                    
                    #if the item is a file - notify listener
                    if os.path.isfile(buildPath(item.path, os.path.sep)):
                        uri = buildItemPath(item, PATH_SEP)
                        listener.doOnContentCreated(uri, getContent(uri))
                
                if not listener.doMatch(listener.path, item.path): continue
                # add the listener
                item.listeners.append(listener)
                
                # get the children of this node and add them to the queue
                pathStr = buildPath(item.path, PATH_SEP)
                if os.path.isdir(pathStr):
                    for child in [f for f in os.listdir(pathStr) if not f.startswith('.')]:
                        queue.append((child, item))
        
        return root.children.get(startName)
    
    def scanItems(self, itemTree):
        '''
        Scans the items tree and keeps it updated. Also launches create, update, delete notifications for listeners.
        '''
        assert isinstance(itemTree, FItem)
        
        #scan the tree
        queue = deque()
        queue.append(itemTree)
        while queue:
            #get the node
            item = queue.pop()
            assert isinstance(item, FItem), 'Invalid item %s' % item
            
            #check that the path still exists; if not, delete it from the items tree
            if item.name != 'ROOT':
                path = buildPath(item.path, os.path.sep)
                if not os.path.exists(path):
                    item.parent.children.pop(item.name)
                    continue
            
            #see if the item has changed - for ROOT item lastModified will be None
            if item.lastModified:
                #compare the lastModified attribute on the item with the ... 
                lastModified = int(os.path.getmtime(path))
                if item.lastModified != lastModified:
                    assert log.debug('Item changed: %s' % item.path) or True
                    #recreate child items if item.path is a directory
                    if os.path.isdir(buildPath(item.path, os.path.sep)): item = self.rebuildItems(item)
                    #do something else if item.path is a file - like launch the file parser
                    elif os.path.isfile(buildPath(item.path, os.path.sep)):
                        for listener in item.listeners:
                            assert isinstance(listener, FListener), 'Invalid listener %s' % listener
                            uri = buildItemPath(item, PATH_SEP)
                            listener.doOnContentChanged(uri, getContent(uri))
                        
                    item.lastModified = lastModified
            
            if item.children: queue.extend(item.children.values())
    
    def rebuildItems(self, item):
        '''
        The method is called when an item is modified. It will update the children of the item. 
        '''
        assert isinstance(item, FItem), 'Invalid item %s' % item
        assert isinstance(self._chain, Chain), 'Invalid chain %s' % self._chain
        
        #compare the list of known children with the list of newly read children
        currentChildren = set(item.children.keys())
        newChildren = set()
        pathStr = buildPath(item.path, PATH_SEP)
        if os.path.isdir(pathStr):
            for child in os.listdir(pathStr):
                newChildren.add(child)
        
        #create the children that are missing; at the end
        for child in newChildren:
            if child in currentChildren: currentChildren.remove(child) 
            else:
                #create the child item and add it to the parent children list
                self.onCreateItem(item, child)
        
        #delete the children that are no longer present on the disk
        assert isinstance(item.children, dict)
        for child in currentChildren:
            childItem = item.children.pop(child)
            self.onDeleteItem(childItem)
        
        return item
    
    def onCreateItem(self, item, childName):
        '''
        Recursively creates the subtree starting with childName for the given item, and launches on_content_created notifications on the way.
        '''
        assert isinstance(item, FItem), 'Invalid item %s' % item
        assert isinstance(childName, str), 'Invalid item name %s' % childName
        #create the child item and add it to the parent children list
        queue = deque()
        queue.append((childName, item))
        
        while queue:
            childName, parent = queue.popleft()
            childPath = parent.path + [childName]
            
            listeners = []
            for listener in parent.listeners:
                assert isinstance(listener, FListener), 'Invalid listener %s' % listener
                if listener.doMatch(listener.path, childPath):
                    listeners.append(listener)
        
            if not listeners: continue
                
            childItem = createItem(childName, self._chain, childPath, parent)
            childItem.listeners = listeners
            #add the child item to its parent
            parent.children[childItem.name] = childItem
            
            childPathStr = buildPath(childItem.path, PATH_SEP)
            #if the child is a file, send on_created notification
            if os.path.isfile(childPathStr):
                for listener in childItem.listeners:
                    uri = buildItemPath(childItem, PATH_SEP)
                    listener.doOnContentCreated(uri, getContent(uri))
            #else if child is a directory, add its children to the queue
            elif os.path.isdir(childPathStr):
                for child in os.listdir(childPathStr):
                    queue.append((child, childItem))
        return item
            
    def onDeleteItem(self, item):
        '''
        Recursively launches do_on_delete events for the given item and all of its children.
        '''
        assert isinstance(item, FItem), 'Invalid item %s' % item
        
        queue = deque()
        queue.append(item)
        while queue:
            item = queue.popleft()
            path = buildPath(item.path, PATH_SEP)
            #if child is file, launch do_on_content_removed for each listener 
            for listener in item.listeners:
                assert isinstance(listener, FListener), 'Invalid listener %s' % listener
                listener.doOnContentRemoved(path)
            
            if item.children: queue.extend(item.children.values())

def createItem(name, chain, path, parent=None):
    assert isinstance(chain, Chain), 'Invalid chain %s' % chain
    item = chain.arg.Item()
    assert isinstance(item, FItem), 'Invalid item %s' % item
    item.name = name
    item.path = path
    item.parent = parent
    item.listeners = []
    item.children = dict()
    item.URIType = ''
    #only set lastModified time-stamp for non ROOT items
    if parent:
        item.lastModified = int(os.path.getmtime(buildPath(item.path, PATH_SEP)))
        item.hash = str(datetime.datetime.fromtimestamp(item.lastModified))
    return item

def buildPath(path, separator):
    assert isinstance(path, list), 'Invalid path list %s' % path
    assert isinstance(separator, str), 'Invalid separator %s' % separator
    return '%s%s' % (separator, separator.join(path))

def getContent(uri):
    try:
        return open(uri, "r")
    except Exception as e:
        log.debug(str(e))
        return None

def buildItemPath(item, separator):
    assert isinstance(item, FItem), 'Invalid item %s' % item
    return '%s%s' % (item.URIType, buildPath(item.path, separator))

class ScannerThread(Thread):
    def run(self):
        while True:
            if self._target:
                self._target(*self._args, **self._kwargs)
            sleep(1)
    