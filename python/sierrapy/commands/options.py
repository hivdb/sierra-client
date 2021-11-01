import click  # type: ignore
from typing import Any, Callable


DEFAULT_URLS = {
    'HIV1': 'https://hivdb.stanford.edu/graphql',
    'HIV2': 'https://hivdb.stanford.edu/hiv2/graphql',
    'SARS2': 'https://covdb.stanford.edu/sierra-sars2/graphql'
}


def url_option_callback(
    ctx: click.Context,
    param: click.Option,
    value: str
) -> str:
    if value == '__default_url__':
        value = ctx.obj.get('URL', DEFAULT_URLS[ctx.params['virus']])
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


def virus_option(*args: Any) -> Callable:
    func: Callable = click.option(
        *args,
        type=click.Choice(['HIV1', 'HIV2', 'SARS2']),
        default='HIV1',
        show_default=True,
        is_eager=True,
        help='Specify virus to be analyzed.')
    return func
