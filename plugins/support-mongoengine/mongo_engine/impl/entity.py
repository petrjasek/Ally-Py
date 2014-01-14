'''
Created on Jun 23, 2011

@package: support mongoengine
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Mongo engine implementation for the generic ided or named entities API.
'''
 
from inspect import isclass
import logging
from mongoengine.document import Document

from ally.api.error import IdError
from ally.api.operator.type import TypeModel, TypeProperty, TypeQuery
from ally.api.type import typeFor
from ally.support.api.util_service import modelId
from mongo_engine.support.util_service import buildQuery, iterateCollection, \
    insertModel, updateModel


# --------------------------------------------------------------------
log = logging.getLogger(__name__)
 
# --------------------------------------------------------------------
 
class EntitySupportMongo:
    '''
    Provides support generic entity handling.
    '''
 
    def __init__(self, Mapped, QEntity=None, **mapping):
        '''
        Construct the entity support for the provided model class and query class.
         
        @param Mapped: class
            The mapped entity model class.
        @param QEntity: class|None
            The query mapped class if there is one.
        @param mapping: key arguments of columns
            The column mappings provided for criteria name in case they are needed, this is only used if a QEntity is
            provided.
        '''
        assert isclass(Mapped), 'Invalid class %s' % Mapped
        assert issubclass(Mapped, Document), 'Invalid mapped class %s' % Mapped
        model = typeFor(Mapped)
        assert isinstance(model, TypeModel), 'Invalid model class %s' % Mapped
        assert isinstance(model.propertyId, TypeProperty), 'Invalid model property id %s' % model.propertyId
         
        self.Entity = model.clazz
        self.EntityId = model.propertyId.name
        self.Mapped = Mapped
 
        if QEntity is not None:
            assert isclass(QEntity), 'Invalid class %s' % QEntity
            assert isinstance(typeFor(QEntity), TypeQuery), 'Invalid query entity class %s' % QEntity
            if __debug__:
                for name in mapping:
                    assert name in typeFor(QEntity).properties, 'Invalid criteria name \'%s\' for %s' % (name, QEntity)
            self._mapping = mapping
        else: assert not mapping, 'Illegal mappings %s with no QEntity provided' % mapping
        self.QEntity = QEntity
 
# --------------------------------------------------------------------
 
class EntityGetServiceMongo(EntitySupportMongo):
    '''
    Generic implementation for @see: IEntityGetPrototype
    '''
 
    def getById(self, identifier):
        '''
        @see: IEntityGetPrototype.getById
        '''
        item = self.Mapped.objects(**{self.EntityId: identifier}).first()
        if item is None: raise IdError(self.Entity)
        return item

class EntityFindServiceMongo(EntitySupportMongo):
    '''
    Generic implementation for @see: IEntityFindPrototype
    '''
 
    def getAll(self, **options):
        '''
        @see: IEntityFindPrototype.getAll
        '''
        return iterateCollection(self.Mapped.objects, self.EntityId, **options)
 
class EntityQueryServiceMongo(EntitySupportMongo):
    '''
    Generic implementation for @see: IEntityQueryPrototype
    '''
 
    def getAll(self, q=None, **options):
        '''
        @see: IEntityQueryPrototype.getAll
        '''
        assert self.QEntity is not None, 'No query available for this service'
        objects = self.Mapped.objects
        if q is not None:
            assert isinstance(q, self.QEntity), 'Invalid query %s' % q
            objects = buildQuery(objects, q, self.Mapped, **self._mapping)
        return iterateCollection(objects, self.EntityId, **options)
 
class EntityCRUDServiceMongo(EntitySupportMongo):
    '''
    Generic implementation for @see: IEntityCRUDPrototype
    '''
 
    def insert(self, entity):
        '''
        @see: IEntityCRUDPrototype.insert
        '''
        return modelId(insertModel(self.Mapped, entity))
 
    def update(self, entity):
        '''
        @see: IEntityCRUDPrototype.update
        '''
        updateModel(self.Mapped, entity)
 
    def delete(self, identifier):
        '''
        @see: IEntityCRUDPrototype.delete
        '''
        obj = self.Mapped.objects(**{self.EntityId: identifier}).first()
        if obj is not None: return obj.delete()
        return False
 
class EntityGetCRUDServiceMongo(EntityGetServiceMongo, EntityCRUDServiceMongo):
    '''
    Generic implementation for @see: IEntityGetCRUDPrototype
    '''
 
class EntityNQServiceMongo(EntityGetServiceMongo, EntityFindServiceMongo, EntityCRUDServiceMongo):
    '''
    Generic implementation for @see: IEntityNQPrototype
    '''

    def __init__(self, Entity):
        '''
        @see: EntitySupportAlchemy.__init__
        '''
        EntitySupportMongo.__init__(self, Entity)

class EntityServiceMongo(EntityGetServiceMongo, EntityQueryServiceMongo, EntityCRUDServiceMongo):
    '''
    Generic implementation for @see: IEntityPrototype
    '''

