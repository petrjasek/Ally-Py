'''
Created on Nov 14, 2012

@package: assemblage
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

The plugin that provides the indexing support.
'''

# --------------------------------------------------------------------

NAME = 'ally-indexing-provider'
VERSION = '1.0'
AUTHOR = 'Gabriel Nistor'
AUTHOR_EMAIL = 'gabriel.nistor@sourcefabric.org'
DESCRIPTION = '''The plugin that provides the indexing support.'''
LONG_DESCRIPTION = '''This plugin offers the Indexing API and the implementation provides details related to 
the REST models content response indexing based on data associate with ally-core.'''
INSTALL_REQUIRES = ['ally-api >= 1.0', 'ally-core >= 1.0']
