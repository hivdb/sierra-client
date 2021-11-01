import click  # type: ignore
from typing import Any, Callable

from .. import viruses


def url_option_callback(
    ctx: click.Context,
    param: click.Option,
    value: str
) -> str:
    if value == '__default_url__':
        value = ctx.obj.get(
            'URL', ctx.params['virus'].default_url)
    ctx.obj['URL'] = value
    return value


def url_option(*args: Any) -> Callable:
    func: Callable = click.option(
        *args,
        default='__default_url__',
        callback=url_option_callback,
        help=(
            'URL of Sierra GraphQL Web Service.  '
            '[default: production URL varied by virus]'
        ))
    return func


def virus_option_callback(
    ctx: click.Context,
    param: click.Option,
    value: str
) -> viruses.Virus:
    virus: viruses.Virus = getattr(viruses, value)
    if 'fasta' in virus.supported_commands:
        from . import fasta  # noqa
    elif ctx.command.name == 'fasta':
        raise click.UsageError(
            f"Command 'fasta' is not supported by --virus={value}."
        )
    if 'mutations' in virus.supported_commands:
        from . import mutations  # noqa
    elif ctx.command.name == 'mutations':
        raise click.UsageError(
            f"Command 'mutations' is not supported by --virus={value}."
        )
    if 'patterns' in virus.supported_commands:
        from . import patterns  # noqa
    elif ctx.command.name == 'patterns':
        raise click.UsageError(
            f"Command 'patterns' is not supported by --virus={value}."
        )
    if 'seqreads' in virus.supported_commands:
        from . import seqreads  # noqa
    elif ctx.command.name == 'seqreads':
        raise click.UsageError(
            f"Command 'seqreads' is not supported by --virus={value}."
        )
    return virus


def virus_option(*args: Any) -> Callable:
    func: Callable = click.option(
        *args,
        type=click.Choice(['HIV1', 'HIV2', 'SARS2']),
        default='HIV1',
        show_default=True,
        is_eager=True,
        callback=virus_option_callback,
        help='Specify virus to be analyzed.')
    return func
