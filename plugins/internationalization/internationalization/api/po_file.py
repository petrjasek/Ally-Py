'''
Created on Mar 9, 2012

@package: internationalization
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mugur Rus

API specifications for PO file management.
'''

from ally.api.config import service, call, model
from ally.api.model import Content
from ally.api.type import Scheme, Reference
from internationalization.api.domain import modelLocalization
from internationalization.language.api.language import Language

# --------------------------------------------------------------------
@modelLocalization(id='Name')
class PO:
    '''
    Model for a PO file.
    '''
    Name = str
    Reference = Reference
    
# --------------------------------------------------------------------

@service
class IInternationlizationFileService:
    '''
    The PO/POT file management service.
    '''
    @call
    def getPOFile(self, locale:Language.Code, scheme:Scheme, name:PO.Name=None) -> PO.Reference:
        '''
        Provides the PO file for the whole application and the given locale.

        @param locale: string
            The locale for which to return the translation.
        @return: Content
            The content of the PO file.
        '''

    @call
    def updatePOFile(self, locale:Language.Code, content:Content, name:PO.Name=None) -> bool:
        '''
        Update a PO file for specified locale or upload new locale if doesn't exist
        
        @param PO: PO object
            The PO object that need to be updated/uploaded
        '''
                
    # ----------------------------------------------------------------
    
    @call(webName='Template')
    def getPOTFile(self, scheme:Scheme, name:PO.Name=None) -> PO.Reference:
        '''
        Provides the POT file for the whole application and the given locale.

        @return: Content
            The content of the PO file.
        '''
    
    @call(webName='Template')
    def updatePOTFile(self, name:PO.Name, content: Content) -> bool:
        '''
        Update a POT file or upload if doesn't exist
        
        @param potFile: POT object
            The POT object that needs to be updated/uploaded
        '''