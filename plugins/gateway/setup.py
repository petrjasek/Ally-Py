
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

setup(install_requires=['support-sqlalchemy>=1.0'],
description='\nThis plugin provides the default gateway service. \n',
version='1.0',
name='gateway',
long_description='This plugin provides the Gateway API and also the means of setting up custom gateways, for instance allowing for a certain IP full access to REST models. The gateway plugin is agnostic to the actual services that are published by the REST server and any type of URLs and rules can be placed with this plugin.',
packages=find_packages('.'),
      platforms=['all'],
      zip_safe=True,
      license='GPL v3',
      url='http://www.sourcefabric.org/en/superdesk/', # project home page
      )
