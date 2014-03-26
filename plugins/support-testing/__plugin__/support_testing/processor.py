'''
Created on Mar 21, 2014

@package: support testing
@copyright: 2011 Sourcefabric o.p.s.
@license http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the testing support processors.
'''

import logging

from __setup__.ally_plugin.deploy import plugins
from __setup__.ally_plugin.distribution import application_mode, APP_DEVEL, \
    APP_NORMAL
from ally.container import ioc, app, support
from ally.container._impl._call import CallEvent, CallEventControlled, WithCall
from ally.container.context import activate
from ally.container.event import Trigger
from ally.testing.container.switcher import Switcher
from ally.design.priority import PRIORITY_LAST


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

SWITCHER_TESTING = Switcher()  # The switcher used for testing.

EVENT_CLASSES = (CallEvent, CallEventControlled)
# The event call classes.

BEFORE_SWITCH = Trigger('before switch')
# Trigger used for triggering events before switching.
# --------------------------------------------------------------------

@ioc.config
def testing_allowed():
    ''' Flag indicating that the testing support should be enabled.'''
    return True

# --------------------------------------------------------------------

@ioc.entity
def creator():
    assembly = plugins()
    def create():
        try:
            for name, call in assembly.calls.items():
                if not isinstance(call, EVENT_CLASSES):
                    if isinstance(call, WithCall) and isinstance(call.call, EVENT_CLASSES):
                        call = call.call
                    continue
                call._processed = False
            
            SWITCHER_TESTING.switchToAlternate()
            with activate(assembly, 'create'):
                for call, name, ctriggers in support.eventsFor(BEFORE_SWITCH):
                    log.debug('Executing before trigger event call \'%s\'', name)
                    call()
                
                for call, name, ctriggers in support.eventsFor(app.POPULATE):
                    if app.DEVEL.isTriggered(ctriggers) and application_mode() != APP_DEVEL: continue
                    if app.NORMAL.isTriggered(ctriggers) and application_mode() != APP_NORMAL: continue
                    log.debug('Executing event call \'%s\'', name)
                    call()

        finally: SWITCHER_TESTING.switchToMain()
    return create

# --------------------------------------------------------------------

@app.deploy(priority=PRIORITY_LAST)
def createTest():
    if testing_allowed(): creator()()
