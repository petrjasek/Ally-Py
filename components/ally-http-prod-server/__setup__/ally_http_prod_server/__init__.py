'''
Created on Jul 15, 2011

@package: ally core http
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains setup and configuration files for the HTTP REST server.
'''

from .. import ally_api
from ..ally_core_http import server_type
from ally.container import ioc

# --------------------------------------------------------------------

NAME = 'ally HTTP production server'
GROUP = ally_api.GROUP
VERSION = '1.0'
DESCRIPTION = 'Provides the HTTP production server'

# --------------------------------------------------------------------
# The default configurations

@ioc.replace(server_type)
def server_type_production() -> str:
    '''
    The type of the server to use, the options are:
        "basic"- single threaded server, the safest but slowest server to use.
        "production"- multiprocessor support, suited for production environments.
    '''
    return 'production'
