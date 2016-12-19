# -*- coding: utf-8 -*-

from tqdm import tqdm
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from requests.exceptions import HTTPError

VERSION = '0.1.2'
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
            transport = RequestsHTTPTransport(
                self.url, use_json=True, timeout=300)
            transport.headers = {
                'Content-Type': 'application/json',
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
            errors = [
                e['exception']['detailMessage']
                if 'detailMessage' in e['exception']
                else 'Unknown server error'
                for e in e.response.json()['errors']
                if 'exception' in e]
            raise ResponseError(
                'Sierra GraphQL webservice returned errors:\n - ' +
                '\n - '.join(errors))

    def get_introspection(self):
        return self.client.introspection

    def _sequence_analysis(self, sequences, query):
        result = self.execute(
            gql("""
                query sierrapy($sequences:[UnalignedSequenceInput]!) {{
                    viewer {{
                        sequenceAnalysis(sequences:$sequences) {{
                            ...F0
                        }}
                    }}
                }}
                fragment F0 on SequenceAnalysis {{
                    {query}
                }}
                """.format(query=query)),
            variable_values={"sequences": sequences})
        return result['viewer']['sequenceAnalysis']

    def _pattern_analysis(self, patterns, query):
        result = self.execute(
            gql("""
                query sierrapy($patterns:[[String]!]!) {{
                    viewer {{
                        patternAnalysis(patterns:$patterns) {{
                            ...F0
                        }}
                    }}
                }}
                fragment F0 on MutationsAnalysis {{
                    {query}
                }}
                """.format(query=query)),
            variable_values={"patterns": patterns})
        return result['viewer']['patternAnalysis']

    def iter_sequence_analysis(self, sequences, query, step=20):
        if self._progress:
            pbar = tqdm(total=len(sequences))
        while sequences:
            for result in self._sequence_analysis(sequences[:step], query):
                yield result
            sequences = sequences[step:]
            self._progress and pbar.update(step)

    def iter_pattern_analysis(self, patterns, query, step=20):
        if self._progress:
            pbar = tqdm(total=len(patterns))
        while patterns:
            for result in self._pattern_analysis(patterns[:step], query):
                yield result
            patterns = patterns[step:]
            self._progress and pbar.update(step)

    def sequence_analysis(self, sequences, query, step=20):
        return list(self.iter_sequence_analysis(sequences, query, step))

    def pattern_analysis(self, patterns, query, step=20):
        return list(self.iter_pattern_analysis(patterns, query, step))

    def mutations_analysis(self, mutations, query):
        result = self.execute(
            gql("""
                query sierrapy($mutations:[String]!) {{
                    viewer {{
                        mutationsAnalysis(mutations:$mutations) {{
                            ...F0
                        }}
                    }}
                }}
                fragment F0 on MutationsAnalysis {{
                    {query}
                }}
                """.format(query=query)),
            variable_values={"mutations": mutations})
        return result['viewer']['mutationsAnalysis']

    def current_version(self):
        result = self.execute(
            gql("""
                query sierrapy {
                    viewer {
                        currentVersion { text, publishDate }
                    }
                }
                """))
        return result['viewer']['currentVersion']
