'''
Created on Oct 29, 2013

@package: ally api
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the validation marking mechanism, this module contains classes that allow for model marking.
'''

import abc
from ally.api.operator.type import TypeProperty, TypeModel, TypePropertyContainer
from ally.api.type import typeFor
from ally.support.api.util_service import isCompatible
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.mapper import Mapper
from ally.internationalization import _
from ally.api.config import INSERT, UPDATE
import re

# --------------------------------------------------------------------

DEFAULT_METHODS = (INSERT, UPDATE)

class IValidation(metaclass=abc.ABCMeta):
    '''
    The validation specification.
    '''
    
    @abc.abstractmethod
    def isFor(self, target, method):
        '''
        Checks if the validation is for the provided target.
        
        @param target: object
            The target to check.
        @param method: int
            The method for which to check if the validation applies (e.g. INSERT, UPDATE)
        @return: boolean
            True if the validation is for the provided target, False otherwise.
        '''

class ValidationProperty(IValidation):
    '''
    The validation basic property target container class.
    '''
    
    def __init__(self, prop, methods=DEFAULT_METHODS):
        '''
        Create the validation.
        
        @param prop: TypeProperty reference
            The property to register the validation to.
        '''
        ptype = typeFor(prop)
        assert isinstance(ptype, TypeProperty), 'Invalid property %s' % prop
        assert isinstance(ptype.parent, TypeModel), 'Invalid property model %s' % ptype.parent
        assert isinstance(methods, tuple), 'Invalid methods list %s' % methods
        if __debug__:
            for method in methods:
                assert isinstance(method, int), 'Invalid method %s' % method
        
        self.property = ptype
        self.methods = methods
    
    def isFor(self, target, method):
        '''
        @see: IValidation.isFor
        '''
        assert isinstance(method, int), 'Invalid method %s' % method
        return method in self.methods and isCompatible(self.property, target)
    
    def __str__(self):
        return '%s:%s' % (self.property, self.__class__.__name__)

class IValidator(IValidation, metaclass=abc.ABCMeta):
    '''
    The custom validator specification.
    '''

    @abc.abstractmethod
    def validate(self, value):
        '''
        Validate the given value.
        
        @param value: object
            The value to validate.
        @return: None|tuple
            None if the value is valid, tuple of error code and message otherwise. 
        '''

# --------------------------------------------------------------------

class ValidatorRegex(IValidator, ValidationProperty):
    '''
    Implements a regular expression validator
    '''
    
    def __init__(self, prop, regex, error, flags=0, methods=DEFAULT_METHODS):
        '''
        Initialize the regular expression validator.
        '''
        assert isinstance(methods, tuple), 'Invalid methods list %s' % methods
        if __debug__:
            for method in methods:
                assert isinstance(method, int), 'Invalid method %s' % method
        
        super().__init__(prop, methods)
        
        assert isinstance(regex, str), 'Invalid regular expression %s' % regex
        assert error is not None, 'Invalid error %s' % error
        self.regex = regex
        self.error = error
        self.flags = flags
        self.cregex = re.compile(self.regex, flags)
    
    def validate(self, value):
        '''
        @see: IValidator.validate
        '''
        if value and self.cregex.match(value) is None:
            return self.error

# --------------------------------------------------------------------

class Unique(IValidation):
    '''
    Implements unique validator
    '''
    
    def __init__(self, *props, methods=DEFAULT_METHODS):
        '''
        Initialize the unique validator.
        '''
        assert len(props) > 0, 'Unique validation requires at least one property'
        assert isinstance(methods, tuple), 'Invalid methods list %s' % methods
        if __debug__:
            for method in methods:
                assert isinstance(method, int), 'Invalid method %s' % method
        
        mapper = None
        self.attributes = []
        for prop in props:
            assert isinstance(prop, InstrumentedAttribute), 'Invalid property %s' % prop
            assert isinstance(prop.parent, Mapper), 'Invalid mapper %s' % prop.parent
            if mapper is None: mapper = prop.parent
            assert mapper == prop.parent, 'All attributes must be from the same mapper'
            assert isinstance(mapper.class_._ally_type, TypeModel), 'Invalid model %s' % mapper.class_._ally_type
            self.attributes.append(prop)
        
        self.mapper = mapper
        self.model = self.mapper.class_._ally_type
        self.methods = methods
    
    def isFor(self, target, method):
        '''
        @see: IValidation.isFor
        '''
        assert isinstance(method, int), 'Invalid method %s' % method
        if method not in self.methods or not isinstance(target, TypeModel): return False
        assert isinstance(target, TypeModel), 'Invalid model %s' % target
        return issubclass(target.clazz, self.model.clazz)
    
    def __str__(self):
        return '%s:%s' % (','.join(str(prop) for prop in self.properties), self.__class__.__name__)

