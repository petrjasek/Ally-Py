'''
Created on Nov 14, 2012

@package: assemblage
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the setup files for assemblage.
'''

# --------------------------------------------------------------------

NAME = 'assemblage'
GROUP = 'assemblage'
VERSION = '1.0.dev'
DESCRIPTION = \
'''
This plugin provides the assemblage service. 
'''
INSTALL_REQUIRES = ['ally-api', 'ally-core']
LONG_DESCRIPTION = '''This plugin offers the Indexing API and the implementation provides details related to 
                    the REST models content response indexing based on data associate with ally-core.'''