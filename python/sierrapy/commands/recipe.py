import click  # type: ignore

from typing import TextIO

from .cli import cli
from .. import recipes


@cli.group()
@click.option('--input', default='-', type=click.File('r'),
              help='JSON result from Sierra web service.')
@click.option('--output', default='-', type=click.File('w'),
              help='File path to store the result.')
@click.pass_context
def recipe(ctx: click.Context, input: TextIO, output: TextIO) -> None:
    """Post process Sierra web service output."""
    ctx.obj['INPUT'] = input
    ctx.obj['OUTPUT'] = output


for subcommand in recipes.__all__:
    subcommand = getattr(recipes, subcommand)
    recipe.command()(subcommand)
