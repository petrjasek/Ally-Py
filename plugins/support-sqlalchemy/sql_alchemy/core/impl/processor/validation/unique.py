'''
Created on Mar 11, 2014

@package: support sqlalchemy
@copyright: 2014 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mugur Rus

Implementation of unique validator.
'''

from ally.api.validate import Unique
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
from ally.support.util_spec import IDo
from ally.internationalization import _
from ally.core.impl.processor.decoder.base import addError
from sql_alchemy.support.mapper import InstrumentedAttribute
from ally.api.operator.type import TypeProperty
from sqlalchemy.orm.session import Session
from ally.container.impl.proxy import Proxy
from sql_alchemy.core.impl.processor.binder.session import BindSessionHandler
from sql_alchemy.support.session import beginWith, openSession, endCurrent, commit
from ally.api.config import UPDATE, DELETE, INSERT
from sqlalchemy.orm.exc import NoResultFound
import logging

# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Decoding(Context):
    '''
    The model decoding context.
    '''
    # ---------------------------------------------------------------- Defined
    doEnd = defines(IDo, doc='''
    @rtype: callable(target)
    Required to be triggered in order to end the decoding.
    @param target: Context
        Target context object that the decoding ends on.
    ''')
    # ---------------------------------------------------------------- Required
    validations = requires(list)
    doSet = requires(IDo)

class Invoker(Context):
    '''
    The invoker context.
    '''
    # ---------------------------------------------------------------- Optional
    implementation = requires(object)
    method = requires(int)

# --------------------------------------------------------------------

class ValidateUnique(HandlerProcessor):
    '''
    Implementation for a handler that provides the unique validation.
    '''
    
    def process(self, chain, decoding:Decoding, invoker:Invoker, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Process the unique validation.
        '''
        assert isinstance(decoding, Decoding), 'Invalid decoding %s' % decoding
        if not decoding.validations or invoker.method == DELETE: return
        
        sessionCreator = None
        assert isinstance(invoker.implementation, Proxy), 'Invalid service %s' % invoker.implementation
        for handler in invoker.implementation._proxy_handlers:
            if isinstance(handler, BindSessionHandler):
                sessionCreator = handler.sessionCreator
                break
        assert sessionCreator is not None, 'Required a session creator'
        
        validations = []
        for validation in decoding.validations:
            if isinstance(validation, Unique):
                assert isinstance(validation, Unique)
                decoding.doEnd = self.createEnd(decoding, validation, decoding.doEnd, sessionCreator, invoker.method)
            else: validations.append(validation)
        
        decoding.validations = validations
    
    # ----------------------------------------------------------------
    
    def createEnd(self, decoding, validation, wrapped, sessionCreator, method):
        '''
        Create the do end for unique validation.
        '''
        assert isinstance(decoding, Decoding), 'Invalid decoding %s' % decoding
        
        def doEnd(target):
            '''
            Do end the unique validation.
            '''
            assert isinstance(target, Context), 'Invalid target %s' % target
            mvalue = decoding.doGet(target)
            assert mvalue, 'Invalid model %s' % mvalue
            if wrapped: wrapped(target)
            
            missing = list()
            for attr in validation.attributes:
                assert isinstance(attr, InstrumentedAttribute), 'Invalid attribute %s' % attr
                if validation.model.properties[attr.key] not in mvalue:
                    missing.append(attr)
            
            beginWith(sessionCreator)
            session = openSession()
            assert isinstance(session, Session), 'Invalid session %s' % session
            
            propId = validation.model.propertyId
            assert isinstance(propId, TypeProperty), 'Invalid identifier property %s' % propId
            attrId = getattr(validation.mapper.class_, propId.name)
            if missing and method == UPDATE:
                sql = session.query(validation.mapper).filter(attrId == getattr(mvalue, attrId.key))
                try:
                    rvalue = sql.one()
                    assert isinstance(rvalue, validation.mapper.class_), 'Invalid mapped %s' % rvalue
                    for attr in missing:
                        setattr(mvalue, attr.key, getattr(rvalue, attr.key))
                except NoResultFound:
                    log.debug('Invalid property id %s for model %s', getattr(mvalue, attrId.key), str(validation.model))
                    return
            
            try:
                sql = session.query(validation.mapper)
                if method == UPDATE:
                    sql = sql.filter(attrId != getattr(mvalue, attrId.key))
                for attr in validation.attributes:
                    assert isinstance(attr, InstrumentedAttribute), 'Invalid property %s' % attr
                    val = getattr(mvalue, attr.key)
                    if val is None and method == INSERT and attr.property.columns[0].default is not None:
                        val = attr.property.columns[0].default.arg
                    sql = sql.filter(attr == val)
                
                if sql.count() > 0:
                    for attr in validation.attributes:
                        prop = validation.model.properties[attr.key]
                        addError(target, 'unique', prop, _('Unique constraint failed'))
            finally:
                endCurrent(commit)
        
        return doEnd
