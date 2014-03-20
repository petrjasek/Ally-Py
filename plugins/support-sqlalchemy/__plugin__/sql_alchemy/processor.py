'''
Created on Aug 19, 2013

@package: support sqlalchemy
@copyright: 2011 Sourcefabric o.p.s.
@license http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the configurations for general SQL alchemy processors.
'''

from ally.container import ioc
from ally.design.processor.handler import Handler
from sql_alchemy.core.impl.processor.transaction import TransactionHandler
from __setup__.ally_core.decode import assemblyDecodeContent, validateMandatory
from sql_alchemy.core.impl.processor.validation.unique import ValidateUnique

# --------------------------------------------------------------------

@ioc.entity
def transaction() -> Handler: return TransactionHandler()

# --------------------------------------------------------------------

@ioc.entity
def validateUnique() -> Handler: return ValidateUnique()

@ioc.before(assemblyDecodeContent)
def updateAssemblyDecodeContent():
    assemblyDecodeContent().add(validateUnique(), after=validateMandatory())
