import re
from .. import fragments
from .virus import Virus


HCV = Virus(
    virus_name='HCV',

    strain_name='HCV',

    supported_commands=[
        'fasta'
    ],

    default_url='https://hivdb.stanford.edu/hcv/graphql',

    gene_defs=[
        {
            'name': 'NS3'
        },
        {
            'name': 'NS5A_NTD'
        },
        {
            'name': 'NS5B'
        },

    ],

    default_queries={
        'fasta': fragments.HCV_SEQUENCE_ANALYSIS_DEFAULT
    }
)
