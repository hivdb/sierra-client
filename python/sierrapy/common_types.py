from typing import TypedDict, List


class CodonReads(TypedDict):
    codon: str
    reads: int


class PosReads(TypedDict):
    gene: str
    position: int
    totalReads: int
    allCodonReads: List[CodonReads]


class SeqReads(TypedDict):
    name: str
    strain: str
    allReads: List[PosReads]
    minPrevalence: float
    minCodonCount: int
    minReadDepth: int


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
