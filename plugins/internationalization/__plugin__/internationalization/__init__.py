'''
Created on Jul 15, 2011

@package: internationalization
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Nistor Gabriel

Contains the internationalization setup files.
'''

# --------------------------------------------------------------------

NAME = 'ally-internationalization'
VERSION = '1.0'
AUTHOR = 'Gabriel Nistor'
AUTHOR_EMAIL = 'gabriel.nistor@sourcefabric.org'
KEYWORDS = ['Ally', 'REST', 'plugin', 'internationalization']
DESCRIPTION = 'Provides the managmenet for the localized messages'
LONG_DESCRIPTION = ''' Provides the services for managing PO and POT files.'''
INSTALL_REQUIRES = ['ally-api >= 1.0', 'ally-support-sqlalchemy >= 1.0', 'ally-support-cdm >= 1.0', 'Babel >= 1.3']
