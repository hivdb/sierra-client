# -*- coding: utf-8 -*-

import csv
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
        Required('alignedNAs'): str
    }]
}], extra=ALLOW_EXTRA)


@click.pass_context
def sequencetsv(ctx):
    """Export mutation set of each sequences from Sierra result."""
    output = ctx.obj['OUTPUT']
    sequences = json.load(ctx.obj['INPUT'])
    try:
        schema(sequences)
    except MultipleInvalid as e:
        raise click.ClickException(str(e))
    writer = csv.writer(output, delimiter='\t')
    writer.writerow(['Header', 'Gene', 'FirstAA', 'LastAA', 'AlignedNAs'])
    for seq in sequences:
        seqheader = seq['inputSequence']['header']
        geneseqs = {gs['gene']['name']: gs
                    for gs in seq['alignedGeneSequences']}
        for gene, _ in GENES.items():
            geneseq = geneseqs.get(gene)
            if not geneseq:
                continue
            first_aa = geneseq['firstAA']
            last_aa = geneseq['lastAA']
            aligned_nas = geneseq['alignedNAs']
            writer.writerow([seqheader, gene, first_aa, last_aa, aligned_nas])
