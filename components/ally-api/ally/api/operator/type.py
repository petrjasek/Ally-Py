'''
Created on Mar 13, 2012

@package: ally api
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the operator types.
'''

from ..type import Type
from .container import Model, Container, Query, Criteria
from ally.api.operator.container import Service
from ally.api.type import typeFor, TypeClass

# --------------------------------------------------------------------

class TypeContainer(TypeClass):
    '''
    Provides the type for the properties container.
    '''

    __slots__ = ('container',)

    def __init__(self, clazz, container):
        '''
        Constructs the container type for the provided container.
        @see: TypeClass.__init__
        
        @param clazz: class
            The class associated with the container.
        @param container: Container
            The container that this type is constructed on.
        '''
        assert isinstance(container, Container), 'Invalid container provided %s' % container
        TypeClass.__init__(self, clazz, False, True)

        self.container = container

    def childTypes(self):
        '''
        Provides the child properties types.
        
        @return: list[TypeProperty]
            The properties types.
        '''
        return [self.childTypeFor(name) for name in self.container.properties]

    def childTypeFor(self, name):
        '''
        Provides the child type property for the provided name.
        
        @param name: string
            The name of the type property to provide.
        @return: TypeProperty
            The type property for the provided name.
        '''
        return typeFor(getattr(self.clazz, name))

class TypeModel(TypeContainer):
    '''
    Provides the type for the model.
    '''

    __slots__ = ()

    def __init__(self, clazz, container):
        '''
        Constructs the model type for the provided model.
        @see: Type.__init__
        
        @param clazz: class
            The model class associated with the model.
        @param container: Model
            The model that this type is constructed on.
        @param baseClass: class
            The base model class, a super type of the for class that needs to be considered valid for this model.
            This is used whenever a model is mapped to also validate classes that are API standard.
        '''
        assert isinstance(container, Model), 'Invalid model provided %s' % container
        TypeContainer.__init__(self, clazz, container)

    def childTypeId(self):
        '''
        Provides the child type property id.
        '''
        return self.childTypeFor(self.container.propertyId)

class TypeCriteria(TypeContainer):
    '''
    Provides the type for the criteria.
    '''

    __slots__ = ()

    def __init__(self, clazz, container):
        '''
        Constructs the criteria type for the provided criteria.
        @see: Type.__init__
        
        @param clazz: class
            The model class associated with the model.
        @param container: Criteria
            The criteria that this type is constructed on.
        '''
        assert isinstance(container, Criteria), 'Invalid criteria provided %s' % container
        TypeContainer.__init__(self, clazz, container)

class TypeQuery(TypeClass):
    '''
    Provides the type for the query.
    '''

    __slots__ = ('query', 'owner')

    def __init__(self, clazz, query, owner):
        '''
        Constructs the query type for the provided query.
        @see: TypeClass.__init__
        
        @param clazz: class
            The class associated with the query.
        @param query: Query
            The query that this type is constructed on.
        @param owner: TypeModel
            The type model that is this type query is owned by.
        '''
        assert isinstance(query, Query), 'Invalid query %s' % query
        assert isinstance(owner, TypeModel), 'Invalid owner %s' % owner
        TypeClass.__init__(self, clazz, False, False)

        self.query = query
        self.owner = owner

    def childTypes(self):
        '''
        Provides the child criteria entry types.
        
        @return: list[TypeCriteriaEntry]
            The criteria entry types.
        '''
        return [self.childTypeFor(name) for name in self.query.criterias]

    def childTypeFor(self, name):
        '''
        Provides the child criteria entry type for the provided name.
        
        @param name: string
            The name of the type property to provide.
        @return: TypeCriteriaEntry
            The criteria entry type for the name.
        '''
        return typeFor(getattr(self.clazz, name))

# --------------------------------------------------------------------

