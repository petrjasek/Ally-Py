'''
Created on Jan 17, 2012

@package: support mongoengine
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the database settings for the application mongo database.
'''

from ally.container import ioc
from ally.container.impl.processor.binder import BinderHandler
from ally.design.processor.assembly import Assembly
from ally.design.processor.handler import Handler
from mongo_engine.core.impl.processor.binder.connection import \
    BindConnectionHandler


# --------------------------------------------------------------------
@ioc.config
def database_url():
    ''' The database URL, something like "mongodb://localhost:27017"'''
    return 'mongodb://localhost:27017'

@ioc.config
def database():
    ''' The database name, something like "application-db"'''
    return 'application'

# --------------------------------------------------------------------

@ioc.entity
def assemblyBind() -> Assembly:
    '''The assembly containing the handlers used for binding services/classes with Mongo engine support'''
    return Assembly('Bind Mongo engine')

# --------------------------------------------------------------------

@ioc.entity
def binder():
    b = BinderHandler()
    b.bindAssembly = assemblyBind()
    return b

@ioc.entity
def bindConnection() -> Handler:
    b = BindConnectionHandler()
    b.url = database_url()
    b.database = database()
    return b
    
# --------------------------------------------------------------------

@ioc.before(assemblyBind)
def updateAssemblyBind():
    assemblyBind().add(bindConnection())
 
# --------------------------------------------------------------------

def bindApplicationConnection(proxy):
    binder().bind(proxy)

