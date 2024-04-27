import json
import click  # type: ignore

from typing import TextIO, Dict, Any

from .cli import cli
from .options import url_option

from ..sierraclient import SierraClient


@cli.command()
@url_option('--url')
@click.option('-o', '--output', default='-', type=click.File('w'),
              help='File path to store the JSON result.')
@click.option('--ugly', is_flag=True, help='Output compressed JSON result.')
@click.pass_context
def introspection(ctx: click.Context, url, output: TextIO, ugly: bool) -> None:
    """Output introspection of Sierra GraphQL web service."""
    client: SierraClient = SierraClient(url)
    client.current_version()
    result: Dict[str, Any] = client.get_introspection()
    json.dump(result, output, indent=None if ugly else 2)
