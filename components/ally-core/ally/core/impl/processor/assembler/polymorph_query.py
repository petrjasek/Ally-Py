'''
Created on Dec 5, 2013

@package: ally core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the polymorph merging of queries.
'''

from inspect import getmro
import logging

from ally.api.config import GET, query
from ally.api.operator.type import TypeModel, TypeQuery
from ally.api.type import typeFor, Input
from ally.design.processor.attribute import requires
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Register(Context):
    '''
    The register context.
    '''
    # ---------------------------------------------------------------- Required
    polymorphed = requires(dict)
    invokers = requires(list)
    
class Invoker(Context):
    '''
    The invoker context.
    '''
    # ---------------------------------------------------------------- Required
    method = requires(int)
    inputs = requires(tuple)
    target = requires(TypeModel)
    isCollection = requires(bool)

class Polymorph(Context):
    '''
    The polymorph context.
    '''
    # ---------------------------------------------------------------- Required
    queries = requires(list)
    
# --------------------------------------------------------------------

class PolymorphQueryHandler(HandlerProcessor):
    '''
    Implementation for a processor that provides the polymorph merging of queries.
    '''
    
    def __init__(self):
        super().__init__(Invoker=Invoker, Polymorph=Polymorph)

    def process(self, chain, register:Register, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Provides the polymorph models.
        '''
        assert isinstance(register, Register), 'Invalid register %s' % register
        if not register.invokers or not register.polymorphed: return

        for invoker in register.invokers:
            assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
            if invoker.method != GET or not invoker.isCollection or not invoker.target: continue
            polymorphed = register.polymorphed.get(invoker.target)
            if not polymorphed: continue
            
            inputs, replace = [], False
            for inp in invoker.inputs:
                assert isinstance(inp, Input), 'Invalid input %s' % inp
                if not isinstance(inp.type, TypeQuery): continue
                assert isinstance(inp.type, TypeQuery)
            
                classes = []
                for polymorph in polymorphed:
                    assert isinstance(polymorph, Polymorph), 'Invalid polymorph %s' % polymorph
                    if not polymorph.queries: continue
                    for q in polymorph.queries:
                        assert isinstance(q, TypeQuery), 'Invalid query %s' % q
                        if issubclass(q.clazz, inp.type.clazz): classes.append(q.clazz)
                
                if not classes:
                    inputs.append(inp)
                    continue
                top = set(classes)
                for clazz in classes:
                    top.difference_update(getmro(clazz))
                    top.add(clazz)
                
                mergedCls = query(inp.type.target)(type('%s$Merged' % inp.type.clazz.__name__, tuple(top), {}))
                merged = typeFor(mergedCls)
                
                inputs.append(Input(inp.name, merged, inp.hasDefault, inp.default))
                replace = True
            
            if replace: invoker.inputs = tuple(inputs)
