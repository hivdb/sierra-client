# -*- coding: utf-8 -*-
import re
import json
import click
from sierrapy import fragments

from .cli import cli


@cli.command()
@click.argument('patterns', nargs=-1, required=True, type=click.File('r'))
@click.option('-q', '--query', type=click.File('r'),
              help=('A file contains GraphQL fragment definition '
                    'on `MutationsAnalysis`.'))
@click.option('-o', '--output', default='-', type=click.File('w'),
              help='File path to store the JSON result.')
@click.option('--ugly', is_flag=True, help='Output compressed JSON result.')
@click.pass_context
def patterns(ctx, patterns, query, output, ugly):
    """
    Run drug resistance and other analysis for one or more files contains
    lines of PR, RT and/or IN mutations based on HIV-1 type B consensus.
    Each line is treated as a unique pattern. For example:

    \b
    RT:M41L + RT:M184V + RT:L210W + RT:T215Y
    PR:L24I + PR:M46L + PR:I54V + PR:V82A

    The following delimiters are supported: commas (,), plus signs (+),
    semicolon(;), whitespaces and tabs. The consensus sequences can be
    retrieved from HIVDB website: <https://goo.gl/ZBthkt>.
    """
    ptns = []
    for fp in patterns:
        for line in fp:
            if line.startswith('#'):
                continue
            ptns.append(re.split(r'[,;+ \t]+', line.strip()))
    if query:
        query = query.read()
    else:
        query = fragments.MUTATIONS_ANALYSIS_DEFAULT
    result = ctx.obj['CLIENT'].pattern_analysis(ptns, query)
    json.dump(result, output, indent=None if ugly else 2)
