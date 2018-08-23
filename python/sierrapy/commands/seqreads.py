# -*- coding: utf-8 -*-
import click
import csv
import json

from .. import fragments
from .cli import cli

VALID_GENES = ['PR', 'RT', 'IN']


def parse_seqreads(fp, min_prevalence=-1, min_read_depth=-1):
    gpmap = {}
    for row in csv.reader(fp, delimiter='\t'):
        num_cols = len(row)
        if num_cols >= 5:
            gene, aapos, total_reads, codon, codon_reads = row[:5]
        else:
            continue
        if gene not in VALID_GENES or not aapos.isdigit() or \
                not total_reads.isdigit() or len(codon) < 3 or \
                not codon_reads.isdigit():
            continue
        aapos = int(aapos)
        total_reads = int(total_reads)
        codon_reads = int(codon_reads)
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
        'allReads': sorted(
            gpmap.values(),
            key=lambda pcr: (VALID_GENES.index(pcr['gene']), pcr['position'])),
        'minPrevalence': min_prevalence,
        'minReadDepth': min_read_depth
    }


@cli.command()
@click.argument('seqreads', nargs=-1, type=click.File('r'), required=True)
@click.option('-p', '--cutoff', type=float, default=-1,
              help=('Minimal prevalence cutoff applied on the sequence reads'))
@click.option('-d', '--min-read-depth', type=int, default=-1,
              help=('Minimal read depth applied to '
                    'each codon of this sequence'))
@click.option('-q', '--query', type=click.File('r'),
              help=('A file contains GraphQL fragment definition '
                    'on `SequenceAnalysis`.'))
@click.option('-o', '--output', default='-', type=click.File('w'),
              help='File path to store the JSON result.')
@click.option('--ugly', is_flag=True, help='Output compressed JSON result.')
@click.pass_context
def seqreads(ctx, seqreads, cutoff, min_read_depth, query, output, ugly):
    """
    Run alignment, drug resistance and other analysis for one or more
    tab-delimited text files contained codon reads of HIV-1 pol DNA sequences.
    """
    seqreads = [parse_seqreads(fp, cutoff, min_read_depth) for fp in seqreads]
    if query:
        query = query.read()
    else:
        query = fragments.SEQUENCE_READS_ANALYSIS_DEFAULT
    result = ctx.obj['CLIENT'].sequence_reads_analysis(seqreads, query, 2)
    json.dump(result, output, indent=None if ugly else 2)
