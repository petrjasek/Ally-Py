
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

setup(install_requires=['ally-api>=1.0'],
description='Provides the support for SQL alchemy',
version='1.0',
name='support-sqlalchemy',
long_description='The [SQLAlchemy] support plugin that facilitates the work with SQL Alchemy object relational mapping. Contains support for mapping REST models with SQL Alchemy, also support for transaction handling at a request scope level. Has a central database application configuration but also the means of setting a different or multiple databases.',
packages=find_packages('.'),
      platforms=['all'],
      zip_safe=True,
      license='GPL v3',
      url='http://www.sourcefabric.org/en/superdesk/', # project home page
      )
