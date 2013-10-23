
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

setup(name='administration',
author='Gabriel Nistor',
install_requires=['ally-http >= 1.0'],
author_email='gabriel.nistor@sourcefabric.org',
version='1.0',
keywords=['Ally', 'REST', 'administration'],
description='Provides the administration services that interact with the application code',
packages=find_packages('.'),
      platforms=['all'],
      zip_safe=True,
      license='GPL v3',
      url='http://www.sourcefabric.org/en/superdesk/', # project home page
      )
