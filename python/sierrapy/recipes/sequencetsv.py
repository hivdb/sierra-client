import csv
import _csv
import json
import click  # type: ignore
from collections import OrderedDict
from typing import OrderedDict as tOrderedDict, TextIO, List, Dict, Optional
from voluptuous import (  # type: ignore
    Schema, Required, MultipleInvalid, ALLOW_EXTRA
)

from ..common_types import SequenceResult, AlignedGeneSeq

GENES: tOrderedDict = OrderedDict([
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
        Required('firstAA'): int,
        Required('lastAA'): int,
        Required('alignedNAs'): str
    }]
}], extra=ALLOW_EXTRA)


@click.pass_context
def sequencetsv(ctx: click.Context) -> None:
    """Export mutation set of each sequences from Sierra result."""
    seq: SequenceResult
    seqheader: str
    geneseqs: Dict[str, AlignedGeneSeq]
    geneseq: Optional[AlignedGeneSeq]
    first_aa: int
    last_aa: int
    aligned_nas: str
    output: TextIO = ctx.obj['OUTPUT']
    sequences: List[SequenceResult] = json.load(ctx.obj['INPUT'])
    try:
        schema(sequences)
    except MultipleInvalid as e:
        raise click.ClickException(str(e))
    writer: _csv._writer = csv.writer(output, delimiter='\t')
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
