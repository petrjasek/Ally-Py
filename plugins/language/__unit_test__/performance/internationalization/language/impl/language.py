'''
Created on Feb 21, 2012

@package: superdesk
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides unit testing for the language module.
'''

# Required in order to register the package extender whenever the unit test is run.
if True:
    import package_extender
    package_extender.PACKAGE_EXTENDER.setForUnitTest(True)

# --------------------------------------------------------------------

from ally.container import ioc
from profile import Profile
from internationalization.language.api.language import QLanguage
from internationalization.language.impl.language import LanguageServiceBabelAlchemy
import pstats
import unittest

# --------------------------------------------------------------------

class TestLanguage(unittest.TestCase):
        
    def testPerformance(self):
        languageService = LanguageServiceBabelAlchemy()
        ioc.initialize(languageService)
        
        profile = Profile()
        qlang = QLanguage(name='rom%')
        try:
            profile = profile.runctx("languageService.getAllAvailable(['en'], 0, 10, qlang)", globals(), locals())
        except SystemExit: pass
        pstats.Stats(profile).sort_stats('time', 'cum').print_stats()
        
# --------------------------------------------------------------------
  
if __name__ == '__main__': unittest.main()
