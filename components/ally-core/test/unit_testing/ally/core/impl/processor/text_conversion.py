'''
Created on Jun 21, 2012

@package: ally core
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Text conversion testing.
'''

# Required in order to register the package extender whenever the unit test is run.
if True:
    import package_extender
    package_extender.PACKAGE_EXTENDER.setForUnitTest(True)

# --------------------------------------------------------------------

from ally.container import ioc
from ally.core.impl.processor.text_conversion import ConversionSetHandler, \
    Content
from ally.core.spec.resources import Normalizer, Converter
from ally.design.processor import Chain
import unittest

# --------------------------------------------------------------------

class TestTextConversion(unittest.TestCase):

    def testTextConversion(self):
        handler = ConversionSetHandler()
        handler.normalizer = Normalizer()
        handler.converter = Converter()
        ioc.initialize(handler)

        requestCnt, responseCnt = Content(), Content()
        chain = Chain([handler.process])
        chain.process(requestCnt=requestCnt, responseCnt=responseCnt)

        self.assertTrue(chain.isConsumed())
        self.assertEqual(handler.normalizer, requestCnt.normalizer)
        self.assertEqual(handler.normalizer, responseCnt.normalizer)

        self.assertEqual(handler.converter, responseCnt.converter)
        self.assertEqual(handler.converter, responseCnt.converter)


# --------------------------------------------------------------------

if __name__ == '__main__': unittest.main()
