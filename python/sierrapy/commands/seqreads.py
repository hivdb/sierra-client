import click  # type: ignore
import csv
import re
import json

from typing import Tuple, Optional, TextIO, List, Dict

from .. import viruses
from ..sierraclient import SierraClient
from ..common_types import PosReads, SeqReads, UntransRegion

from .cli import cli
from .options import url_option, virus_option

UTR_BEGIN: re.Pattern = re.compile(
    r'^# *--- *untranslated regions begin *---'
)
UTR_END: re.Pattern = re.compile(
    r'^# *--- *untranslated regions end *---'
)
UTR_PATTERN: re.Pattern = re.compile(
    r'# *(?P<name>[\S]+) (?P<refStart>\d+)'
    r'\.\.(?P<refEnd>\d+): *(?P<consensus>[\S]+)'
)


def parse_untrans_regions(fp: TextIO) -> List[UntransRegion]:
    row: str
    groupdict: Dict[str, str]
    begin: bool = False
    results: List[UntransRegion] = []
    for row in fp:
        if UTR_END.search(row):
            begin = False
        elif begin:
            match: Optional[re.Match] = UTR_PATTERN.search(row)
            if match:
                groupdict = match.groupdict()

                results.append({
                    'name': groupdict['name'],
                    'refStart': int(groupdict['refStart']),
                    'refEnd': int(groupdict['refEnd']),
                    'consensus': groupdict['consensus']
                })
        elif UTR_BEGIN.search(row):
            begin = True
    return results


def parse_seqreads(
    fp: TextIO,
    virus: viruses.Virus,
    min_prevalence: float,
    max_mixture_rate: float,
    min_codon_reads: int,
    min_position_reads: int
) -> SeqReads:
    aapos_text: str
    total_reads_text: str
    codon_reads_text: str
    gene: Optional[str]
    aapos: Optional[int]
    total_reads: int
    codon_reads: int
    codon: str
    gpkey: Tuple[str, int]

    untrans_regions: List[UntransRegion] = parse_untrans_regions(fp)
    fp.seek(0)
    while True:
        firstrow = fp.readline()
        if firstrow.startswith('#'):
            continue
        delimiter = ','
        if '\t' in firstrow:
            delimiter = '\t'
        break
    fp.seek(0)

    gpmap: Dict[Tuple[str, int], PosReads] = {}
    for row in csv.reader(fp, delimiter=delimiter):
        if row[0].startswith('#'):
            continue
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
        try:
            aapos = int(aapos_text)
        except (TypeError, ValueError):
            continue
        gene = virus.synonym_to_gene_name(gene)
        # skip header and problem rows
        if (
            not gene or
            not aapos_text.isdigit() or
            not total_reads_text.isdigit() or
            len(codon) < 3 or
            not codon_reads_text.isdigit()
        ):
            continue
        gene, aapos = virus.source_gene_to_target_gene_position(gene, aapos)
        if gene is None or aapos is None:
            continue
        try:
            total_reads = int(total_reads_text)
        except (TypeError, ValueError):
            continue
        if total_reads == 0:
            continue
        try:
            codon_reads = int(codon_reads_text)
        except (TypeError, ValueError):
            continue
        if codon_reads == 0:
            continue
        if codon.count('-') < 3:
            codon = codon.replace('-', '')
        if len(codon) < 3:
            continue
        gpkey = (gene, aapos)
        if gpkey not in gpmap:
            gpmap[gpkey] = {
                'allCodonReads': [],
                'gene': gene,
                'position': aapos,
                'totalReads': total_reads
            }
        gpmap[gpkey]['allCodonReads'].append(
            {'codon': codon, 'reads': codon_reads})
    return {
        'name': fp.name,
        'strain': virus.strain_name,
        'allReads': sorted(
            gpmap.values(),
            key=lambda pcr: (virus.gene_index(pcr['gene']), pcr['position'])
        ),
        'untranslatedRegions': untrans_regions,
        'minPrevalence': min_prevalence,
        'maxMixtureRate': max_mixture_rate,
        'minCodonReads': min_codon_reads,
        'minPositionReads': min_position_reads
    }


@cli.command()
@click.argument('seqreads', nargs=-1, type=click.File('r'), required=True)
@url_option('--url')
@virus_option('--virus')
@click.option('-p', '--pcnt-cutoff',
              type=float, default=0.1, show_default=True,
              help=('Minimal prevalence cutoff for this sequence reads '
                    '(range: 0-1.0)'))
@click.option('-m', '--mixture-cutoff',
              type=float, default=0.0005, show_default=True,
              help=('Maximum mixture rate for this sequence reads '
                    '(range: 0-1.0)'))
@click.option('-d', '--min-codon-reads', type=int, default=10,
              show_default=True,
              help=('Minimal read depth applied to '
                    'each codon of this sequence'))
@click.option('-D', '--min-position-reads', type=int, default=1,
              show_default=True,
              help=('Minimal read depth applied to '
                    'each position of this sequence'))
@click.option('-q', '--query', type=click.File('r'), show_default=True,
              help=('A file contains GraphQL fragment definition '
                    'on `SequenceAnalysis`'))
@click.option('-o', '--output', default='-', type=click.File('w'),
              show_default=True, help='File path to store the JSON result')
@click.option('--ugly', is_flag=True, help='Output compressed JSON result')
@click.pass_context
def seqreads(
    ctx: click.Context,
    url: str,
    virus: viruses.Virus,
    seqreads: List[TextIO],
    pcnt_cutoff: float,
    mixture_cutoff: float,
    min_codon_reads: int,
    min_position_reads: int,
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
        fp,
        virus,
        pcnt_cutoff,
        mixture_cutoff,
        min_codon_reads,
        min_position_reads
    ) for fp in seqreads]
    if query:
        query_text = query.read()
    else:
        query_text = virus.get_default_query('seqreads')
    result = client.sequence_reads_analysis(seqreads_payload, query_text, 2)
    json.dump(result, output, indent=None if ugly else 2)
