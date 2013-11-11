'''
Created on Mar 13, 2012

@package: internationalization
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mugur Rus

API specifications for PO file management.
'''

import abc

# --------------------------------------------------------------------

class InvalidLocaleError(Exception):
    '''
    Raise whenever there is a invalid locale provided.
    '''

# --------------------------------------------------------------------

class IPOFileManager(metaclass=abc.ABCMeta):
    '''
    The PO file manager: processes and returns the global, component or plugin
    PO files content from anywhere.
    '''

    @abc.abstractmethod
    def getPOFileContent(self, name, locale):
        '''
        Provides the messages catalog for  and the given locale.

        @param name: string
            The name of the component to return the translation. Default is global
        @param locale: string
            The locale for which to return the translation.
        @return: catalog
            The PO file catalog containing the translation.
        '''

    @abc.abstractmethod
    def getPOTFileContent(self, name):
        '''
        Provides the POT file messages catalog for the whole application
         
        @param name: string
            The name of the component to return the translation. Default is global
        '''

    @abc.abstractmethod
    def updatePOFile(self, name, locale, poFile):
        '''
        Updates the PO file of the given component with the provided locale. 
        
        @param name: string
            The name of the component. Default is global
        @param locale: string
            The locale for which to return translation
        '''
        
    @abc.abstractmethod
    def updatePOTFile(self, name, poFile):
        '''
        Updates the POT file of the given component. 
        
        @param name: string
            The name of the component. Default is global
        '''
