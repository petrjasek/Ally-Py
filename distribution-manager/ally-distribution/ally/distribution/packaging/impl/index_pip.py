'''
Created on Feb 25, 2014

@package: ally distribution
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the pip index file creation.
'''

from ally.container.ioc import injected
import logging
import os
from os.path import join, isfile, isdir
import re


# --------------------------------------------------------------------
log = logging.getLogger(__name__)
  
# --------------------------------------------------------------------

@injected
class IndexPip:
    '''
    Provides the pip index file.
    '''
    
    locations = list
    # The locations where to scan for packages.
    rootURI = str
    # The index root URI that can be used for fetching the files. 
    fileIndex = 'pip'
    # The name of the pip index file.
    regex = '([^\.]+)(?=.*)-([0-9]{1}.[0-9]{1}).tar.gz'
    # The regex used for extracting the name and version based on the file name.
    template = '''
<html><head><title>Pip Install Listing</title><meta name="api-version" value="1"/></head><body>
%s
</body></html>'''
    # The template used for constructing the file.
    templateEntry = '<a href=\'%s/%s\'>%s</a><br/>'
    # The template used for a package entry.
    
    def __init__(self):
        assert isinstance(self.locations, list), 'Invalid locations %s' % self.locations
        assert isinstance(self.rootURI, str), 'Invalid root URI %s' % self.rootURI
        assert isinstance(self.fileIndex, str), 'Invalid pip index file name %s' % self.fileIndex
        assert isinstance(self.regex, str), 'Invalid regex %s' % self.regex
        self._reg = re.compile(self.regex)
        self.rootURI = self.rootURI.rstrip('/')

    def __call__(self):
        ''' Create the pip index file.'''
        entries = []
        for location in self.locations:
            if not isdir(location):
                log.info('Invalid folder \'%s\'', location)
                continue
            
            for name in os.listdir(location):
                if not isfile(join(location, name)): continue
                match = self._reg.match(name)
                if not match or len(match.groups()) != 2:
                    log.info('Invalid package file \'%s\'', join(location, name))
                    continue
                
                entries.append(self.templateEntry % (self.rootURI, name, match.groups()[0]))
        
            with open(join(location, self.fileIndex), 'w') as f:
                print(self.template % '\n'.join(entries), file=f) 
