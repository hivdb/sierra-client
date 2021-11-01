import os

HIV1_MUTATIONS_ANALYSIS_DEFAULT: str
HIV1_SEQUENCE_ANALYSIS_DEFAULT: str
HIV1_SEQUENCE_READS_ANALYSIS_DEFAULT: str
HIV2_SEQUENCE_ANALYSIS_DEFAULT: str
SARS2_MUTATIONS_ANALYSIS_DEFAULT: str
SARS2_SEQUENCE_ANALYSIS_DEFAULT: str
SARS2_SEQUENCE_READS_ANALYSIS_DEFAULT: str

__all__ = []

_globals = globals()
dirpath = os.path.dirname(__file__)

for name in _globals['__annotations__']:
    path = name.lower()
    with open(
        os.path.join(dirpath, os.path.extsep.join([path, 'gql']))
    ) as fp:
        _globals[name] = fp.read()
        __all__.append(name)
