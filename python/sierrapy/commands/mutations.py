# -*- coding: utf-8 -*-
import json
import click

from .. import fragments
from .cli import cli


@cli.command()
@click.argument('mutations', nargs=-1, required=True)
@click.option('-q', '--query', type=click.File('r'),
              help=('A file contains GraphQL fragment definition '
                    'on `MutationsAnalysis`.'))
@click.option('-o', '--output', default='-', type=click.File('w'),
              help='File path to store the JSON result.')
@click.option('--ugly', is_flag=True, help='Output compressed JSON result.')
@click.pass_context
def mutations(ctx, mutations, query, output, ugly):
    """
    Run drug resistance and other analysis for PR, RT and/or IN mutations.
    For Example:

    \b
    sierrapy mutations PR:E35E_D RT:T67- IN:M50MI

    Use command "sierrapy patterns" instead if you want to run multiple sets
    of mutations in one request.
    """
    if query:
        query = query.read()
    else:
        query = fragments.MUTATIONS_ANALYSIS_DEFAULT
    result = ctx.obj['CLIENT'].mutations_analysis(mutations, query)
    json.dump(result, output, indent=None if ugly else 2)
