'''
Created on Jul 15, 2011

@package: distribution ally REST basic
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the distutlis setup for the collection of components that represent the basic ally REST service platform.
'''

# --------------------------------------------------------------------

NAME = 'ally-rest-basic'
VERSION = '1.0'
DESCRIPTION = 'The basic ally REST service platform '
AUTHOR = 'Gabriel Nistor'
AUTHOR_EMAIL = 'gabriel.nistor@sourcefabric.org'
KEYWORDS = ['Ally', 'REST', 'basic', 'service']
LONG_DESCRIPTION = '''The components that represent the basic ally REST service platform.'''
CLASSIFIERS = ['Development Status :: 4 - Beta']
INSTALL_REQUIRES = ['ally-core-http >= 1.0', 'ally-plugin >= 1.0']
__extra__ = dict(packages=[])
