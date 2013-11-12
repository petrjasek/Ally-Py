'''
Created on Nov 8, 2013
 
@package: internationalization
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Cristian Domsa
 
Internationalization database meta class.
'''

from sqlalchemy.dialects.mysql.base import INTEGER
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, LargeBinary
from internationalization.meta.metadata_internationalization import Base
from internationalization.api.po_file import PO
# --------------------------------------------------------------------

class LocalizationCollection(Base, PO):
    '''
    Provides the mapping for @see: PO.
    '''
    __tablename__ = 'localization'
    __table_args__ = dict(mysql_engine='InnoDB', mysql_charset='utf8')
    
    id = Column('id', INTEGER(unsigned=True), primary_key=True)
    Name = Column('Name', String(20), nullable=False, unique=True)
    locale = Column('locale', String(20), nullable=False)
    timestamp = Column('timestamp', INTEGER(unsigned=True), nullable=False)
    poFile = Column('poFile', LargeBinary())