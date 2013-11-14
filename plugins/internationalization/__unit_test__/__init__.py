'''
Created on Jun 1, 2011

@package: internationalization
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Nistor Gabriel

Contains the unit tests.
'''
import requests
import unittest
# 
# class POFileTest:
#     
#     def setUp(self):
#         '''
#         Setup the environment for testing
#         '''
#     def tearDown(self):
#         '''
#         Cleaning after tests are run
#         '''
class TestInternationalization(unittest.TestCase):
    def test_get_existing_PO(self):
        '''
        Test verifying getting an existing PO file.
        '''
        r = requests.get('http://localhost:8080/resources/Localization/TemplatePO/vasile/')
        assert r.status_code == 200
        assert r.text == '{"Reference":"/content/cache/locale/vasile.pot"}'
        
    def test_get_nonexisting_PO(self):
        '''
        Test verifying getting an nonexisting PO file.
        '''
        r = requests.get('http://localhost:8080/resources/Localization/Language/en/PO/ion/')
        assert r.status_code == 400
        assert 'Unable to find PO file or template for ion with locale en' in r.text 
        assert 'Status: 400 Input error' in r.text
        
    def test_get_nonexisting_locale_PO(self):
        '''
        Test verifying getting an nonexisting locale PO file.
        '''
        r = requests.get('http://localhost:8080/resources/Localization/Language/fr/PO/ion/')
        assert r.status_code == 400
        assert 'Unable to find PO file or template for ion with locale en' in r.text 
        assert 'Status: 400 Input error' in r.text
        