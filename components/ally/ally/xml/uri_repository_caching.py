'''
Created on Jan 7, 2014

@package: ally.xml
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Gociu

Caches the repositories resulted from parsing configuration files.
'''

from ally.container.ioc import injected
from ally.design.processor.attribute import requires
from ally.design.processor.context import Context
from ally.design.processor.execution import Chain
from ally.design.processor.handler import HandlerProcessor
import logging

# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Solicit(Context):
    '''
    The solicit context.
    '''
    # ---------------------------------------------------------------- Required
    uri = requires(str)
    repository = requires(Context)

# --------------------------------------------------------------------
@injected
class UriRepositoryCaching(HandlerProcessor):
    '''
    Implementation for a processor that caches repositories resulted from parsing configuration files.
    '''
    def __init__(self):
        super().__init__()
        self.uriRepository = {}
    
    def process(self, chain, solicit:Solicit, Repository:Context=None, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Cache the repository for the uri.
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(solicit, Solicit), 'Invalid solicit %s' % solicit
        
        #if there is no new repository, just clean the current repository for this URI
        if solicit.repository is None: self.uriRepository.pop(solicit.uri, None)
        else: self.uriRepository[solicit.uri] = solicit.repository
        
        #will make a root repository that contains all the repositories created so far (from the parsed files)
        root = chain.arg.Repository()
        root.children = []
        for repository in self.uriRepository.values():
            root.children.append(repository)
        solicit.repository = root
        
        
