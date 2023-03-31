import re
from .. import fragments
from .virus import Virus


HIV1 = Virus(
    virus_name='HIV1',

    strain_name='HIV1',

    supported_commands=[
        'fasta',
        'mutations',
        'patterns',
        'seqreads'
    ],

    default_url='https://hivdb.stanford.edu/graphql',

    gene_defs=[
        {
            'name': 'gag',
            'synonym_pattern': re.compile(r'^\s*(gag|gp0?2)\s*$', re.I)
        },
        {
            'name': 'CA',
            'synonym_pattern': re.compile(
                r'^\s*(ca|capsid)([ _-]?protein)?\s*$', re.I)
        },
        {
            'name': 'pol',
            'synonym_pattern': re.compile(r'^\s*(pol|polyprotein)\s*$', re.I)
        },
        {
            'name': 'PR',
            'synonym_pattern': re.compile(
                r'^\s*(pr|protease)([ _-]?protein)?\s*$', re.I)
        },
        {
            'name': 'RT',
            'synonym_pattern': re.compile(
                r'^\s*(rt|reverse[ -]transcriptase)([ _-]?protein)?\s*$', re.I)
        },
        {
            'name': 'IN',
            'synonym_pattern': re.compile(
                r'^\s*(in|integrase)([ _-]?(pro|protein|proteinase))?\s*$',
                re.I)
        },
        {
            'name': 'vif',
            'synonym_pattern': re.compile(r'^\s*(vif|gp0?3)\s*$', re.I)
        },
        {
            'name': 'vpr',
            'synonym_pattern': re.compile(r'^\s*(vpr|gp0?4)\s*$', re.I)
        },
        {
            'name': 'tat',
            'synonym_pattern': re.compile(r'^\s*(tat|gp0?5)\s*$', re.I)
        },
        {
            'name': 'rev',
            'synonym_pattern': re.compile(r'^\s*(rev|gp0?6)\s*$', re.I)
        },
        {
            'name': 'vpu',
            'synonym_pattern': re.compile(r'^\s*(vpu|gp0?7)\s*$', re.I)
        },
        {
            'name': 'env',
            'synonym_pattern': re.compile(r'^\s*(env|gp0?8)\s*$', re.I)
        },
        {
            'name': 'nef',
            'synonym_pattern': re.compile(r'^\s*(env|gp0?9)\s*$', re.I)
        }
    ],

    default_queries={
        'fasta': fragments.HIV1_SEQUENCE_ANALYSIS_DEFAULT,
        'mutations': fragments.HIV1_MUTATIONS_ANALYSIS_DEFAULT,
        'patterns': fragments.HIV1_MUTATIONS_ANALYSIS_DEFAULT,
        'seqreads': fragments.HIV1_SEQUENCE_READS_ANALYSIS_DEFAULT
    }
)
