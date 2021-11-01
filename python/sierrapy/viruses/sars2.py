import re
from .. import fragments
from .virus import Virus


SARS2 = Virus(

    virus_name='SARS2',

    strain_name='SARS2',

    supported_commands=[
        'fasta',
        'mutations',
        'patterns',
        'seqreads'
    ],

    default_url='https://covdb.stanford.edu/sierra-sars2/graphql',

    gene_defs=[
        {
            'name': 'nsp1',
            'synonym_pattern': re.compile(
                r'^\s*nsp1([ _-]?protein)?\s*$', re.I)
        },
        {
            'name': 'nsp2',
            'synonym_pattern': re.compile(
                r'^\s*nsp2([ _-]?protein)?\s*$', re.I)
        },
        {
            'name': 'PLpro',
            'synonym_pattern': re.compile(
                r'^\s*(nsp3|pl|papain-like)'
                r'([ _-]?(pro|protein|proteinase))?\s*$',
                re.I
            )
        },
        {
            'name': 'nsp4',
            'synonym_pattern': re.compile(
                r'^\s*nsp4([ _-]?protein)?\s*$', re.I)
        },
        {
            'name': '_3CLpro',
            'synonym_pattern': re.compile(
                r'^\s*(nsp5|_?3cl|3c-like|mpro|main)'
                r'([ _-]?(pro|protein|proteinase))?\s*$', re.I)
        },
        {
            'name': 'nsp6',
            'synonym_pattern': re.compile(
                r'^\s*nsp6([ _-]?protein)?\s*$', re.I)
        },
        {
            'name': 'nsp7',
            'synonym_pattern': re.compile(
                r'^\s*nsp7([ _-]?protein)?\s*$', re.I)
        },
        {
            'name': 'nsp8',
            'synonym_pattern': re.compile(
                r'^\s*nsp8([ _-]?protein)?\s*$', re.I)
        },
        {
            'name': 'nsp9',
            'synonym_pattern': re.compile(
                r'^\s*nsp9([ _-]?protein)?\s*$', re.I)
        },
        {
            'name': 'nsp10',
            'synonym_pattern': re.compile(
                r'^\s*nsp10([ _-]?protein)?\s*$', re.I)
        },
        {
            'name': 'nsp11',
            'synonym_pattern': re.compile(
                r'^\s*nsp11([ _-]?protein)?\s*$', re.I),
            'target_genes': [
                {
                    'name': 'RdRP',
                    'offset': 0,
                    'range': (1, 9)
                }
            ]
        },
        {
            'name': 'RdRP',
            'synonym_pattern': re.compile(
                r'^\s*(rdrp|rna-dependent rna polymerase)\s*$', re.I)
        },
        {
            'name': 'nsp12',
            'synonym_pattern': re.compile(
                r'^\s*nsp12([ _-]?protein)?\s*$', re.I),
            'target_genes': [
                {
                    'name': 'RdRP',
                    'offset': 9,
                    'range': (1, 923)
                }
            ]
        },
        {
            'name': 'nsp13',
            'synonym_pattern': re.compile(
                r'^\s*nsp13([ _-]?protein)?\s*$', re.I)
        },
        {
            'name': 'nsp14',
            'synonym_pattern': re.compile(
                r'^\s*nsp14([ _-]?protein)?\s*$', re.I)
        },
        {
            'name': 'nsp15',
            'synonym_pattern': re.compile(
                r'^\s*nsp15([ _-]?protein)?\s*$', re.I)
        },
        {
            'name': 'nsp16',
            'synonym_pattern': re.compile(
                r'^\s*nsp16([ _-]?protein)?\s*$', re.I)
        },
        {
            'name': 'ORF1a',
            'synonym_pattern': re.compile(
                r'^\s*orf1a([ _-]?protein)?\s*$', re.I),
            'target_genes': [
                {
                    'name': 'nsp1',
                    'offset': 0,
                    'range': (1, 180)
                },
                {
                    'name': 'nsp2',
                    'offset': 0,
                    'range': (181, 818)
                },
                {
                    'name': 'PLpro',
                    'offset': 0,
                    'range': (819, 2763)
                },
                {
                    'name': 'nsp4',
                    'offset': 0,
                    'range': (2764, 3263)
                },
                {
                    'name': '_3CLpro',
                    'offset': 0,
                    'range': (3264, 3569)
                },
                {
                    'name': 'nsp6',
                    'offset': 0,
                    'range': (3570, 3859)
                },
                {
                    'name': 'nsp7',
                    'offset': 0,
                    'range': (3860, 3942)
                },
                {
                    'name': 'nsp8',
                    'offset': 0,
                    'range': (3943, 4140)
                },
                {
                    'name': 'nsp9',
                    'offset': 0,
                    'range': (4141, 4253)
                },
                {
                    'name': 'nsp10',
                    'offset': 0,
                    'range': (4254, 4392)
                },
                {
                    'name': 'RdRP',
                    'offset': 0,
                    'range': (4393, 4401)
                }
            ]
        },
        {
            'name': 'ORF1b',
            'synonym_pattern': re.compile(
                r'^\s*orf1b([ _-]?protein)?\s*$', re.I),
            'target_genes': [
                {
                    'name': 'RdRP',
                    'offset': 9,
                    'range': (1, 923)
                },
                {
                    'name': 'nsp13',
                    'offset': 9,
                    'range': (924, 1524)
                },
                {
                    'name': 'nsp14',
                    'offset': 9,
                    'range': (1525, 2051)
                },
                {
                    'name': 'nsp15',
                    'offset': 9,
                    'range': (2052, 2397)
                },
                {
                    'name': 'nsp16',
                    'offset': 9,
                    'range': (2398, 2695)
                }
            ]
        },
        {
            'name': 'S',
            'synonym_pattern': re.compile(
                r'^\s*(GU280_gp02|(s|spike|surface)'
                r'([ _-]?(protein|glycoprotein))?)\s*$', re.I)
        },
        {
            'name': 'ORF3a',
            'synonym_pattern': re.compile(
                r'^\s*(GU280_gp03|(orf3a?)([ _-]?protein)?)\s*$', re.I)
        },
        {
            'name': 'E',
            'synonym_pattern': re.compile(
                r'^\s*(GU280_gp04|(orf4|e|envelope|env)([ _-]?protein)?)\s*$',
                re.I
            )
        },
        {
            'name': 'M',
            'synonym_pattern': re.compile(
                r'^\s*(GU280_gp05|(orf5|m|membranes?|mp)([ _-]?protein)?)\s*$',
                re.I
            )
        },
        {
            'name': 'ORF6',
            'synonym_pattern': re.compile(
                r'^\s*(GU280_gp06|orf6([ _-]?protein)?)\s*$',
                re.I
            )
        },
        {
            'name': 'ORF7a',
            'synonym_pattern': re.compile(
                r'^\s*(GU280_gp07|orf7a([ _-]?protein)?)\s*$',
                re.I
            )
        },
        {
            'name': 'ORF7b',
            'synonym_pattern': re.compile(
                r'^\s*(GU280_gp08|orf7b([ _-]?protein)?)\s*$',
                re.I
            )
        },
        {
            'name': 'ORF8',
            'synonym_pattern': re.compile(
                r'^\s*(GU280_gp09|orf8([ _-]?protein)?)\s*$',
                re.I
            )
        },
        {
            'name': 'N',
            'synonym_pattern': re.compile(
                r'^\s*(GU280_gp10|(orf9|n|nucleocapsid|np)'
                r'([ _-]?(protein|phosphoprotein))?)\s*$',
                re.I
            )
        },
        {
            'name': 'ORF10',
            'synonym_pattern': re.compile(
                r'^\s*(GU280_gp11|orf10([ _-]?protein)?)\s*$',
                re.I
            )
        }
    ],

    default_queries={
        'fasta': fragments.SARS2_SEQUENCE_ANALYSIS_DEFAULT,
        'mutations': fragments.SARS2_MUTATIONS_ANALYSIS_DEFAULT,
        'patterns': fragments.SARS2_MUTATIONS_ANALYSIS_DEFAULT,
        'seqreads': fragments.SARS2_SEQUENCE_READS_ANALYSIS_DEFAULT
    }
)
