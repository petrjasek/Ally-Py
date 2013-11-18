'''
Created on Nov 8, 2013
 
@package: internationalization
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Cristian Domsa
 
Internationalization database meta class.
'''

from sqlalchemy.dialects.mysql.base import INTEGER
from sqlalchemy.schema import Column
from sqlalchemy.types import String, LargeBinary
from internationalization.meta.metadata_internationalization import Base
from internationalization.api.po_file import PO
# --------------------------------------------------------------------

class POTMapped(Base, PO):
    '''
    Provides the mapping for POT files @see: PO.
    '''
    __tablename__ = 'localization_pot'
    __table_args__ = dict(mysql_engine='InnoDB', mysql_charset='utf8')
    
    Name = Column('Name', String(20), nullable=False, unique=True)
    # Non REST model attribute --------------------------------------    
    id = Column('id', INTEGER(unsigned=True), primary_key=True)
    timestamp = Column('timestamp', INTEGER(unsigned=True), nullable=False)
    file = Column('file', LargeBinary())
    
class POMapped(Base, PO):
    '''
    Provides the mapping for PO files @see: PO
    '''
    __tablename__ = 'localization_po'
    __table_args__ = dict(mysql_engine='InnoDB', mysql_charset='utf8')
    
    Name = Column('Name', String(20), nullable=False, unique=True)
    # Non REST model attribute --------------------------------------    
    id = Column('id', INTEGER(unsigned=True), primary_key=True)
    timestamp = Column('timestamp', INTEGER(unsigned=True), nullable=False)
    Locale = Column('Locale', String(20), nullable=False, unique=True)
    file = Column('file', LargeBinary())