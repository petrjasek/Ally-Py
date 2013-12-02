'''
Created on Nov 1, 2013

@package: support mongoengine
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the mongo engine validation based on meta mappings.
'''

from inspect import isclass
import logging
from mongoengine.base.fields import BaseField
from mongoengine.document import Document
from mongoengine.fields import StringField

from ally.api.operator.type import TypeModel, TypePropertyContainer
from ally.api.type import typeFor
from ally.api.validate import IValidation, Mandatory, MaxLen, MinLen, Relation, \
    validationsFor
from ally.design.processor.attribute import requires
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
from ally.support.util_sys import getAttrAndClass


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Register(Context):
    '''
    The register context.
    '''
    # ---------------------------------------------------------------- Required
    validations = requires(dict)
    
# --------------------------------------------------------------------

class MappedValidationHandler(HandlerProcessor):
    '''
    Implementation for a processor that provides the mongo engine validation based on meta mappings.
    '''

    def process(self, chain, register:Register, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Register the vlaidations based on the meta data definitions.
        '''
        assert isinstance(register, Register), 'Invalid register %s' % register
        if not register.validations: return
        
        for validations in register.validations.values():
            assert isinstance(validations, list), 'Invalid validations %s' % validations
            
            k, mvalidations = 0, []
            while k < len(validations):
                validation, _target = validations[k]
                k += 1
                if isclass(validation) and issubclass(validation, Document):
                    mvalidations.extend(self.validations(validation))
                    k -= 1
                    del validations[k]
                    continue
            validations.extend(mvalidations)

    def validations(self, mapped):
        '''
        Provides the mapped class validations that can be performed based on the mongo engine mapping.
        
        @param mapped: class
            The mapped model class.
        @return: list[Validation, Document class]
            The list of validations obtained.
        '''
        assert isclass(mapped), 'Invalid class %s' % mapped
        assert issubclass(mapped, Document), 'Invalid mapped document %s' % mapped
        model = typeFor(mapped)
        assert isinstance(model, TypeModel), 'Invalid model class %s' % mapped
        
        validations = []
        mvalidations = validationsFor(mapped)
        if mvalidations:
            for validation, target in mvalidations:
                assert isinstance(validation, IValidation), 'Invalid created validation %s' % validation
                validations.append((validation, target))
         
        for name, prop in model.properties.items():
            field, fclazz = getAttrAndClass(mapped, name)
            dvalidations = validationsFor(field)
            if dvalidations:
                for creator, target in dvalidations:
                    validation = creator(prop)
                    assert isinstance(validation, IValidation), 'Invalid created validation %s' % validation
                    if target == field: target = fclazz
                    validations.append((validation, target))
                continue
             
            if not isinstance(field, BaseField): continue
            assert isinstance(field, BaseField)
     
            if field.primary_key:
                validations.append((Mandatory(prop), fclazz))
            elif not field.required and field.default is None:
                validations.append((Mandatory(prop), fclazz))
     
            if isinstance(field, StringField):
                assert isinstance(field, StringField)
                if field.max_length is not None: validations.append((MaxLen(prop, field.max_length), fclazz))
                if field.min_length is not None: validations.append((MinLen(prop, field.min_length), fclazz))
             
            if isinstance(prop, TypePropertyContainer): validations.append((Relation(prop), fclazz))
        
        return validations        
