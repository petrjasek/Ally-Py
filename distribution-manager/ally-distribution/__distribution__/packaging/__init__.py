'''
Created on Jul 15, 2011

@package: ally distribution
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

The distribution manager.
'''

# --------------------------------------------------------------------

NAME = 'ally-distribution'
VERSION = '1.0'
AUTHOR = 'Gabriel Nistor'
AUTHOR_EMAIL = 'gabriel.nistor@sourcefabric.org'
KEYWORDS = ['Ally', 'distribution', 'packaging']
INSTALL_REQUIRES = ['ally >= 1.0']
DESCRIPTION = 'Provides the means for packaging and publishing ally packages (components and plugins)'
LONG_DESCRIPTION = '''Contains support for packaging components and plugins.'''
CLASSIFIERS = ['Development Status :: 4 - Beta']
__extra__ = dict(py_modules=['ally_distribution'])
