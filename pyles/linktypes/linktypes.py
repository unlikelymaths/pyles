import importlib
import pkgutil

import linktypes.default_linktype as default

all = {mod.name: mod for mod in [default] + [
    importlib.import_module('linktypes.{}'.format(name))
    for finder, name, ispkg
    in pkgutil.iter_modules(path=['pyles\linktypes'])
    if name.startswith('pylesltype_')
    ]}

for t in all.keys():
    print(t)