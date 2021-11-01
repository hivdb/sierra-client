import re
from .. import fragments
from .virus import Virus


HIV2 = Virus(
    virus_name='HIV2',

    strain_name='HIV2A',

    supported_commands=[
        'fasta'
    ],

    default_url='https://hivdb.stanford.edu/hiv2/graphql',

    gene_defs=[
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
                    'range': (100, 659)
                },
                {
                    'name': 'IN',
                    'offset': 0,
                    'range': (660, 952)
                }
            ]
        }
    ],

    default_queries={
        'fasta': fragments.HIV1_SEQUENCE_ANALYSIS_DEFAULT
    }
)
