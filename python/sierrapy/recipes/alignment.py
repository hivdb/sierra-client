import json
import click  # type: ignore
from collections import OrderedDict
from typing import (
    List,
    Dict,
    TextIO,
    Optional,
    OrderedDict as tOrderedDict
)

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
        Required('alignedNAs'): str,
        Required('prettyPairwise'): {
            Required('positionLine'): [str],
            Required('alignedNAsLine'): [str]
        }
    }]
}], extra=ALLOW_EXTRA)


@click.option('--gap-handling', default="hxb2strip",
              type=click.Choice(['squeeze', 'hxb2strip', 'hxb2stripkeepins']),
              help=('Specify how you want the recipe to handle the gaps.\n\n'
                    'Specify "squeeze" to keep every gap in the result '
                    'alignment; "hxb2strip" to strip out non-HXB2 columns; '
                    '"hxb2stripkeepins" to strip not non-HXB2 columns except '
                    'codon insertions.'))
@click.pass_context
def alignment(ctx: click.Context, gap_handling: str) -> None:
    """Export aligned pol sequences from Sierra result."""
    seqheader: str
    concat_seqs: str
    geneseqs: Dict[str, AlignedGeneSeq]
    gene: str
    genesize: int
    geneseq: Optional[AlignedGeneSeq]
    first_aa: int
    last_aa: int
    naseq: List[str]
    posline: List[str]
    naline: List[str]
    pos: str
    nas: str
    naseq_text: str
    output: TextIO = ctx.obj['OUTPUT']
    sequences: List[SequenceResult] = json.load(ctx.obj['INPUT'])
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
                if gap_handling.endswith('keepins'):
                    naseq = []
                    posline = geneseq['prettyPairwise']['positionLine']
                    naline = geneseq['prettyPairwise']['alignedNAsLine']
                    for pos, nas in zip(posline, naline):
                        if not pos.strip() and ' ' in nas:
                            # fs insertions
                            continue
                        naseq.append(nas)
                    naseq_text = ''.join(naseq)
                else:
                    naseq_text = geneseq['alignedNAs']
            else:
                first_aa = 1
                last_aa = genesize
                naseq_text = '.' * genesize * 3
            if gap_handling.startswith('hxb2strip'):
                naseq_text = (
                    ('.' * (first_aa - 1) * 3) +
                    naseq_text +
                    '.' * (genesize - last_aa) * 3
                )
            else:  # gap_handling == 'squeeze'
                raise NotImplementedError()
            concat_seqs += naseq_text
        output.write('>{}\n{}\n'.format(seqheader, concat_seqs))
