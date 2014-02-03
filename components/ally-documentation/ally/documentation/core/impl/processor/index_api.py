'''
Created on Oct 8, 2013

@package: ally documentation
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Processor that provides the API data to be documented.
'''

from ally.api.operator.type import TypeModel, TypeCall, TypeService, \
    TypeProperty
from ally.api.type import Type, Iter
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
from ally.http.spec.server import HTTP_PUT, HTTP_GET, HTTP_DELETE


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
    output = requires(Type)
    target = requires(TypeModel)
    isCollection = requires(bool)
    call = requires(TypeCall)
    filterName = requires(str)
    links = requires(set)
    
class Element(Context):
    '''
    The element context.
    '''
    # ---------------------------------------------------------------- Required
    name = requires(str)
    property = requires(TypeProperty)
    
class Document(Context):
    '''
    The introspect context.
    '''
    # ---------------------------------------------------------------- Defined
    data = defines(dict, doc='''
    @rtype: dictionary{string: object}
    The data constructed for templates.
    ''')
    invokerData = defines(list, doc='''
    @rtype: list[tuple(Context, dictionary{string: object})]
    The list containing tuples with the invoker context and the data dictionary associated with it.
    ''')
    # ---------------------------------------------------------------- Required
    modelData = requires(dict)
      
# --------------------------------------------------------------------

class IndexAPIHandler(HandlerProcessor):
    '''
    Handler that provides the API data to be documented.
    '''
    
    def __init__(self):
        super().__init__(Invoker=Invoker, Element=Element)
    
    def process(self, chain, register:Register, document:Document, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Index the API data to be documented.
        '''
        assert isinstance(register, Register), 'Invalid register %s' % register
        assert isinstance(document, Document), 'Invalid document %s' % document
        if not register.invokers: return  # No invokers to process.

        if document.data is None: document.data = {}
        if document.invokerData is None: document.invokerData = []
        
        requests = document.data.get('requests')
        if requests is None: requests = document.data['requests'] = []
        
        methods = document.data.get('methods')
        if methods is None: methods = document.data['methods'] = {}

        for invoker in register.invokers:
            assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
            if not invoker.path: continue
            if invoker.filterName is not None: continue  # We remove the filters which are not direct part of the API.
            
            request = {}
            requests.append(request)
            
            method = invoker.methodHTTP
            if method == HTTP_PUT and invoker.target is None: method = 'LINK'
            if method == HTTP_DELETE and invoker.links and len(invoker.links) > 1: method = 'UNLINK'

            mrequests = methods.get(method)
            if mrequests is None: mrequests = methods[method] = []
            mrequests.append(request)
            
            request['path'] = '/'.join(el.name if el.name else '*' for el in invoker.path)
            
            pathParams = request['path_params'] = []
            for el in invoker.path:
                if el.name: continue
                paramData = {'name': str(el.property)}
                pathParams.append(paramData)
                paramData['entity'] = document.modelData[el.property.parent]
            
            request['method'] = method
            request['doc'] = invoker.call.doc
            assert isinstance(invoker.call, TypeCall), 'Invalid invoker call %s' % invoker.call
            assert isinstance(invoker.call.parent, TypeService), 'Invalid call parent %s' % invoker.call.parent
            request['call'] = '%s.%s.%s' % (invoker.call.parent.clazz.__module__,
                                            invoker.call.parent.clazz.__name__, invoker.call.name)
            
            models = set()
            if invoker.links: models.update(invoker.links)
            if invoker.target: models.add(invoker.target)
            
            for target in models:
                assert isinstance(target, TypeModel), 'Invalid target %s' % target
                entity = request['entity'] = document.modelData[target]
                modelMethods = entity['model'].get('methods')
                if modelMethods is None: modelMethods = entity['model']['methods'] = {}
                modelRequests = modelMethods.get(method)
                if modelRequests is None: modelRequests = modelMethods[method] = []
                modelRequests.append(request)
            
            flags = request['flags'] = set()
            
            if method == HTTP_GET:
                assert isinstance(invoker.target, TypeModel), 'Invalid target %s' % invoker.target
                if invoker.isCollection:
                    flags.add('isCollection')
                    assert isinstance(invoker.output, Iter), 'Invalid output %s' % invoker.output
                    output = invoker.output.itemType
                else: output = invoker.output
                
                if output == invoker.target: flags.add('isModel')
                elif output == invoker.target.propertyId: flags.add('isModelRef')
                else:
                    assert isinstance(output, TypeProperty), 'Invalid type property %s' % output
                    request['property'] = output.name
            
            document.invokerData.append((invoker, request))
        
        requests.sort(key=lambda request: request['path'])
        requests.sort(key=lambda request: request['method'])
        
        for mrequests in methods.values():
            mrequests.sort(key=lambda request: request['path'])
        
        for entity in document.modelData.values():
            for requests in entity['model']['methods'].values():
                requests.sort(key=lambda request: request['path'])
                requests.sort(key=lambda request: 'isModel' not in request['flags'])  # We put the get model first
                 
        
