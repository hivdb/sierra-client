import re
from typing import List

from ..common_types import GeneDef


VIRUS_NAME: str = 'HIV1'

STRAIN_NAME: str = 'HIV1'

DEFAULT_URL: str = 'https://hivdb.stanford.edu/graphql'

GENE_DEFS: List[GeneDef] = [
    {
        'name': 'PR',
        'synonym_pattern': re.compile(r'^\s*(PR|protease)\s*$', re.I)
    },
    {
        'name': 'RT',
        'synonym_pattern': re.compile(
            r'^\s*(RT|reverse transcriptase)\s*$', re.I)
    },
    {
        'name': 'IN',
        'synonym_pattern': re.compile(r'^\s*(IN|INT|integrase)\s*$', re.I)
    },
    {
        'name': 'POL',
        'synonym_pattern': re.compile(r'^\s*(pol)\s*$', re.I),
        'target_genes': [
            {
                'name': 'PR',
                'offset': 0,
                'range': (1, 99)
            },
            {
                'name': 'RT',
                'offset': 0,
                'range': (100, 660)
            },
            {
                'name': 'IN',
                'offset': 0,
                'range': (661, 949)
            }
        ]
    }
]

VALID_GENES: List[str] = [gdef['name'] for gdef in GENE_DEFS]
