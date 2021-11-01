import _csv
import csv
import json
import click  # type: ignore
from collections import OrderedDict
from typing import OrderedDict as tOrderedDict, TextIO, List, Dict, Optional
from voluptuous import (  # type: ignore
    Schema, Required, MultipleInvalid, ALLOW_EXTRA
)

from ..common_types import SequenceResult, AlignedGeneSeq


GENES: tOrderedDict[str, int] = OrderedDict([
    ('PR', 99),
    ('RT', 560),
    ('IN', 288)
])


schema: Schema = Schema([{
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
def mutationtsv(ctx: click.Context) -> None:
    """Export mutation set of each sequences from Sierra result."""
    seq: SequenceResult
    seqheader: str
    geneseqs: Dict[str, AlignedGeneSeq]
    row: List[str]
    gene: str
    geneseq: Optional[AlignedGeneSeq]
    mutations: str
    output: TextIO = ctx.obj['OUTPUT']
    sequences: List[SequenceResult] = json.load(ctx.obj['INPUT'])
    try:
        schema(sequences)
    except MultipleInvalid as e:
        raise click.ClickException(str(e))
    writer: _csv._writer = csv.writer(output, delimiter='\t')
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
