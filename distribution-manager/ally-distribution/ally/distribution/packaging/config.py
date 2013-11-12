'''
Created on Oct 31, 2013
 
@package: ally.distribution
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Cristian Domsa
 
Provides configuration mechanisms used in distribution manager.
'''

from configparser import SafeConfigParser
import os

class Config:
    '''
    Class used for generating configuration files.
    '''
    packagePath = str
    #path to the current package
    packageName = str
    #The name of the current package
    
    def __init__(self):
        '''
        do nothing
        '''
        
    def _generateParser(self, configOptions):
        '''
        Generates content to be written from configOptions dictionary
        '''
        parser = SafeConfigParser()
        for section, content in configOptions.items():
            parser.add_section(section)
            if isinstance(content, dict):
                for option, value in content.items():
                    parser.set(section, option, value)
        return parser 
        
    def writeCfgFiles(self, configOptions):
        '''
        fills the configuration object with data from configOptions and writes the configuration file   
        '''
        os.chdir(self.packagePath)
        for filename, content in configOptions.items():
            if os.path.isfile(filename): return 1
            with open(filename, 'w') as f:
                parser = self._generateParser(content)
                parser.write(f)
            f.close()