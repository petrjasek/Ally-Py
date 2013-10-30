'''
Created on Jan 12, 2012

@package: ally core
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the setup registry for the plugins.
'''

from collections import Iterable
from functools import partial

from __setup__.ally_core.decode import validations
from __setup__.ally_core.resources import services
from ally.api.validate import Validation
from ally.container.bind import processBinders
from ally.container.impl.proxy import proxyWrapFor


# --------------------------------------------------------------------
def registerService(service, binders=None):
    '''
    A listener to register the service.
    
    @param service: object
        The service instance to be registered.
    @param binders: list[Callable]|tuple(Callable)
        The binders used for the registered services.
    '''
    if binders:
        service = proxyWrapFor(service)
        if binders:
            for binder in binders: binder(service)
    services().append(service)

def addService(*binders):
    '''
    Create listener to register the service with the provided binders.
    
    @param binders: arguments[Callable]
        The binders used for the registered services.
    '''
    binders = processBinders(binders)
    assert binders, 'At least a binder is required, if you want the register without binders use the \'registerService\' function'
    return partial(registerService, binders=binders)

# --------------------------------------------------------------------

def registerValidations(*validators):
    '''
    Register the validations for the services.
    
    @param validations: arguments[Validation|Iterable(Validation)]
        The validations to register.
    '''
    assert validators, 'At least a validation is required'
    for validator in validators:
        if isinstance(validator, Validation): validations().append(validator)
        else:
            assert isinstance(validator, Iterable), 'Invalid validation %s' % validator
            if __debug__:
                for valid in validator: assert isinstance(valid, Validation), 'Invalid validation %s' % valid
            validations().extend(validator)
