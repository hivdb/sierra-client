import json
import click  # type: ignore
from typing import List, Dict, TextIO, Any

from .. import viruses
from ..sierraclient import SierraClient

from .cli import cli
from .options import url_option, virus_option


@cli.command()
@click.argument('mutations', nargs=-1, required=True)
@url_option('--url')
@virus_option('--virus')
@click.option('-q', '--query', type=click.File('r'),
              help=('A file contains GraphQL fragment definition '
                    'on `MutationsAnalysis`.'))
@click.option('-o', '--output', default='-', type=click.File('w'),
              help='File path to store the JSON result.')
@click.option('--ugly', is_flag=True, help='Output compressed JSON result.')
@click.pass_context
def mutations(
    ctx: click.Context,
    url: str,
    virus: viruses.Virus,
    mutations: List[str],
    query: TextIO,
    output: TextIO,
    ugly: bool
) -> None:
    """
    Run drug resistance and other analysis for PR, RT and/or IN mutations.
    For Example:

    \b
    sierrapy mutations PR:E35E_D RT:T67- IN:M50MI

    Use command "sierrapy patterns" instead if you want to run multiple sets
    of mutations in one request.
    """
    query_text: str
    client: SierraClient = SierraClient(url)
    client.toggle_progress(True)
    if query:
        query_text = query.read()
    else:
        query_text = virus.get_default_query('mutations')
    result: Dict[str, Any] = client.mutations_analysis(mutations, query_text)
    json.dump(result, output, indent=None if ugly else 2)
