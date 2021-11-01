import click  # type: ignore
import json
from itertools import chain
from typing import List, Dict, TextIO, Any

from .. import fastareader, fragments
from ..sierraclient import SierraClient
from ..common_types import Sequence

from .cli import cli
from .options import url_option


@cli.command()
@click.argument('fasta', nargs=-1, type=click.File('r'), required=True)
@url_option('--url')
@click.option('-q', '--query', type=click.File('r'),
              help=('A file contains GraphQL fragment definition '
                    'on `SequenceAnalysis`.'))
@click.option('-o', '--output', default='-', type=click.File('w'),
              help='File path to store the JSON result.')
@click.option('--ugly', is_flag=True, help='Output compressed JSON result.')
@click.pass_context
def fasta(
    ctx: click.Context,
    url: str,
    fasta: List[TextIO],
    query: TextIO,
    output: TextIO,
    ugly: bool
) -> None:
    """
    Run alignment, drug resistance and other analysis for one or more
    FASTA-format files contained HIV-1 pol DNA sequences.
    """
    query_text: str
    client: SierraClient = SierraClient(url)
    client.toggle_progress(True)
    sequences: List[Sequence] = list(
        chain(*[fastareader.load(fp) for fp in fasta])
    )
    if query:
        query_text = query.read()
    else:
        query_text = fragments.SEQUENCE_ANALYSIS_DEFAULT
    result: List[
        Dict[str, Any]
    ] = client.sequence_analysis(sequences, query_text, 100)
    json.dump(result, output, indent=None if ugly else 2)
