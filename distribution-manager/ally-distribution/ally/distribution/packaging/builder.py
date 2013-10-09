'''
Created on Oct 8, 2013
 
@package: ally.distribution
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Cristian Domsa
 
Functionality for building eggs.
'''
from configparser import ConfigParser
from os.path import join, dirname, isfile, normpath
from os import chdir
import logging
import sys
from copy import copy
from io import StringIO
import os

# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------
SETUP_CFG_FILE = 'setup.cfg'
SETUP_FILENAME = 'setup.py'


class Builder:
    
#     packageDir = str
#     #location of the current package
#     packageName = str
#     #name of the package
    
    def __init__(self, packageDir, packageName):
        
        assert isinstance(packageDir, str), 'Invalid package dir %s' % packageDir
        self.packageDir = packageDir
        self.packageName = packageName
        
        
    def getDistDir(self, packageDir):
        '''
        Return the distribution directory corresponding to the given package.
        '''
        if isfile(join(packageDir, SETUP_CFG_FILE)):
            p = ConfigParser()
            p.read(join(packageDir, SETUP_CFG_FILE))
            return normpath(join(packageDir, p.get('bdist_egg', 'dist_dir')))
        else:
            return dirname(join(packageDir, 'build'))
        
    def generateEggFile(self):
        packageDir = self.packageDir
        packageName = self.packageName

        # do a preclean
        chdir(packageDir)
        assert logging.info('*** BUILD %s' % packageName) or True
        #os.system('python3 {0} bdist_egg'.format(SETUP_FILENAME))
        assert logging.info("\n".rjust(79, '-')) or True
        print(self.getDistDir(self.packageDir))
#         assert logging.info(os.walk())
        