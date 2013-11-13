'''
Created on Nov 13, 2013

@package: ally core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the optional validation.
'''

from ally.api.validate import Mandatory, Optional
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor


# --------------------------------------------------------------------
class Invoker(Context):
    '''
    The invoker context.
    '''
    # ---------------------------------------------------------------- Required
    method = requires(int)
    
class Decoding(Context):
    '''
    The model decoding context.
    '''
    # ---------------------------------------------------------------- Defined
    isMandatory = defines(bool, doc='''
    @rtype: boolean
    Flag indicating if the decoding is mandatory.
    ''')
    # ---------------------------------------------------------------- Required
    validations = requires(list)
    
# --------------------------------------------------------------------

class ValidateOptional(HandlerProcessor):
    '''
    Implementation for a handler that provides the optional validation.
    '''
    
    def process(self, chain, decoding:Decoding, invoker:Invoker, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Remove the mandatory validation.
        '''
        assert isinstance(decoding, Decoding), 'Invalid decoding %s' % decoding
        assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
        if not decoding.validations: return
        
        found, validationsNoOptional = False, []
        for validation in decoding.validations:
            if isinstance(validation, Optional):
                found = True
            else: validationsNoOptional.append(validation)
        if not found: return
        
        validations = []
        for validation in validationsNoOptional:
            if isinstance(validation, Mandatory): continue
            validations.append(validation)
        
        decoding.validations = validations
