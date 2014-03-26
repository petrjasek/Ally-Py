'''
Created on Aug 31, 2013

@package: gateway acl
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the ally core setup patch.
'''

import logging

from __setup__.ally_core.resources import injectorAssembly
from ally.container import support, app, ioc
from ally.design.processor.assembly import Assembly
from ally.design.processor.execution import Processing, FILL_ALL

from ..sql_alchemy.db_application import assemblySQLAssembler
from ..sql_alchemy.processor import transaction


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

try:
    from __setup__ import ally_core  # @UnusedImport
except ImportError: log.info('No ally core component available, thus no need to register ACL assemblers to it')
else:
    from __setup__.ally_core.resources import assemblyAssembler, updateAssemblyAssembler, processMethod
    from acl.core.impl.processor import assembler
    from ..sql_alchemy.patch_ally_core import updateAssemblySQLAssembler

    # The assembler processors
    processFilter = indexFilter = indexAccess = support.notCreated  # Just to avoid errors
    support.createEntitySetup(assembler)
    
    # ----------------------------------------------------------------
    
    @ioc.entity
    def assemblyIndex() -> Assembly:
        return Assembly('Index access')
    
    @ioc.entity
    def processingIndex() -> Processing:  # We need to create the processing
        return assemblyIndex().create()

    # ----------------------------------------------------------------

    @ioc.after(updateAssemblyAssembler)
    def updateAssemblyAssemblerForFilter():
        assemblyAssembler().add(processFilter(), before=processMethod())

    @ioc.after(updateAssemblySQLAssembler)
    def updateAssemblySQLAssemblerForFilter():
        assemblySQLAssembler().add(processFilter(), before=processMethod())
    
    @ioc.before(assemblyIndex)
    def updateAssemblyIndex():
        assemblyIndex().add(injectorAssembly(), transaction(), indexFilter(), indexAccess())

    # ----------------------------------------------------------------

    @app.setup(app.CHANGED)
    def triggerProcess():
        # We need to trigger the processing in setup area since otherwise no more
        # registration is available
        processingIndex()
    
    @app.populate(app.CHANGED)
    def populateAccess():
        processingIndex().execute(FILL_ALL)
        

