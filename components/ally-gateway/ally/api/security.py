'''
Created on Dec 18, 2012

@package: ally gateway
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides support for defining security roles.
'''
from ally.api.config import GET, INSERT, UPDATE, DELETE
from ally.api.operator.container import Service, Call
from ally.api.operator.type import TypeService
from ally.api.type import typeFor
from inspect import isclass, isfunction
from itertools import chain
import re

# --------------------------------------------------------------------

class SchemeError(Exception):
    '''
    Error raised when there is a problem with scheme configuration.
    '''

class SchemeRepository:
    '''
    Defines the security scheme.
    '''
    
    def __init__(self):
        '''
        Construct the scheme.
        '''
        self.indexers = {}
        self.schemes = {}
        self.descriptions = {}
        
    def __getitem__(self, name):
        '''
        Provides the scheme indexer for the provided name. If there is no scheme for the provided name one will be
        created.
        
        @param name: string
            The scheme name.
        @return: Indexer
            The indexer for the provided scheme name.
        '''
        assert isinstance(name, str), 'Invalid scheme name %s' % name
        indexer = self.indexers.get(name)
        if indexer is None: indexer = self.indexers[name] = SchemeIndexer(name, self)
        return indexer
    
class SchemeIndexer:
    '''
    Defines a scheme indexer object. This class facilitates the configuration of the security schemes.
    '''
    
    def __init__(self, name, scheme):
        '''
        Construct the security scheme indexer.
        
        @param name: string
            The scheme name.
         @param scheme: Scheme
            The scheme to index to.
        '''
        assert isinstance(name, str), 'Invalid name %s' % name
        assert isinstance(scheme, SchemeRepository), 'Invalid scheme %s' % scheme
        self.name = name
        self.schemes = scheme.schemes
        self.descriptions = scheme.descriptions
        
    def doc(self, description):
        '''
        Provide the documentation for the security schema represented by the indexer.
        
        @return: self
            This indexer for chaining purposes.
        '''
        assert isinstance(description, str), 'Invalid description %s' % description
        descriprions = self.descriptions.get(self.name)
        if descriprions is None: self.descriptions[self.name] = [description]
        else: descriprions.append(description)
        return self
        
    def addByName(self, clazz, pattern, *patterns):
        '''
        Add a new calls to the scheme.
        
        @param clazz: class
            The API service class.
        @param pattern: string|function
            The pattern used for extracting the calls from the service class to be added.
            If the pattern is a string it will be checked as a wild card against the call names from the service.
            If the pattern is a function then the function name will be used for extracting the call.
        @param patterns: arguments[string|integer|function]
            Additional patterns used for extracting the calls.
        @return: self
            This indexer for chaining purposes.
        '''
        assert isclass(clazz), 'Invalid service class %s' % clazz
        serviceType = typeFor(clazz)
        assert isinstance(serviceType, TypeService), 'Invalid service %s for class %s' % (serviceType, clazz)
        service = serviceType.service
        assert isinstance(service, Service), 'Invalid service %s' % service
        
        scheme = self.schemes.get(self.name)
        if scheme is None: scheme = self.schemes[self.name] = {}
        calls = scheme.get(serviceType)
        if calls is None: calls = scheme[serviceType] = set()
        for pattern in chain((pattern,), patterns):
            if isinstance(pattern, str):
                # We create the matcher based on the provided string
                matcher = re.compile('[a-zA-Z0-9_]*'.join([re.escape(e) for e in pattern.split('*')]))
                calls.update(call.name for call in service.calls if matcher.match(call.name))
            else:
                assert isfunction(pattern), 'Invalid pattern %s' % pattern
                for call in service.calls:
                    assert isinstance(call, Call)  # Just to have type hinting
                    if pattern.__name__ == call.name:
                        calls.add(call.name)
                        break
                else: raise SchemeError('Invalid function \'%s\' for service class \'%s\'' % (pattern, clazz))
        
        return self
        
    def addMethod(self, method, clazz, *clazzes):
        '''
        Adds all the calls from the provided API service classes that have the provided method(s).
        
        @param method: integer
            The method(s) of the calls to be added, for multiple methods just use bitwise or.
        @param clazz: class
            The API service class to add the calls from.
        @param clazzes: arguments[class]
            Additional API service classes to add the calls from.
        @return: self
            This indexer for chaining purposes.
        '''
        assert isinstance(method, int), 'Invalid method %s' % method
        assert isclass(clazz), 'Invalid class %s' % clazz
        serviceType = typeFor(clazz)
        assert isinstance(serviceType, TypeService), 'Invalid service %s for class %s' % (serviceType, clazz)
        
        serviceTypes = [serviceType]
        for clazz in clazzes:
            assert isclass(clazz), 'Invalid class %s' % clazz
            serviceType = typeFor(clazz)
            assert isinstance(serviceType, TypeService), 'Invalid service %s for class %s' % (serviceType, clazz)
            serviceTypes.append(serviceType)
        scheme = self.schemes.get(self.name)
        if scheme is None: scheme = self.schemes[self.name] = {}
        for serviceType in serviceTypes:
            service = serviceType.service
            assert isinstance(service, Service), 'Invalid service %s' % service
            calls = scheme.get(serviceType)
            if calls is None: calls = scheme[serviceType] = set()
            
            new = {call.name for call in service.calls if call.method & method}
            if not new: raise SchemeError('No calls found for service class \'%s\' for method %s' % 
                                          (serviceType.clazz, method))
            calls.update(new)
            
        return self
    
    def addGet(self, clazz, *clazzes):
        '''
        Adds all the calls from the provided API service classes that are of a GET method.
        
        @param clazz: class
            The API service class to add the calls from.
        @param clazzes: arguments[class]
            Additional API service classes to add the calls from.
        @return: self
            This indexer for chaining purposes.
        '''
        return self.addMethod(GET, clazz, *clazzes)
    
    def addModify(self, clazz, *clazzes):
        '''
        Adds all the calls from the provided API service classes that are of a INSERT|UPDATE|DELETE method.
        
        @param clazz: class
            The API service class to add the calls from.
        @param clazzes: arguments[class]
            Additional API service classes to add the calls from.
        @return: self
            This indexer for chaining purposes.
        '''
        return self.addMethod(INSERT|UPDATE|DELETE, clazz, *clazzes)
    
    def addAll(self, clazz, *clazzes):
        '''
        Adds all the calls from the provided API service classes.
        
        @param clazz: class
            The API service class to add the calls from.
        @param clazzes: arguments[class]
            Additional API service classes to add the calls from.
        @return: self
            This indexer for chaining purposes.
        '''
        assert isclass(clazz), 'Invalid class %s' % clazz
        serviceType = typeFor(clazz)
        assert isinstance(serviceType, TypeService), 'Invalid service %s for class %s' % (serviceType, clazz)
        
        serviceTypes = [serviceType]
        for clazz in clazzes:
            assert isclass(clazz), 'Invalid class %s' % clazz
            serviceType = typeFor(clazz)
            assert isinstance(serviceType, TypeService), 'Invalid service %s for class %s' % (serviceType, clazz)
            serviceTypes.append(serviceType)
        scheme = self.schemes.get(self.name)
        if scheme is None: scheme = self.schemes[self.name] = {}
        for serviceType in serviceTypes:
            service = serviceType.service
            assert isinstance(service, Service), 'Invalid service %s' % service
            calls = scheme.get(serviceType)
            if calls is None: calls = scheme[serviceType] = set()
            calls.update(call.name for call in service.calls)
            
        return self
