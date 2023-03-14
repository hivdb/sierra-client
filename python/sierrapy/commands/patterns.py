# -*- coding: utf-8 -*-
import os
import re
import json
import math
import tqdm  # type: ignore
import click  # type: ignore
from more_itertools import chunked
from typing import List, Dict, Any, TextIO, Optional, Iterator, Tuple

from .. import viruses
from ..sierraclient import SierraClient

from .cli import cli
from .options import url_option, virus_option


def iter_patterns(
    pattern_files: List[TextIO]
) -> Iterator[Tuple[str, List[str]]]:
    fp: TextIO
    ptn_name: Optional[str]
    for fp in pattern_files:
        ptn_name = None
        for line in fp:
            ptn = line.strip()
            if not ptn:
                continue
            if line.startswith('#'):
                continue
            if line.startswith('>'):
                ptn_name = line[1:].strip()
                continue
            elif ptn_name is None:
                ptn_name = ptn
            yield ptn_name, re.split(r'[,;+ \t]+', ptn)
            ptn_name = None


@cli.command()
@click.argument('patterns', nargs=-1, required=True, type=click.File('r'))
@url_option('--url')
@virus_option('--virus')
@click.option('-q', '--query', type=click.File('r'),
              help=('A file contains GraphQL fragment definition '
                    'on `MutationsAnalysis`.'))
@click.option('-o', '--output', default='-',
              type=click.Path(dir_okay=False),
              help='File path to store the JSON result.')
@click.option('--sharding', type=int, default=100,
              help='Save JSON result files per n patterns.')
@click.option('--no-sharding', is_flag=True,
              help='Save JSON result to a single file.')
@click.option('--step', type=int, default=40,
              help='Send batch requests per n patterns.')
@click.option('--skip', type=int, default=0,
              help='Skip first n patterns.')
@click.option('--total', type=int, default=0,
              help=(
                  'Total number of patterns; '
                  'specify one to visualize a progress bar.'
              ))
@click.option('--ugly', is_flag=True, help='Output compressed JSON result.')
@click.pass_context
def patterns(
    ctx: click.Context,
    url: str,
    virus: viruses.Virus,
    patterns: List[TextIO],
    query: TextIO,
    output: str,
    sharding: int,
    no_sharding: bool,
    step: int,
    skip: int,
    total: int,
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
    client.toggle_progress(False)

    fp: TextIO
    query_text: str
    ptns: Iterator[Tuple[str, List[str]]] = iter_patterns(patterns)
    idx_offset: int = math.ceil(skip / sharding)
    for _ in zip(range(skip), ptns):
        pass

    if query:
        query_text = query.read()
    else:
        query_text = virus.get_default_query('patterns')

    result: Iterator[
        Dict[str, Any]
    ] = tqdm.tqdm(
        client.iter_pattern_analysis(ptns, query_text, step),
        total=total,
        initial=skip
    )
    if no_sharding:
        with open(output, 'w') as fp:
            json.dump(list(result), fp, indent=None if ugly else 2)
    else:
        output, ext = os.path.splitext(output)
        if not ext:
            ext = 'json'
        for idx, partial in enumerate(chunked(result, sharding)):
            with open('{}.{}{}'.format(
                output, idx + idx_offset, ext
            ), 'w') as fp:
                json.dump(partial, fp, indent=None if ugly else 2)
