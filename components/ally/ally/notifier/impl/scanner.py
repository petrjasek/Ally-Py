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
from ally.notifier.impl.register import buildPath, createItem,\
    matchPaths
from threading import Thread
from time import sleep

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
    # ---------------------------------------------------------------- Requires
    itemTree = requires(Context, doc='''
    @rtype: Context
    The root of the item tree structure
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
        
        Scans the items tree and launches notifications.
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(solicit, Solicit), 'Invalid solicit %s' % solicit
        
        self._chain = chain
        
        scanThread = ScannerThread(target=self.scanItems, name='Scanner thread', args=(solicit.itemTree,))
        scanThread.start()
    
    def scanItems(self, itemTree):
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
                    print('Item changed: ' + str(item))
                    #recreate child items if item.path is a directory
                    if os.path.isdir(buildPath(item.path, os.path.sep)): item = self.rebuildItems(item)
                    #do something else if item.path is a file - like launch the file parser
                    else:
                        print('Parse file %s' % item.path)
                    item.lastModified = lastModified
                    continue
            
            if item.children: queue.extend(item.children.values())
    
    def rebuildItems(self, item):
        ''' '''
        assert isinstance(item, FItem), 'Invalid item %s' % item
        assert isinstance(self._chain, Chain), 'Invalid chain %s' % self._chain
        
        #compare the list of known children with the list of newly read children
        currentChildren = set(item.children.keys())
        newChildren = set()
        pathStr = buildPath(item.path, PATH_SEPARATOR)
        if os.path.isdir(pathStr):
            for child in os.listdir(pathStr):
                newChildren.add(child)
        
        #create the children that are missing; at the end
        for child in newChildren:
            if child in currentChildren: currentChildren.remove(child) 
            else:
                #create the child item and add it to the parent children list
                childPath = item.path + [child]
                listeners = []
                for listener in item.listeners:
                    assert isinstance(listener, FListener), 'Invalid listener %s' % listener
                    if matchPaths(childPath, listener.path):
                        listeners.append(listener)
                        break
                if listeners:
                    childItem = createItem(child, self._chain, childPath, item)
                    item.children[childItem.name] = childItem
        
        #delete the children that are no longer present on the disk
        assert isinstance(item.children, dict)
        for child in currentChildren:
            item.children.pop(child)
        
        return item

class ScannerThread(Thread):
    def run(self):
        while True:
            if self._target:
                self._target(*self._args, **self._kwargs)
            sleep(1)
    