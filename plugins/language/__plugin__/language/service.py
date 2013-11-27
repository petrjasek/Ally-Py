'''
Created on Nov 22, 2013

@package: internationalization.language
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the services setup for internationalization.language.
'''

from ..plugin.registry import registerService
from .database import binders
from ally.container import bind, support
import logging

log = logging.getLogger(__name__)

# --------------------------------------------------------------------

SERVICES = 'internationalization.language.api.**.I*Service'

# --------------------------------------------------------------------

bind.bindToEntities('internationalization.language.impl.**.*Alchemy', binders=binders)
support.createEntitySetup('internationalization.language.impl.**.*')
support.listenToEntities(SERVICES, listeners=registerService, beforeBinding=False)
support.loadAllEntities(SERVICES)
