'''
Created on Oct 29, 2013

@package: ally core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the properties validation.
'''

import logging

from ally.api.operator.type import TypeProperty
from ally.api.validate import Validation
from ally.container.ioc import injected
from ally.design.processor.attribute import defines, requires
from ally.design.processor.context import Context
from ally.design.processor.execution import Chain
from ally.design.processor.handler import HandlerProcessor


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Decoding(Context):
    '''
    The model decoding context.
    '''
    # ---------------------------------------------------------------- Defined
    validations = defines(list, doc='''
    @rtype: list[Validation]
    The list of validations to process for the property, this list needs to be consumed
    of the validations that are resolved.
    ''')
    # ---------------------------------------------------------------- Required
    property = requires(TypeProperty)
    
# --------------------------------------------------------------------

@injected
class ValidationPropertyProvider(HandlerProcessor):
    '''
    Implementation for a handler that provides the properties validation requirements.
    '''
    
    validations = list
    # The list of assigned validations.
    
    def __init__(self):
        assert isinstance(self.validations, list), 'Invalid validations %s' % self.validations
        super().__init__()
        
        self._validationsByProperty = {}
        for validation in self.validations:
            assert isinstance(validation, Validation), 'Invalid validation %s' % validation
            assert isinstance(validation.property, TypeProperty), 'Invalid property type %s' % validation.property
            validations = self._validationsByProperty.get(validation.property)
            if validations is None: validations = self._validationsByProperty[validation.property] = []
            validations.append(validation)
    
    def process(self, chain, decoding:Decoding, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Provide the validations for the property.
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(decoding, Decoding), 'Invalid decoding %s' % decoding
        if not decoding.property: return
        assert isinstance(decoding.property, TypeProperty), 'Invalid property type %s' % decoding.property
        
        validations = self._validationsByProperty.get(decoding.property)
        if not validations: return
        
        decoding.validations = list(validations)
        chain.onFinalize(self.checkUnhandled)
    
    # ----------------------------------------------------------------

    def checkUnhandled(self, final, decoding, **keyargs):
        '''
        Checks if all validations have been handled.
        '''
        assert isinstance(decoding, Decoding), 'Invalid decoding %s' % decoding
        if decoding.validations: log.warn('Unknown validation specifications:\n\t%s',
                                          '\t\n'.join(str(valid) for valid in decoding.validations))
