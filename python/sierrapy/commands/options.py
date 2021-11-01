import click  # type: ignore
from typing import Any, Callable


DEFAULT_URL = 'https://hivdb.stanford.edu/graphql'


def url_option_callback(
    ctx: click.Context,
    param: Any,
    value: str
) -> str:
    if value == '__default_url__':
        value = ctx.obj.get('URL', DEFAULT_URL)
    ctx.obj['URL'] = value
    return value


def url_option(*args: Any) -> Callable:
    func: Callable = click.option(
        *args,
        default='__default_url__',
        callback=url_option_callback,
        help='URL of Sierra GraphQL Web Service.')
    return func
