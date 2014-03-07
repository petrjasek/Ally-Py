'''
Created on Jul 17, 2013

@package: ally core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides aid contexts and support functions that are generally used.
'''

from ally.core.spec.codes import Coded
from ally.design.processor.attribute import defines
from ally.design.processor.context import Context
from collections import Iterable

# --------------------------------------------------------------------

class ErrorResponse(Coded):
    '''
    The error response context.
    '''
    # ---------------------------------------------------------------- Defined
    failures = defines(list, doc='''
    @rtype: list[tuple(list[string], dictionary{string: object}, list[Context]]
    Contains the failure messages and definition contexts that have not been respected, on the first position the error
    messages on the second the data used for messages place holders and on the last the definition context that the
    error is targeting.
    ''')
    errors = defines(list, doc='''
    @rtype: list[tuple(string, Context, object, string, dictionary{string: object})]
    Contains the errors: on the first position the error code, on the second the decoding context,
    on the third position the value, on the forth position the error message and on the last position
    the data used for messages place holders.
    ''')

# --------------------------------------------------------------------

def addFailure(response, *items, **data):
    '''
    Adds a new failure message.
    
    @param response: Context
        The response context to add the error to.
    @param items: arguments[string|Iterable(string)|Context|Iterable(Context)]
        The error messages to add.
    @param data: key arguments
        Data to be used for messages place holders.
    '''
    assert items, 'At least one item is required'
    messages, contexts = [], []
    for item in items:
        if isinstance(item, str): messages.append(item)
        elif isinstance(item, Context): contexts.append(item)
        else:
            assert isinstance(item, Iterable), 'Invalid item %s' % item
            for it in item:
                if isinstance(it, str): messages.append(it)
                else:
                    assert isinstance(it, Context), 'Invalid item %s' % it
                    contexts.append(it)
    assert isinstance(response, ErrorResponse), 'Invalid context %s' % response
    
    if response.failures is None: response.failures = []
    response.failures.append((messages, data, contexts))

def addError(response, code, decoding, message, **data):
    '''
    Adds a new error message.
    
    @param response: Context
        The response context to add the error to.
    @param code: str
        The error code.
    @param decoding: Context
        The decoding context the error refers to.
    @param message: str
        The error message.
    @param data: key arguments
        Data to be used for messages place holders.
    '''
    assert isinstance(code, str), 'Invalid error code %s' % code
    assert isinstance(decoding, Context), 'Invalid decoding %s' % decoding
    assert isinstance(message, str), 'Invalid error message %s' % message
    if response.errors is None: response.errors = []
    response.errors.append((code, decoding, message, data))
