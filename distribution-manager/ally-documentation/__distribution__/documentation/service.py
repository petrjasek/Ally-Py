'''
Created on Oct 2, 2013

@package: ally documentation
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the services setup for documentation.
'''

from ..general. request_api import requesterGetJSON
from ally.container import ioc

# --------------------------------------------------------------------

@ioc.config
def path_source():
    ''' The source path where the code to be documented is found.'''
    return ''

@ioc.config
def path_location():
    ''' The location path where to dump the documentation.'''
    return ''

@ioc.config
def path_template():
    ''' The path where the template files are located.'''
    return 'templates'

# --------------------------------------------------------------------

@ioc.entity
def generatorCode():
    from ally.distribution.documentation.generator_code import DocumentCodeGenerator
    b = DocumentCodeGenerator()
    b.pathSource = path_source()
    b.pathLocation = path_location()
    return b

@ioc.entity
def generatorAPI():
    from ally.distribution.documentation.generator_api import DocumentAPIGenerator
    b = DocumentAPIGenerator()
    b.pathTemplate = path_template()
    b.pathLocation = path_location()
    b.requesterGetJSON = requesterGetJSON()
    return b

