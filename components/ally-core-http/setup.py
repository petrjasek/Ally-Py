'''
Created on June 14, 2012

@package: ally core
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mugur Rus
'''

# --------------------------------------------------------------------

from setuptools import setup, find_packages

# --------------------------------------------------------------------

setup(
    name="ally_core_http",
    version="1.0",
    packages=find_packages(),
    install_requires=['ally_core >= 1.0'],
    platforms=['all'],
    test_suite='test',
    zip_safe=True,

    # metadata for upload to PyPI
    author="Gabriel Nistor",
    author_email="gabriel.nistor@sourcefabric.org",
    description="Ally framework - core HTTP component",
    long_description='The core HTTP component of the Ally framework',
    license="GPL v3",
    keywords="Ally REST framework",
    url="http://www.sourcefabric.org/en/superdesk/", # project home page
)
