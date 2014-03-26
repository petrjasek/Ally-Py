'''
Created on Jan 17, 2012

@package: support sqlalchemy
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the database settings for the application database.
'''

import logging
import os
from urllib.parse import urlparse

from ally.container import ioc, app
from ally.container.impl.processor.binder import BinderHandler
from ally.design.priority import PRIORITY_NORMAL, Priority
from ally.design.processor.assembly import Assembly
from ally.design.processor.handler import Handler
from sql_alchemy.core.impl.processor.binder.error_translator import \
    ErrorTranslatorHandler
from sql_alchemy.core.impl.processor.binder.session import BindSessionHandler
from sqlalchemy import event
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import sessionmaker


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

PRIORITY_CREATE_TABLES = Priority('Create tables', before=PRIORITY_NORMAL)

# --------------------------------------------------------------------

@ioc.config
def database_url():
    '''This database URL is used for the application tables'''
    return 'sqlite:///workspace/shared/application.db'

@ioc.config
def alchemy_pool_recycle():
    '''The time to recycle pooled connection'''
    return 3600

# --------------------------------------------------------------------

@ioc.entity
def assemblyBind() -> Assembly:
    '''The assembly containing the handlers used for binding services/classes with SQL alchemy support'''
    return Assembly('Bind SQL alchemy')

@ioc.entity
def assemblySQLAssembler() -> Assembly:
    '''
    The assembly containing the handlers to be used in the assembly of invokers for error handling.
    '''
    return Assembly('Assemblers SQL alchemy', reportUnused=False)

@ioc.entity
def alchemySessionCreator(): return sessionmaker(bind=alchemyEngine())

@ioc.entity
def alchemyEngine() -> Engine:
    engine = create_engine(database_url(), pool_recycle=alchemy_pool_recycle())

    if database_url().startswith('sqlite://'):
        @event.listens_for(engine, 'connect')
        def setSQLiteFKs(dbapi_con, con_record):
            dbapi_con.execute('PRAGMA foreign_keys=ON')

    return engine

@ioc.entity
def metas(): return []

# --------------------------------------------------------------------

@app.populate(app.DEVEL, priority=PRIORITY_CREATE_TABLES)
def createTables():
    path = str(alchemyEngine().url)
    if path.startswith('sqlite://'):
        # We need to make sure that the database file has the folders created.
        url = urlparse(path)
        location = url.path.lstrip('/') 
        # We need to remove the start slash since in order not to confuse it with a relative path.
        location = os.path.dirname(location.replace('/', os.sep))
        if not os.path.exists(location):
            log.info('Creating folder \'%s\' for SQLite database', location)
            os.makedirs(location)
    
    if path.startswith('mysql'): alchemyEngine().execute('SET foreign_key_checks = 0;')
        
    for meta in metas(): meta.create_all(alchemyEngine())
    
    if path.startswith('mysql'): alchemyEngine().execute('SET foreign_key_checks = 1;')

# --------------------------------------------------------------------

@ioc.entity
def binder():
    b = BinderHandler()
    b.bindAssembly = assemblyBind()
    return b

@ioc.entity
def bindSession() -> Handler:
    b = BindSessionHandler()
    b.sessionCreator = alchemySessionCreator()
    return b

@ioc.entity
def errorTranslator() -> Handler:
    b = ErrorTranslatorHandler()
    b.assembly = assemblySQLAssembler()
    return b

# --------------------------------------------------------------------

@ioc.before(assemblyBind)
def updateAssemblyBind():
    assemblyBind().add(bindSession(), errorTranslator())
    
# --------------------------------------------------------------------

def bindApplicationSession(proxy):
    binder().bind(proxy)
