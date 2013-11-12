'''
Created on Oct 30, 2013
 
@package: distribution manager
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Cristian Domsa
 
Collection of templates used in distribution manager.
'''

SETUP_TEMPLATE_BEGIN = '''
\'\'\'
Created on Oct 1, 2013
 
@package: distribution_manager
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Cristian Domsa
 
Auto-generated setup configuration for components/plugins needed for pypi.
\'\'\'

# --------------------------------------------------------------------

from setuptools import setup, find_packages

# --------------------------------------------------------------------

setup(packages=find_packages('.'),
      platforms=['all'],
      zip_safe=True,
      license='GPL v3',
      url='http://www.sourcefabric.org/en/superdesk/', # project home page
      '''

SETUP_TEMPLATE_END = '''
     )'''

SETUP_CFG_TEMPLATE = '''
[bdist_egg]
dist_dir = {0}

[rotate]
match = .egg
keep = 1
'''

BABEL_CFG_OPTIONS = {'babel.cfg' : 
                    {'python: **.py'         : '', 
                     'javascript: **.js'     : '', 
                     'extractors'            : 
                        {'extract_html': 'internationalization.core.impl.extract_html:extract_html'},
                     'extract_html: **.dust' : '',
                     'extract_html: **.html' : ''
                     }}

SETUP_CFG_UI_OPTIONS = {'setup.cfg' :
                        {'extract_messages' : {'output_file'  : 'messages.pot',
                                              'mapping_file' : 'babel.cfg',
                                              'add_comments' : 'NOTE',
                                              'keywords'     : 'gettext _ ngettext pgettext C_ npgettext N_ NC_',
                                              'input_dirs'   : './'
                                              },
                        'init_catalog'     : {'input_file'   : 'messages.pot',
                                              'output_dir'   : 'foo/bar',
                                              'output_file'  : 'mmm.po',
                                              'locale'       : 'en',
                                              'input_dirs'   : './'
                                              }
                        }}

SETUP_UI_TEMPLATE = '''
\'\'\'
Created on Nov 4, 2013
 
@package: distribution_manager
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Cristian Domsa
 
Auto-generated setup configuration for ui plugins needed for pypi.
\'\'\'

# --------------------------------------------------------------------

from setuptools import setup, find_packages

# --------------------------------------------------------------------

setup(
      install_requires=[], 
      description='Core UI plugin',
      version='1.0',
      name='{packageName}',
      long_description='Long Core UI description',
      platforms=['all'],
      zip_safe=True,
      license='GPL v3',
      url='http://www.sourcefabric.org/en/superdesk/', # project home page
      entry_points = \"\"\"
      [babel.extractors]
        extract_html = internationalization.core.impl.extract_html:extract_html
        \"\"\"
    )
'''