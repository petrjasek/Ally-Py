'''
Created on Oct 2, 2013

@package: ally distribution
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the setup for general resources.
'''

from distutils.config import DEFAULT_PYPIRC
import logging
import os
from pydoc import getdoc
import sys

from ally.design.priority import PRIORITY_FIRST
from ally.design.processor.execution import FILL_ALL

from ally.container import deploy
from ally_distribution import parser, options

from .service import assemblyBuild, assemblyPublish, indexPip, sources, path_build, root_uri, build_cmds


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

FLAG_BUILD = 'build'
# Flag indicating the build eggs action.
FLAG_ONLY_EGG = 'egg'
# Flag indicating the build eggs action.
FLAG_ONLY_DIST = 'dist'
# Flag indicating the build eggs action.
FLAG_PIP_INDEX = 'pip_index'
# Flag indicating that the source should have created pip index file.

# --------------------------------------------------------------------

@deploy.prepare
def prepare():
    options.credentials = None
    options.registerFlag(FLAG_BUILD)
    options.registerFlag(FLAG_PIP_INDEX)
    options.registerFlag(FLAG_ONLY_EGG)
    options.registerFlag(FLAG_ONLY_DIST)
    
    destSources = options.registerConfiguration(sources)
    destBuild = options.registerConfiguration(path_build)
    destRootURI = options.registerConfiguration(root_uri)
    
    options.registerFlagLink(destBuild, FLAG_BUILD)
    options.registerFlagLink(destRootURI, FLAG_PIP_INDEX)

    parser.add_argument(metavar='folder', dest=destSources, nargs='+', help=getdoc(sources))
    parser.add_argument('-build', dest=destBuild, help=getdoc(path_build))
    parser.add_argument('-publish', dest='credentials', nargs=2, help=
                        'Expected two values to publish, on the first position the user name and on the second the password')
    parser.add_argument('-pip-index', dest=destRootURI, help=
                'Provide this flag in order to create a pip index html file that can be used for web servers.\n%s' % getdoc(root_uri))
    
    parser.add_argument('--egg', dest=FLAG_ONLY_EGG, action='store_true',
                        help='Provide this flag in order to build only the eggs.')
    parser.add_argument('--dist', dest=FLAG_ONLY_DIST, action='store_true',
                        help='Provide this flag in order to build only source distribution packages.')

@deploy.start(priority=PRIORITY_FIRST)
def deploy():
    if options.isFlag(FLAG_BUILD):
        if options.isFlag(FLAG_ONLY_EGG): build_cmds().append('bdist_egg')
        elif options.isFlag(FLAG_ONLY_DIST): build_cmds().append('sdist')
        else:
            build_cmds().append('bdist_egg')
            build_cmds().append('sdist')
            
        assemblyBuild().create().execute(FILL_ALL)
    elif options.isFlag(FLAG_PIP_INDEX):
        indexPip()()
    else:
        if not options.credentials:
            log.error('Expected one of: -build, -publish or -pip-index')
            sys.exit()
            
        with open(os.path.join(os.path.expanduser('~'), '.pypirc'), 'w') as f:
            f.write(DEFAULT_PYPIRC % tuple(options.credentials))
            
        assemblyPublish().create().execute(FILL_ALL)
