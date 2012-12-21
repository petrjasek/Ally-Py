'''
Created on Dec 18, 2012

@package: ally gateway
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides unit testing for the API security scheme.
'''

# Required in order to register the package extender whenever the unit test is run.
if True:
    import package_extender
    package_extender.PACKAGE_EXTENDER.setForUnitTest(True)

# --------------------------------------------------------------------

import unittest
from ally.api.config import model, service, call, GET, INSERT, UPDATE
from ally.api.security import SchemeRepository, SchemeError

# --------------------------------------------------------------------

@model(id='Key')
class Model:
    Key = str
    Name = str

@service
class IService:

    @call
    def getModel(self, key:Model.Key) -> Model:
        '''
        '''

# --------------------------------------------------------------------

class TestScheme(unittest.TestCase):

    def testSuccess(self):
        scheme = SchemeRepository()
        
        scheme['test1'].addMethod(GET, IService)
        services = {typ.clazz.__name__:calls for typ, calls in scheme.schemes['test1'].items()}
        self.assertEqual(services, {'IService':{'getModel'}})
        
        self.assertRaises(SchemeError, scheme['test2'].addMethod, INSERT | UPDATE, IService)
        
        scheme['test3'].addByName(IService, '*')
        services = {typ.clazz.__name__:calls for typ, calls in scheme.schemes['test3'].items()}
        self.assertEqual(services, {'IService':{'getModel'}})
        
        scheme['test4'].addByName(IService, 'getModel')
        services = {typ.clazz.__name__:calls for typ, calls in scheme.schemes['test4'].items()}
        self.assertEqual(services, {'IService':{'getModel'}})
        
        scheme['test5'].addByName(IService, IService.getModel)
        services = {typ.clazz.__name__:calls for typ, calls in scheme.schemes['test5'].items()}
        self.assertEqual(services, {'IService':{'getModel'}})

# --------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
