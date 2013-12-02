'''
Created on Aug 30, 2013

@package: support mongoengine
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the configurations patch for the processors used in handling the request.
'''

import logging

from ally.container import ioc
from ally.design.processor.handler import Handler
from mongo_engine.core.impl.processor.assembler.mapped_validation import \
    MappedValidationHandler


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

try:
    from __setup__ import ally_core  # @UnusedImport
except ImportError: log.info('No ally core component available, thus no need to apply the validation patch')
else:
    from __setup__.ally_core.resources import assemblyAssembler, updateAssemblyAssembler, decoding
    
    @ioc.entity
    def mappedValidation() -> Handler: return MappedValidationHandler()

    # ----------------------------------------------------------------

    @ioc.after(updateAssemblyAssembler)
    def updateAssemblyAssemblerForMetaValidation():
        assemblyAssembler().add(mappedValidation(), before=decoding())
