'''
Created on Jul 15, 2011

@package: support sqlalchemy
@copyright: 2011 Sourcefabric o.p.s.
@license http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the sql alchemy setup files.
'''

# --------------------------------------------------------------------

NAME = 'ally-support-sqlalchemy'
VERSION = '1.0'
AUTHOR = 'Gabriel Nistor'
AUTHOR_EMAIL = 'gabriel.nistor@sourcefabric.org'
KEYWORDS = ['Ally', 'REST', 'framework', 'plugin', 'SQLAlchemy']
DESCRIPTION = 'Provides the support for SQL alchemy'
LONG_DESCRIPTION = '''The [SQLAlchemy] support plugin that facilitates the work with SQL Alchemy object 
relational mapping. Contains support for mapping REST models with SQL Alchemy, also support for transaction
handling at a request scope level. Has a central database application configuration but also the means of setting
a different or multiple databases.'''
INSTALL_REQUIRES = ['ally-api >= 1.0', 'SQLAlchemy>=0.7.1']
TEST_SUITE = '__unit_test__'
