'''
Created on Aug 11, 2011

@package: ally core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the basic decoding processor handler.
'''

from ally.api.operator.type import TypeModel
from ally.api.type import Input
from ally.container.ioc import injected
from ally.core.spec.resources import Normalizer, Converter, Invoker
from ally.core.spec.server import Processor
import logging

# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------

@injected
class DecodingTextBaseHandler(Processor):
    '''
    Provides the base decoder for request content.
    '''

    normalizer = Normalizer
    # The normalizer used by the encoding for the XML tag names.
    converterId = Converter
    # The converter to use on the id's of the models.
    charSetDefault = str
    # The default character set to be used if none provided for the content.
    contentTypes = list
    # The list[string] of content types known by this decoding.

    def __init__(self):
        assert isinstance(self.normalizer, Normalizer), 'Invalid Normalizer object %s' % self.normalizer
        assert isinstance(self.converterId, Converter), 'Invalid Converter object %s' % self.converterId
        assert isinstance(self.charSetDefault, str), 'Invalid default character set %s' % self.charSetDefault
        assert isinstance(self.contentTypes, list), 'Invalid content types list %s' % self.contentTypes

# --------------------------------------------------------------------

def findLastModel(invoker):
    '''
    Provides if is the case the Model represented by the invoker as the last mandatory input.
    
    @param invoker: Invoker
        The invoker to find the model for.
    @return: tuple(string, Model)
        A tuple containing the name of the input and the model. None if there is no such input.
    '''
    assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
    if invoker.inputs:
        inp = invoker.inputs[invoker.mandatory - 1]
        assert isinstance(inp, Input)
        if isinstance(inp.type, TypeModel):
            return inp.name, inp.type
    return None

