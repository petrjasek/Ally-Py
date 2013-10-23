'''
Created on Sep 26, 2013

@package: ally base
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Gociu

Provides the general notifier system setup.
'''

from ally.container import ioc
from ally.design.processor.assembly import Assembly
from ally.design.processor.execution import Processing, FILL_ALL
from ally.design.processor.handler import Handler
from ally.notifier.impl.processor.scanner_file_system import FileSystemScanner

# --------------------------------------------------------------------

@ioc.entity
def registersListeners() -> list:
    ''' The list of register like handlers that push the listeners for notifying'''
    return []

@ioc.entity
def assemblyNotifier() -> Assembly:
    ''' The assembly used for notifying changes on resources'''
    return Assembly('Notifier')

# --------------------------------------------------------------------

@ioc.entity
def fileSystemScanner() -> Handler: return FileSystemScanner()

# --------------------------------------------------------------------

@ioc.after(assemblyNotifier)
def updateNotifierForFileSystemScanner():
    assemblyNotifier().add(fileSystemScanner())

@ioc.start
def startNotifications():
    if registersListeners():
        assemblyNotifier().add(*registersListeners(), before=fileSystemScanner())
        processing = assemblyNotifier().create()
        assert isinstance(processing, Processing), 'Invalid processing %s' % processing
        processing.execute(FILL_ALL)