# -*- coding: utf-8 -*-

import json
import click
from collections import OrderedDict
from voluptuous import Schema, Required, MultipleInvalid, ALLOW_EXTRA

GENES = OrderedDict([
    ('PR', 99),
    ('RT', 560),
    ('IN', 288)
])


schema = Schema([{
    Required('inputSequence'): {
        Required('header'): str
    },
    Required('alignedGeneSequences'): [{
        Required('gene'): {
            Required('name'): str
        },
        Required('firstAA'): int,
        Required('lastAA'): int,
        Required('alignedNAs'): str,
        Required('prettyPairwise'): {
            Required('positionLine'): [str],
            Required('alignedNAsLine'): [str]
        }
    }]
}], extra=ALLOW_EXTRA)


@click.option('--gap-handling', default="hxb2strip",
              type=click.Choice(['squeeze', 'hxb2strip']),
              help=('Specify how you want the recipe to handle the gaps.\n\n'
                    'Specify "squeeze" to keep every gap in the result '
                    'alignment; "hxb2_strip" to strip out non-HXB2 columns.'))
@click.pass_context
def alignment(ctx, gap_handling):
    """Export aligned pol sequences from Sierra result."""
    output = ctx.obj['OUTPUT']
    sequences = json.load(ctx.obj['INPUT'])
    try:
        schema(sequences)
    except MultipleInvalid as e:
        raise click.ClickException(str(e))
    for seq in sequences:
        seqheader = seq['inputSequence']['header']
        concat_seqs = ''
        geneseqs = {gs['gene']['name']: gs
                    for gs in seq['alignedGeneSequences']}
        for gene, genesize in GENES.items():
            geneseq = geneseqs.get(gene)
            if geneseq:
                first_aa = geneseq['firstAA']
                last_aa = geneseq['lastAA']
                naseq = geneseq['alignedNAs']
            else:
                first_aa = 1
                last_aa = genesize
                naseq = '.' * genesize * 3
            if gap_handling == 'hxb2strip':
                naseq = (('.' * (first_aa - 1) * 3) +
                         naseq +
                         '.' * (genesize - last_aa) * 3)
            else:  # gap_handling == 'squeeze'
                raise NotImplementedError()
            concat_seqs += naseq
        output.write('>{}\n{}\n'.format(seqheader, concat_seqs))
