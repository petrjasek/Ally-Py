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
from ally.api.operator.type import TypeModel
from sqlalchemy.orm.session import Session
from ally.container.impl.proxy import Proxy
from sql_alchemy.core.impl.processor.binder.session import BindSessionHandler
from sql_alchemy.support.session import beginWith, openSession, endCurrent, commit

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
        if not decoding.validations: return
        
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
                decoding.doEnd = self.createEnd(decoding, validation, decoding.doEnd, sessionCreator)
            else: validations.append(validation)
        
        decoding.validations = validations
    
    # ----------------------------------------------------------------
    
    def createEnd(self, decoding, validation, wrapped, sessionCreator):
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
            assert getattr(mvalue, '_ally_type', None) is not None and isinstance(mvalue._ally_type, TypeModel), \
            'Invalid model %s' % mvalue
            
            beginWith(sessionCreator)
            session = openSession()
            assert isinstance(session, Session), 'Invalid session %s' % session
            
            try:
                exists = True
                sql = session.query(validation.mapper)
                for prop in validation.properties:
                    assert isinstance(prop, InstrumentedAttribute), 'Invalid property %s' % prop
                    value = getattr(mvalue, prop.key)
                    if value is None:
                        exists = False
                        break
                    sql = sql.filter(prop == value)
                
                if exists and sql.count() > 0:
                    for prop in validation.properties:
                        propType = prop.class_._ally_reference[prop.key]._ally_type
                        addError(target, 'unique', propType, _('Unique constraint failed'))
                if wrapped:
                    wrapped(target)
            finally:
                endCurrent(commit)
        
        return doEnd
