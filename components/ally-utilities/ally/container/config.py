'''
Created on Jan 11, 2012

@package: Newscoop
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides configurations serializing support.
'''

import re

# --------------------------------------------------------------------

REGEX_SPLIT = re.compile('[\s]+')
# Regex used in spliting the descriptions for wrapping

# --------------------------------------------------------------------

def save(configurations, fwrite, maxwidth=60):
    '''
    Saves the configurations to the provided file writer.
    
    @param configurations: dictionary{string, Config}
        A dictionary of the configurations to be saved, the key is the configuration name and the value is a Config
        object.
    @param fwrite: file
        A file writer type object.
    @param maxwidth: integer
        The maximum width to use for the description comments.
    '''
    assert isinstance(configurations, dict), 'Invalid configurations %s' % configurations
    assert fwrite, 'No writer provided'
    assert isinstance(maxwidth, int), 'Invalid maximum width %s' % maxwidth

    import yaml
    split = REGEX_SPLIT
    groups = {config.group for config in configurations.values()}
    for group in sorted(groups):
        fwrite.write('\n# %s %r\n' % ('-' * maxwidth, group))
        configByGroup = [(config.name, name) for name, config in configurations.items() if config.group == group]
        configByGroup.sort(key=lambda pack: pack[0])
        for _fullName, name in configByGroup:
            config = configurations[name]
            assert isinstance(config, Config), 'Invalid configuration %s' % config
            if config.description:
                # Wrapping description
                text = split.split(config.description)
                w = 0; line = []; matrix = [line]
                for txt in text:
                    if txt:
                        w += len(txt) + 1
                        if w > maxwidth: w = len(txt) + 1; line = [txt]; matrix.append(line)
                        else: line.append(txt)
                fwrite.write('\n# %s\n' % '\n# '.join(' '.join(line) for line in matrix))
            yaml.dump({name: config.value}, fwrite, default_flow_style=False)

def load(fread):
    '''
    Loads the configurations from the provided read file handler.
    
    @param fread: file
        A file read type object.
    @return: dictionary{string, object}
        The configuration dictionary.
    '''
    assert fread, 'No reader provided'

    import yaml
    config = yaml.load(fread)
    if config is None: config = {}
    assert isinstance(config, dict), 'Invalid configuration loaded %s' % config
    return config

# --------------------------------------------------------------------

class Config:
    '''
    Class for providing a configuration data.
    '''

    def __init__(self, name, value, group=None, description=None):
        '''
        Construct the configuration.
        
        @param name: string
            The full name of the configuration.
        @param value: object|None
            The configuration value.
        @param group: string
            The configuration group.
        @param description: string
            The configuration description.
        '''
        assert isinstance(name, str), 'Invalid name %s' % name
        assert not group or isinstance(group, str), 'Invalid group %s' % group
        assert not description or isinstance(description, str), 'Invalid description %s' % description
        self.name = name
        self.value = value
        self.group = group
        self.description = description

