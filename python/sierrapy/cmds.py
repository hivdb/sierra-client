#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import re
import sys
import json
import argparse
from itertools import chain
from sierrapy import fastareader, SierraClient, fragments, VERSION


class SmartFormatter(argparse.HelpFormatter):
    """A piece of code from http://stackoverflow.com/a/22157136/2644759"""

    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)


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


def add_fasta_subparser(subparsers):
    seqparser = subparsers.add_parser(
        'fasta', help='Analyze input FASTA sequences.')
    seqparser.add_argument(
        'fasta', metavar='FASTAFILE',
        nargs='+', type=argparse.FileType('r'),
        help=(
            'one or more FASTA-format files contains HIV-1 pol DNA sequences.'
        ))
    seqparser.add_argument(
        '-q', '--query', type=argparse.FileType('r'),
        help=('a file contains GraphQL fragment definition '
              'on `SequenceAnalysis`.'))
    add_common_arguments(seqparser)


def add_mutations_subparser(subparsers):
    mutparser = subparsers.add_parser(
        'mutations', help='Analyze a list of mutations.')
    mutparser.add_argument(
        'mutations', metavar='MUTATION',
        nargs='+', type=str,
        help=(
            'PR, RT, and/or IN mutations based on HIV-1 type B consensus. '
            'Examples: PR:E35E_D RT:T67- IN:M50MI. Retrieve the consensus '
            'sequences from HIVDB website: <https://goo.gl/ZBthkt>.'))
    mutparser.add_argument(
        '-q', '--query', type=argparse.FileType('r'),
        help=('a file contains GraphQL fragment definition '
              'on `MutationsAnalysis`.'))
    add_common_arguments(mutparser)


def add_patterns_subparser(subparsers):
    patparser = subparsers.add_parser(
        'patterns',
        formatter_class=SmartFormatter,
        help='Analyze a list of patterns (multiple lists of mutations).')
    patparser.add_argument(
        'patterns', metavar='PATTERNS_FILE',
        nargs='+', type=argparse.FileType('r'),
        help=(
            'R|'
            'one or more files contains lines of PR, RT and/or IN\n'
            'mutations based on HIV-1 type B consensus. Each line\n'
            'is treated as a unique pattern. For example:\n\n'
            'RT:M41L + RT:M184V + RT:L210W + RT:T215Y\n'
            'PR:L24I + PR:M46L + PR:I54V + PR:V82A\n\n'
            'The following delimiters are supported: commas (,),\n'
            'plus signs (+), semicolon(;), whitespaces and tabs.\n'
            'The consensus sequences can be retrieved from HIVDB\n'
            'website: <https://goo.gl/ZBthkt>.'))
    patparser.add_argument(
        '-q', '--query', type=argparse.FileType('r'),
        help=('a file contains GraphQL fragment definition '
              'on `MutationsAnalysis`.'))
    add_common_arguments(patparser)


def add_introspection_subparser(subparsers):
    introspection_parser = subparsers.add_parser(
        'introspection',
        help='output introspection of Sierra GraphQL service.')
    add_common_arguments(introspection_parser)


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description='A Client of HIVdb Sierra GraphQL Webservice.')
    subparsers = parser.add_subparsers(
        dest='method', metavar='METHOD',
        help="method to be used for querying the webservice.")

    subparsers.required = False
    add_fasta_subparser(subparsers)
    add_mutations_subparser(subparsers)
    add_patterns_subparser(subparsers)
    add_introspection_subparser(subparsers)
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


def patterns_handler(client, args):
    patterns = []
    for fp in args.patterns:
        for line in fp:
            patterns.append(re.split(r'[,;+ \t]+', line))
    query = fragments.MUTATIONS_ANALYSIS_DEFAULT
    if args.query:
        query = args.query.read()
    result = client.pattern_analysis(patterns, query)
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


if __name__ == '__main__':
    main()
