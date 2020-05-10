import click


DEFAULT_URL = 'https://hivdb.stanford.edu/graphql'


def url_option_callback(ctx, param, value):
    if value == '__default_url__':
        value = ctx.obj.get('URL', DEFAULT_URL)
    ctx.obj['URL'] = value
    return value


def url_option(*args):
    return click.option(
        *args,
        default='__default_url__',
        callback=url_option_callback,
        help='URL of Sierra GraphQL Web Service.')
