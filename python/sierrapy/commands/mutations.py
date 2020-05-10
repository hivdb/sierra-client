# -*- coding: utf-8 -*-
import json
import click

from .. import fragments
from ..sierraclient import SierraClient

from .cli import cli
from .options import url_option


@cli.command()
@click.argument('mutations', nargs=-1, required=True)
@url_option('--url')
@click.option('-q', '--query', type=click.File('r'),
              help=('A file contains GraphQL fragment definition '
                    'on `MutationsAnalysis`.'))
@click.option('-o', '--output', default='-', type=click.File('w'),
              help='File path to store the JSON result.')
@click.option('--ugly', is_flag=True, help='Output compressed JSON result.')
@click.pass_context
def mutations(ctx, url, mutations, query, output, ugly):
    """
    Run drug resistance and other analysis for PR, RT and/or IN mutations.
    For Example:

    \b
    sierrapy mutations PR:E35E_D RT:T67- IN:M50MI

    Use command "sierrapy patterns" instead if you want to run multiple sets
    of mutations in one request.
    """
    client = SierraClient(url)
    client.toggle_progress(True)
    if query:
        query = query.read()
    else:
        query = fragments.MUTATIONS_ANALYSIS_DEFAULT
    result = client.mutations_analysis(mutations, query)
    json.dump(result, output, indent=None if ugly else 2)
