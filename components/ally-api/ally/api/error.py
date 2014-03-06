'''
Created on Aug 2, 2013

@package: ally api
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the exceptions that are used in communicating issues in the API.
'''

from ..internationalization import _
from .type import typeFor, Type
from itertools import chain

# --------------------------------------------------------------------

class InputError(Exception):
    '''
    Exception to be raised when the input is invalid.
    '''

    def __init__(self, *items, errCode=None, **data):
        '''
        Initializes the exception based on the items(s).
        
        ex:
            raise InputError('No idea what is wrong %(reason)s')
            # The message is not associated with any type.
            
            raise InputError('Something wrong with the id', Entity.Id) # The message is associated with the entity id.
            
            raise InputError('Something wrong with the id', Entity.Id, )
            # The first message is associated with the entity id, and the following two with the entity name.
        
        @param items: parameters
            List of parameters: the first
            The mandatory message to be associated with the error, optionally with place holders which have the value provided
            in the data
        @param refType: Type
            The type to which the error refers.
        @param errCode: string
            The code identifying this error.
        @param data: key arguments
            Data that will be used in the messages place holders.
        '''
        self.message = None
        self.type = None
        for item in items:
            if isinstance(item, str):
                if not self.message: self.message = item
            elif not self.type:
                typ = typeFor(item)
                if typ is not None:
                    assert isinstance(typ, Type), 'Invalid type %s' % typ
                    self.type = typ
        self.errCode = errCode
        self.data = data
        
        super().__init__()
    
    def __str__(self):
        '''
        @see: Exception.__str__
        '''
        header = []
        if self.type: header.append(str(self.type))
        if self.errCode: header.append(str(self.errCode))
        message = [':'.join(header)]
        message.append('\t%s' % self.message)
        return '\n'.join(message)

# --------------------------------------------------------------------

class IdError(InputError):
    '''
    Exception to be raised when a model id is invalid.
    '''
    
    def __init__(self, *items, **data):
        '''
        Initializes the invalid id exception based on the items(s).
        @see: InputError.__init__
        '''
        for item in items:
            if isinstance(item, str): break
        else:
            items = tuple(chain((_('Unknown value'),), items))
        super().__init__(*items, **data)
