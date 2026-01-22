from .. import fragments
from .virus import Virus


HBV = Virus(
    virus_name='HBV',

    strain_name='HBV',

    supported_commands=[
        'fasta'
    ],

    default_url='https://hivdb.stanford.edu/hbv/graphql',

    gene_defs=[
        {
            'name': 'RT'
        }
    ],

    default_queries={
        'fasta': fragments.HBV_SEQUENCE_ANALYSIS_DEFAULT
    }
)
