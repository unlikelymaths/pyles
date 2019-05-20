import importlib
import pkgutil

import linktypes.default_linktype as default

all = {mod.name: mod for mod in [default] + [
    importlib.import_module('linktypes.{}'.format(name))
    for finder, name, ispkg
    in pkgutil.iter_modules(path=['pyles\linktypes'])
    if name.startswith('pylesltype_')
    ]}

def get_config(linktypename):
    try:
        config = all[linktypename].config()
    except  AttributeError:
        config = []
    return config
    
def serialize(config):
    return [setting.serialize() for setting in config]
    
def deserialize(config_list):
    config = []
    for setting in config_list:
        module = importlib.import_module(setting.pop('__module__'))
        cls = getattr(module, setting.pop('__name__'))
        config.append(cls(**setting))
    return config