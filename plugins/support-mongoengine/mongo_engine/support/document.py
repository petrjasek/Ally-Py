'''
Created on Jan 5, 2012

@package: support mongoengine
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides support for mongo engine document handling.
'''

from mongoengine.queryset.manager import QuerySetManager
from mongoengine.document import Document

# --------------------------------------------------------------------
# 
# class MappedSupportDocument(type):
#     '''
#     Meta class for document base support.
#     '''
#     
#     def __new__(cls, name, bases, namespace):
#         if name == 'Base' and namespace.get('__module__') == __name__:
#             return type.__new__(cls, name, bases, namespace)
#         
#         meta = namespace.get('meta')
#         if meta is None: meta = dict(Base.meta)
#         else: meta.update(Base.meta)
#         dbases = list(bases)
#         dbases.remove(Base)
#         dbases.insert(0, Document)
#         return type(name, tuple(dbases), namespace)

class Base(Document):
    '''
    Provides the base for Document mapping.
    '''
    objects = QuerySetManager()  # Just to have type hinting no real value.
    meta = {'allow_inheritance': True, 'abstract': True}
