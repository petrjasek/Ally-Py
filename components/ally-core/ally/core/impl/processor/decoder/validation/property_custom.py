'''
Created on Mar 12, 2014

@package: ally core
@copyright: 2014 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mugur Rus

Provides the custom validations processor.
'''

from ally.api.validate import IValidator
from ally.design.processor.attribute import requires
from ally.design.processor.context import Context
from ally.design.processor.execution import Chain
from ally.design.processor.handler import HandlerProcessor
from ally.api.operator.type import TypeProperty
from ally.core.impl.processor.decoder.base import addError

# --------------------------------------------------------------------
    
class Decoding(Context):
    '''
    The model decoding context.
    '''
    # ---------------------------------------------------------------- Required
    validations = requires(list)
    
# --------------------------------------------------------------------

class ValidatePropertyCustom(HandlerProcessor):
    '''
    Implementation for a handler that provides the custom property validations.
    '''
    
    def process(self, chain, decoding:Decoding, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Process the custom property validations.
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(decoding, Decoding), 'Invalid decoding %s' % decoding
        if not decoding.validations: return
        
        validations = []
        for validation in decoding.validations:
            if isinstance(validation, IValidator):
                decoding.doSet = self.createValidator(decoding.doSet, decoding.property, validation)
            else: validations.append(validation)
        
        decoding.validations = validations

    # ----------------------------------------------------------------
    
    def createValidator(self, wrapped, prop, validation):
        '''
        Create the do set to use with validation.
        '''
        assert callable(wrapped), 'Invalid wrapped set %s' % wrapped
        assert isinstance(prop, TypeProperty), 'Invalid property %s' % prop
        assert isinstance(validation, IValidator), 'Invalid validator %s' % validation
        
        def doSet(target, value):
            error = validation.validate(value)
            if error is not None:
                assert isinstance(error, tuple) and len(error) == 2, 'Invalid error result %s' % error
                addError(target, error[0], prop, error[1])
            wrapped(target, value)
        
        return doSet
