'''
Created on Mar 4, 2014

@package: ally distribution
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides versioning for development source distribution.
'''

from collections import deque
import hashlib
import json
import logging
import os
import re

from ally.container.ioc import injected
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Distribution(Context):
    '''
    The distribution context.
    '''
    # ---------------------------------------------------------------- Defined
    versions = defines(dict, doc='''
    @rtype: dictionary{string: dictionary{string: string}}
    The versions meta data indexed by package name.
    ''')
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
        
        versionsPath = os.path.join(self.pathBuild, 'versions.json')
        if os.path.exists(versionsPath):
            with open(versionsPath, 'r') as f: versions = json.load(f)
        else: versions = {}
        
        if distribution.versions is None: distribution.versions = {}
        
        packages = []
        for package in distribution.packages:
            assert isinstance(package, Package), 'Invalid package %s' % package
            
            paths, versionHash = deque(), hashlib.md5()
            paths.append(package.path)
            while paths:
                path = paths.popleft()                
                for name in os.listdir(path):
                    if self._exc.match(name): continue
                    full = os.path.join(path, name)
                    if os.path.isdir(full): paths.append(full)
                    else:
                        versionHash.update(full.encode())
                        with open(full, 'rb') as f:
                            while True:
                                data = f.read(1024)
                                if not data: break
                                versionHash.update(data)
            
            currentHash = versionHash.hexdigest()
            versionMinor = 1
            
            meta = versions.get(package.name)
            if meta:
                versionMinor, packageHash = meta['minor'], meta['hash']
                if packageHash == currentHash:
                    distribution.versions[package.name] = meta
                    log.info('%s Up to date: %s', '=' * 50, package.name)
                    continue
                else:
                    versionMinor += 1
                    packageDist = meta['dist']
                    if os.path.isfile(packageDist): os.remove(packageDist)
            else: meta = {}
            
            meta['minor'] = versionMinor
            meta['hash'] = currentHash
            distribution.versions[package.name] = meta
        
            package.arguments[self.attributeVersion] = '%s.%s' % \
            (package.arguments.get(self.attributeVersion, '0.0'), versionMinor)
            packages.append(package)
            
        distribution.packages = packages
