from .. import fragments
from .virus import Virus


HCV = Virus(
    virus_name='HCV',

    strain_name='HCV',

    supported_commands=[
        'fasta',
        'mutations',
        'patterns'
    ],

    default_url='https://hivdb.stanford.edu/hcv/graphql',

    gene_defs=[],

    default_queries={
        'fasta': fragments.HCV_SEQUENCE_ANALYSIS_DEFAULT,
        'mutations': fragments.HCV_MUTATIONS_ANALYSIS_DEFAULT,
        'patterns': fragments.HCV_MUTATIONS_ANALYSIS_DEFAULT
    }
)
