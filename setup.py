'''
Created on Feb 28, 2014

@package: ally
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the means of installing as a development environment through git.
'''

from distutils.errors import DistutilsOptionError
from os.path import os
import pip
from pip.vcs.git import Git
from setuptools import setup
from setuptools.command.develop import develop
import sys
from urllib.parse import parse_qs


# --------------------------------------------------------------------
class AllyDevelop(develop):
    ''' Provides the ally packages development install.'''
    
    description = 'install ally packages in \'development mode\''
    
    user_options = develop.user_options + [
        ('add-git=', None, 'Additional git repositories to fetch ally packages, in order to provide more then one git repository '\
         'then provide a pipe \'|\' separator between the git URLs. The git URLs need to be identical to those in \'-e\' command.'),
        ('install=', None, 'The name of the package to be installed from the git repositories.')
        ]
    
    def initialize_options(self):
        self.add_git = None
        self.install = None
        super().initialize_options()
    
    def run(self):
        repositories = [self.egg_path]
        root = os.path.dirname(self.egg_path)
        if self.add_git:
            for path in self.add_git.split('|'):
                badFragment = False
                fragments = path.split('#')
                if len(fragments) == 2:
                    fragments = parse_qs(fragments[1])
                    egg = fragments.get('egg')
                    if not egg: badFragment = True
                    else: egg = os.path.join(root, egg[0])
                else: badFragment = True
                
                if badFragment:
                    raise DistutilsOptionError('Missing the git URL egg fragment ex:\'https://github.com/../somwhere#eqq=somwhere\'')
                
                Git(path).obtain(egg)
                repositories.append(egg)
                
        sys.path.append(os.path.join(self.egg_path, 'components', 'ally'))
        sys.path.append(os.path.join(self.egg_path, 'distribution-manager', 'ally-distribution'))
        try: import ally_distribution
        except: raise DistutilsOptionError('Cannot locate the \'ally_distribution\' package.')
        
        argv = [None]
        for folder in repositories:
            pkg = os.path.join(folder, 'setup.pkg')
            if os.path.isfile(pkg):
                with open(pkg, 'r') as f:
                    for line in f.readlines(): argv.append(os.path.join(folder, *line.strip().split('/')))
            else: argv.append(os.path.join(folder, '*'))
        
        argv.append('-build')
        argv.append(root)
        argv.append('--dev')
        sys.argv = argv
        ally_distribution.__distribution__()
        
        if self.install:
            sys.argv = [None, 'install', self.install, '--upgrade', '--find-links', 'file://%s' % root]
            pip.main()
        
setup(platforms=['all'],
      license='GPL v3',
      url='http://www.sourcefabric.org/en/superdesk/',
      author='Gabriel Nistor',
      author_email='gabriel.nistor@sourcefabric.org',
      description='Provides the installation using git.',
      keywords=['ally', 'installation', 'git'],
      cmdclass={'develop': AllyDevelop}
      )
