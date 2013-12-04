'''
Created on Oct 8, 2013

@package: ally documentation
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Processor that provides the API service mapping.
'''

from ally.api.operator.type import TypeCall, TypeService
from ally.design.processor.attribute import requires
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
from ally.container.ioc import injected
from ally.support.util import TextTable


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
    path = requires(list)
    methodHTTP = requires(str)
    call = requires(TypeCall)
    
class Element(Context):
    '''
    The element context.
    '''
    # ---------------------------------------------------------------- Required
    name = requires(str)
      
# --------------------------------------------------------------------

@injected
class MappingDumpHandler(HandlerProcessor):
    '''
    Handler that provides the API data to be documented.
    '''
    
    pathMapping = str
    # The path where the mapping will be dumped.
    
    def __init__(self):
        assert isinstance(self.pathMapping, str), 'Invalid mapping path %s' % self.pathMapping
        super().__init__(Invoker=Invoker, Element=Element)
    
    def process(self, chain, register:Register, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Dump the mappings.
        '''
        assert isinstance(register, Register), 'Invalid register %s' % register
        if not register.invokers: return  # No invokers to process.

        mapping = []
        for invoker in register.invokers:
            assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
            if not invoker.path: continue
            if not invoker.call: continue
            assert isinstance(invoker.call, TypeCall)
            assert isinstance(invoker.call.parent, TypeService)
            
            path = []
            for el in invoker.path:
                assert isinstance(el, Element)
                if el.name: path.append(el.name)
                else: path.append('*')
            
            mapping.append((invoker.methodHTTP, '/'.join(path),
                '%s.%s.%s' % (invoker.call.parent.clazz.__module__, invoker.call.parent.clazz.__name__, invoker.call.name)))

        mapping.sort(key=lambda pack: pack[0])
        mapping.sort(key=lambda pack: pack[1])
        
        table = TextTable('Method', 'URI', 'Service call')
        for row in mapping: table.add(*row)
        
        with open(self.pathMapping, 'w') as f: table.render(f)