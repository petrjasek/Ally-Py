'''
Created on Jul 15, 2011

@package: GUI core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Balaceanu

Contains the GUI setup files.
'''

from ally.container import ioc

# --------------------------------------------------------------------

NAME = 'GUI core'
GROUP = 'GUI'
VERSION = '1.0'
AUTHOR = 'Mihai Balaceanu'
AUTHOR_EMAIL = 'mihai.balaceanu@sourcefabric.org'
DESCRIPTION = 'Provides the core for the GUI (Graphical User Interface)'
INSTALL_REQUIRES = ['ally_api >= 1.0', 'ally_core_plugin >= 1.0', 'support_cdm >= 1.0']

# --------------------------------------------------------------------

__extra__ = dict(include_package_data=True)

@ioc.config
def publish_gui_resources():
    '''Allow for the publish of the gui resources'''
    return True
