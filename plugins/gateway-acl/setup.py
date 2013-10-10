
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

setup(install_requires=['gateway>=1.0', 'ally-core-http>=1.0'],
description='\nThis plugin provides the service gateways. \n',
version='1.0',
name='gateway-acl',
long_description='The ACL (access control layer) gateway plugin integrates gateways that are designed based on published REST models and services, basically makes the conversion between access allowed on a service call and a gateway REST model.',
packages=find_packages('.'),
      platforms=['all'],
      zip_safe=True,
      license='GPL v3',
      url='http://www.sourcefabric.org/en/superdesk/', # project home page
      )
