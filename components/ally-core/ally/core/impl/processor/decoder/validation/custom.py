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


# --------------------------------------------------------------------
    
class Decoding(Context):
    '''
    The model decoding context.
    '''
    # ---------------------------------------------------------------- Required
    validations = requires(list)
    
# --------------------------------------------------------------------

class ValidateCustom(HandlerProcessor):
    '''
    Implementation for a handler that provides the custom validations.
    '''
    
    def process(self, chain, decoding:Decoding, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Process the custom validations.
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(decoding, Decoding), 'Invalid decoding %s' % decoding
        if not decoding.validations: return
        
        found, validations = False, []
        for validation in decoding.validations:
            if isinstance(validation, IValidator):
                found = True
                # TODO implement validation
            else: validations.append(validation)
        if not found: return
        
        decoding.validations = validations
