'''
Created on Mar 9, 2012

@package: internationalization
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mugur Rus

Implementation for the PO file management.
'''

from ally.api.model import Content
from ally.cdm.spec import ICDM, PathNotFound
from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.core.error import DevelError
from ally.api.error import InputError
from ally.internationalization import _, C_
from datetime import datetime
from internationalization.api.po_file import IInternationlizationFileService
from internationalization.core.spec import IPOFileManager, InvalidLocaleError
from babel.messages.catalog import Catalog
import codecs
import logging
import sys

FORMAT_PO = '{filename}.po'
# The format of the po files.
FORMAT_MO = '{filename}.mo'
# The format of the mo files.
FORMAT_POT = '{filename}.pot'
# The format of the pot files.

# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------
@injected
@setup(IInternationlizationFileService, name='poFileService')
class POFileService(IInternationlizationFileService):
    '''
    Implementation for @see: IInternationlizationFileService
    '''

    default_charset = 'UTF-8'; wire.config('default_charset', doc='''
    The default character set to use whenever a PO file is uploaded and the character
    set of the content is not specified''')

    poFileManager = IPOFileManager; wire.entity('poFileManager')
    cdmLocale = ICDM; wire.entity('cdmLocale')

    def __init__(self):
        assert isinstance(self.default_charset, str), 'Invalid default charset %s' % self.default_charset
        assert isinstance(self.poFileManager, IPOFileManager), 'Invalid PO file manager %s' % self.poFileManager
        assert isinstance(self.cdmLocale, ICDM), 'Invalid PO CDM %s' % self.cdmLocale

    def getPOFile(self, locale, scheme, name=None):
        '''
        @see: IInternationlizationFileService.getGlobalPOFile
        '''
        path = self._cdmPath(name=name, locale=locale, format=FORMAT_PO)
        oldMetadata = self.cdmLocale.getMetadata(path)
        try:
            content, newMetadata = self.poFileManager.getPOFileContent(name=name, locale=locale)
            if newMeta['_ts'] > oldMeta['_ts']:
                self.cdmLocale.publishFromFile(path, content)
                self.cdmLocale.publishMetadata(path, newMetadata)
        except InvalidLocaleError: raise InputError(_('Invalid locale %(locale)s') % dict(locale=locale))
        return self.cdmLocale.getURI(path, scheme)

    def getPOTFile(self, scheme, name=None):
        '''
        @see: IInternationlizationFileService.getGlobalPOTFile
        '''
        path = self._cdmPath(name=name, format=FORMAT_POT)
        oldMetadata = self.cdmLocale.getMetadata(path)
        try:
            content, newMetadata = self.poFileManager.getPOTFileContent(name=name)
            if newMeta['_ts'] > oldMeta['_ts']:
                self.cdmLocale.publishFromFile(path, content)
                self.cdmLocale.publishMetadata(path, newMetadata)
        except InvalidLocaleError: raise InputError(_('Invalid locale %(locale)s') % dict(locale=locale))
        return self.cdmLocale.getURI(path, scheme)

    # ----------------------------------------------------------------

    def updatePOFile(self, locale, poFile, name=None):
        '''
        @see: IInternationlizationFileService.updateGlobalPOFile
        '''
        assert isinstance(poFile, Content), 'Invalid PO content %s' % poFile
        # Convert the byte file to text file
        poFile = codecs.getreader(poFile.charSet or self.default_charset)(poFile)
        try: self.poFileManager.updatePOFile(name=name, locale=locale, poFile=poFile)
        except UnicodeDecodeError: raise InvalidPOFile(poFile)
        if poFile.next(): raise ToManyFiles()
        return True

        
    def updatePOTFile(self, name, poFile):
        '''
        @see: IInternationlizationFileService.updateComponentPOTFile
        '''
        assert isinstance(poFile, Content), 'Invalid PO content %s' % poFile
        # Convert the byte file to text file
#         poFile = codecs.getreader(poFile.charSet or self.default_charset)(poFile)
        print(poFile)
#         sys.exit()
        try: self.poFileManager.updatePOTFile(name=name, poFile=poFile)
        except UnicodeDecodeError: raise InvalidPOFile(poFile)
        if poFile.next(): raise ToManyFiles()
        return True

    # ----------------------------------------------------------------
    def _cdmPath(self, name, format, locale=None):
        '''
        Returns the path to the CDM file corresponding to the given locale and / or
        component / plugin. If no component of plugin was specified it returns the
        name of the global file.
        
        @param locale: string
            The locale.
        @param component: string
            The component id.
        @param plugin: string
            The plugin id.
        @return: string
            The file path.
        '''
        path = []
        name = name if name else 'global'
        path.append(name)
        if locale: path.append(locale)
        return format.format(filename='-'.join(path))
    
    def _toPOFile(self, catalog):
        '''
        Convert the catalog to a PO file like object.
    
        @param catalog: Catalog
            The catalog to convert to a file.
        @return: file read object
            A file like object to read the PO file from.
        '''
        assert isinstance(catalog, Catalog), 'Invalid catalog %s' % catalog
    
        fileObj = BytesIO()
        write_po(fileObj, catalog, **self.write_po_config)
        fileObj.seek(0)
        return fileObj
# --------------------------------------------------------------------

def asDict(self, catalog):
    '''
    Convert the catalog to a dictionary.
    Format description: @see IPOFileManager.getGlobalAsDict

    @param catalog: Catalog
        The catalog to convert to a dictionary.
    @return: dict
        The dictionary in the format specified above.
    '''
    assert isinstance(catalog, Catalog), 'Invalid catalog %s' % catalog

    d = { }
    d[''] = { 'lang' : catalog.locale.language, 'plural-forms' : catalog.plural_forms }
    for msg in catalog:
        if not msg or msg.id == '': continue
        if isinstance(msg.id, (list, tuple)):
            key, key_plural = msg.id
            singular, plural = msg.string[0], msg.string[1]
        else:
            key, key_plural = msg.id, ''
            singular, plural = msg.string, ''
        singular = singular if singular is not None else ''
        plural = plural if plural is not None else ''
        key = key if not msg.context else "%s:%s" % (msg.context, key)
        d[key] = [ key_plural, singular, plural ]
    return { domain : d }



# Raised when there is an invalid PO content
InvalidPOFile = lambda poFile:InputError(_('Invalid content for PO file %(file)s') % dict(file=poFile.getName() or
                                                                                    C_('Unknown file name', 'unknown')))

# Raised if there are to many files provided in content.
ToManyFiles = lambda :DevelError('To many PO files, only one accepted')
