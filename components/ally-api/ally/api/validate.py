'''
Created on Oct 29, 2013

@package: ally api
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the validation marking mechanism, this module contains classes that allow for model marking.
'''

from ally.api.operator.type import TypeProperty, TypeModel, \
    TypePropertyContainer
from ally.api.type import typeFor


# --------------------------------------------------------------------
class Validation:
    '''
    The validation basic container class.
    '''
    
    def __init__(self, prop):
        '''
        Create the validation.
        
        @param prop: TypeProperty reference
            The property to register the validation to.
        '''
        ptype = typeFor(prop)
        assert isinstance(ptype, TypeProperty), 'Invalid property %s' % prop
        assert isinstance(ptype.parent, TypeModel), 'Invalid property model %s' % ptype.parent
        
        self.property = ptype
        
    def __str__(self):
        return '%s:%s' % (self.property, self.__class__.__name__)
        
# --------------------------------------------------------------------

class Mandatory(Validation):
    '''
    Mandatory property type validation.
    '''
    
    def __init__(self, prop):
        '''
        @see: Validation
        '''
        super().__init__(prop)
        
class ReadOnly(Validation):
    '''
    Read only property type validation.
    '''
    
    def __init__(self, prop):
        '''
        @see: Validation
        '''
        super().__init__(prop)

class AutoId(Validation):
    '''
    Auto generated id property type validation.
    '''
    
    def __init__(self, prop):
        '''
        @see: Validation
        '''
        super().__init__(prop)

class MaxLen(Validation):
    '''
    String property maximum length type validation.
    '''
    
    def __init__(self, prop, length):
        '''
        @see: Validation
        
        @param length: integer
            The maximum length.
        '''
        assert isinstance(length, int), 'Invalid length %s' % length
        super().__init__(prop)
        
        self.length = length

class Relation(Validation):
    '''
    Relation property type with other models validation.
    '''
    
    def __init__(self, prop):
        '''
        @see: Validation
        '''
        assert isinstance(prop, TypePropertyContainer), 'Invalid property type %s' % prop
        super().__init__(prop)
