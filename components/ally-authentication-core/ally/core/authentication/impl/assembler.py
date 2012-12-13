'''
Created on Jun 18, 2011

@package: ally authenticated core
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the call assemblers used for authentication.
'''

from ally.api.config import INSERT, UPDATE
from ally.api.operator.authentication.type import IAuthenticated, TypeModelAuth
from ally.api.operator.type import TypeModel
from ally.api.type import Input
from ally.container.ioc import injected
from ally.core.impl.invoker import InvokerRestructuring
from ally.core.spec.resources import Node, Invoker, IAssembler
import logging

# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------

@injected
class AssembleAuthenticationExplode(IAssembler):
    '''
    This assembler will wrap any invoker that has an authenticated property inside a model in order to expose the
    authenticated property as an input and thus being in the URL. Also the invoker inputs are restructured so the model
    will be populated with the authenticated values.
    '''

    def knownModelHints(self):
        '''
        @see: IAssembler.knownModelHints
        '''
        return {}

    def knownCallHints(self):
        '''
        @see: IAssembler.knownCallHints
        '''
        return {}

    def assemble(self, root, invokers):
        '''
        @see: IAssembler.assemble
        '''
        assert isinstance(root, Node), 'Invalid node %s' % root
        assert isinstance(invokers, list), 'Invalid invokers %s' % invokers
        for k in range(len(invokers)):
            invokerAuth = self.process(invokers[k])
            if invokerAuth is not None: invokers[k] = invokerAuth

    # ----------------------------------------------------------------

    def process(self, invoker):
        '''
        Processes the invoker to an authenticated invoker.
        '''
        assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
        assert not isinstance(invoker.output, IAuthenticated), 'Invalid authenticated output for %s' % invoker

        if invoker.method not in (INSERT, UPDATE): return
        
        # First we determine if the input models have authenticated properties
        modelSet, modelAuthTypes = {}, set()
        for k, inp in enumerate(invoker.inputs):
            assert isinstance(inp, Input), 'Invalid input %s' % inp
            typ = inp.type

            if isinstance(typ, TypeModel):
                assert isinstance(typ, TypeModel)
                props = {}
                for prop, mtyp in typ.container.properties.items():
                    if isinstance(mtyp, TypeModelAuth):
                        ptyp = mtyp.childTypeId()
                        modelAuthTypes.add(ptyp)
                        props[prop] = ptyp
                modelSet[k] = props
        
        if not modelAuthTypes: return
        
        # If there are authenticated properties on input models we search if the authenticated properties are not already
        # provided in the inputs before we try to explode them
        authTypes = {inp.type:k for k, inp in enumerate(invoker.inputs) if isinstance(inp.type, IAuthenticated)}
        for k, inp in enumerate(invoker.inputs):
            if isinstance(inp.type, IAuthenticated):
                assert not inp.hasDefault, 'The authenticated input %s from invoker %s cannot have a default value'\
                % (inp, invoker)
                authTypes[inp.type] = k
        if __debug__:
            inputModelsAuth = [str(typ) for typ in authTypes if isinstance(typ, TypeModel)]
            assert not inputModelsAuth, 'Invalid authenticated model inputs %s for %s' % (inputModelsAuth, invoker)
        inputs = []
        for typ in modelAuthTypes:
            if typ not in authTypes: inputs.append(Input(''.join(('auth$', typ.container.name, '.', typ.property)), typ))
        
        offset = len(inputs)
        if offset > 0:
            # We exploded the authenticated model properties and we need to adjust the types 
            for typ in authTypes: authTypes[typ] += offset
            for k, inp in enumerate(inputs): authTypes[inp.type] = k
        
        inputs.extend(invoker.inputs)  # We add the rest of the inputs to the restructuring invoker inputs
        # We nor create the dictionary of indexes and properties to be set
        indexesSetValue = {}
        for k, props in modelSet.items():
            indexesSetValue[k] = {prop:authTypes[typ] for prop, typ in props.items()}

        invoker = InvokerRestructuring(invoker, inputs, list(range(offset, len(inputs))), indexesSetValue)
        log.info('Assembled as an authenticated invoker %s' % invoker)

        return invoker
