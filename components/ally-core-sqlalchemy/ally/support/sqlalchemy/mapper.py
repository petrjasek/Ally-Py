'''
Created on Jan 4, 2012

@package Newscoop
@copyright 2011 Sourcefabric o.p.s.
@license http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides support for SQL alchemy mapper that is able to link the alchemy with REST models.
'''

from .session import getSession
from ally.api.configure import modelFor, queryFor
from ally.api.operator import Model, Property, Query
from ally.api.type import TypeProperty, typeFor
from ally.exception import InputException, Ref
from ally.listener.binder_op import validateAutoId, validateRequired, \
    validateMaxLength, validateProperty, validateManaged, validateModelProperties, \
    validateModel, EVENT_VALID_UPDATE
from ally.support.util import Attribute
from inspect import isclass
from sqlalchemy import event
from sqlalchemy.orm import mapper
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.mapper import Mapper
from sqlalchemy.orm.properties import ColumnProperty
from sqlalchemy.schema import Table, Column, ForeignKey
from sqlalchemy.sql.expression import Join
from sqlalchemy.types import String
import functools

# --------------------------------------------------------------------

ATTR_SQL_MAPPER = Attribute(__name__, 'mapper')
ATTR_SQL_COLUMN = Attribute(__name__, 'column', Column)

# --------------------------------------------------------------------

def mapperSimple(modelClass, sql, **keyargs):
    '''
    Maps a table to a ally REST model. Use this instead of the classical SQL alchemy mapper since this will
    also provide to the model additional information extracted from the SQL alchemy configurations.
    
    @param modelClass: class
        The model class to be mapped with the provided sql table.
    @param sql: Table|Join|Select
        The table or join to map the model with.
    @param keyargs: key arguments
        This key arguments are directly delivered to the SQL alchemy @see mapper.
    @return: Mapper
        The obtained mapper.
    '''
    assert isclass(modelClass), 'Invalid model class %s' % modelClass
    model = modelFor(modelClass)
    assert isinstance(model, Model), 'Invalid class %s is not a model' % modelClass
    assert isinstance(sql, Table) or isinstance(sql, Join), 'Invalid SQL alchemy table/join %s' % sql
    
    typeProperties = {name:v for name, v in modelClass.__dict__.items() if isinstance(v, TypeProperty)}
    mapping = mapper(modelClass, sql, **keyargs)
    for name, typ in typeProperties.items():
        col = getattr(modelClass, name, None)
        if col: typeFor(col, typ)

    event.remove(mapping, 'load', _onLoad)
    event.listen(mapping, 'load', _onLoad)
    event.remove(mapping, 'after_insert', _onInsert)
    event.listen(mapping, 'after_insert', _onInsert)
    
    ATTR_SQL_MAPPER.set(model, mapping)
    return mapping

def mapperModelProperties(modelClass, mapping=None, exclude=None):
    '''
    Maps the model class properties to the provided SQL alchemy mapping.
    
    @param modelClass: class
        The model class to be mapped with the provided sql table.
    @param mapping: Mapper|None
        The mapper to link properties with. If not provided it will be extracted from the property model.
    @param exclude: list[string]
        A list of column names to be excluded from automatic validation.
    @return: Property|None
        The property id if found one.
    '''
    assert isclass(modelClass), 'Invalid model class %s' % modelClass
    model = modelFor(modelClass)
    assert isinstance(model, Model), 'Invalid class %s is not a model' % modelClass
    
    if not mapping: mapping = ATTR_SQL_MAPPER.get(model)
    assert isinstance(mapping, Mapper), 'Invalid mapper %s' % mapping
    
    properties = dict(model.properties)
    propertyId = None
    for cp in mapping.iterate_properties:
        assert isinstance(cp, ColumnProperty)
        if cp.key:
            prop = properties.pop(cp.key, None)
            if prop:
                assert isinstance(prop, Property)
                isExclude = False if exclude is None else prop.name in exclude
                column = cp.columns[0]
                assert isinstance(column, Column)
                #TODO: add checking if the column type is the same with the property, meaning that the alchemy
                # specification is same with REST
                columnFor(prop, column)
                if column.primary_key and column.autoincrement:
                    if propertyId:
                        raise AssertionError('Found another property id %s for model %s' % (prop, model))
                    propertyId = prop
                if not isExclude:
                    if propertyId == prop: validateAutoId(prop)
                    elif not column.nullable: validateRequired(prop)
                    if isinstance(column.type, String): validateMaxLength(prop, column.type.length)
                    if column.unique: validateProperty(prop, _onPropertyUniue)
                    if column.foreign_keys:
                        for fk in column.foreign_keys:
                            assert isinstance(fk, ForeignKey)
                            validateProperty(prop, functools.partial(_onPropertyForeignKey, fk.column), index=5)
    if not propertyId: raise AssertionError('No id found for model %s' % model)
    model.propertyId = propertyId
    
    for prop in properties.values():
        if exclude is None or prop.name not in exclude: validateManaged(prop)
    
    validateModelProperties(model)
    
    return propertyId

