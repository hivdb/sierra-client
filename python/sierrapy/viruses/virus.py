from typing import List, Set, Dict, Tuple, Optional
from ..common_types import GeneDef, TargetGeneDef


class Virus:
    virus_name: str
    strain_name: str
    supported_commands: List[str]
    default_url: str
    gene_defs: Dict[str, GeneDef]
    source_genes: Set[str]
    ordered_genes: List[str]
    default_queries: Dict[str, str]

    def __init__(
        self,
        virus_name: str,
        strain_name: str,
        supported_commands: List[str],
        default_url: str,
        gene_defs: List[GeneDef],
        default_queries: Dict[str, str]
    ):
        self.virus_name = virus_name
        self.strain_name = strain_name
        self.supported_commands = supported_commands
        self.default_url = default_url
        self.gene_defs = {gdef['name']: gdef for gdef in gene_defs}
        self.source_genes = {
            gdef['name'] for gdef in gene_defs
            if 'target_genes' in gdef
        }
        self.ordered_genes = [gdef['name'] for gdef in gene_defs]
        self.default_queries = default_queries

    def get_default_query(self, command: str) -> str:
        return self.default_queries[command]

    def gene_index(self, gene: str) -> int:
        return self.ordered_genes.index(gene)

    def synonym_to_gene_name(self, gene: str) -> Optional[str]:
        if gene in self.gene_defs:
            return gene

        gene_def: GeneDef
        for gene_def in self.gene_defs.values():
            if gene_def['synonym_pattern'].match(gene):
                return gene_def['name']
        else:
            return None

    def source_gene_to_target_gene_position(
        self, gene: str, pos: int
    ) -> Tuple[Optional[str], Optional[int]]:
        target_gene: TargetGeneDef
        pos_start: int
        pos_end: int
        pos_offset: int
        if gene in self.source_genes:
            for target_gene in self.gene_defs[gene]['target_genes']:
                pos_start, pos_end = target_gene['range']
                pos_offset = target_gene['offset']
                if pos < pos_start:
                    continue
                elif pos > pos_end:
                    continue
                return target_gene['name'], pos + 1 - pos_start + pos_offset
            else:
                return None, None
        else:
            return gene, pos
