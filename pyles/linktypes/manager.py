import linktypes.default
import linktypes.steam
from linktypes.settings import LinktypeException

default = linktypes.default

all = {linktypes.default.name: linktypes.default,
    linktypes.steam.name: linktypes.steam}

def get_config(linktypename):
    try:
        linktype = all[linktypename]
    except KeyError:
        raise LinktypeException('Invalid linktypename "{}"'
            .format(linktypename))
    return {'name': linktype.name,
            'linktype': linktype,
            'settings': linktype.settings()}

def deserialize(config):
    linktypename = config['name']
    try:
        linktype = all[linktypename]
    except KeyError:
        raise LinktypeException('Invalid linktypename "{}"'
            .format(linktypename))
    try:
        settings = config['settings']
    except KeyError:
        raise LinktypeException('Missing settings')
    return {'name': linktype.name,
            'linktype': linktype,
            'settings': linktype.settings(settings)}

def serialize(config):
    settings = {key: setting.serialize()
                for key,setting in config['settings'].items()}
    return {'name': config['name'],
            'settings': settings}
    
def apply(config):
    for key, setting in config['settings'].items():
        setting.apply()
