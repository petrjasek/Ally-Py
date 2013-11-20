'''
Created on Nov 13, 2013
   
@package: internationalization
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Cristian Domsa
   
CDM syncronyzer for the internationlization PO files.
'''
import logging
from ally.container.ioc import injected
from internationalization.core.spec import ICDMSyncronizer
from ally.container.support import setup
from ally.cdm.spec import ICDM
from ally.container import wire
from os.path import join, isdir
import os
from babel.compat import BytesIO
from json.encoder import JSONEncoder
from babel.messages.catalog import Catalog
from babel.messages.pofile import write_po
  
# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------

FILENAME_PO = 'messages.po'
# The format of the po files.
FILENAME_POT = 'messages.pot'
# The format of the pot files.

# --------------------------------------------------------------------

@injected
@setup(ICDMSyncronizer, name='poCDMSync')
class poCDMSyncronyzer(ICDMSyncronizer):
    '''
    Implementaion for @see: ICDMSyncronizer
    '''
    cdmLocale = ICDM; wire.entity('cdmLocale')
    
    locale_dir_path = join('workspace', 'shared', 'locale'); wire.config('locale_dir_path', doc='''
    The locale repository path''')
    
    #TODO: get rid of this from here
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
    
    cdm_po_file_path = join('{name}', 'locale', '{locale}', 'LC_MESSAGES', FILENAME_PO); wire.config('cdm_po_file_path', doc='''
                                The CDM path for PO files''')
    cdm_pot_file_path = join('{name}', 'locale', FILENAME_POT); wire.config('cdm_pot_file_path', doc='''
                                The CDM path for POT files''')
    
    def __init__(self):
        assert isinstance(self.locale_dir_path, str), 'Invalid locale directory %s' % self.locale_dir_path
        if not os.path.exists(self.locale_dir_path): os.makedirs(self.locale_dir_path)
        if not isdir(self.locale_dir_path) or not os.access(self.locale_dir_path, os.W_OK):
            raise IOError('Unable to access the locale directory %s' % self.locale_dir_path)
    
    def publish(self, content, name, locale, timestamp):
        '''
        Publish content to path in CDM if content changed
        '''
        if locale:
            path = self.cdm_po_file_path.format(name=name, locale=locale)
        else:
            path = self.cdm_pot_file_path.format(name=name)
        cdmMetadata = self.cdmLocale.getMetadata(path)
        cdmTimestamp = -1 if not cdmMetadata else cdmMetadata['timestamp']
        if timestamp > cdmTimestamp:
            self.cdmLocale.publishFromFile(path, self._toPOFile(content))
            dbMetadata = {'timestamp': timestamp}
            self.cdmLocale.publishMetadata(path, dbMetadata)
        return path
          
    def asReference(self, path, protocol):
        '''
        returns reference to CDM path using scheme
        '''
        return self.cdmLocale.getURI(path, protocol)
    
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
    return { 'domain' : d }
  

