'''
Created on May 28, 2013

@package: ally core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the processing on callers based on methods.
'''

from ally.api.config import GET, INSERT, UPDATE, DELETE
from ally.api.operator.type import TypeProperty, TypeModel
from ally.api.type import Iter, Type, Input
from ally.design.processor.attribute import requires, defines, definesIf
from ally.design.processor.context import Context
from ally.design.processor.execution import Abort
from ally.design.processor.handler import HandlerProcessor
import logging
from ally.support.util_spec import IDo

# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Register(Context):
    '''
    The register context.
    '''
    # ---------------------------------------------------------------- Required
    invokers = requires(list)
    doCopyInvoker = requires(IDo)
    
class Invoker(Context):
    '''
    The invoker context.
    '''
    # ---------------------------------------------------------------- Defined
    target = defines(TypeModel, doc='''
    @rtype: TypeModel
    The target model of the caller.
    ''')
    isCollection = defines(bool, doc='''
    @rtype: boolean
    If True it means that the invoker provides a collection.
    ''')
    isModel = defines(bool, doc='''
    @rtype: boolean
    If True it means that the invoker provides a full model, attention the model can be in a collection.
    ''')
    modelInput = defines(Input, doc='''
    @rtype: Input
    The input that is expected to receive a model object, this is only available for INSERT or UPDATE methods.
    ''')
    links = definesIf(set, doc='''
    @rtype: set(TypeModel)
    The models that are linked by the caller.
    ''')
    # ---------------------------------------------------------------- Required
    method = requires(int)
    inputs = requires(tuple)
    output = requires(Type)
    location = requires(str)
    
# --------------------------------------------------------------------

class ProcessMethodHandler(HandlerProcessor):
    '''
    Implementation for a processor that provides the inputs and output processing and validation based on the method.
    '''
    
    def __init__(self):
        super().__init__(Invoker=Invoker)

    def process(self, chain, register:Register, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Process the invokers based on method.
        '''
        assert isinstance(register, Register), 'Invalid register %s' % register
        if not register.invokers: return
        
        aborted = []
        for invoker in register.invokers:
            assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
            
            keep = False
            if invoker.method == GET: keep = self.processGET(invoker)
            elif invoker.method == INSERT: keep = self.processINSERT(invoker)
            elif invoker.method == UPDATE: keep = self.processUPDATE(invoker)
            elif invoker.method == DELETE: keep = self.processDELETE(invoker)
            else:
                log.error('Cannot use because the method %s is not known, at:%s', invoker.method, invoker.location)
                keep = False
            if not keep: aborted.append(invoker)
        
        if aborted: raise Abort(*aborted)
        
        register.doCopyInvoker = self.createCopyInvoker(register.doCopyInvoker)

    # ----------------------------------------------------------------
    
    def processGET(self, invoker):
        '''
        Process the GET invoker, returns True if the invoker should be kept.
        '''
        assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
        
        if isinstance(invoker.output, Iter):
            assert isinstance(invoker.output, Iter)
            output = invoker.output.itemType
            invoker.isCollection = True
        else:
            output = invoker.output
            
        if isinstance(output, TypeProperty):
            assert isinstance(output, TypeProperty)
            output = output.parent
        else: invoker.isModel = True

        if isinstance(output, TypeModel):
            invoker.target = output
            return True
        
        log.error('Cannot use because the output %s is not for a model, at:%s', invoker.output, invoker.location)
        
    def processINSERT(self, invoker):
        '''
        Process the INSERT invoker, returns True if the invoker should be kept.
        '''
        assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker

        output = invoker.output
        if isinstance(output, TypeProperty):
            assert isinstance(output, TypeProperty)
            output = output.parent

        if not isinstance(output, TypeModel):
            log.error('Cannot use because the output %s is not for a model, at:%s', invoker.output, invoker.location)
            return False
        
        inputs = [inp for inp in invoker.inputs if isinstance(inp.type, TypeModel)]
        if len(inputs) > 1:
            log.error('Cannot use because there are to many models %s to insert, at:%s',
                     ', '.join(str(inp.type) for inp in inputs), invoker.location)
            return False
        if inputs: invoker.modelInput = inputs[0]
            
        invoker.target = output
        if Invoker.links in invoker:
            if invoker.links is None: invoker.links = set()
            invoker.links.update(inp.type.parent for inp in invoker.inputs if isinstance(inp.type, TypeProperty))
        return True
 
    def processUPDATE(self, invoker):
        '''
        Process the UPDATE invoker, returns True if the invoker should be kept.
        '''
        assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker

        inputs = [inp for inp in invoker.inputs if isinstance(inp.type, TypeModel)]
        if len(inputs) > 1:
            log.error('Cannot use because there are to many models %s to update, at:%s',
                     ', '.join(str(inp.type) for inp in inputs), invoker.location)
            return False
        if inputs:
            invoker.modelInput = inputs[0]
            invoker.target = invoker.modelInput.type
        if Invoker.links in invoker:
            if invoker.links is None: invoker.links = set()
            invoker.links.update(inp.type.parent for inp in invoker.inputs if isinstance(inp.type, TypeProperty))
        return True
    
    def processDELETE(self, invoker):
        '''
        Process the DELETE invoker, returns True if the invoker should be kept.
        '''
        assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker

        if not invoker.output.isOf(bool):
            log.error('Cannot use because a boolean return is expected, at:%s', invoker.location)
            return False
        properties = [inp.type for inp in invoker.inputs if isinstance(inp.type, TypeProperty)]
        if len(properties) == 1:
            invoker.isModel = True
            invoker.target = properties[0].parent
        if Invoker.links in invoker:
            if invoker.links is None: invoker.links = set()
            invoker.links.update(prop.parent for prop in properties)
        return True
    
    # ----------------------------------------------------------------
    
    def createCopyInvoker(self, copyInvoker):
        assert isinstance(copyInvoker, IDo), 'Invalid copy invoker %s' % copyInvoker
        def doCopy(destination, source, exclude=None):
            '''
            Do copy the invoker.
            '''
            assert isinstance(destination, Invoker), 'Invalid destination %s' % destination
            assert isinstance(source, Invoker), 'Invalid source %s' % source
            assert exclude is None or isinstance(exclude, set), 'Invalid exclude %s' % exclude
            
            if Invoker.links in source and Invoker.links in destination:
                if not(exclude and 'links' not in exclude) and source.links: destination.links = set(source.links)
            
            return copyInvoker(destination, source, exclude=exclude)
        return doCopy
