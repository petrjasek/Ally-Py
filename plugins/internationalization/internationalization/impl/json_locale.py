'''
Created on Mar 9, 2012

@package: internationalization
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mugur Rus

Implementation for the PO file management.
'''

from ally.cdm.spec import ICDM, PathNotFound
from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.api.error import InputError
from ally.internationalization import _
from datetime import datetime
from internationalization.api.json_locale import IJSONLocaleFileService
from internationalization.core.spec import IPOFileManager, InvalidLocaleError
from .po_file import asDict
from io import BytesIO
from json.encoder import JSONEncoder
from sys import getdefaultencoding

# --------------------------------------------------------------------

@injected
@setup(IJSONLocaleFileService, name='jsonFileService')
class JSONFileService(IJSONLocaleFileService):
    '''
    Implementation for @see: IJSONLocaleFileService
    '''

    default_charset = 'UTF-8'; wire.config('default_charset', doc='''
    The default character set to use whenever a JSON locale file is uploaded and
    the character set of the content is not specified''')

    poFileManager = IPOFileManager; wire.entity('poFileManager')
    cdmLocale = ICDM; wire.entity('cdmLocale')

    def __init__(self):
        assert isinstance(self.default_charset, str), 'Invalid default charset %s' % self.default_charset
        assert isinstance(self.poFileManager, IPOFileManager), 'Invalid PO file manager %s' % self.poFileManager
        assert isinstance(self.cdmLocale, ICDM), 'Invalid PO CDM %s' % self.cdmLocale

    def getGlobalJSONFile(self, locale, scheme):
        '''
        @see: IPOService.getGlobalPOFile
        '''
        path = self._cdmPath(locale)
        try:
            catalog = asDict(self.poFileManager.getPOFileContent(name='global', locale=locale))
            jsonString = JSONEncoder(ensure_ascii=False).encode(catalog)
            self.cdmLocale.publishContent(path, BytesIO(bytes(jsonString, getdefaultencoding())))
        except InvalidLocaleError: raise InputError(_('Invalid locale %(locale)s') % dict(locale=locale))
        return self.cdmLocale.getURI(path, scheme)

    def getComponentJSONFile(self, name, locale, scheme):
        '''
        @see: IPOService.getComponentPOFile
        '''
        path = self._cdmPath(locale, name=name)
        try:
            catalog = asDict(self.poFileManager.getPOFileContent(name=name, locale=locale))
            jsonString = JSONEncoder(ensure_ascii=False).encode(catalog)
            self.cdmLocale.publishContent(path, BytesIO(bytes(jsonString, getdefaultencoding())))
        except InvalidLocaleError: raise InputError(_('Invalid locale %(locale)s') % dict(locale=locale))
        return self.cdmLocale.getURI(path, scheme)



    def _cdmPath(self, locale, name='global'):
        '''
        Returns the path to the CDM JSON file corresponding to the given locale and / or
        component / plugin. If no component of plugin was specified it returns the
        name of the global JSON file.

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
        path.append(component)
        if locale: path.append(locale)
        return '%s.json' % '-'.join(path)
