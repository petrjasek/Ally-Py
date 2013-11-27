'''
Created on Nov 8, 2013
 
@package: internationlization
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Cristian Domsa
 
Provides the decorator to be used by the models in the internationlization domain.
'''

from functools import partial
from ally.api.config import model

# --------------------------------------------------------------------

DOMAIN_LOCALIZATION = 'Localization/'
modelLocalization = partial(model, domain=DOMAIN_LOCALIZATION)