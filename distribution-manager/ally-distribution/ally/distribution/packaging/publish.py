'''
Created on Oct 10, 2013
 
@package: pypi publish
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Cristian Domsa
 
Simple implementation for publishing components/plugins on pypi.
'''
import os

class Publisher:
    
    def __init__(self, publish_list):
        
        self.publish_list = publish_list
        
    def publish(self):
        '''
        Register and update a pypi component
        '''
        for path in self.publish_list:
            os.chdir(path)
            os.system('python3 setup.py register -r pypitest sdist bdist_egg upload -r pypitest')