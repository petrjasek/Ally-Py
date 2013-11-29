'''
Created on Jul 15, 2011

@package: support mongoengine
@copyright: 2011 Sourcefabric o.p.s.
@license http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the mongo engine setup files.
'''

# --------------------------------------------------------------------

NAME = 'Mongo engine support'
GROUP = 'Mongo'
VERSION = '1.0'
DESCRIPTION = 'Provides the support for using Mongo engine ORM'
INSTALL_REQUIRES = ['ally-api >= 1.0', 'mongoengine >= 0.8.4']
LONG_DESCRIPTION = '''The [Mongo Engine] support plugin that facilitates the work with Mongo Engine object relational
mapping. Contains support for mapping REST models with Mongo Documents.'''
KEYWORDS = ['Ally', 'REST', 'framework', 'plugin', 'Mongo']
