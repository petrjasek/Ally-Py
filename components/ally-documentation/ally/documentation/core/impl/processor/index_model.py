'''
Created on Jan 21, 2014

@package: ally documentation
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Processor that provides the API data to be documented.
'''

from inspect import getdoc

from ally.api.operator.type import TypeModel, TypeProperty, \
    TypePropertyContainer
from ally.api.type import Iter, Boolean, Integer, Number, String, Time, Date, \
    DateTime, TypeReference, typeFor
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor


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
    target = requires(TypeModel)
    links = requires(set)
    
class Document(Context):
    '''
    The introspect context.
    '''
    # ---------------------------------------------------------------- Defined
    data = defines(dict, doc='''
    @rtype: dictionary{string: object}
    The data constructed for templates.
    ''')
    modelData = defines(dict, doc='''
    @rtype: dictionary{TypeModel: dictionary{string: object}}
    The dictionary containing the type model and data associated with it.
    ''')
      
# --------------------------------------------------------------------

class IndexModelHandler(HandlerProcessor):
    '''
    Handler that provides the model data to be documented.
    '''
    
    typeOrders = [Boolean, Integer, Number, String, Time, Date, DateTime, Iter]
    # The type that define the order in which the properties should be rendered.
    hintName = 'domain'
    # The hint name for the model domain.
    
    def __init__(self):
        assert isinstance(self.hintName, str), 'Invalid hint name %s' % self.hintName
        super().__init__(Invoker=Invoker)
    
    def process(self, chain, register:Register, document:Document, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Index the model API data to be documented.
        '''
        assert isinstance(register, Register), 'Invalid register %s' % register
        assert isinstance(document, Document), 'Invalid document %s' % document
        if not register.invokers: return  # No invokers to process.
        
        typeModels = set()
        for invoker in register.invokers:
            assert isinstance(invoker, Invoker)
            if invoker.target: typeModels.add(invoker.target)
            if invoker.links: typeModels.update(invoker.links)
        
        # We need to remove the allowed model since is part of filtering.
        try: from gateway.api.gateway import Allowed
        except ImportError: pass
        else: typeModels.discard(typeFor(Allowed))
        
        if document.data is None: document.data = {}
        if document.modelData is None: document.modelData = {}
        
        models = {}
        for model in typeModels:
            assert isinstance(model, TypeModel), 'Invalid model %s' % model
            
            entityName = '%s.%s' % (model.clazz.__module__, model.clazz.__name__)
            
            name = self.modelName(model)
            data = models.get(name)
            if data is None: data = models[name] = dict(name=name, entities=[])
            entityData = dict(name=entityName, model=data)
            data['entities'].append(entityData)
            document.modelData[model] = entityData
            entityData['doc'] = getdoc(model.clazz)
            entityData['model'] = data
            properties = entityData['properties'] = []
            
            for prop in self.sortedTypes(model):
                assert isinstance(prop, TypeProperty)
                flags = set()
                propData = {'name': prop.name, 'type': str(prop.type), 'flags': flags}
                properties.append(propData)
                if prop == model.propertyId: flags.add('isId')
                if isinstance(prop.type, TypeReference): flags.add('isReference')
                
                if isinstance(prop, TypePropertyContainer):
                    assert isinstance(prop, TypePropertyContainer)
                    cname = self.modelName(prop.container)
                    cdata = models.get(cname)
                    if cdata is None: cdata = models[cname] = dict(name=cname, entities=[])
                    propData['model'] = cdata

        document.data['models'] = list(models.values())
        document.data['models'].sort(key=lambda data: data['name'])

    # ----------------------------------------------------------------
    
    def modelName(self, model):
        ''' Provides the model name.'''
        assert isinstance(model, TypeModel), 'Invalid model %s' % model
        name = model.name
        if self.hintName in model.hints:
            domain = str(model.hints[self.hintName]).rstrip('/')
            name = '%s/%s' % (domain, name)
        return name
       
    def sortedTypes(self, model):
        '''
        Provides the sorted properties type for the model type.
        '''
        assert isinstance(model, TypeModel), 'Invalid type model %s' % model
        sorted = list(model.properties.values())
        if model.propertyId: sorted.remove(model.propertyId)
        sorted.sort(key=lambda prop: prop.name)
        sorted.sort(key=self.sortKey)
        if model.propertyId: sorted.insert(0, model.propertyId)
        return sorted
    
    def sortKey(self, prop):
        '''
        Provides the sorting key for property types, used in sort functions.
        '''
        assert isinstance(prop, TypeProperty), 'Invalid property type %s' % prop

        for k, ord in enumerate(self.typeOrders):
            if prop.type == ord: break
        return k
