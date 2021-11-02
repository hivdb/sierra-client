from __future__ import annotations
import re
from typing import TypedDict, List, Tuple


class CodonReads(TypedDict):
    codon: str
    reads: int


class PosReads(TypedDict):
    gene: str
    position: int
    totalReads: int
    allCodonReads: List[CodonReads]


class UntransRegion(TypedDict):
    name: str
    refStart: int
    refEnd: int
    consensus: str


class SeqReads(TypedDict):
    name: str
    strain: str
    allReads: List[PosReads]
    untranslatedRegions: List[UntransRegion]
    minPrevalence: float
    maxMixtureRate: float
    minCodonReads: int
    minPositionReads: int


class Sequence(TypedDict):
    header: str
    sequence: str


class ServerVer(TypedDict):
    text: str
    publishDate: str


class InputSequence(TypedDict):
    header: str


class Gene(TypedDict):
    name: str


class Mutation(TypedDict):
    consensus: str
    position: int
    AAs: str


class PrettyPairwise(TypedDict):
    positionLine: List[str]
    alignedNAsLine: List[str]


class AlignedGeneSeq(TypedDict):
    gene: Gene
    firstAA: int
    lastAA: int
    prettyPairwise: PrettyPairwise
    alignedNAs: str
    mutations: List[Mutation]


class SequenceResult(TypedDict):
    inputSequence: InputSequence
    alignedGeneSequences: List[AlignedGeneSeq]


class TargetGeneDef(TypedDict):
    name: str
    offset: int
    range: Tuple[int, int]


class _GeneDefRequired(TypedDict):
    # TODO: this hack will be eventually replaced by PEP 655
    name: str
    synonym_pattern: re.Pattern


class GeneDef(_GeneDefRequired, total=False):
    target_genes: List[TargetGeneDef]
