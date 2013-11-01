'''
Created on Aug 25, 2011

@package: ally core sql alchemy
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the SQL alchemy meta for article type API.
'''

from . import meta
from ..api.article_type import ArticleType
# from ally.support.sqlalchemy.mapper import mapperModel
from sqlalchemy.schema import Table, Column
from sqlalchemy.types import String, Integer
from ally.api.config import model
from ally.support.api.entity_ided import Entity
from __unit_test__.ally.support.sqlalchemy.mapper import Base
from sql_alchemy.support.mapper import mapperModel

# --------------------------------------------------------------------

# @model(id='Id')
# class ArticleType(Base, ArticleType):
#     '''
#     Provides the article type model.
#     '''
#     
#     __tablename__ = 'article_type'
#     
#     id = Column('id', INTEGER(255), nullable=False, unique=True)
#     Name = str
#     
# 
# class UserTypeMapped(Base, UserType):
#     '''
#     Provides the mapping for UserType.
#     '''
#     __tablename__ = 'user_type'
#     __table_args__ = dict(mysql_engine='InnoDB')
# 
#     Key = Column('key', String(255), nullable=False, unique=True)
#     # None REST model attribute --------------------------------------
#     id = Column('id', INTEGER(unsigned=True), primary_key=True)


table = Table('article_type', meta,
              Column('id', Integer, primary_key=True, key='Id'),
              Column('name', String(255), nullable=False, unique=True, key='Name'))
 
ArticleType = mapperModel(ArticleType, table)
