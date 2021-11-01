import click  # type: ignore

from ..sierraclient import SierraClient, VERSION

from .options import url_option


@click.group(invoke_without_command=True)
@url_option('--url')
@click.option('--version', is_flag=True,
              help='Show client and the HIVDB algorithm version.')
@click.pass_context
def cli(ctx: click.Context, url: str, version: bool) -> None:
    """A Client of HIVDB Sierra GraphQL Web Service"""
    client: SierraClient = SierraClient(url)
    client.toggle_progress(True)
    if version:
        algv, progv = client.current_version()
        click.echo(
            'SierraPy {}; Sierra {} ({}); HIVdb {} ({})'
            .format(VERSION,
                    progv['text'], progv['publishDate'],
                    algv['text'], algv['publishDate']))
        exit(0)
    elif not ctx.invoked_subcommand:
        click.echo(cli.get_help(ctx))