def mapperModel(modelClass, sql, exclude=None, hasPartialUpdate=True, **keyargs):
    '''
    Maps a table to a ally REST model. Use this instead of the classical SQL alchemy mapper since this will
    also provide to the model additional information extracted from the SQL alchemy configurations. Use
    this mapper to also add validations for updating and inserting on the model.
    
    @param modelClass: class
        The model class to be mapped with the provided sql table.
    @param sql: Table|Join|Select
        The table or join to map the model with.
    @param exclude: list[string]
        A list of column names to be excluded from automatic validation.
    @param hasPartialUpdate: boolean
        If True it will add support for partial updates to the model.
    @param keyargs: key arguments
        This key arguments are directly delivered to the SQL alchemy @see mapper.        
    '''
    assert isclass(modelClass), 'Invalid model class %s' % modelClass
    model = modelFor(modelClass)
    assert isinstance(model, Model), 'Invalid class %s is not a model' % modelClass
    
    mapperSimple(modelClass, sql, **keyargs)
    
    propertyId = mapperModelProperties(modelClass, exclude)
    
    if hasPartialUpdate: supportForPartialUpdate(TypeProperty(model, propertyId))
    
    return modelClass

# --------------------------------------------------------------------

def mapperQuery(queryClass, sql):
    '''
    Maps a table to a ally REST query. This will provide the ability to use the 
    
    @param queryClass: class
        The query class to be mapped with the provided sql table.
    @param sql: Table|Join|Mapped Model
        The table, join or a mapped model class to map the query with.
    '''
    assert isclass(queryClass), 'Invalid query class %s' % queryClass
    model = modelFor(sql)
    if isinstance(model, Model):
        sql = ATTR_SQL_MAPPER.get(model, None)
        assert sql is not None, 'Invalid model %s, it has not been mapped yet' % model
    if isinstance(sql, Mapper):
        columns = [(cp.key, cp.columns[0]) for cp in sql.iterate_properties if cp.key]
    else:
        assert isinstance(sql, Table) or isinstance(sql, Join), 'Invalid SQL alchemy table/join %s' % sql
        columns = [(column.key, column) for column in sql.columns if column.key]
    query = queryFor(queryClass)
    assert isinstance(query, Query), 'Invalid class %s is not a query' % queryClass
    criteriaEntries = {name.lower():crtEntry for name, crtEntry in query.criteriaEntries.items()}
    for name, column in columns:
        assert isinstance(column, Column)
        crtEntry = criteriaEntries.get(name.lower(), None)
        if crtEntry: columnFor(crtEntry, column)
    return queryClass

# --------------------------------------------------------------------

def supportForPartialUpdate(propertyId, mapping=None):
    '''
    Provides support for partial updates.
    
    @param param: propertyId
        The type property used in identifying the entity primary id.
    @param mapping: Mapper|None
        The mapper used to query database entities, if not provided it will be extracted from the property
        model.
    '''
    typ = typeFor(propertyId)
    assert isinstance(typ, TypeProperty), 'Invalid type property %s' % propertyId
    
    if not mapping: mapping = ATTR_SQL_MAPPER.get(typ.model)
    assert isinstance(mapping, Mapper), 'Invalid mapper %s' % mapping
        
    validateModel(typ.model, functools.partial(_onModelMerge, mapping, typ.property), key=EVENT_VALID_UPDATE)

# --------------------------------------------------------------------

def _onDBUpdate(targetIndex, *args):
    '''
    FOR INTERNAL USE.
    Listener method called when an database mapped instance is updated by SQL alchemy.
    '''
    target = args[targetIndex]
    model = modelFor(target)
    if model:
        assert isinstance(model, Model)
        for name, prop in model.properties.items():
            if name in target.__dict__:
                assert isinstance(prop, Property)
                if not prop.has(target): prop.hasSet(target)

_onLoad = functools.partial(_onDBUpdate, 0)
_onInsert = functools.partial(_onDBUpdate, 2)

# --------------------------------------------------------------------

def _onPropertyUniue(entity, model, prop, errors):
    assert isinstance(model, Model)
    assert isinstance(model.propertyId, Property)
    assert isinstance(prop, Property)
    if prop.has(entity):
        val = prop.get(entity)
        if val is not None:
            assert isinstance(model, Model)
            column = getattr(model.modelClass, prop.name)
            try:
                db = getSession().query(model.modelClass).filter(column == val).one()
            except NoResultFound: return
            if model.propertyId.get(db) != model.propertyId.get(entity):
                errors.append(Ref(_('Already an entry with this value'), ref=column))
                return False
    
def _onPropertyForeignKey(foreignColumn, entity, model, prop, errors):
    assert isinstance(prop, Property)
    if prop.has(entity):
        val = prop.get(entity)
        if val is not None:
            count = getSession().query(foreignColumn).filter(foreignColumn == val).count()
            if count == 0:
                errors.append(Ref(_('Unknown foreign id'), model=model, property=prop))
                return False

def _onModelMerge(mapper, propertyId, entity, model):
    assert isinstance(model, Model)
    assert isinstance(propertyId, Property)
    if model.isPartial(entity):
        session = getSession()
        aq = session.query(mapper).filter(columnFor(propertyId) == propertyId.get(entity))
        try: dbEntity = aq.one()
        except NoResultFound: raise InputException(Ref(_('Unknown id'), model=model, property=propertyId))
        session.expunge(dbEntity)
        model.merge(entity, dbEntity)
        
# --------------------------------------------------------------------

def columnFor(obj, column=None):
    '''
    If the column is provided it will be associate with the obj, if the column is not provided than this 
    function will try to provide if it exists the column associated with the obj.
    
    @param obj: object|class
        The class to associate or extract the model.
    @param properties: Properties
        The properties to associate with the obj.
    @return: Properties|None
        If the properties has been associate then the return will be none, if the properties is being extracted 
        it can return either the Properties or None if is not found.
    '''
    if column is None: return ATTR_SQL_COLUMN.get(obj, None)
    assert not ATTR_SQL_COLUMN.hasOwn(obj), 'Already has a column %s' % obj
    ATTR_SQL_COLUMN.set(obj, column)
    return column