class TypeProperty(Type):
    '''
    This type is used to wrap a container property as types.
    '''

    __slots__ = ('parent', 'property', 'container', 'type')

    def __init__(self, parent, property, type=None):
        '''
        Constructs the property type for the provided property name and parent container type.
        @see: Type.__init__
        
        @param parent: TypeContainer
            The container of the property type.
        @param property: string
            The property name that this type represents.
        @param type: Type|None
            The type used by the property for validation, if not provided then it will use the type specified in the
            container.
        '''
        assert isinstance(parent, TypeContainer), 'Invalid container type %s' % parent
        assert isinstance(property, str), 'Invalid property %s' % property
        assert property in parent.container.properties, \
        'Property %s is not contained in container %s' % (property, parent.container)
        assert type is None or isinstance(type, Type), 'Invalid type %s' % type

        self.parent = parent
        self.property = property
        self.container = parent.container
        self.type = type or self.container.properties[property]
        Type.__init__(self, False, True)

    def isOf(self, type):
        '''
        @see: Type.isOf
        '''
        return self == type or self.type.isOf(type)

    def isValid(self, obj):
        '''
        @see: Type.isValid
        '''
        return self.type.isValid(obj)

    def __hash__(self):
        '''
        @see: Type.__hash__
        '''
        return hash((self.parent, self.property))

    def __eq__(self, other):
        '''
        @see: Type.__eq__
        '''
        if isinstance(other, self.__class__):
            return self.parent == other.parent and self.property == other.property
        return False

    def __str__(self):
        '''
        @see: Type.__str__
        '''
        return '%s.%s' % (self.parent, self.property)

class TypeModelProperty(TypeProperty):
    '''
    This type is used to wrap a model property as types.
    '''

    __slots__ = ()

    def __init__(self, parent, property, type=None):
        '''
        Constructs the property type for the provided property name and parent container type.
        @see: TypeProperty.__init__
        
        @param parent: TypeModel
            The model of the property type.
        '''
        assert isinstance(parent, TypeModel), 'Invalid model type %s' % parent
        TypeProperty.__init__(self, parent, property, type)

class TypeCriteriaEntry(TypeClass):
    '''
    This type is used to wrap a query criteria as types.
    '''

    __slots__ = ('parent', 'name', 'criteriaType', 'criteria')

    def __init__(self, parent, name):
        '''
        Constructs the criteria type for the provided criteria name and parent query type.
        @see: TypeClass.__init__
        
        @param parent: TypeQuery
            The query type of the criteria type.
        @param name: string
            The criteria name represented by the type.
        '''
        assert isinstance(parent, TypeQuery), 'Invalid query type %s' % parent
        assert isinstance(name, str), 'Invalid name %s' % name
        assert name in parent.query.criterias, \
        'Criteria %s is not contained in query %s' % (name, parent.query)

        self.parent = parent
        self.name = name
        self.criteriaType = typeFor(parent.query.criterias[name])
        assert isinstance(self.criteriaType, TypeCriteria), 'Invalid criteria class %s' % self.criteriaClass
        self.criteria = self.criteriaType.container
        TypeClass.__init__(self, self.criteriaType.clazz, False, False)

    def childTypes(self):
        '''
        Provides the child criteria entry types.
        
        @return: list[TypeProperty]
            The criteria entry types.
        '''
        return self.criteriaType.childTypes()

    def childTypeFor(self, name):
        '''
        Provides the child criteria entry type for the provided name.
        
        @param name: string
            The name of the type property to provide.
        @return: TypeProperty
            The criteria entry type for the name.
        '''
        return self.criteriaType.childTypeFor(name)

    def __hash__(self):
        '''
        @see: Type.__hash__
        '''
        return hash((self.parent, self.name))

    def __eq__(self, other):
        '''
        @see: Type.__eq__
        '''
        if isinstance(other, self.__class__):
            return self.parent == other.parent and self.name == other.name
        return False

    def __str__(self):
        '''
        @see: Type.__str__
        '''
        return '%s.%s' % (self.parent, self.name)

# --------------------------------------------------------------------

class TypeService(TypeClass):
    '''
    Provides the type for the service.
    '''

    __slots__ = ('service',)

    def __init__(self, clazz, service):
        '''
        Constructs the service type for the provided service.
        @see: TypeClass.__init__
        
        @param service: Service
            The service that this type is constructed on.
        '''
        assert isinstance(service, Service), 'Invalid service provided %s' % service
        TypeClass.__init__(self, clazz, False, False)

        self.service = service
