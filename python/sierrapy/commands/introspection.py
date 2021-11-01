import json
import click  # type: ignore

from typing import TextIO, Dict, Any

from .cli import cli


@cli.command()
@click.option('-o', '--output', default='-', type=click.File('w'),
              help='File path to store the JSON result.')
@click.option('--ugly', is_flag=True, help='Output compressed JSON result.')
@click.pass_context
def introspection(ctx: click.Context, output: TextIO, ugly: bool) -> None:
    """Output introspection of Sierra GraphQL web service."""
    result: Dict[str, Any] = ctx.obj['CLIENT'].get_introspection()
    json.dump(result, output, indent=None if ugly else 2)
