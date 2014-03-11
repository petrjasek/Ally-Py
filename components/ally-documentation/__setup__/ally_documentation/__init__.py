'''
Created on Jul 15, 2011

@package: ally core
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

The automatic documentation creator for REST services.
'''

# --------------------------------------------------------------------

NAME = 'ally-documentation'
VERSION = '1.0'
DESCRIPTION = 'Provides automatically generated documentation for REST services and models'
AUTHOR = 'Gabriel Nistor'
AUTHOR_EMAIL = 'gabriel.nistor@sourcefabric.org'
KEYWORDS = ['Ally', 'documentation', 'REST']
LONG_DESCRIPTION = '''Provides the documentation support for the [API] services adn models.'''
INSTALL_REQUIRES = ['ally-core-http >= 1.0', 'jinja2 == 2.5']
CLASSIFIERS = ['Development Status :: 4 - Beta']
__extra__ = dict(package_data={'__setup__.ally_documentation': ['templates/*']})
