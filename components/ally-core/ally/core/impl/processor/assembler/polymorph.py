'''
Created on Dec 2, 2013

@package: ally core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the polymorph handling decoding.
'''

import logging

from ally.container.ioc import injected
from ally.design.processor.attribute import requires, definesIf
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Register(Context):
    '''
    The register context.
    '''
    # ---------------------------------------------------------------- Defined
    hintsModel = definesIf(dict)
    # ---------------------------------------------------------------- Required
    invokers = requires(list)
    
class Invoker(Context):
    '''
    The invoker context.
    '''
    # ---------------------------------------------------------------- Required
    location = requires(str)
    
# --------------------------------------------------------------------

@injected
class PolymorphHandler(HandlerProcessor):
    '''
    Implementation for a processor that provides the polymorph models.
    '''
    
    hintName = 'polymorph'
    # The hint name for the model polymorph.
    hintDescription = '(dictionary{string|TypeProperty: object}) The polymorphic specifications for the model'
    # The hint description.
    
    def __init__(self):
        assert isinstance(self.hintName, str), 'Invalid hint name %s' % self.hintName
        assert isinstance(self.hintDescription, str), 'Invalid hint description %s' % self.hintDescription
        super().__init__(Invoker=Invoker)

    def process(self, chain, register:Register, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Provides the polymorph models.
        '''
        assert isinstance(register, Register), 'Invalid register %s' % register
        if not register.invokers: return
        
        if Register.hintsModel in register:
            if register.hintsModel is None: register.hintsModel = {}
            register.hintsModel[self.hintName] = self.hintDescription

        aborted = []
        for invoker in register.invokers:
            assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
        # TODO: index polymorphic.
