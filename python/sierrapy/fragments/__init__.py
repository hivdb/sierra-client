# -*- coding: utf-8 -*-

import os

MUTATIONS_ANALYSIS_DEFAULT: str
SEQUENCE_ANALYSIS_DEFAULT: str
SEQUENCE_READS_ANALYSIS_DEFAULT: str

_globals = globals()
__all__ = []

dirpath = os.path.dirname(__file__)

for name in _globals.__annotations__:
    path = name.lower()
    with open(
        os.path.join(dirpath, os.path.extsep.join([path, 'gql']))
    ) as fp:
        _globals[name] = fp.read()
        __all__.append(name)
