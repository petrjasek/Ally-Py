'''
Created on Mar 13, 2012

@package: internationalization
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mugur Rus

Implementation for the PO file management.
'''

from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.support.util_io import IInputStream
from babel import localedata, core
from babel.core import Locale, UnknownLocaleError
from babel.messages.catalog import Catalog
from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po, write_po
from collections import Iterable
from copy import copy
from datetime import datetime
from genericpath import isdir, isfile
from internationalization.core.spec import IPOFileManager, InvalidLocaleError
from internationalization.support.babel.util_babel import msgId, isMsgTranslated, \
    copyTranslation, fixBabelCatalogAddBug
from io import BytesIO
from os.path import dirname, join
import os
from sql_alchemy.support.util_service import SessionSupport
from internationalization.meta.database import LocalizationCollection
from sqlalchemy.sql.expression import and_
from sql_alchemy.support.util_meta import JSONEncodedDict
from json.encoder import JSONEncoder
#TODO: be carefull with encoding
from sys import getdefaultencoding
from internationalization.impl.po_file import asDict, InvalidPOFile
from json.decoder import JSONDecoder
import logging

# --------------------------------------------------------------------

# Babel FIX: We need to adjust the dir name for locales since they need to be outside the .egg file
# localedata._dirname = localedata._dirname.replace('.egg', '')
# core._filename = core._filename.replace('.egg', '')


log = logging.getLogger(__name__)
# --------------------------------------------------------------------

# TODO: add lock in order to avoid problems when a file is being updated an then read.
@injected
@setup(IPOFileManager, name='poFileManager')
class POFileManager(SessionSupport, IPOFileManager):
    '''
    Implementation for @see: IPOFileManager
    '''

    locale_dir_path = join('workspace', 'shared', 'locale'); wire.config('locale_dir_path', doc='''
    The locale repository path''')
    catalog_config = {
                      'header_comment':'''\
# Translations template for PROJECT.
# Copyright (C) YEAR ORGANIZATION
# This file is distributed under the same license as the PROJECT project.
# Gabriel Nistor <gabriel.nistor@sourcefabric.org>, YEAR.
#''',
                      'project': 'Sourcefabric',
                      'version': '1.0',
                      'copyright_holder': 'Sourcefabric o.p.s.',
                      'msgid_bugs_address': 'contact@sourcefabric.org',
                      'last_translator': 'Automatic',
                      'language_team': 'Automatic',
                      'fuzzy': False,
                      }; wire.config('catalog_config', doc='''
    The global catalog default configuration for templates.

    :param header_comment: the header comment as string, or `None` for the default header
    :param project: the project's name
    :param version: the project's version
    :param copyright_holder: the copyright holder of the catalog
    :param msgid_bugs_address: the email address or URL to submit bug reports to
    :param creation_date: the date the catalog was created
    :param revision_date: the date the catalog was revised
    :param last_translator: the name and email of the last translator
    :param language_team: the name and email of the language team
    :param charset: the encoding to use in the output
    :param fuzzy: the fuzzy bit on the catalog header
    ''')
    write_po_config = {
                       'no_location': False,
                       'omit_header': False,
                       'sort_output': True,
                       'sort_by_file': True,
                       'ignore_obsolete': True,
                       'include_previous': False,
                       }; wire.config('write_po_config', doc='''
    The configurations used when writing the PO files.

    :param width: the maximum line width for the generated output; use `None`, 0, or a negative number to
                  completely disable line wrapping
    :param no_location: do not emit a location comment for every message
    :param omit_header: do not include the ``msgid ""`` entry at the top of the output
    :param sort_output: whether to sort the messages in the output by msgid
    :param sort_by_file: whether to sort the messages in the output by their locations
    :param ignore_obsolete: whether to ignore obsolete messages and not include them in the output; by default
                            they are included as comments
    :param include_previous: include the old msgid as a comment when updating the catalog
    ''')

    def __init__(self):
        assert isinstance(self.locale_dir_path, str), 'Invalid locale directory %s' % self.locale_dir_path
        assert isinstance(self.catalog_config, dict), 'Invalid catalog configurations %s' % self.catalog_config
        assert isinstance(self.write_po_config, dict), 'Invalid write PO configurations %s' % self.write_po_config
        
#         if not os.path.exists(self.locale_dir_path): os.makedirs(self.locale_dir_path)
#         if not isdir(self.locale_dir_path) or not os.access(self.locale_dir_path, os.W_OK):
#             raise IOError('Unable to access the locale directory %s' % self.locale_dir_path)

    def getPOFileContent(self, name, locale):
        '''
        @see: IPOFileManager.getGlobalPOFileContent
        '''
        try: locale = Locale.parse(locale)
        except UnknownLocaleError: raise InvalidLocaleError(locale)
        meta = {}
        template, templateMeta = self.getPOTFileContent(name=name)
        catalog, catalogMeta = self._getData(name=name, locale=locale)
        meta['_ts'] = templateMeta['_ts'] if templateMeta['_ts'] > catalogMeta['_ts'] else catalogMeta['_ts'] 
        return catalog.update(template), meta

    def getPOTFileContent(self, name):
        '''
        @see: IPOFileManager.getGlobalPOTFileContent
        '''
        return self._getData(name=name)
        
    def updatePOFile(self, name, locale, poFile):
        '''
        @see IPOFileManager.updatePOFile
        '''
        oldCatalog = self.getPOFileContent(name, locale)
        try:
            newCatalog = read_po(poFile, locale=locale)
        except:
            raise InvalidPOFile
        content = self._toFile(newCatalog.update(oldCatalog))
        return self._storeData(name=name, locale=locale, content=content)

    def updatePOTFile(self, name, poFile):
        '''
        @see IPOFileManager.updatePOTFile
        '''
        try:
            oldCatalog = self.getPOTFileContent(name)
        except: 
            oldCatalog = Catalog()
        try:
            newCatalog = read_po(poFile)
            assert log.info('poFile {poFile}'.format(poFile=poFile)) or True
        except:
            raise InvalidPOFile
#        print(newCatalog.update(oldCatalog))
        content = self._toFile(oldCatalog.update(newCatalog))
        return self._storeData(name=name, content=content)
    
    # --------------------------------------------------------------------

    def _getData(self, name=None, locale=None):
        '''
        Provides the actual content
        '''
        name = name if name else 'global'
        locale = locale if locale else 'global'
        
        poFile, timestamp = self.session().query(LocalizationCollection.poFile, 
                                                 LocalizationCollection.timestamp).filter(and_(LocalizationCollection.Name == name, \
                                                                                               LocalizationCollection.locale == locale))
        return poFile, {'_ts': timestamp}
        
    def _storeData(self, content, name=None, locale=None):
        '''
        Stores new/updated content
        '''
        name = name if name else 'global'
        locale = locale if locale else 'global'
        
        timestamp = self._doTimestamp() 
        entry = LocalizationCollection(Name=name, locale=locale, timestamp=timestamp, poFile=content)
        if self.session().query(LocalizationCollection).filter(and_(LocalizationCollection.Name == name, \
                                                                    LocalizationCollection.locale == locale)).count():
            self.session().query(LocalizationCollection).update(entry)
        else:
            self.session().query(LocalizationCollection).add(entry)
        
    def _doTimestamp(self):
        '''
        Generates the current timestamp for the item stored in db 
        '''
        return int(datetime.now().strftime('%s'))
                                                        
    def _toFile(self, catalog):
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
