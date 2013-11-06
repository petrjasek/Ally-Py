'''
Created on Oct 31, 2013
 
@package: ally.distribution
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Cristian Domsa
 
Broker used for different actions needed by the distribution manager.
'''
from ally.distribution.util import getDirs, checkPathExists, createSymLink
from ally.distribution.packaging.packager import Packager
from ally.distribution.packaging.builder import Builder
from ally.distribution.packaging.publisher import Publisher
from ally.distribution.packaging.scanner import Scanner
import logging
import os

log = logging.getLogger(__name__)

action_worker = {'package' : Packager,
                 'build'   : Builder,
                 'publish' : Publisher,
                 'scan'    : Scanner,
                }

class Broker:
        
    actions = dict
    #TODO: update description
    #actions to be performed with information
    plugins_ui_path = str
    #The path to the plugins-ui folder
        
    def __init__(self):
        '''
        Constructor
        '''

    def preparePackage(self, path):
        '''
        Prepares the env for packaging, building, publishing
        '''
        #TODO: extact preparing from Packager and move it here
        
    def preparePluginsUI(self):
        '''
        Prepares the plugins-ui folder for packaging, building, publishing
        '''
    
    def process(self): 
        '''
        Process all actions
        '''
        for action, targets in self.actions.items():
            for target in targets:
                packagesPaths = getDirs(target['path'])
                if target['type']=='plugins-ui':
                    checkPathExists(self.plugins_ui_path)
                for packageName in packagesPaths:
                    sourcePath = os.path.abspath(os.path.join(target['path'], packageName))
                    packagePath = os.path.abspath(os.path.join(self.plugins_ui_path, packageName))
                    if target['type']=='plugins-ui': 
                        checkPathExists(packagePath)
                        createSymLink(source=sourcePath, dest=packagePath)
                    assert log.info('*** {name} *** {action} *** STARTED'.format(name=packageName, action=action)) or True
                    worker = action_worker[action]()
                    worker.packagePath = packagePath
                    worker.packageName = packageName
                    getattr(worker, action)()
                    assert log.info('*** {name} *** {action} *** DONE'.format(name=packageName, action=action)) or True