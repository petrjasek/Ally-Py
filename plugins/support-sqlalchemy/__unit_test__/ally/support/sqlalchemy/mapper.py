'''
Created on Mar 23, 2012

@package: ally core sql alchemy
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides unit testing for the sql alchemy mapper.
'''

# Required in order to register the package extender whenever the unit test is run.
if True:
    import package_extender
    package_extender.PACKAGE_EXTENDER.setForUnitTest(True)

# --------------------------------------------------------------------

from ally.api.config import model
from sql_alchemy.support.mapper import DeclarativeMetaModel, \
    mapperSimple
from sqlalchemy.dialects.mysql.base import INTEGER
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.schema import Table, Column, MetaData, ForeignKey
from sqlalchemy.sql.expression import case
from sqlalchemy.types import String
import unittest

# --------------------------------------------------------------------

meta = MetaData()

# --------------------------------------------------------------------

Base = declarative_base(metadata=meta, metaclass=DeclarativeMetaModel)

@model(id='Id')
class Person:
    '''    
    Provides the person model.
    '''
    Id = int
    FirstName = str
    LastName = str
    FullName = str
    Address = str
    EMail = str

@model
class User(Person):
    '''    
    Provides the user model.
    '''
    Name = str

class PersonMapped(Base, Person):
    '''
    Provides the mapping for Person entity.
    '''
    __tablename__ = 'person'
    __table_args__ = dict(mysql_engine='InnoDB', mysql_charset='utf8')

    Id = Column('id', INTEGER(unsigned=True), primary_key=True)
    FirstName = Column('first_name', String(255))
    LastName = Column('last_name', String(255))
    Address = Column('address', String(255))
    EMail = Column('email', String(255))
    @hybrid_property
    def FullName(self):
        if self.FirstName is None: return self.LastName
        if self.LastName is None: return self.FirstName
        return self.FirstName + ' ' + self.LastName

    # Expression for hybrid ------------------------------------
    FullName.expression(lambda cls: case([(cls.FirstName == None, cls.LastName)], else_=
                                    case([(cls.LastName == None, cls.FirstName)], else_=
                                    cls.FirstName + ' ' + cls.LastName)))

class UserMapped(PersonMapped, User):
    '''
    Provides the mapping for User entity.
    '''
    __tablename__ = 'user'
    __table_args__ = dict(mysql_engine='InnoDB', mysql_charset='utf8')

    Name = Column('name', String(20), nullable=False, unique=True)

    # Non REST model attribute --------------------------------------
    userId = Column('fk_person_id', ForeignKey(PersonMapped.Id), primary_key=True)
    # Never map over the inherited id

# --------------------------------------------------------------------

tableParent = Table('user_parent', meta,
                    Column('id', INTEGER(unsigned=True), primary_key=True, key='Id'),
                    Column('name', String(20), nullable=False, unique=True, key='Name'))

tableUserParent = Table('user_with_parent', meta,
                Column('fk_user_id', INTEGER(unsigned=True), ForeignKey(UserMapped.userId), primary_key=True, key='Id'),
                Column('fk_parent_id', INTEGER(unsigned=True), ForeignKey(tableParent.c.Id), key='Parent'))

@model(id='Id')
class Parent:
    '''    
    Provides the user parent.
    '''
    Id = int
    Name = str

@model
class UserWithParent(User):
    '''
    A user model with a parent.
    '''
    Parent = Parent

UserWithParent = mapperSimple(UserWithParent, tableUserParent, inherits=UserMapped)

# --------------------------------------------------------------------

class TestMapping(unittest.TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        self.sessionCreate = sessionmaker(bind=engine)
        meta.create_all(engine)

    def testSuccesSimpleMapping(self):
        session = self.sessionCreate()
        user = UserMapped()        
        user.Name = 'Hello world'
        
        session.add(user)
        session.flush((user,))
        self.assertTrue(user.Id)

        session.commit()
        session.close()

        session = self.sessionCreate()
        users = session.query(UserMapped).filter(UserMapped.Name == 'Hello world').all()
        self.assertEqual(len(users), 1)
        self.assertTrue(users[0].Id)
        self.assertTrue(users[0].Name)
        self.assertEqual(users[0].Name, 'Hello world')
        self.assertEqual(users[0].Id, 1)
        session.close()

    def testSuccessInheritAndForeignKey(self):
        session = self.sessionCreate()
        user = UserWithParent()        
        user.Name = 'Hello world'
        user.Parent = 1
        
        session.add(user)
        session.flush((user,))
        self.assertTrue(user.Id)

        session.commit()
        session.close()

        session = self.sessionCreate()
        users = session.query(UserWithParent).filter(UserWithParent.Name == 'Hello world').all()
        self.assertEqual(len(users), 1)
        user = users[0]
        self.assertTrue(user.Id)
        self.assertTrue(user.Name)
        self.assertTrue(user.Parent)
        self.assertEqual(user.Name, 'Hello world')
        self.assertEqual(user.Id, 1)
        self.assertEqual(user.Parent, 1)
        session.close()

        session = self.sessionCreate()
        users = session.query(UserWithParent).filter(UserWithParent.Parent == 1).all()
        self.assertEqual(len(users), 1)
        user = users[0]
        self.assertTrue(user.Id)
        self.assertTrue(user.Name)
        self.assertTrue(user.Parent)
        self.assertEqual(user.Name, 'Hello world')
        self.assertEqual(user.Id, 1)
        self.assertEqual(user.Parent, 1)
        session.close()

# --------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
