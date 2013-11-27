'''
Created on Oct 29, 2013
 
@package: distribution manager
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Cristian Domsa
 
Collection of Utilities used in distribution manager.
'''
import os

IGNORE_DIRS = ['__pycache__']
PYTHON_CLI = 'python3.2'
SETUP_FILENAME = 'setup.py'
SETUP_CFG_FILENAME = 'setup.cfg'
INIT_FILENAME = '__init__.py'
BUILD_EGG = 'bdist_egg'

def getDirs(path):
    '''
    returns the list of directories filtering out IGNORE_DIRS
    '''
    children = os.listdir(path)
    return [child for child in children if os.path.isdir(os.path.join(path, child)) 
                                        and child not in IGNORE_DIRS]

def runCmd(path, command):
    '''
    runs an os command from the provided path
    '''
    os.chdir(path)
    os.system(command + ' > log.txt')
    