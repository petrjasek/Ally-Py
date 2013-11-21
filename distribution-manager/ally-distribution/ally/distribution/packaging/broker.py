'''
Created on Oct 31, 2013
 
@package: ally.distribution
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Cristian Domsa
 
Broker used for different actions needed by the distribution manager.
'''
from ally.distribution.util import getDirs, checkPathExists, createSymLink,\
    SETUP_FILENAME
from ally.distribution.packaging.packager import Packager
from ally.distribution.packaging.builder import Builder
from ally.distribution.packaging.publisher import Publisher
from ally.distribution.packaging.scanner import Scanner
import logging
import os
from ally.distribution.templates import SETUP_UI_TEMPLATE
from ally.container.ioc import injected

log = logging.getLogger(__name__)

action_worker = {'package' : Packager,
                 'build'   : Builder,
                 'publish' : Publisher,
                 'scan'    : Scanner,
                }

@injected
class Broker:
        
    actions = dict
    #actions to be performed with information
    path_ui = str
    #The path to the ui source folder
        
    def __init__(self):
        '''
        Constructor
        '''
        assert isinstance(self.actions, dict), 'Invalid actions dictionary %s' % self.actions
        assert isinstance(self.path_ui, str), 'Invalid ui plugins source path %s' % self.path_ui
        
    def preparePackage(self, path):
        '''
        Prepares the env for packaging, building, publishing
        '''
        #TODO: extact preparing from Packager and move it here
        
    def preparePluginUI(self, packagePath, packageName):
        '''
        Prepares the ui plugin for packaging, building, publishing.
            - writes setup.py if doesn't exist
            - creates path for mockup folder
            - creates symlink to the source folder
             
        '''
        checkPathExists(packagePath)
        symlink = os.path.join(packagePath, packageName)
        sourcePath = os.path.abspath(os.path.join(self.path_ui, packageName))
        createSymLink(source=sourcePath, dest=symlink)
        filename = os.path.join(packagePath, SETUP_FILENAME)
        if not os.path.isfile(filename):
            with open(filename, 'w') as f:
                f.write(SETUP_UI_TEMPLATE.format(packageName=packageName))
                f.close()
    
    def process(self): 
        '''
        Process all actions
        '''
        for action, targets in self.actions.items():
            for target in targets:
                checkPathExists(target['path'])
                packagesPaths = getDirs(target['path']) if not target['type']=='plugins-ui' else getDirs(self.path_ui)
                for packageName in packagesPaths:
                    packagePath = os.path.abspath(os.path.join(target['path'], packageName))
                    if target['type']=='plugins-ui': 
                        self.preparePluginUI(packagePath, packageName)
                    assert log.info('*** {name} *** {action} *** STARTED'.format(name=packageName, action=action)) or True
                    worker = action_worker[action](packageName, packagePath)
                    getattr(worker, action)()
                    assert log.info('*** {name} *** {action} *** DONE'.format(name=packageName, action=action)) or True