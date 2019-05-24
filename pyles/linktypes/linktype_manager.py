import importlib
import pkgutil

import linktypes.default_linktype as default
import linktypes.pylesltype_steam as steam

all = {default.name: default,
    steam.name: steam}
for finder, name, ispkg in pkgutil.iter_modules(path=['pyles\linktypes']):
    print(name)
    if not name.startswith('pylesltype_'):
        continue
    mod = importlib.import_module('linktypes.{}'.format(name))
    if not mod.active:
        continue
    if mod.name in all:
        continue
    all[mod.name] = mod

def get_config(linktypename):
    try:
        config = all[linktypename].config()
    except  AttributeError:
        config = []
    return config
    
def serialize(config):
    return [setting.serialize() for setting in config]
    
def apply(config):
    for setting in config:
        setting.apply()
    
def deserialize(config_list):
    config = []
    for setting in config_list:
        module = importlib.import_module(setting.pop('__module__'))
        cls = getattr(module, setting.pop('__name__'))
        config.append(cls(**setting))
    return config