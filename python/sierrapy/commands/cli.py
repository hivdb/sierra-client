# -*- coding: utf-8 -*-
import click

from ..sierraclient import SierraClient, VERSION


@click.group(invoke_without_command=True)
@click.option('--url',
              default='https://hivdb.stanford.edu/graphql',
              help='URL of Sierra GraphQL Web Service.')
@click.option('--version', is_flag=True,
              help='Show client and the HIVDB algorithm version.')
@click.pass_context
def cli(ctx, url, version):
    """A Client of HIVDB Sierra GraphQL Web Service"""
    ctx.obj['URL'] = url
    client = ctx.obj['CLIENT'] = SierraClient(url)
    client.toggle_progress(True)
    if version:
        result = client.current_version()
        click.echo(
            'SierraPy {}; HIVdb {} ({})'
            .format(VERSION, result['text'], result['publishDate']))
        exit(0)
    elif not ctx.invoked_subcommand:
        click.echo(cli.get_help(ctx))
    """
    args = parse_args(sys.argv[1:])
    method = args.method
    client = SierraClient(args.url)
    client.toggle_progress(True)
    if method == 'fasta':
        fasta_handler(client, args)
    elif method == 'mutations':
        mutations_handler(client, args)
    elif method == 'patterns':
        patterns_handler(client, args)
    elif method == 'introspection':
        introspection_handler(client, args)
    else:
        print('Program error. If you keep seeing this message please submit \n'
              'an issue on https://github.com/hivdb/sierra-client/issues.',
              file=sys.stderr)
        exit(127)
    """
