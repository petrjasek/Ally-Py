'''
Created on Oct 14, 2013

@package: support sqlalchemy
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the translation of SQL Alchemy errors to proper API input errors.
'''

import logging
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm.exc import NoResultFound

from ally.api.config import DELETE, GET
from ally.api.error import InputError, IdError
from ally.design.processor.attribute import defines, requires
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
from ally.internationalization import _
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
    
class Invoker(Context):
    '''
    The invoker context.
    '''
    # ---------------------------------------------------------------- Defined
    doError = defines(IDo, doc='''
    @rtype: callable(Exception)
    The error handler, specific for the invoker.
    ''')
    # ---------------------------------------------------------------- Required
    method = requires(int)

# --------------------------------------------------------------------

class ErrorTranslatorHandler(HandlerProcessor):
    '''
    Implementation for a processor that provides the translation of SQL Alchemy errors to proper API input errors.
    '''
    
    def __init__(self):
        super().__init__(Invoker=Invoker)

    def process(self, chain, register:Register, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Wraps the invoking and all processors after in a single transaction.
        '''
        assert isinstance(register, Register), 'Invalid register %s' % register
        if not register.invokers: return
        
        for invoker in register.invokers:
            assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
            invoker.doError = self.createGetHandler()

    # ----------------------------------------------------------------   
    
    def createHandler(self, invoker):
        '''Create the do error handler for the invoker.'''
        assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
        
        def doError(exc):
            '''Handle the error.'''
            assert isinstance(invoker, Invoker)
            if isinstance(exc, NoResultFound): iexc = IdError()
            elif isinstance(exc, IntegrityError):
                iexc = InputError(_('There is already an entity having this unique properties'))
            elif isinstance(exc, OperationalError):
                if invoker.method == DELETE: iexc = InputError(_('Cannot delete because is used'))
                elif invoker.method != GET: iexc = InputError(_('An entity relation identifier is not valid'))
                
            if exc is not None:
                log.info('SQL Alchemy handled exception occurred', exc_info=(type(exc), exc, exc.__traceback__))
                iexc.with_traceback(exc.__traceback__)
                exc = iexc
                
            raise exc
        return doError
