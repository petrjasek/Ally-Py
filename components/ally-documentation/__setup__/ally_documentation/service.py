'''
Created on Oct 8, 2013

@package: ally documentation
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the services for documentations.
'''

from ally.container import ioc
from ally.design.processor.assembly import Assembly
from ally.design.processor.execution import FILL_ALL, Processing
from ally.design.processor.handler import Handler
from ally.documentation.core.impl.processor.definition_invoker import \
    DefinitionInvokerHandler
from ally.documentation.core.impl.processor.definition_register import \
    DefinitionRegisterHandler
from ally.documentation.core.impl.processor.generator import GeneratorHandler
from ally.documentation.core.impl.processor.index_api import IndexAPIHandler
from ally.documentation.core.impl.processor.index_model import IndexModelHandler
from ally.documentation.core.impl.processor.mapping import MappingDumpHandler
from ally.documentation.core.impl.processor.templates import TemplateHandler

from ..ally_core.definition import descriptions
from ..ally_core.parsing_rendering import CATEGORY_CONTENT_OBJECT
from ..ally_core.resources import assemblyAssembler, injectorAssembly, register
from ..ally_core_http import definition_header, definition_parameter
from ..ally_core_http.definition_header import parameterHeaderVerifier
from ally.core.impl.definition import Category


# --------------------------------------------------------------------
@ioc.config
def path_documentation():
    '''
    The system path where the documentation will be placed, if not provided it will default to 'doc' folder in the current
    folder.
    '''
    return 'doc'

@ioc.config
def paths_templates():
    '''
    The system path where jinja2 documentation templates can be found, this templates will be used joined with the default
    templates. The order in which the template folder are provided establishes the priority for the files having the
    same name.
    '''
    return []

@ioc.config
def pattern_template():
    '''
    The pattern used to identify templates versus images or other files in the template paths.
    '''
    return '.+\.rst$'

@ioc.config
def pattern_copy():
    '''
    The pattern used to identify resources that need to be copied, this pattern will be applied to non template paths.
    '''
    return '(?!.*\~$)'

@ioc.config
def pattern_generate():
    '''
    The pattern used to identify templates that are documentation generating entry points, this pattern is aplyed on the
    templates paths.
    '''
    return '(?!^\_)'

@ioc.config
def path_mapping():
    '''
    The file path where the mapping will be placed.
    '''
    return 'mapping.txt'

# --------------------------------------------------------------------

@ioc.entity
def assemblyDocumentation() -> Assembly:
    '''
    The assembly containing the documentation handling.
    '''
    return Assembly('Documentation')

@ioc.entity
def assemblyMapping() -> Assembly:
    '''
    The assembly containing the mapping handling.
    '''
    return Assembly('Mapping')

# --------------------------------------------------------------------

@ioc.entity
def indexModel() -> Handler: return IndexModelHandler()

@ioc.entity
def indexAPI() -> Handler: return IndexAPIHandler()

@ioc.entity
def indexHeader() -> Handler:
    b = DefinitionRegisterHandler()
    b.name = 'headers'
    b.verifier = definition_header.VERIFY_CATEGORY
    b.descriptions = descriptions()
    return b

@ioc.entity
def indexHeaderParameters() -> Handler:
    b = DefinitionRegisterHandler()
    b.name = 'headersAsParam'
    b.verifier = parameterHeaderVerifier()
    b.descriptions = []
    return b

@ioc.entity
def indexParameter() -> Handler:
    b = DefinitionInvokerHandler()
    b.name = 'parameters'
    b.verifier = definition_parameter.VERIFY_CATEGORY
    b.descriptions = descriptions()
    return b

@ioc.entity
def indexProperties() -> Handler:
    b = DefinitionInvokerHandler()
    b.name = 'properties'
    b.verifier = Category(CATEGORY_CONTENT_OBJECT)
    b.descriptions = descriptions()
    return b

@ioc.entity
def template() -> Handler:
    b = TemplateHandler()
    b.pathDocumentation = path_documentation()
    b.packageName = __name__[:__name__.rfind('.')]
    b.pathsTemplates = paths_templates()
    b.patternTemplate = pattern_template()
    b.patternCopy = pattern_copy()
    return b

@ioc.entity
def generator() -> Handler:
    b = GeneratorHandler()
    b.pathDocumentation = path_documentation()
    b.patternGenerate = pattern_generate()
    return b

@ioc.entity
def mappingDump() -> Handler:
    b = MappingDumpHandler()
    b.pathMapping = path_mapping()
    return b

# --------------------------------------------------------------------

@ioc.before(assemblyAssembler)
def disableUnusedReport():
    assemblyAssembler().reportUnused = False

@ioc.before(assemblyDocumentation)
def updateAssemblyDocumentation():
    assemblyDocumentation().add(injectorAssembly(), indexModel(), indexAPI(), indexHeader(), indexHeaderParameters(),
                                indexParameter(), indexProperties(), template(), generator())

@ioc.before(assemblyMapping)
def updateAssemblyMapping():
    assemblyMapping().add(injectorAssembly(), mappingDump())
    
# --------------------------------------------------------------------

def createDocumentation():
    processing = assemblyDocumentation().create()
    assert isinstance(processing, Processing), 'Invalid processing %s' % processing
    
    register()
    processing.execute(FILL_ALL)
    
def createMapping():
    processing = assemblyMapping().create()
    assert isinstance(processing, Processing), 'Invalid processing %s' % processing
    
    register()
    processing.execute(FILL_ALL)
