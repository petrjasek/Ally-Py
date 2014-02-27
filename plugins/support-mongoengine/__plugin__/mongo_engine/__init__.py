'''
Created on Jul 15, 2011

@package: support mongoengine
@copyright: 2011 Sourcefabric o.p.s.
@license http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the mongo engine setup files.
'''

# --------------------------------------------------------------------

NAME = 'ally-support-mongoengine'
VERSION = '1.0'
AUTHOR = 'Gabriel Nistor'
AUTHOR_EMAIL = 'gabriel.nistor@sourcefabric.org'
KEYWORDS = ['Ally', 'REST', 'framework', 'plugin', 'Mongo']
DESCRIPTION = 'Provides the support for using Mongo engine ORM'
LONG_DESCRIPTION = '''The [Mongo Engine] support plugin that facilitates the work with Mongo Engine object relational
mapping. Contains support for mapping REST models with Mongo Documents.'''
INSTALL_REQUIRES = ['ally-api >= 1.0', 'mongoengine >= 0.8.4']
