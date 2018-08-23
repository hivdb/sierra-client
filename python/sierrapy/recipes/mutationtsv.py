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
        Required('mutations'): [{
            Required('consensus'): str,
            Required('position'): int,
            Required('AAs'): str
        }]
    }]
}], extra=ALLOW_EXTRA)


@click.pass_context
def mutationtsv(ctx):
    """Export mutation set of each sequences from Sierra result."""
    output = ctx.obj['OUTPUT']
    sequences = json.load(ctx.obj['INPUT'])
    try:
        schema(sequences)
    except MultipleInvalid as e:
        raise click.ClickException(str(e))
    writer = csv.writer(output, delimiter='\t')
    writer.writerow(['Header'] + ['{} Mutations'.format(gene)
                                  for gene in GENES.keys()])
    for seq in sequences:
        seqheader = seq['inputSequence']['header']
        geneseqs = {gs['gene']['name']: gs
                    for gs in seq['alignedGeneSequences']}
        row = [seqheader]
        for gene, _ in GENES.items():
            geneseq = geneseqs.get(gene)
            mutations = ''
            if geneseq:
                mutations = ', '.join([
                    '{consensus}{position}{AAs}'
                    .format(**m).replace('-', 'Deletion')
                    for m in geneseq['mutations']])
            row.append(mutations)
        writer.writerow(row)
