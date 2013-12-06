'''
Created on Mar 9, 2012

@package: internationalization
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mugur Rus

Implementation for the PO file management.
'''

from ally.api.model import Content
from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.core.error import DevelError
from ally.api.error import InputError, IdError
from ally.internationalization import _, C_
from internationalization.api.po_file import IInternationlizationFileService
from internationalization.core.spec import ICatalogManager, InvalidLocaleError,\
    ICDMSyncronizer
from babel.core import Locale, UnknownLocaleError
import logging

# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------
@injected
@setup(IInternationlizationFileService, name='poFileService')
class POFileService(IInternationlizationFileService):
    '''
    Implementation for @see: IInternationlizationFileService
    '''

    poFileManager = ICatalogManager; wire.entity('poFileManager')
    cdmSync = ICDMSyncronizer; wire.entity('cdmSync')

    def __init__(self):
        assert isinstance(self.poFileManager, ICatalogManager), 'Invalid PO file manager %s' % self.poFileManager
        assert isinstance(self.cdmSync, ICDMSyncronizer), 'Invalid CDM syncronizer %s' % self.cdmSync
        
    def getPOFile(self, locale, scheme, name=None):
        '''
        @see: IInternationlizationFileService.getPOFile
        '''
        try: Locale.parse(locale)
        except UnknownLocaleError: raise InvalidLocaleError(locale)
        if not name:
            name = self.poFileManager.global_messages_name
            timestamp = self.poFileManager.getLatestTimestampForPO(name, locale)
            path, isNeeded = self.cdmSync.publishNeeded(name, locale, timestamp)
            if isNeeded:
                result = self.poFileManager.getGlobalPOCatalog(locale, scheme)
                if not result: raise IdError('No global PO file available. Upload one before trying to get one!')
        else:
            timestamp = self.poFileManager.getLatestTimestampForPO(name, locale)
            path, isNeeded = self.cdmSync.publishNeeded(name, locale, timestamp)
            if isNeeded:
                result = self.poFileManager.getPluginPOCatalog(name, locale)
                if not result:
                    raise IdError('No PO file available for name: {0}, locale: {1}. Upload one before trying to get one!'.format(name, locale))
        metadata = {'timestamp': timestamp}
        if isNeeded: 
            if result: self.cdmSync.publish(result, path, metadata)
        
        return self.cdmSync.asReference(path, scheme)

    def getPOTFile(self, scheme, name=None):
        '''
        @see: IInternationlizationFileService.getPOTFile
        '''
        if not name:
            name = self.poFileManager.global_messages_name
            timestamp = self.poFileManager.getLatestTimestampForPOT(name)
            path, isNeeded = self.cdmSync.publishNeeded(name, None, timestamp)
            if isNeeded: 
                result = self.poFileManager.getGlobalPOTCatalog()
                if not result: raise IdError('No POT file available for application. Debug!')
        else:
            timestamp = self.poFileManager.getLatestTimestampForPOT(name)
            path, isNeeded = self.cdmSync.publishNeeded(name, None, timestamp)
            if isNeeded:
                result = self.poFileManager.getPluginPOTCatalog(name) 
                if not result: raise IdError('No POT file available for plugin {name}. Upload one before trying to get one!'.format(name=name))
        metadata = {'timestamp': timestamp}
        
        if isNeeded: 
            self.cdmSync.publish(result, path, metadata)
            
        return self.cdmSync.asReference(path, scheme)

    def updatePOFile(self, locale, poFile, name=None):
        '''
        @see: IInternationlizationFileService.updatePOFile
        '''
        try: Locale.parse(locale)
        except UnknownLocaleError: raise InvalidLocaleError(locale)
        assert isinstance(poFile, Content), 'Invalid PO content %s' % poFile
        if name:
            try:
                result = self.poFileManager.updatePluginPO(name=name, locale=locale, poFile=poFile)
            except UnicodeDecodeError: raise InvalidPOFile(poFile)
        else:
            try:
                result = self.poFileManager.updateGlobalPO(locale=locale, poFile=poFile)
            except UnicodeDecodeError: raise InvalidPOFile(poFile)
        if poFile.next(): raise ToManyFiles()
        return result

        
    def updatePOTFile(self, name, poFile):
        '''
        @see: IInternationlizationFileService.updatePOTFile
        '''
        assert isinstance(poFile, Content), 'Invalid PO content %s' % poFile
        try: result = self.poFileManager.updatePluginPOT(name=name, poFile=poFile)
        except UnicodeDecodeError: raise InvalidPOFile(poFile)
        if poFile.next(): raise ToManyFiles()
        return name

    # ----------------------------------------------------------------
    
# Raised when there is an invalid PO content
InvalidPOFile = lambda poFile:InputError(_('Invalid content for PO file %(file)s') % dict(file=poFile.getName() or
                                                                                    C_('Unknown file name', 'unknown')))

# Raised if there are to many files provided in content.
ToManyFiles = lambda :DevelError('To many PO files, only one accepted')