class Mandatory(IValidation):
    '''
    Mandatory property type validation.
    '''
    
    def __init__(self, prop, methods=DEFAULT_METHODS):
        '''
        Initialize the mandatory validator.
        '''
        ptype = typeFor(prop)
        assert isinstance(ptype, TypeProperty), 'Invalid property %s' % prop
        assert isinstance(ptype.parent, TypeModel), 'Invalid property model %s' % ptype.parent
        assert isinstance(methods, tuple), 'Invalid methods list %s' % methods
        if __debug__:
            for method in methods:
                assert isinstance(method, int), 'Invalid method %s' % method
        
        self.property = ptype
        self.model = self.property.parent
        self.methods = methods
    
    def isFor(self, target, method):
        '''
        @see: IValidation.isFor
        '''
        if method not in self.methods or not isinstance(target, TypeModel): return False
        assert isinstance(target, TypeModel), 'Invalid model %s' % target
        return issubclass(target.clazz, self.model.clazz)
    
    def __str__(self):
        return '%s:%s' % (self.property, self.__class__.__name__)

class ReadOnly(ValidationProperty):
    '''
    Read only property type validation.
    '''
    
    def __init__(self, prop, methods=DEFAULT_METHODS):
        '''
        @see: Validation
        '''
        super().__init__(prop, methods)

class AutoId(ValidationProperty):
    '''
    Auto generated id property type validation.
    '''
    
    def __init__(self, prop, methods=DEFAULT_METHODS):
        '''
        @see: Validation
        '''
        super().__init__(prop, methods)

class MinLen(ValidationProperty):
    '''
    String property minimum length type validation.
    '''
    
    def __init__(self, prop, length, methods=DEFAULT_METHODS):
        '''
        @see: Validation
        
        @param length: integer
            The minimum length.
        '''
        assert isinstance(length, int), 'Invalid length %s' % length
        super().__init__(prop, methods)
        
        self.length = length
        
class MaxLen(ValidationProperty):
    '''
    String property maximum length type validation.
    '''
    
    def __init__(self, prop, length, methods=DEFAULT_METHODS):
        '''
        @see: Validation
        
        @param length: integer
            The maximum length.
        '''
        assert isinstance(length, int), 'Invalid length %s' % length
        super().__init__(prop, methods)
        
        self.length = length

class Relation(ValidationProperty):
    '''
    Relation property type with other models validation.
    '''
    
    def __init__(self, prop, methods=DEFAULT_METHODS):
        '''
        @see: Validation
        '''
        assert isinstance(prop, TypePropertyContainer), 'Invalid property type %s' % prop
        super().__init__(prop, methods)

class EMail(ValidatorRegex):
    '''
    Email format validation
    '''
    regex = "^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@" \
            "(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,4}[a-z0-9]){1}$"
    error = ('format', _('Invalid EMail'))
    
    def __init__(self, prop, methods=DEFAULT_METHODS):
        super().__init__(prop, self.regex, self.error, re.I, methods=methods)

class PhoneNumber(ValidatorRegex):
    '''
    Phone number format validation
    '''
    regex = "^(?:(?:0?[1-9][0-9]{8})|(?:(?:\+|00)[1-9][0-9]{9,11}))$"
    error = ('format', _('Invalid phone number format'),
             {'example':_('+123123456789 or 0123456789 or 123456789')})
    
    def __init__(self, prop, methods=DEFAULT_METHODS):
        super().__init__(prop, self.regex, self.error, methods=methods)

class UserName(ValidatorRegex):
    '''
    User name format validation
    '''
    regex = "^[a-z0-9._'-]+$"
    error = ('user name', _('Invalid user name format'),
             {'example':_('The user name must contain only letters, digits and characters ".", "_", "\'", "-"')})
    
    def __init__(self, prop, methods=DEFAULT_METHODS):
        super().__init__(prop, self.regex, self.error, re.I, methods=methods)

# --------------------------------------------------------------------

def validate(validation, *validations):
    '''
    Decorator used for binding validations or validation targets on support objects.
    The purpose of this is just to say that for a certain class, attribute or even object there are some validations
    that are required.
    Even though the validations are binded there needs to be other mechanism that manages the validations, so even
    if the validation can be binded anyware it doesn't mean necessarily that is used.
    
    @param validation: object
        The validation or validation target to be binded by the decorator.
    @param validations: argument[object]
        Additional validations to be binded.
    '''
    assert validation is not None, 'None is not a validation'
    if __debug__:
        for valid in validations: assert valid is not None, 'None is not a validation'
    def decorator(target):
        try: current = target._ally_validations
        except AttributeError: current = target._ally_validations = []
        current.append(validation)
        current.extend(validations)
        return target
    return decorator

def validationsFor(obj):
    '''
    Provides the validations binded to the provided object.
    @see: validate
    
    @param obj: object
        The object to extract the validations from.
    @return: list[object, target]
        A list that provides on the first position the binded validation target and on the second
        the binded target
    '''
    assert obj is not None, 'None is not a validation target'
    
    validations = []
    try:
        for validation in obj._ally_validations:  validations.append((validation, obj))
    except AttributeError: pass
    return validations
