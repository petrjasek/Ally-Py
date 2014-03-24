'''
Created on Oct 30, 2013

@package: ally core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the length validation.
'''

from ally.api.operator.type import TypeProperty
from ally.api.validate import MinLen, MaxLen
from ally.design.processor.attribute import requires, definesIf
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
from ally.support.util_spec import IDo
from ally.internationalization import _
from ally.core.impl.processor.decoder.base import addError

# --------------------------------------------------------------------

class Decoding(Context):
    '''
    The model decoding context.
    '''
    # ---------------------------------------------------------------- Defined
    minimumLength = definesIf(int, doc='''
    @rtype: integer
    Provides the minimum string length.
    ''')
    maximumLength = definesIf(int, doc='''
    @rtype: integer
    Provides the maximum string length.
    ''')
    # ---------------------------------------------------------------- Required
    validations = requires(list)
    property = requires(TypeProperty)
    doSet = requires(IDo)
    
# --------------------------------------------------------------------

class ValidateLen(HandlerProcessor):
    '''
    Implementation for a handler that provides the length validation.
    '''
    
    def process(self, chain, decoding:Decoding, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Process the length validation.
        '''
        assert isinstance(decoding, Decoding), 'Invalid decoding %s' % decoding
        if not decoding.validations: return
        
        lengthMax, lengthMin, validations = None, None, []
        for validation in decoding.validations:
            if isinstance(validation, MaxLen):
                assert isinstance(validation, MaxLen)
                if lengthMax is None: lengthMax = validation.length
                else: lengthMax = min(lengthMax, validation.length)
            elif isinstance(validation, MinLen):
                assert isinstance(validation, MinLen)
                if lengthMin is None: lengthMin = validation.length
                else: lengthMin = max(lengthMin, validation.length)
            else: validations.append(validation)
        
        decoding.validations = validations

        if lengthMax is not None:
            if Decoding.maximumLength in decoding:
                decoding.maximumLength = lengthMax
            decoding.doSet = self.createMaxSet(decoding.doSet, decoding.property, lengthMax)
            
        if lengthMin is not None:
            if Decoding.minimumLength in decoding:
                decoding.minimumLength = lengthMin
            decoding.doSet = self.createMinSet(decoding.doSet, decoding.property, lengthMin)

    # ----------------------------------------------------------------
    
    def createMaxSet(self, wrapped, prop, length):
        '''
        Create the do maximum set to use with validation.
        '''
        assert callable(wrapped), 'Invalid wrapped set %s' % wrapped
        assert isinstance(prop, TypeProperty), 'Invalid property %s' % prop
        def doSet(target, value):
            if len(value) > length:
                addError(target, 'max_len', prop, _('Maximum text size exceed'), value=length)
            wrapped(target, value)
        return doSet
    
    def createMinSet(self, wrapped, prop, length):
        '''
        Create the do minimum set to use with validation.
        '''
        assert callable(wrapped), 'Invalid wrapped set %s' % wrapped
        assert isinstance(prop, TypeProperty), 'Invalid property %s' % prop
        def doSet(target, value):
            if len(value) < length:
                addError(target, 'min_len', prop, _('Minimum text size exceeded'), value=length)
            wrapped(target, value)
        return doSet
