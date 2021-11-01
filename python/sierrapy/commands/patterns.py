# -*- coding: utf-8 -*-
import re
import json
import click  # type: ignore
from typing import List, Dict, Any, TextIO, Optional

from .. import viruses
from ..sierraclient import SierraClient

from .cli import cli
from .options import url_option, virus_option


@cli.command()
@click.argument('patterns', nargs=-1, required=True, type=click.File('r'))
@url_option('--url')
@virus_option('--virus')
@click.option('-q', '--query', type=click.File('r'),
              help=('A file contains GraphQL fragment definition '
                    'on `MutationsAnalysis`.'))
@click.option('-o', '--output', default='-', type=click.File('w'),
              help='File path to store the JSON result.')
@click.option('--ugly', is_flag=True, help='Output compressed JSON result.')
@click.pass_context
def patterns(
    ctx: click.Context,
    url: str,
    virus: viruses.Virus,
    patterns: List[TextIO],
    query: TextIO,
    output: TextIO,
    ugly: bool
) -> None:
    """
    Run drug resistance and other analysis for one or more files contains
    lines of PR, RT and/or IN mutations based on HIV-1 type B consensus.
    Each line is treated as a unique pattern. For example:

    \b
    >set1
    RT:M41L + RT:M184V + RT:L210W + RT:T215Y
    >set2
    PR:L24I + PR:M46L + PR:I54V + PR:V82A

    The following delimiters are supported: commas (,), plus signs (+),
    semicolon(;), whitespaces and tabs. The consensus sequences can be
    retrieved from HIVDB website: <https://goo.gl/ZBthkt>.
    """
    client: SierraClient = SierraClient(url)
    client.toggle_progress(True)

    fp: TextIO
    query_text: str
    ptn_name: Optional[str]
    ptn_names: List[Optional[str]] = []
    ptns: List[List[str]] = []
    for fp in patterns:
        ptn_name = None
        for line in fp:
            if line.startswith('#'):
                continue
            if line.startswith('>'):
                ptn_name = line[1:].strip()
                continue
            ptn_names.append(ptn_name)
            ptns.append(re.split(r'[,;+ \t]+', line.strip()))
            ptn_name = None
    if query:
        query_text = query.read()
    else:
        query_text = virus.get_default_query('patterns')
    result: List[
        Dict[str, Any]
    ] = client.pattern_analysis(ptns, ptn_names, query_text)
    json.dump(result, output, indent=None if ugly else 2)
