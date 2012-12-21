'''
Created on Jan 9, 2012

@package: internationalization
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the services setup for internationalization.
'''

from ..cdm.local_cdm import contentDeliveryManager
from ..plugin.registry import addService
from .db_internationalization import bindInternationalizationSession, \
    bindInternationalizationValidations, createTables
from __setup__.ally_gateway.security import scheme
from ally.api.security import SchemeRepository
from ally.container import support, ioc
from cdm.spec import ICDM
from cdm.support import ExtendPathCDM
from internationalization.api.file import IFileService
from internationalization.api.json_locale import IJSONLocaleFileService
from internationalization.api.message import IMessageService
from internationalization.api.po_file import IPOFileService
from internationalization.api.source import ISourceService
from internationalization.impl.json_locale import JSONFileService
from internationalization.impl.po_file import POFileService
from internationalization.scanner import Scanner
from sys import modules

# --------------------------------------------------------------------

SERVICES = 'internationalization.api.**.I*Service'

support.createEntitySetup('internationalization.impl.**.*')
support.createEntitySetup('internationalization.*.impl.**.*')
support.bindToEntities('internationalization.impl.**.*Alchemy', binders=bindInternationalizationSession)
support.listenToEntities(SERVICES, listeners=addService(bindInternationalizationValidations), beforeBinding=False)
support.loadAllEntities(SERVICES)
support.wireEntities(Scanner)

# --------------------------------------------------------------------

@ioc.config
def scan_localized_messages():
    '''Flag indicating that the application should be scanned for localized messages'''
    return False

# --------------------------------------------------------------------

@ioc.entity
def scanner(): return Scanner()

@ioc.entity
def cdmLocale() -> ICDM:
    '''
    The content delivery manager (CDM) for the locale files.
    '''
    return ExtendPathCDM(contentDeliveryManager(), 'cache/locale/%s')

@ioc.replace(ioc.getEntity(IPOFileService, modules[__name__]))
def poFileService() -> IPOFileService:
    srv = POFileService()
    srv.cdmLocale = cdmLocale()
    return srv

@ioc.replace(ioc.getEntity(IJSONLocaleFileService))
def jsonFileService() -> IJSONLocaleFileService:
    srv = JSONFileService()
    srv.cdmLocale = cdmLocale()
    return srv

# --------------------------------------------------------------------

@ioc.before(scheme)
def updateSchemeForInternationalization():
    s = scheme(); assert isinstance(s, SchemeRepository), 'Invalid scheme %s' % s
    
    s['Translations access'].doc('''
    Allows read only access to the translation files
    ''').addGet(IPOFileService, IJSONLocaleFileService)
    
    s['Translations modify'].doc('''
    Allows for the modification of translation files by the upload of updated PO files
    ''').addAll(IPOFileService)
    
    s['Translations messages modify'].doc('''
    Allows for the modification of translatable messages that the application uses
    ''').addAll(IFileService, ISourceService, IMessageService)

@ioc.after(createTables)
def scan():
    if scan_localized_messages():
        scanner().scanComponents()
        scanner().scanPlugins()
