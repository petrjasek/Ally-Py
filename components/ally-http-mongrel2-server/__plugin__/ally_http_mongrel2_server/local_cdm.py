'''
Created on Nov 23, 2011

@package: ally core http
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the Mongrel2 web server plugins settings.
'''

from ally.container import ioc, support
from __setup__.ally_core_http import server_type

# --------------------------------------------------------------------

try: from ..cdm.local_cdm import use_linked_cdm
except ImportError: pass  # No CDM to setup.
else:
    ioc.doc(use_linked_cdm, '''
    !!!Attention, if the mongrel2 server is selected this option will always be "false"
    ''')
    
    @ioc.before(use_linked_cdm, auto=False)
    def use_linked_cdm_force():
        if server_type() == 'mongrel2': support.force(use_linked_cdm, False)

# --------------------------------------------------------------------
