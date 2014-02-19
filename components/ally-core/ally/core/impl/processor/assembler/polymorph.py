'''
Created on Dec 2, 2013

@package: ally core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the polymorph indexing.
'''

import logging
from ally.api.operator.type import TypeModel, TypeProperty, TypeQuery
from ally.api.type import typeFor, Input
from ally.container.ioc import injected
from ally.design.processor.attribute import requires, definesIf, defines
from ally.design.processor.context import Context
from ally.design.processor.execution import Abort
from ally.design.processor.handler import HandlerProcessor
from ally.support.api.util_service import isAvailableIn
from ally.api.config import GET
from ally.api.operator.extract import inheritedTypesFrom
from collections import OrderedDict

# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Register(Context):
    '''
    The register context.
    '''
    # ---------------------------------------------------------------- Defined
    hintsModel = definesIf(dict)
    polymorphs = defines(dict, doc='''
    @rtype: dictionary{TypeModel: Context}
    The polymorphers contexts indexed by the polymorphing model type.
    ''')
    polymorphed = defines(dict, doc='''
    @rtype: dictionary{TypeModel: list[Context]}
    The polymorphing contexts indexed by the polymorphed model type.
    ''')
    # ---------------------------------------------------------------- Required
    invokers = requires(list)
    
class Invoker(Context):
    '''
    The invoker context.
    '''
    # ---------------------------------------------------------------- Required
    method = requires(int)
    inputs = requires(tuple)
    target = requires(TypeModel)
    modelInput = requires(Input)
    isModel = requires(bool)
    isCollection = requires(bool)
    location = requires(str)
    decodingContent = requires(Context)

class PolymorphModel(Context):
    '''
    The polymorph context.
    '''
    # ---------------------------------------------------------------- Defined
    target = defines(TypeModel, doc='''
    @rtype: TypeModel
    The polymorphic target.
    ''')
    parents = defines(list, doc='''
    @rtype: list[TypeModel]
    A list of the type models that are polymorphed.
    ''')
    queries = defines(list, doc='''
    @rtype: list[TypeQuery]
    A list of the type queries that are used by polymorphed.
    ''')
    values = defines(dict, doc='''
    @rtype: dictionary{string: object}
    A dictionary containing the polymorphic values.
    ''')

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

    def process(self, chain, register:Register, Polymorph:PolymorphModel, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Provides the polymorph models.
        '''
        assert isinstance(register, Register), 'Invalid register %s' % register
        assert issubclass(Polymorph, PolymorphModel), 'Invalid polymorph class %s' % PolymorphModel
        if not register.invokers: return
        
        if Register.hintsModel in register:
            if register.hintsModel is None: register.hintsModel = {}
            register.hintsModel[self.hintName] = self.hintDescription

        aborted = []
        for invoker in register.invokers:
            assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
            if invoker.target: target = invoker.target
            elif invoker.modelInput:
                assert isinstance(invoker.modelInput, Input)
                target = invoker.modelInput.type
            else: continue
            
            assert isinstance(target, TypeModel), 'Invalid target %s' % target
            
            if self.hintName not in target.hints: continue
            
            if register.polymorphs is None: register.polymorphs = {}
            polymorph = register.polymorphs.get(target)
            if polymorph is None:
                polymorph = register.polymorphs[target] = Polymorph()
                assert isinstance(polymorph, PolymorphModel)
                
                polymorph.target = target
                polymorph.parents = []
                hint = {}
                
                for parent in inheritedTypesFrom(target.clazz, TypeModel, inDepth=True):
                    if parent == target.clazz: continue
                    assert isinstance(parent, TypeModel)
                    
                    polymorph.parents.append(parent)
                    
                    if self.hintName in parent.hints:
                        hint.update(parent.hints[self.hintName])
                    else:
                        break  # This is the root model for polymorph

                hint.update(target.hints[self.hintName])
                    
                if not polymorph.parents:
                    log.error('Cannot use invoker because the model %s is set as polymorph \'%s\' but is not '
                              'inheriting any other model, at:%s', target, invoker.location)
                    aborted.append(invoker)
                    continue
                
                polymorph.values = OrderedDict()
                valid = False
                if isinstance(hint, dict) and hint:
                    valid = True
                    for key, value in hint.items():
                        typ = typeFor(key)
                        if isinstance(typ, TypeProperty):
                            assert isinstance(typ, TypeProperty)
                            valid = isAvailableIn(target, typ.name, typ.type)
                            if value is None:
                                valid = False
                                log.warn('None is not a valid polymorph value for %s', target)
                            polymorph.values[typ.name] = value
                        else:
                            valid = isinstance(key, str)
                            polymorph.values[key] = value
                        if not valid: break
                
                if not valid:
                    log.error('Cannot use invoker because the model %s polymorph \'%s\' is invalid, at:%s',
                              target, hint, invoker.location)
                    aborted.append(invoker)
                else:
                    for prop in polymorph.values:
                        if prop not in polymorph.parents[0].properties:
                            log.error('Cannot use invoker because the model %s has invalid '
                                      'property \'%s\' for inherited %s at:%s', target, prop,
                                      polymorph.parents[0], invoker.location)
                            aborted.append(invoker)
                            break
                
                if register.polymorphed is None: register.polymorphed = {}
                polymorphed = register.polymorphed.get(polymorph.parents[-1])
                if polymorphed is None: polymorphed = register.polymorphed[polymorph.parents[-1]] = []
                polymorphed.append(polymorph)
            
            if invoker.method == GET and invoker.isCollection:
                for inp in invoker.inputs:
                    assert isinstance(inp, Input), 'Invalid input %s' % inp
                    if isinstance(inp.type, TypeQuery):
                        if polymorph.queries is None: polymorph.queries = []
                        polymorph.queries.append(inp.type)
                
        if aborted: raise Abort(*aborted)
