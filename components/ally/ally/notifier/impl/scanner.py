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
    parent = attribute(Context)
    name = attribute(str)
    children = attribute(dict)
    path = attribute(str)
    URIType = attribute(str)
    lastModified = attribute(int)
    hash = attribute(str)
    listeners = attribute(list)
        
class FListener(Context):
    #---------------------------------------------------Defined
    path = attribute(list, doc='''
    @rtype: list[str]
    The path of the listener.
    ''')
    #----------------------------------------------------Requires
    doMatch = requires(IDo, doc='''
    ''')
    doOnContentCreated = requires(IDo, doc='''
    ''')
    doOnContentChanged = requires(IDo, doc='''
    ''')
    doOnContentRemoved = requires(IDo, doc='''
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
        
        if not solicit.itemTree: solicit.itemTree = createItem(None, chain, '')
        if not solicit.itemTree.children: solicit.itemTree.children = dict()
        
        solicit.itemTree = self.createItemTree(solicit.listeners, solicit.itemTree, chain)
        
        scanThread = ScannerThread(target=self.scanItems, name='File system notifier scanner thread', args=(solicit.itemTree, chain))
        scanThread.start()
    
    def createItemTree(self, listeners, root, chain):
        '''
        Creates a tree structure of items that matches the given path.
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(listeners, list), 'Invalid listeners %s' % listeners 
        
        for listener in listeners:
            assert isinstance(listener, FListener), 'Invalid listener %s' % listener
            assert listener.path, 'Invalid listener path %s' % listener.path
            
            offset = 0
            if os.path.isabs(listener.path): offset = 1
            startName = listener.path[:listener.path.find(PATH_SEP, offset)]
            if not os.path.isdir(startName) and not os.path.isfile(startName) : continue
             
            queue = deque()
            queue.append((startName, root))  # name, parent
            while queue:
                name, parent = queue.popleft()
                assert isinstance(name, str), 'Invalid item name %s' % name
                assert isinstance(parent, FItem), 'Invalid item parent %s' % parent
                
                item = parent.children.get(name)
                if item is None:
                    path = os.path.join(parent.path, name)
                    if not listener.doMatch(path): continue
                    # if the item does not exist, create it and add it to the tree
                    item = createItem(name, chain, path, parent)
                    assert isinstance(item, FItem), 'Invalid item %s' % item
                    # add the new item to the tree (by linking the parent to it)
                    if item.parent.children is None: item.parent.children = {} 
                    item.parent.children[item.name] = item
                    
                    #if the item is a file - notify listener
                    if os.path.isfile(item.path):
                        uri = buildItemPath(item, PATH_SEP)
                        listener.doOnContentCreated(uri, getContent(uri))
                
                if not listener.doMatch(item.path): continue
                # add the listener
                item.listeners.append(listener)
                
                # get the children of this node and add them to the queue
                path = item.path
                if os.path.isdir(path):
                    queue.extend((f, item) for f in os.listdir(path) if not f.startswith('.'))
        
        return root
    
    def scanItems(self, itemTree, chain):
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
            if item.name != None:
                path = item.path
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
                    if os.path.isdir(item.path): item = self.rebuildItems(item, chain)
                    #do something else if item.path is a file - like launch the file parser
                    elif os.path.isfile(item.path):
                        for listener in item.listeners:
                            assert isinstance(listener, FListener), 'Invalid listener %s' % listener
                            uri = buildItemPath(item, PATH_SEP)
                            listener.doOnContentChanged(uri, getContent(uri))
                        
                    item.lastModified = lastModified
            
            if item.children: queue.extend(item.children.values())
    
    def rebuildItems(self, item, chain):
        '''
        The method is called when an item is modified. It will update the children of the item. 
        '''
        assert isinstance(item, FItem), 'Invalid item %s' % item
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        
        #compare the list of known children with the list of newly read children
        currentChildren = set(item.children.keys())
        newChildren = set()
        path = item.path
        if os.path.isdir(path):
            for child in os.listdir(path):
                newChildren.add(child)
        
        #create the children that are missing; at the end
        for child in newChildren:
            if child in currentChildren: currentChildren.remove(child) 
            else:
                #create the child item and add it to the parent children list
                self.onCreateItem(item, child, chain)
        
        #delete the children that are no longer present on the disk
        assert isinstance(item.children, dict)
        for child in currentChildren:
            childItem = item.children.pop(child)
            self.onDeleteItem(childItem)
        
        return item
    
    def onCreateItem(self, item, childName, chain):
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
            childPath = os.path.join(parent.path, childName)
            
            listeners = []
            for listener in parent.listeners:
                assert isinstance(listener, FListener), 'Invalid listener %s' % listener
                if listener.doMatch(childPath):
                    listeners.append(listener)
        
            if not listeners: continue
                
            childItem = createItem(childName, chain, childPath, parent)
            childItem.listeners = listeners
            #add the child item to its parent
            parent.children[childItem.name] = childItem
            
            #if the child is a file, send on_created notification
            if os.path.isfile(childItem.path):
                for listener in childItem.listeners:
                    listener.doOnContentCreated(childItem.path, getContent(childItem.path))
            #else if child is a directory, add its children to the queue
            elif os.path.isdir(childItem.path):
                for child in os.listdir(childItem.path):
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
            path = item.path
            #if child is file, launch do_on_content_removed for each listener 
            for listener in item.listeners:
                assert isinstance(listener, FListener), 'Invalid listener %s' % listener
                listener.doOnContentRemoved(path)
            
            if item.children: queue.extend(item.children.values())

def createItem(name, chain, path, parent=None):
    assert isinstance(chain, Chain), 'Invalid chain %s' % chain
    assert isinstance(path, str)
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
        item.lastModified = int(os.path.getmtime(item.path))
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
    return '%s%s' % (item.URIType, item.path)

class ScannerThread(Thread):
    def run(self):
        while True:
            if self._target:
                self._target(*self._args, **self._kwargs)
            sleep(1)
    