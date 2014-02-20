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

from .service import assemblyBuild, assemblyPublish, sources, path_build


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

FLAG_BUILD = 'build'
# Flag indicating the build eggs action.

# --------------------------------------------------------------------

@deploy.prepare
def prepare():
    options.credentials = None
    options.registerFlag(FLAG_BUILD)
    
    destSources = options.registerConfiguration(sources)
    destBuild = options.registerConfiguration(path_build)
    
    options.registerFlagLink(destBuild, FLAG_BUILD)

    parser.add_argument(metavar='folder', dest=destSources, nargs='+', help=getdoc(sources))
    parser.add_argument('-build', dest=destBuild, help=getdoc(path_build))
    parser.add_argument('-publish', dest='credentials', nargs=2, help=
                        'Expected two values to publish, on the first position the user name and on the second the password')

@deploy.start(priority=PRIORITY_FIRST)
def deploy():
    if options.isFlag(FLAG_BUILD):
        assemblyBuild().create().execute(FILL_ALL)
    else:
        if not options.credentials:
            log.error('Expected one of: -build or -publish')
            sys.exit()
            
        with open(os.path.join(os.path.expanduser('~'), '.pypirc'), 'w') as f:
            f.write(DEFAULT_PYPIRC % tuple(options.credentials))
            
        assemblyPublish().create().execute(FILL_ALL)
