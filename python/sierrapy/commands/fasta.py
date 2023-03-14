import os
import re
import json
import math
import tqdm  # type: ignore
import click  # type: ignore
from itertools import chain
from typing import Dict, TextIO, Any, Tuple, Iterator
from more_itertools import chunked

from .. import fastareader, viruses
from ..sierraclient import SierraClient
from ..common_types import Sequence

from .cli import cli
from .options import url_option, virus_option

FASTA_PATTERN = re.compile(r'\.fa(?:s(?:ta)?)?$', re.I)


def iter_fasta_files(
    file_or_dir: Tuple[str, ...]
) -> Iterator[TextIO]:
    for one in file_or_dir:
        if os.path.isfile(one):
            yield open(one)
        else:
            for fn in os.listdir(one):
                if not FASTA_PATTERN.search(fn):
                    continue
                yield open(os.path.join(one, fn))


@cli.command()
@click.argument(
    'fasta',
    nargs=-1,
    type=click.Path(exists=True),
    required=True)
@url_option('--url')
@virus_option('--virus')
@click.option('-q', '--query', type=click.File('r'),
              help=('A file contains GraphQL fragment definition '
                    'on `SequenceAnalysis`.'))
@click.option('-o', '--output', default='-',
              type=click.Path(dir_okay=False),
              help='File path to store the JSON result.')
@click.option('--sharding', type=int, default=100,
              help='Save JSON result files per n sequences.')
@click.option('--no-sharding', is_flag=True,
              help='Save JSON result to a single file.')
@click.option('--step', type=int, default=40,
              help='Send batch requests per n sequences.')
@click.option('--skip', type=int, default=0,
              help='Skip first n sequences.')
@click.option('--total', type=int, default=0,
              help=(
                  'Total number of sequences; '
                  'specify one to visualize a progress bar.'
              ))
@click.option('--ugly', is_flag=True, help='Output compressed JSON result.')
@click.pass_context
def fasta(
    ctx: click.Context,
    url: str,
    virus: viruses.Virus,
    fasta: Tuple[str, ...],
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
    Run alignment, drug resistance and other analysis for one or more
    FASTA-format files contained DNA sequences.
    """
    ext: str
    query_text: str
    client: SierraClient = SierraClient(url)
    client.toggle_progress(False)

    fasta_fps: Iterator[TextIO] = iter_fasta_files(fasta)

    sequences: Iterator[Sequence] = chain(*(
        fastareader.load(fp) for fp in fasta_fps
    ))
    idx_offset: int = math.ceil(skip / sharding)
    for _ in zip(range(skip), sequences):
        pass

    if query:
        query_text = query.read()
    else:
        query_text = virus.get_default_query('fasta')

    result: Iterator[
        Dict[str, Any]
    ] = tqdm.tqdm(
        client.iter_sequence_analysis(sequences, query_text, step),
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
