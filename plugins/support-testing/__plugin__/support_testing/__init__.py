'''
Created on Jul 15, 2011

@package: support testing
@copyright: 2011 Sourcefabric o.p.s.
@license http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the testing support.
'''

# --------------------------------------------------------------------

NAME = 'ally-support-testing'
VERSION = '1.0'
AUTHOR = 'Gabriel Nistor'
AUTHOR_EMAIL = 'gabriel.nistor@sourcefabric.org'
KEYWORDS = ['Ally', 'REST', 'framework', 'plugin', 'testing']
DESCRIPTION = 'Provides the support for testing the API, basically the means for reseting data.'
LONG_DESCRIPTION = ''' The testing plugin provides the means of testing the application using other databases
and the ability to reset the data.'''
INSTALL_REQUIRES = ['ally-core-http >= 1.0', 'ally-plugin >= 1.0']
