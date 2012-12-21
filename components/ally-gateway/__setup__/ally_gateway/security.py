'''
Created on Dec 19, 2012

@package: ally gateway
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the security setup for components.
'''

from ally.container import ioc
from ally.api.security import SchemeRepository

# --------------------------------------------------------------------

@ioc.entity
def scheme() -> SchemeRepository: return SchemeRepository()

@ioc.entity
def repositories(): return [scheme()]
