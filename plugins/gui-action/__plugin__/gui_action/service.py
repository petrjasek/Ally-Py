'''
Created on Feb 23, 2012

@package: ally actions gui 
@copyright: 2011 Sourcefabric o.p.s.
@license:  http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Balaceanu

Provides the services setup.
'''

from ..gui_core import service
from __setup__.ally_gateway.security import scheme
from ally.api.security import SchemeRepository
from ally.container import ioc
from gui.action.api.action import IActionManagerService
from gui.action.impl.action import ActionManagerService

# --------------------------------------------------------------------

@ioc.replace(ioc.getEntity(IActionManagerService, service))
def actionManagerService() -> IActionManagerService: return ActionManagerService()

# --------------------------------------------------------------------

@ioc.before(scheme)
def updateSchemeForGUIActions():
    s = scheme(); assert isinstance(s, SchemeRepository), 'Invalid scheme %s' % s
    
    scheme()['GUI Actions'].doc('''
    Allows access to the GUI actions, basically the applications menus
    ''').addAll(IActionManagerService)
