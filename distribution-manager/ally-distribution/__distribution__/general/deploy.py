'''
Created on Oct 2, 2013

@package: ally distribution
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the setup for general resources.
'''

from pydoc import getdoc

from ally.container import deploy
from distribution import parser, options

from .service import path_sources, path_build


# --------------------------------------------------------------------
@deploy.prepare
def prepare():
    pathSources = options.registerConfiguration(path_sources)
    pathBuild = options.registerConfiguration(path_build)

    parser.add_argument('-sources', dest=pathSources, help=getdoc(path_sources))
    parser.add_argument('-build', dest=pathBuild, help=getdoc(path_build))
