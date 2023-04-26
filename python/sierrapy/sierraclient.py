# -*- coding: utf-8 -*-

import json
from typing import (
    Optional,
    Dict,
    Any,
    Union,
    List,
    Sequence as ListOrTuple,
    Generator,
    Tuple,
    Iterator
)
from more_itertools import chunked

from tqdm import tqdm  # type: ignore
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from requests.exceptions import HTTPError  # type: ignore
from graphql.language.ast import DocumentNode as gqlDocument

from .common_types import Sequence, SeqReads, ServerVer


VERSION = '0.4.3'
DEFAULT_URL = 'https://hivdb.stanford.edu/graphql'


class ResponseError(Exception):
    pass


class SierraClient:
    url: str
    _client: Optional[Client]
    _progress: bool

    def __init__(self, url: str = DEFAULT_URL):
        self.url = url
        self._client = None
        self._progress = False

    def toggle_progress(self, flag: Union[bool, str] = 'auto') -> None:
        if flag == 'auto':
            self._progress = not self._progress
        else:
            self._progress = bool(flag)

    @property
    def client(self) -> Client:
        if self._client is None:
            transport: RequestsHTTPTransport = \
                RequestsHTTPTransport(self.url, use_json=True, timeout=300)
            transport.headers = {
                'User-Agent': 'sierra-client (python)/{}'.format(VERSION)
            }
            self._client = Client(
                transport=transport,
                fetch_schema_from_transport=True)
        return self._client

    def execute(
        self,
        document: gqlDocument,
        variable_values: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        try:
            result: Dict[str, Any] = self.client.execute(
                document, variable_values=variable_values)
            return result
        except HTTPError as e:
            print(e.response.text)
            errors = [
                e['exception']['detailMessage']
                if 'detailMessage' in e['exception']
                else 'Unknown server error'
                for e in e.response.json()['errors']
                if 'exception' in e]
            raise ResponseError(
                'Sierra GraphQL webservice returned errors:\n - ' +
                json.dumps(errors, indent=4))

    def get_introspection(self) -> Dict[str, Any]:
        result: Dict[str, Any] = self.client.introspection
        return result

    def _sequence_analysis(
        self,
        sequences: List[Sequence],
        query: str
    ) -> List[Dict[str, Any]]:
        result: Dict[str, Any] = self.execute(
            gql("""
                query sierrapy($sequences:[UnalignedSequenceInput]!) {{
                    sequenceAnalysis(sequences:$sequences) {{
                        ...F0
                    }}
                }}
                fragment F0 on SequenceAnalysis {{
                    {query}
                }}
                """.format(query=query)),
            variable_values={"sequences": sequences})
        seqResults: List[Dict[str, Any]] = result['sequenceAnalysis']
        return seqResults

    def _pattern_analysis(
        self,
        patterns: ListOrTuple[List[str]],
        pattern_names: ListOrTuple[Optional[str]],
        query: str,
        **kw: Any
    ) -> List[Dict[str, Any]]:
        enable_hivalg: bool = 'algorithms' in kw or 'customAlgorithms' in kw
        extraparams: str = ''
        if enable_hivalg:
            extraparams = ('$algorithms:[ASIAlgorithm] '
                           '$customAlgorithms:[CustomASIAlgorithm]')
        variables: Dict[str, Any] = {
            "patterns": patterns,
            "patternNames": pattern_names
        }
        if enable_hivalg:
            variables['algorithms'] = kw.get('algorithms')
            variables['customAlgorithms'] = kw.get('custom_algorithms')
        result: Dict[str, Any] = self.execute(
            gql("""
                query sierrapy(
                    $patterns:[[String]!]!
                    $patternNames:[String]
                    {extraparams}
                ) {{
                    patternAnalysis(
                        patterns:$patterns
                        patternNames:$patternNames
                    ) {{
                        ...F0
                    }}
                }}
                fragment F0 on MutationsAnalysis {{
                    {query}
                }}
                """.format(query=query, extraparams=extraparams)),
            variable_values=variables)
        patternResults: List[Dict[str, Any]] = result['patternAnalysis']
        return patternResults

    def _sequence_reads_analysis(
        self,
        all_sequence_reads: List[SeqReads],
        query: str
    ) -> List[Dict[str, Any]]:
        result: Dict[str, Any] = self.execute(
            gql("""
                query sierrapy($allSequenceReads:[SequenceReadsInput]!) {{
                    sequenceReadsAnalysis(
                        sequenceReads:$allSequenceReads

                    ) {{
                        ...F0
                    }}
                }}
                fragment F0 on SequenceReadsAnalysis {{
                    {query}
                }}
                """.format(query=query)),
            variable_values={"allSequenceReads": all_sequence_reads})
        seqReadsResults: List[Dict[str, Any]] = result['sequenceReadsAnalysis']
        return seqReadsResults

    def iter_sequence_analysis(
        self,
        sequences: Union[List[Sequence], Iterator[Sequence]],
        query: str,
        step: int = 20
    ) -> Generator[Dict[str, Any], None, None]:
        pbar: Optional[tqdm] = None
        if self._progress:
            pbar = tqdm()
        for partial in chunked(sequences, step):
            yield from self._sequence_analysis(partial, query)
            pbar and pbar.update(len(partial))

    def iter_pattern_analysis(
        self,
        patterns: Iterator[Tuple[str, List[str]]],
        query: str,
        step: int = 20,
        **kw: Any
    ) -> Generator[Dict[str, Any], None, None]:
        pbar: Optional[tqdm] = None
        pats: Tuple[List[str], ...]
        pat_names: Tuple[str, ...]
        if self._progress:
            pbar = tqdm()
        for partial in chunked(patterns, step):
            pat_names, pats = tuple(zip(*partial))
            yield from self._pattern_analysis(
                pats, pat_names, query, **kw
            )
            pbar and pbar.update(step)

    def iter_sequence_reads_analysis(
        self,
        sequence_reads: List[SeqReads],
        query: str,
        step: int = 20
    ) -> Generator[Dict[str, Any], None, None]:
        pbar: Optional[tqdm]
        if self._progress:
            pbar = tqdm(total=len(sequence_reads))
        while sequence_reads:
            yield from self._sequence_reads_analysis(
                sequence_reads[:step], query
            )
            sequence_reads = sequence_reads[step:]
            pbar and pbar.update(step)

    def sequence_analysis(
        self,
        sequences: List[Sequence],
        query: str,
        step: int = 20
    ) -> List[Dict[str, Any]]:
        return list(self.iter_sequence_analysis(sequences, query, step))

    def pattern_analysis(
        self,
        patterns: Iterator[Tuple[str, List[str]]],
        query: str,
        step: int = 20,
        **kw: Any
    ) -> List[Dict[str, Any]]:
        return list(self.iter_pattern_analysis(
            patterns, query, step, **kw
        ))

    def sequence_reads_analysis(
        self,
        sequence_reads: List[SeqReads],
        query: str,
        step: int = 20
    ) -> List[Dict[str, Any]]:
        return list(self.iter_sequence_reads_analysis(
            sequence_reads, query, step
        ))

    def mutations_analysis(
        self,
        mutations: List[str],
        query: str
    ) -> Dict[str, Any]:
        result: Dict[str, Any] = self.execute(
            gql("""
                query sierrapy($mutations:[String]!) {{
                    mutationsAnalysis(mutations:$mutations) {{
                        ...F0
                    }}
                }}
                fragment F0 on MutationsAnalysis {{
                    {query}
                }}
                """.format(query=query)),
            variable_values={"mutations": mutations})
        mutResults: Dict[str, Any] = result['mutationsAnalysis']
        return mutResults

    def current_version(self) -> Tuple[ServerVer, ServerVer]:
        result = self.execute(
            gql("""
                query sierrapy {
                    currentVersion { text, publishDate }
                    currentProgramVersion { text, publishDate }
                }
                """))
        return (result['currentVersion'],
                result.get('currentProgramVersion', {
                    'text': 'Unknown',
                    'publishDate': 'Unknown'
                }))
