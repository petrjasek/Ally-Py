'''
Created on Mar 13, 2014

@package: ally core
@copyright: 2014 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mugur Rus

Provides the models validation.
'''

import logging
from ally.api.operator.type import TypeService, TypeModel
from ally.api.validate import IValidation
from ally.design.processor.attribute import defines, requires
from ally.design.processor.context import Context
from ally.design.processor.execution import Chain
from ally.design.processor.handler import HandlerProcessor
from ally.support.util_sys import locationStack, isLocated

# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Register(Context):
    '''
    The register context.
    '''
    # ---------------------------------------------------------------- Required
    validations = requires(dict)
    
class Invoker(Context):
    '''
    The invoker context.
    '''
    # ---------------------------------------------------------------- Required
    service = requires(TypeService)
    method = requires(int)
    
class Decoding(Context):
    '''
    The model decoding context.
    '''
    # ---------------------------------------------------------------- Defined
    validations = defines(list, doc='''
    @rtype: list[Validation]
    The list of validations to process for the model, this list needs to be consumed
    of the validations that are resolved.
    ''')
    # ---------------------------------------------------------------- Required
    type = requires(TypeModel)

# --------------------------------------------------------------------

class ValidationModelProvider(HandlerProcessor):
    '''
    Implementation for a handler that provides the model validation requirements.
    '''
    
    def process(self, chain, register:Register, invoker:Invoker, decoding:Decoding, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Provide the validations for the model.
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(register, Register), 'Invalid register %s' % register
        assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
        assert isinstance(decoding, Context), 'Invalid decoding %s' % decoding
        
        if not register.validations: return
        if not decoding.type: return
        if not isinstance(decoding.type, TypeModel): return
        # If the type is not model just move along.
        assert isinstance(decoding.type, TypeModel)
        
        svalidations = register.validations.get(invoker.service)
        if not svalidations: return
        assert isinstance(svalidations, list), 'Invalid validations %s' % svalidations
        
        k, validations = 0, []
        while k < len(svalidations):
            validation, target = svalidations[k]
            k += 1
            if not isinstance(validation, IValidation):
                if isLocated(target): log.warn('Cannot use validation %s from:%s', validation, locationStack(target))
                else: log.warn('Cannot use validation %s from target %s', validation, target)
                k -= 1
                del svalidations[k]
                continue
            
            assert isinstance(validation, IValidation)
            if validation.isFor(decoding.type, invoker.method): validations.append(validation)
        if not validations: return
        
        decoding.validations = validations
        chain.onFinalize(self.checkUnhandled)
    
    # ----------------------------------------------------------------
    
    def checkUnhandled(self, final, decoding, **keyargs):
        '''
        Checks if all validations have been handled.
        '''
        assert isinstance(decoding, Context), 'Invalid decoding %s' % decoding
        if decoding.validations: log.warn('Unknown validation specifications:\n\t%s',
                                          '\t\n'.join(str(valid) for valid in decoding.validations))
