# -*- coding: utf-8 -*-

import os

_globals = globals()
__all__ = []

dirpath = os.path.dirname(__file__)

for path in os.listdir(dirpath):
    if path.endswith('.gql'):
        name, _ = os.path.splitext(path)
        with open(os.path.join(dirpath, path)) as fp:
            _globals[name.upper()] = fp.read()
            __all__.append(name.upper())
