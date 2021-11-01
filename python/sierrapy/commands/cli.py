import click  # type: ignore

from .. import viruses
from ..sierraclient import SierraClient, VERSION

from .options import url_option, virus_option


@click.group(
    context_settings={'max_content_width': 120},
    invoke_without_command=True
)
@url_option('--url')
@virus_option('--virus')
@click.option('--version', is_flag=True,
              help='Show client and the HIVDB algorithm version.')
@click.pass_context
def cli(
    ctx: click.Context,
    url: str,
    virus: viruses.Virus,
    version: bool
) -> None:
    """A Client of HIVDB Sierra GraphQL Web Service

    Default endpoint URLs:

    \b
    - HIV1: https://hivdb.stanford.edu/graphql
    - HIV2: https://hivdb.stanford.edu/hiv2/graphql
    - SARS2: https://covdb.stanford.edu/sierra-sars2/graphql
    """
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
