'''
Created on Nov 7, 2013
 
@package: internationlization
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Cristian Domsa
 
Provides the database settings.
'''

from ..sql_alchemy.db_application import metas, bindApplicationSession
from ally.container import ioc
from internationalization.meta.metadata_internationalization import meta

# --------------------------------------------------------------------

@ioc.entity
def binders(): return [bindApplicationSession]

# --------------------------------------------------------------------

@ioc.before(metas)
def updateMetasForInternationalization(): metas().append(meta)