'''
Created on Oct 29, 2013

@package: ally core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the mandatory validation.
'''

from ally.api.config import INSERT, UPDATE, DELETE
from ally.api.validate import Mandatory
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
from ally.core.impl.processor.decoder.base import addError
from ally.internationalization import _
from ally.api.operator.type import TypeProperty

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

class ValidateMandatory(HandlerProcessor):
    '''
    Implementation for a handler that provides the mandatory validation.
    '''
    
    def process(self, chain, decoding:Decoding, invoker:Invoker, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Process the mandatory validation.
        '''
        assert isinstance(decoding, Decoding), 'Invalid decoding %s' % decoding
        assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
        if not decoding.validations or invoker.method == DELETE: return
        
        found, validations = False, []
        for validation in decoding.validations:
            if isinstance(validation, Mandatory):
                decoding.doEnd = self.createMandatory(decoding, validation, decoding.doEnd, invoker.method)
                found = True
            else: validations.append(validation)
        if not found: return
        
        if invoker.method == INSERT: decoding.isMandatory = True
        decoding.validations = validations
    
    # ----------------------------------------------------------------
    
    def createMandatory(self, decoding, validation, wrapped, method):
        '''
        Create the do end for mandatory validation.
        '''
        assert isinstance(decoding, Decoding), 'Invalid decoding %s' % decoding
        assert isinstance(validation.property, TypeProperty), 'Invalid property %s' % validation.property
        
        def doMandatory(target):
            '''
            Do end the mandatory validation.
            '''
            assert isinstance(target, Context), 'Invalid target %s' % target
            
            mvalue = decoding.doGet(target)
            value = getattr(mvalue, validation.property.name)
            
            if value is None or (isinstance(value, str) and not value):
                if method == INSERT or method == UPDATE and validation.property in mvalue:
                    addError(target, 'mandatory', validation.property, _('Mandatory value is missing'))
            if wrapped:
                wrapped(target)
        
        return doMandatory
