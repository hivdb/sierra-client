# -*- coding: utf-8 -*-
import click
import json
from itertools import chain

from .. import fastareader, fragments
from ..sierraclient import SierraClient

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
def fasta(ctx, url, fasta, query, output, ugly):
    """
    Run alignment, drug resistance and other analysis for one or more
    FASTA-format files contained HIV-1 pol DNA sequences.
    """
    client = SierraClient(url)
    client.toggle_progress(True)
    sequences = list(chain(*[fastareader.load(fp) for fp in fasta]))
    if query:
        query = query.read()
    else:
        query = fragments.SEQUENCE_ANALYSIS_DEFAULT
    result = client.sequence_analysis(sequences, query, 100)
    json.dump(result, output, indent=None if ugly else 2)
