
'''
Created on Oct 1, 2013
 
@package: distribution_manager
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Cristian Domsa
 
Setup configuration for components/plugins needed for pypi.
'''

# --------------------------------------------------------------------

from setuptools import setup, find_packages

# --------------------------------------------------------------------

setup(install_requires=['ally-api >= 1.0', 'ally-core >= 1.0'],
description='The plugin that provides the indexing support.',
version='1.0',
name='indexing',
long_description='This plugin offers the Indexing API and the implementation provides details related to \n                    the REST models content response indexing based on data associate with ally-core.',
packages=find_packages('.'),
      platforms=['all'],
      zip_safe=True,
      license='GPL v3',
      url='http://www.sourcefabric.org/en/superdesk/', # project home page
      )
