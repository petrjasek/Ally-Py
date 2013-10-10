'''
Created on Oct 4, 2013

@package: ally documentation
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the creation of code documentation based on sphinx.
'''

import inspect
import logging
import os
from types import FunctionType, BuiltinFunctionType

from ally.container.ioc import injected
from sphinx import apidoc
import sphinx
from sphinx.ext.autodoc import ClassLevelDocumenter, AttributeDocumenter, \
    FunctionDocumenter, MethodDocumenter, Documenter
from sphinx.util.inspect import getargspec, safe_repr
from sphinx.application import Sphinx
import sys
from ally.api.type import typeFor
from ally.api.operator.type import TypeProperty
from ally.api.operator.descriptor import CallAPI
from inspect import getfullargspec

# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class ReferenceDocumenter(AttributeDocumenter):
    """
    Specialized Documenter subclass for attributes.
    """
    
    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        can = AttributeDocumenter.can_document_member(member, membername, isattr, parent)
        if can and isinstance(typeFor(member), CallAPI): return False
        return can
    
    def add_directive_header(self, sig):
        ClassLevelDocumenter.add_directive_header(self, sig)
        if not self._datadescriptor:
            typ = typeFor(self.object)
            try: 
                if isinstance(typ, TypeProperty): objrepr = str(typeFor(self.object).type)
                else: objrepr = safe_repr(self.object)
            except ValueError: pass
            else: self.add_line('   :annotation: = ' + objrepr, '<autodoc>')

class CallAPIDocumenter(MethodDocumenter):
    """
    Specialized Documenter subclass for functions.
    """
    
    priority = 20
    
    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        return isinstance(member, CallAPI)
    
    def format_args(self):
        if inspect.isbuiltin(self.object.__wrapped__) or \
               inspect.ismethoddescriptor(self.object.__wrapped__):
            # can never get arguments of a C function or method
            return None
        argspec = getargspec(self.object.__wrapped__)
        if argspec[0] and argspec[0][0] in ('cls', 'self'):
            del argspec[0][0]

        annotations = getfullargspec(self.object.__wrapped__).annotations
        return inspect.formatargspec(*argspec, annotations=annotations)
    
# --------------------------------------------------------------------

@injected
class DocumentCodeGenerator:
    '''
    Provides the creation of code documentation based on sphinx.
    '''

    pathSource = str
    # The source path to create documentation for.
    pathLocation = str
    # The location path where to dump the documentation.
    
    def __init__(self):
        assert isinstance(self.pathSource, str), 'Invalid source path %s' % self.pathSource
        assert isinstance(self.pathLocation, str), 'Invalid location path %s' % self.pathLocation
        
    def process(self):
        '''
        Process the documentation.
        '''
        args = ['', self.pathSource, '--full' , '--force', '-o', self.pathLocation, '--doc-project', 'ally-py',
                '--doc-author', 'Gabriel Nistor', '-V', '1.0b1']
        apidoc.main(args)
        
#         args = ['', '-b', 'html', '-d', os.path.join(self.pathLocation, '_build', 'doctrees'), '-D', 'latex_paper_size=a4',
#                 self.pathLocation, os.path.join(self.pathLocation, 'doc', 'html')]
#         sphinx.main(args)

        sphinx = Sphinx(self.pathLocation, self.pathLocation, os.path.join(self.pathLocation, 'doc', 'html'),
                        os.path.join(self.pathLocation, '_build', 'doctrees'), 'html', {'latex_paper_size': 'a4'},
                        None, sys.stderr, False, False, [])
        sphinx.add_autodocumenter(CallAPIDocumenter)
        sphinx.add_autodocumenter(ReferenceDocumenter)
        sphinx.build(True, [])
        
