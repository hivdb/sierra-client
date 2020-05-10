# -*- coding: utf-8 -*-

import json

from tqdm import tqdm
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from requests.exceptions import HTTPError

VERSION = '0.3.0'
DEFAULT_URL = 'https://hivdb.stanford.edu/graphql'


class ResponseError(Exception):
    pass


class SierraClient(object):

    def __init__(self, url=DEFAULT_URL):
        self.url = url
        self._client = None
        self._progress = False

    def toggle_progress(self, flag='auto'):
        if flag == 'auto':
            self._progress = not self._progress
        else:
            self._progress = bool(flag)

    @property
    def client(self):
        if self._client is None:
            transport = \
                RequestsHTTPTransport(self.url, use_json=True, timeout=300)
            transport.headers = {
                'User-Agent': 'sierra-client (python)/{}'.format(VERSION)
            }
            self._client = Client(
                transport=transport,
                fetch_schema_from_transport=True)
        return self._client

    def execute(self, document, variable_values=None):
        try:
            return self.client.execute(
                document, variable_values=variable_values)
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

    def get_introspection(self):
        return self.client.introspection

    def _sequence_analysis(self, sequences, query):
        result = self.execute(
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
        return result['sequenceAnalysis']

    def _pattern_analysis(self, patterns, pattern_names, query, **kw):
        enable_hivalg = 'algorithms' in kw or 'customAlgorithms' in kw
        extraparams = ''
        if enable_hivalg:
            extraparams = ('$algorithms:[ASIAlgorithm] '
                           '$customAlgorithms:[CustomASIAlgorithm]')
        variables = {"patterns": patterns, "patternNames": pattern_names}
        if enable_hivalg:
            variables['algorithms'] = kw.get('algorithms')
            variables['customAlgorithms'] = kw.get('custom_algorithms')
        result = self.execute(
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
        return result['patternAnalysis']

    def _sequence_reads_analysis(self, all_sequence_reads, query):
        result = self.execute(
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
        return result['sequenceReadsAnalysis']

    def iter_sequence_analysis(self, sequences, query, step=20):
        if self._progress:
            pbar = tqdm(total=len(sequences))
        while sequences:
            for result in self._sequence_analysis(sequences[:step], query):
                yield result
            sequences = sequences[step:]
            self._progress and pbar.update(step)

    def iter_pattern_analysis(self, patterns, pattern_names,
                              query, step=20, **kw):
        assert len(patterns) == len(pattern_names)
        if self._progress:
            pbar = tqdm(total=len(patterns))
        while patterns:
            for result in self._pattern_analysis(
                patterns[:step], pattern_names[:step], query, **kw
            ):
                yield result
            patterns = patterns[step:]
            pattern_names = pattern_names[step:]
            self._progress and pbar.update(step)

    def iter_sequence_reads_analysis(self, sequence_reads, query, step=20):
        if self._progress:
            pbar = tqdm(total=len(sequence_reads))
        while sequence_reads:
            for result in self._sequence_reads_analysis(
                    sequence_reads[:step], query):
                yield result
            sequence_reads = sequence_reads[step:]
            self._progress and pbar.update(step)

    def sequence_analysis(self, sequences, query, step=20):
        return list(self.iter_sequence_analysis(sequences, query, step))

    def pattern_analysis(self, patterns, query, step=20, **kw):
        return list(self.iter_pattern_analysis(patterns, query, step, **kw))

    def sequence_reads_analysis(self, sequence_reads, query, step=20):
        return list(
            self.iter_sequence_reads_analysis(sequence_reads, query, step))

    def mutations_analysis(self, mutations, query):
        result = self.execute(
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
        return result['mutationsAnalysis']

    def current_version(self):
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
