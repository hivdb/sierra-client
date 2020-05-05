# -*- coding: utf-8 -*-
import click
import json
from itertools import chain

from .. import fastareader, fragments
from .cli import cli


@cli.command()
@click.argument('fasta', nargs=-1, type=click.File('r'), required=True)
@click.option('-q', '--query', type=click.File('r'),
              help=('A file contains GraphQL fragment definition '
                    'on `SequenceAnalysis`.'))
@click.option('-o', '--output', default='-', type=click.File('w'),
              help='File path to store the JSON result.')
@click.option('--ugly', is_flag=True, help='Output compressed JSON result.')
@click.pass_context
def fasta(ctx, fasta, query, output, ugly):
    """
    Run alignment, drug resistance and other analysis for one or more
    FASTA-format files contained HIV-1 pol DNA sequences.
    """
    sequences = list(chain(*[fastareader.load(fp) for fp in fasta]))
    if query:
        query = query.read()
    else:
        query = fragments.SEQUENCE_ANALYSIS_DEFAULT
    result = ctx.obj['CLIENT'].sequence_analysis(sequences, query, 100)
    json.dump(result, output, indent=None if ugly else 2)
