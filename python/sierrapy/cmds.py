#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
import json
import argparse
from itertools import chain
from sierrapy import fastareader, SierraClient, fragments, VERSION


def add_url_arguments(subparser):
    subparser.add_argument(
        '--url', type=str,
        default='https://hivdb.stanford.edu/graphql',
        help='URL of Sierra GraphQL webservice.')


def add_common_arguments(subparser):
    add_url_arguments(subparser)
    subparser.add_argument(
        '--ugly', action='store_true',
        help='output compressed JSON result instead of pretty formatted.')
    subparser.add_argument(
        '-o', '--output', type=argparse.FileType('w'),
        help=('file path to store the JSON result.'),
        default=sys.stdout)


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description='A Client of HIVdb Sierra GraphQL Webservice.')
    subparsers = parser.add_subparsers(
        dest='method', metavar='METHOD',
        help="method to be used for querying the webservice.")

    subparsers.required = False
    seqparser = subparsers.add_parser(
        'fasta', help='Analyze input FASTA sequences.')
    seqparser.add_argument(
        'fasta', metavar='FASTAFILE',
        nargs='+', type=argparse.FileType('r'),
        help='a FASTA-format file contains HIV-1 pol DNA sequences.')
    seqparser.add_argument(
        '-q', '--query', type=argparse.FileType('r'),
        help=('a file contains GraphQL fragment definition '
              'on `SequenceAnalysis`.'))
    add_common_arguments(seqparser)
    mutparser = subparsers.add_parser(
        'mutations', help='Analyze input mutations.')
    mutparser.add_argument(
        'mutations', metavar='MUTATION',
        nargs='+', type=str,
        help=(
            'PR, RT, and/or IN mutations based on HIV-1 type B consensus. '
            'Examples: PR:E35E_D RT:T67- IN:M50MI. Retrieve the consensus '
            'sequences from HIVdb website: https://goo.gl/ZBthkt.'))
    mutparser.add_argument(
        '-q', '--query', type=argparse.FileType('r'),
        help=('a file contains GraphQL fragment definition '
              'on `MutationsAnalysis`.'))
    add_common_arguments(mutparser)
    introspection_parser = subparsers.add_parser(
        'introspection',
        help='output introspection of Sierra GraphQL service.')
    add_common_arguments(introspection_parser)
    parser.add_argument(
        '-v', '--version', action=VersionAction,
        help=('show client and HIVdb algorithm version then exit.'))
    add_url_arguments(parser)
    subparsers.required = True
    return parser.parse_args(argv)


def fasta_handler(client, args):
    sequences = list(chain(*[fastareader.load(fp) for fp in args.fasta]))
    query = fragments.SEQUENCE_ANALYSIS_DEFAULT
    if args.query:
        query = args.query.read()
    result = client.sequence_analysis(sequences, query)
    json.dump(result, args.output, indent=None if args.ugly else 2)


def mutations_handler(client, args):
    query = fragments.MUTATIONS_ANALYSIS_DEFAULT
    if args.query:
        query = args.query.read()
    result = client.mutations_analysis(args.mutations, query)
    json.dump(result, args.output, indent=None if args.ugly else 2)


def introspection_handler(client, args):
    result = client.get_introspection()
    json.dump(result, args.output, indent=None if args.ugly else 2)


class VersionAction(argparse._VersionAction):

    def __call__(self, parser, namespace, values, option_string=None):
        client = SierraClient(namespace.url)
        result = client.current_version()
        formatter = parser._get_formatter()
        formatter.add_text(
            'SierraPy {}; HIVdb {} ({})'
            .format(VERSION, result['text'], result['publishDate']))
        parser.exit(message=formatter.format_help())


def main():
    args = parse_args(sys.argv[1:])
    method = args.method
    client = SierraClient(args.url)
    if method == 'fasta':
        fasta_handler(client, args)
    elif method == 'mutations':
        mutations_handler(client, args)
    elif method == 'introspection':
        introspection_handler(client, args)
    else:
        print('Program error. If you keep seeing this message please submit \n'
              'an issue on https://github.com/hivdb/sierra-client/issues.',
              file=sys.stderr)
        exit(127)


if __name__ == '__main__':
    main()
