# -*- coding: utf-8 -*-
import re
import click  # type: ignore
import csv
import json

from typing import Tuple, Optional, TextIO, List, Dict

from .. import fragments
from ..sierraclient import SierraClient
from ..common_types import PosReads, SeqReads

from .cli import cli
from .options import url_option

VALID_GENES = ['PR', 'RT', 'IN', 'POL']


def normalize_position(
    gene: str, pos: int
) -> Tuple[Optional[str], Optional[int]]:
    if gene == 'POL':
        pos -= 56
        if pos < 1:
            return None, None
        elif pos < 1 + 99:
            return 'PR', pos
        elif pos < 1 + 99 + 560:
            return 'RT', pos - 99
        else:
            return 'IN', pos - 99 - 560
    else:
        return gene, pos


def normalize_gene(gene: str) -> Optional[str]:
    if re.match(r'^\s*(PR|protease)\s*$', gene, re.I):
        return 'PR'
    elif re.match(r'^\s*(RT|reverse transcriptase)\s*$', gene, re.I):
        return 'RT'
    elif re.match(r'^\s*(IN|INT|integrase)\s*$', gene, re.I):
        return 'IN'
    elif re.match(r'^\s*(pol)\s*$', gene, re.I):
        return 'POL'
    return None


def parse_seqreads(
        fp: TextIO,
        min_prevalence: float = 0.,
        min_codon_count: int = 0,
        min_read_depth: int = -1
) -> SeqReads:
    aapos_text: str
    total_reads_text: str
    codon_reads_text: str
    gene: Optional[str]
    aapos: Optional[int]
    gpmap: Dict[Tuple[str, int], PosReads] = {}
    total_reads: int
    codon_reads: int
    gpkey: Tuple[str, int]
    firstrow = fp.readline()
    delimiter = ','
    if '\t' in firstrow:
        delimiter = '\t'
    fp.seek(0)
    for row in csv.reader(fp, delimiter=delimiter):
        num_cols = len(row)
        if num_cols >= 5:
            (gene,
             aapos_text,
             total_reads_text,
             codon,
             codon_reads_text) = row[:5]
        else:
            continue
        codon = codon.upper()
        gene = normalize_gene(gene)
        # skip header and problem rows
        if (
            not gene or
            gene not in VALID_GENES or
            not aapos_text.isdigit() or
            not total_reads_text.isdigit() or
            len(codon) < 3 or
            not codon_reads_text.isdigit()
        ):
            continue
        try:
            aapos = int(aapos_text)
        except (TypeError, ValueError):
            continue
        gene, aapos = normalize_position(gene, aapos)
        if gene is None or aapos is None:
            continue
        total_reads = int(total_reads_text)
        codon_reads = int(codon_reads_text)
        gpkey = (gene, aapos)
        if gpkey not in gpmap:
            gpmap[gpkey] = {
                'gene': gene,
                'position': aapos,
                'totalReads': total_reads,
                'allCodonReads': []
            }
        gpmap[gpkey]['allCodonReads'].append(
            {'codon': codon, 'reads': codon_reads})
    return {
        'name': fp.name,
        'strain': 'HIV1',
        'allReads': sorted(
            gpmap.values(),
            key=lambda pcr: (VALID_GENES.index(pcr['gene']), pcr['position'])),
        'minPrevalence': min_prevalence,
        'minCodonCount': min_codon_count,
        'minReadDepth': min_read_depth
    }


@cli.command()
@click.argument('seqreads', nargs=-1, type=click.File('r'), required=True)
@url_option('--url')
@click.option('-p', '--pcnt-cutoff', type=float, default=0, show_default=True,
              help=('Minimal prevalence cutoff applied on the sequence reads '
                    '(range: 0-1.0)'))
@click.option('-c', '--num-cutoff', type=int, default=0, show_default=True,
              help='Minimal read count cutoff applied on the sequence reads.')
@click.option('-d', '--min-read-depth', type=int, default=-1,
              show_default=True,
              help=('Minimal read depth applied to '
                    'each position of this sequence'))
@click.option('-q', '--query', type=click.File('r'), show_default=True,
              help=('A file contains GraphQL fragment definition '
                    'on `SequenceAnalysis`.'))
@click.option('-o', '--output', default='-', type=click.File('w'),
              show_default=True, help='File path to store the JSON result.')
@click.option('--ugly', is_flag=True, help='Output compressed JSON result.')
@click.pass_context
def seqreads(
    ctx: click.Context,
    url: str,
    seqreads: List[TextIO],
    pcnt_cutoff: float,
    num_cutoff: int,
    min_read_depth: int,
    query: TextIO,
    output: TextIO,
    ugly: bool
) -> None:
    """
    Run alignment, drug resistance and other analysis for one or more
    tab-delimited text files contained codon reads of HIV-1 pol DNA sequences.
    """
    client: SierraClient = SierraClient(url)
    client.toggle_progress(True)

    query_text: str
    seqreads_payload: List[SeqReads] = [parse_seqreads(
        fp, pcnt_cutoff, num_cutoff, min_read_depth
    ) for fp in seqreads]
    if query:
        query_text = query.read()
    else:
        query_text = fragments.SEQUENCE_READS_ANALYSIS_DEFAULT
    result = client.sequence_reads_analysis(seqreads_payload, query_text, 2)
    json.dump(result, output, indent=None if ugly else 2)
