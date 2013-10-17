
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

setup(description='Provides the core for the GUI (Graphical User Interface)',
author='Mihai Balaceanu',
install_requires=['ally_api >= 1.0', 'ally_core_plugin >= 1.0', 'support_cdm >= 1.0'],
include_package_data=True,
author_email='mihai.balaceanu@sourcefabric.org',
version='1.0',
name='gui-core',
packages=find_packages('.'),
      platforms=['all'],
      zip_safe=True,
      license='GPL v3',
      url='http://www.sourcefabric.org/en/superdesk/', # project home page
      )
