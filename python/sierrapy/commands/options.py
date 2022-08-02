import os
import re
import click  # type: ignore
from typing import Any, Callable, List

from .. import viruses


def url_option_callback(
    ctx: click.Context,
    param: click.Option,
    value: str
) -> str:
    if 'URL' in ctx.obj:
        value = ctx.obj['URL']
    elif value == '__default_url__':
        value = ctx.params['virus'].default_url
    else:
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
    virus: viruses.Virus
    if 'virus' in ctx.obj:
        virus = ctx.obj['virus']
        return virus
    virus = getattr(viruses, value or 'HIV1')
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
    if value is not None:
        ctx.obj['virus'] = virus
    return virus


def virus_option(*args: Any) -> Callable:
    func: Callable = click.option(
        *args,
        type=click.Choice(['HIV1', 'HIV2', 'SARS2']),
        default='HIV1', show_default=True,
        is_eager=True,
        callback=virus_option_callback,
        help='Specify virus to be analyzed.')
    return func


def file_or_dir_argument(*args: Any, pattern: re.Pattern) -> Callable:

    def file_or_dir_callback(
        ctx: click.Context,
        param: click.Argument,
        value: str
    ) -> List[str]:
        if pattern.search(value):
            return [value]
        else:
            new_value: List[str] = []
            for dirpath, _, filenames in os.walk(value, followlinks=True):
                for filename in filenames:
                    if pattern.search(filename):
                        new_value.append(os.path.join(dirpath, filename))
            return new_value

    func: Callable = click.argument(
        *args,
        type=click.Path(exists=True, file_okay=True,
                        dir_okay=True, resolve_path=True),
        callback=file_or_dir_callback,
        required=True)
    return func
