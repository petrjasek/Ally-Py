'''
Created on Jul 15, 2011

@package: Internationlization language
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Balaceanu

Contains the superdesk language setup files.
'''

# --------------------------------------------------------------------

NAME = 'Ally languages'
GROUP = 'internationlization'
VERSION = '1.0'
DESCRIPTION = 'Provides the languages'
LONG_DESCRIPTION = 'Language management functionality (model, service)'
AUTHOR = 'Gabriel Nistor'
AUTHOR_EMAIL = 'gabriel.nistor@sourcefabric.org'
KEYWORDS = ['Ally', 'REST', 'plugin', 'language']
INSTALL_REQUIRES = ['ally-api >= 1.0', 'support-sqlalchemy >= 1.0', 'superdesk >= 1.0']

__extra__  = dict()