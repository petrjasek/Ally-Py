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
from babel.messages.catalog import Catalog
from babel.messages.pofile import read_po, write_po
from datetime import datetime
from internationalization.core.spec import IPOFileManager
from io import BytesIO
from sql_alchemy.support.util_service import SessionSupport
from internationalization.meta.db_mapping import POMapped, POTMapped
from sqlalchemy.sql.expression import and_
import logging
import codecs
from sqlalchemy.orm.exc import NoResultFound
from ally.cdm.spec import ICDM
from os.path import isdir, join
import os
from ally.api.model import Content

# --------------------------------------------------------------------

log = logging.getLogger(__name__)
# --------------------------------------------------------------------

FILENAME_PO = 'messages.po'
# The format of the po files.
FILENAME_POT = 'messages.pot'
# The format of the pot files.

@injected
@setup(IPOFileManager, name='poFileManager')
class POFileManager(SessionSupport, IPOFileManager):
    '''
    Implementation for @see: IPOFileManager
    '''
    cdmLocale = ICDM; wire.entity('cdmLocale')
    locale_dir_path = join('workspace', 'shared', 'locale'); wire.config('locale_dir_path', doc='''
    The locale repository path''')
    
    cdmPOFilePath = join('{name}', 'locale', '{locale}', 'LC_MESSAGES', FILENAME_PO)
    cdmPOTFilePath = join('{name}', 'locale', FILENAME_POT) 
    
    default_charset = 'UTF-8'; wire.config('default_charset', doc='''
    The default character set to use whenever a PO file is uploaded and the character
    set of the content is not specified''')
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
        assert isinstance(self.default_charset, str), 'Invalid default charset %s' % self.default_charset
        assert isinstance(self.write_po_config, dict), 'Invalid write PO configurations %s' % self.write_po_config
        assert isinstance(self.cdmLocale, ICDM), 'Invalid PO CDM %s' % self.cdmLocale

        assert isinstance(self.locale_dir_path, str), 'Invalid locale directory %s' % self.locale_dir_path
        if not os.path.exists(self.locale_dir_path): os.makedirs(self.locale_dir_path)
        if not isdir(self.locale_dir_path) or not os.access(self.locale_dir_path, os.W_OK):
            raise IOError('Unable to access the locale directory %s' % self.locale_dir_path)
        
    def getGlobalPOCatalog(self, locale):
        '''
        @see: IPOFileManager.getGlobalPOFileReference
        '''
        name = 'application'
        
        try:
            content = self._getData(name=name, locale=locale)
            catalog = self._getCatalog(content)
            template = self.getGlobalPOTCatalog()
            if template: catalog.update(template)
            else: assert log.debug('Global POT file could not be generated. Check if you have any POTs in db') or True
            return catalog
        except:
            return

    def getPluginPOCatalog(self, name, locale):
        '''
        @see: IPOFileManager.getPluginPOCatalog
        '''
        try:
            content = self._getData(name=name, locale=locale)
            catalog = self._getCatalog(content)
            template = self._getData(name=name)
            if template: catalog.update(template)
            else: assert log.debug('No POT file found for plugin {name}. Delivering not updated PO'.format(name=name)) or True
            return catalog
        except:
            return

    def getGlobalPOTCatalog(self, name):
        '''
        @see: IPOFileManager.getGlobalPOTCatalog
        '''
        try:
            pots = self.session().query(POTMapped.Name).all()
        except NoResultFound: return
        template = Catalog()
        for name in pots:
            template.update(self._getCatalog(self._getData(name)))
        return template
    
    def getPluginPOTCatalog(self, name):
        '''
        @see: IPOFileManager.getPluginPOTCatalog
        '''
        try:
            content = self._getData(name)
            catalog = self._getCatalog(content)
            return catalog
        except:
            return
    
    def updateGlobalPO(self, locale, poFile):
        '''
        @see IPOFileManager.updateGlobalPO
        '''
        name = 'application'
        poFile = codecs.getreader(poFile.charSet or self.default_charset)(poFile)
        newCatalog = self._getCatalog(poFile, encoding=poFile.charSet)
        if newCatalog == None: raise UnicodeDecodeError
        oldCatalog = self._getCatalog(self._getData(name=name, locale=locale))
        if oldCatalog:
            catalog = oldCatalog.update(newCatalog)
        else:
            catalog = newCatalog
        content = self._toFile(catalog)
        return self._storeData(name=name, locale=locale, content=content.getvalue())
    
    def updatePluginPO(self, name, locale, poFile):
        '''
        @see IPOFileManager.updatePluginPO
        '''
        poFile = codecs.getreader(poFile.charSet or self.default_charset)(poFile)
        newCatalog = self._getCatalog(poFile, encoding=poFile.charSet)
        if newCatalog == None: raise UnicodeDecodeError
        oldCatalog = self.getPluginPOCatalog(name=name, locale=locale)
        if oldCatalog:
            catalog = oldCatalog.update(newCatalog)
        else:
            catalog = newCatalog
        content = self._toFile(catalog)
        return self._storeData(name=name, locale=locale, content=content.getvalue())

    def updatePluginPOT(self, name, poFile):
        '''
        @see IPOFileManager.updatePluginPOT
        '''
        poFile = codecs.getreader(poFile.charSet or self.default_charset)(poFile)
        newTemplate = self._getCatalog(poFile, encoding=poFile.charSet)
        if newTemplate == None: raise UnicodeDecodeError
        #TODO: check if manual POT generation is permited
        oldTemplate = self.getPluginPOTCatalog(name=name)
        if oldTemplate:
            catalog = oldTemplate.update(newTemplate)
        else:
            catalog = newTemplate
        content = self._toFile(catalog)
        return self._storeData(name=name, content=content.getvalue())
            
    # --------------------------------------------------------------------
    def _getCatalog(self, content, encoding='utf-8'):
        '''
        Validate content and return PO messages catalog from it.
        '''
        try:
            catalog = read_po(BytesIO(content))
            return catalog
        except:
            try:
                catalog = read_po(content, encoding)
                return catalog
            except:
                assert log.debug('db content not a PO file!') or True
                return
    
    def _getData(self, name=None, locale=None):
        '''
        Provides the actual content and False if no matching content is in db
        '''
        if not locale:
            sql = self.session().query(POTMapped)
            sql = sql.filter(POTMapped.Name == name)
        else:
            sql = self.session().query(POMapped)
            sql = sql.filter(and_(POMapped.Name == name, POMapped.Locale == locale))
        
        try: 
            result = sql.first()
            return result.file
        except NoResultFound:
            assert log.debug('No result found for name \'%s\' and locale \'%s\'', name, locale) or True   
        
    def _storeData(self, content, name=None, locale=None):
        '''
        Stores new/updated content
        '''
        timestamp = self._doTimestamp()
        if not locale:
            sql = self.session().query(POTMapped)
            sql = sql.filter(POTMapped.Name == name)
        else:
            sql = self.session().query(POMapped)
            sql = sql.filter(and_(POMapped.Name == name, POMapped.Locale == locale))
         
        try:
            item = sql.first()
            item.timestamp = timestamp
            item.file = content
            return self.session().add(item)
        except:
            item = POMapped(Name=name, Locale=locale, timestamp=timestamp, file=content) if locale \
                   else POTMapped(Name=name, timestamp=timestamp, file=content) 
            assert log.debug('Entry does not exist. Adding new entry') or True
            return self.session().add(item)
        

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
