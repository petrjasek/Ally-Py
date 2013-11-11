'''
Created on Nov 8, 2013

@package: ally core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the merging of models that inherit the same base as one single model.
'''

from inspect import getmro, isclass
import logging

from ally.api.config import model
from ally.api.operator.type import TypeProperty, TypeModel
from ally.api.type import Iter, Type, Input, typeFor
from ally.design.processor.attribute import requires
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
from ally.container.ioc import injected


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Register(Context):
    '''
    The register context.
    '''
    # ---------------------------------------------------------------- Required
    invokers = requires(list)
    
class Invoker(Context):
    '''
    The invoker context.
    '''
    # ---------------------------------------------------------------- Required
    inputs = requires(tuple)
    output = requires(Type)
    
# --------------------------------------------------------------------

@injected
class ModelMergerHandler(HandlerProcessor):
    '''
    Implementation for a processor that provides the merging of models that inherit the same base as one single model.
    '''
    
    base = None
    # The base class for the models to be merged.
    
    def __init__(self):
        assert isclass(self.base), 'Invalid base class %s' % self.base
        assert isinstance(typeFor(self.base), TypeModel), 'Invalid model class %s' % self.base
        super().__init__(Invoker=Invoker)

    def process(self, chain, register:Register, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Merge the models.
        '''
        assert isinstance(register, Register), 'Invalid register %s' % register
        if not register.invokers: return

        invokers, classes = [], set()
        for invoker in register.invokers:
            assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
            
            isOnBase = False
            clazz = self.getBaseInherited(invoker.output)
            if clazz:
                classes.add(clazz)
                isOnBase = isOnBase or clazz is self.base
                
            for inp in invoker.inputs:
                assert isinstance(inp, Input), 'Invalid input %s' % inp
                clazz = self.getBaseInherited(inp.type)
                if not clazz: continue
                classes.add(clazz)
                isOnBase = isOnBase or clazz is self.base
                
            if isOnBase: invokers.append(invoker)
        
        classes.discard(self.base)
        if not classes: return
        
        top = set(classes)
        for clazz in classes:
            top.difference_update(getmro(clazz))
            top.add(clazz)
        
        mergedCls = type('%s$Merged' % self.base.__name__, tuple(top), {})
        mergedModel = model(name=typeFor(self.base).name, **typeFor(self.base).hints)(mergedCls)
        mergedType = typeFor(mergedModel)
        
        for invoker in invokers:
            output = self.getBaseMerged(mergedType, invoker.output)
            if output is not None: invoker.output = output
            
            inputs = []
            for inp in invoker.inputs:
                assert isinstance(inp, Input), 'Invalid input %s' % inp
                itype = self.getBaseMerged(mergedType, inp.type)
                if itype is not None: inp = Input(inp.name, itype, inp.hasDefault, inp.default)
                inputs.append(inp)
            
            invoker.inputs = tuple(inputs)
            
    # -----------------------------------------------------------------
    
    def getBaseInherited(self, typ):
        ''' Checks if the provided type is targeting the based model.'''
        if isinstance(typ, Iter):
            assert isinstance(typ, Iter)
            typ = typ.itemType
            
        if isinstance(typ, TypeProperty):
            assert isinstance(typ, TypeProperty)
            typ = typ.parent
        
        if isinstance(typ, TypeModel) and issubclass(typ.clazz, self.base): return typ.clazz
        
    def getBaseMerged(self, merged, typ):
        ''' Return the merged model wrapped in the type given by typ parameter '''
        assert isinstance(merged, TypeModel)
        collFactory = propName = None
        
        if isinstance(typ, Iter):
            assert isinstance(typ, Iter)
            collFactory = type(typ)
            typ = typ.itemType
            
        if isinstance(typ, TypeProperty):
            assert isinstance(typ, TypeProperty)
            propName = typ.name
            typ = typ.parent
        
        if isinstance(typ, TypeModel) and issubclass(typ.clazz, self.base):
            if propName is not None: merged = merged.properties[propName]
            if collFactory is not None: merged = collFactory(merged)
            return merged
        
