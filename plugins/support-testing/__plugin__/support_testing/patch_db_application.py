'''
Created on Mar 21, 2014

@package: support testing
@copyright: 2011 Sourcefabric o.p.s.
@license http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the sql alchemy database test support.
'''

import logging

from ally import container
from ally.container import ioc

from .processor import SWITCHER_TESTING, BEFORE_SWITCH
from .processor import testing_allowed


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

try:
    from __plugin__ import sql_alchemy  # @UnusedImport
except ImportError: log.info('No support-sqlalchemy plugin available, thus no need to apply testing patch')
else:
    from sqlalchemy.engine.base import Engine
    from sqlalchemy.orm.session import sessionmaker
    from sqlalchemy.engine import create_engine
    from sqlalchemy import event
    from sqlalchemy.sql.schema import MetaData
    
    from ..sql_alchemy.db_application import alchemySessionCreator, \
    alchemy_pool_recycle, alchemyEngine

    # --------------------------------------------------------------------
    
    @ioc.config
    def test_database_url():
        '''This database URL is used for the application testing tables'''
        return 'sqlite:///workspace/shared/application_test.db'
    
    # --------------------------------------------------------------------
    
    @SWITCHER_TESTING.switch(alchemyEngine)
    @ioc.entity
    def testAlchemyEngine() -> Engine:
        engine = create_engine(test_database_url(), pool_recycle=alchemy_pool_recycle())
    
        if test_database_url().startswith('sqlite://'):
            @event.listens_for(engine, 'connect')
            def setSQLiteFKs(dbapi_con, con_record):
                dbapi_con.execute('PRAGMA foreign_keys=ON')
    
        return engine
    
    @ioc.entity
    def testAlchemySessionCreator(): return sessionmaker(bind=testAlchemyEngine())
    
    @container.event.on(BEFORE_SWITCH)
    def testClearDatabase():
        meta = MetaData(testAlchemyEngine())
        meta.reflect()
        meta.drop_all()
    
    # --------------------------------------------------------------------
    
    @ioc.replace(alchemySessionCreator)
    def alchemySessionCreatorSwitcher(original):
        if not testing_allowed(): return original
        return SWITCHER_TESTING.switchCall(original, testAlchemySessionCreator())
