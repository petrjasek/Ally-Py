'''
Created on Aug 23, 2011

@package: superdesk person
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Balaceanu

Contains the SQL alchemy meta for person API.
'''

from ally.support.sqlalchemy.mapper import mapperModel
from sqlalchemy.dialects.mysql.base import INTEGER
from sqlalchemy.schema import Table, Column
from sqlalchemy.types import String
from superdesk.meta import meta
from ..api.person import Person

# --------------------------------------------------------------------

table = Table('person', meta,
               Column('id', INTEGER(unsigned=True), primary_key=True, key='Id'),
               Column('first_name', String(20), nullable=True, unique=False, key='FirstName'),
               Column('last_name', String(20), nullable=True, unique=False, key='LastName'),
               Column('address', String(20), nullable=True, unique=False, key='Address'),
               mysql_engine='InnoDB', mysql_charset='utf8')

# map User entity to defined table (above)
Person = mapperModel(Person, table)
