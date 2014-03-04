'''
Created on Mar 4, 2014

@package: ally distribution
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides versioning for development source distribution.
'''

from collections import deque
import logging
import os
import re

from ally.container.ioc import injected
from ally.design.processor.attribute import requires
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Distribution(Context):
    '''
    The distribution context.
    '''
    # ---------------------------------------------------------------- Required
    packages = requires(list)
    
class Package(Context):
    '''
    The package context.
    '''
    # ---------------------------------------------------------------- Required
    path = requires(str)
    name = requires(str)
    arguments = requires(dict)

# --------------------------------------------------------------------

@injected
class VersionerDevHandler(HandlerProcessor):
    '''
    Implementation for a processor that provides versioning for development source distribution.
    '''
    
    pathBuild = str
    # The location where the builds are placed. 
    exclude = '(__pycache__)|(\.\w+)'
    # The regex used for excluding folder or files from the timestamp search.
    attributeVersion = 'version'
    # The name for the version attribute.
    
    def __init__(self):
        assert isinstance(self.pathBuild, str), 'Invalid build path %s' % self.pathBuild
        assert isinstance(self.exclude, str), 'Invalid exclude %s' % self.exclude
        assert isinstance(self.attributeVersion, str), 'Invalid version attribute %s' % self.attributeVersion
        super().__init__(Package=Package)
        
        self._exc = re.compile(self.exclude)

    def process(self, chain, distribution:Distribution, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Provides the package build.
        '''
        assert isinstance(distribution, Distribution), 'Invalid distribution %s' % distribution
        if not distribution.packages: return
        
        available, packages = set(os.listdir(self.pathBuild)), []
        for package in distribution.packages:
            assert isinstance(package, Package), 'Invalid package %s' % package
            
            paths, last = deque(), None
            paths.append(package.path)
            while paths:
                path = paths.popleft()
                for name in os.listdir(path):
                    if self._exc.match(name): continue
                    full = os.path.join(path, name)
                    if os.path.isdir(full): paths.append(full)
                    else:
                        mtime = os.path.getmtime(full)
                        if last is None: last = mtime
                        else: last = max(mtime, last)
            
            version = package.arguments.get(self.attributeVersion, '0.0')
            versionDev = str(int(round(last * 1000)))
            
            packageName = '%s-%s' % (package.name, version)
            versionMark, build = '.%s' % versionDev, True
            for current in available:
                if current.startswith(packageName):
                    if current[len(packageName):].startswith(versionMark): build = False
                    else: os.remove(os.path.join(self.pathBuild, current))
            
            if build:
                packages.append(package)
                package.arguments[self.attributeVersion] = '%s.%s' % (version, versionDev)
            else: log.info('%s Up to date: %s', '=' * 50, package.name)
        
        distribution.packages = packages
