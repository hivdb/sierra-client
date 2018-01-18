# -*- coding: utf-8 -*-

from collections import OrderedDict

import requests
from tqdm import tqdm
from gql import gql, Client
from gql.transport.http import HTTPTransport
from graphql.execution import ExecutionResult
from graphql.language.printer import print_ast
from requests.exceptions import HTTPError

VERSION = '0.2.2dev'
DEFAULT_URL = 'https://hivdb.stanford.edu/graphql'


class ResponseError(Exception):
    pass


class RequestsHTTPTransportWOrderedDict(HTTPTransport):
    def __init__(self, url, timeout=None, **kwargs):
        super(RequestsHTTPTransportWOrderedDict, self).__init__(url, **kwargs)
        self.default_timeout = timeout

    def execute(self, document, variable_values=None, timeout=None):
        query_str = print_ast(document)
        payload = {
            'query': query_str,
            'variables': variable_values or {}
        }
        request = requests.post(
            self.url,
            json=payload,
            headers=self.headers,
            timeout=timeout or self.default_timeout)
        request.raise_for_status()
        result = request.json(object_pairs_hook=OrderedDict)
        assert 'errors' in result or 'data' in result, \
            'Received non-compatible response "{}"'.format(result)
        return ExecutionResult(
            errors=result.get('errors'),
            data=result.get('data')
        )


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
                RequestsHTTPTransportWOrderedDict(self.url, timeout=300)
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

    def _pattern_analysis(self, patterns, query, **kw):
        enable_hivalg = 'algorithms' in kw or 'customAlgorithms' in kw
        extraparams = ''
        if enable_hivalg:
            extraparams = (', $algorithms:[ASIAlgorithm], '
                           '$customAlgorithms: [CustomASIAlgorithm]')
        variables = {"patterns": patterns}
        if enable_hivalg:
            variables['algorithms'] = kw.get('algorithms')
            variables['customAlgorithms'] = kw.get('custom_algorithms')
        result = self.execute(
            gql("""
                query sierrapy($patterns:[[String]!]!{extraparams}) {{
                    viewer {{
                        patternAnalysis(patterns:$patterns) {{
                            ...F0
                        }}
                    }}
                }}
                fragment F0 on MutationsAnalysis {{
                    {query}
                }}
                """.format(query=query, extraparams=extraparams)),
            variable_values=variables)
        return result['viewer']['patternAnalysis']

    def iter_sequence_analysis(self, sequences, query, step=20):
        if self._progress:
            pbar = tqdm(total=len(sequences))
        while sequences:
            for result in self._sequence_analysis(sequences[:step], query):
                yield result
            sequences = sequences[step:]
            self._progress and pbar.update(step)

    def iter_pattern_analysis(self, patterns, query, step=20, **kw):
        if self._progress:
            pbar = tqdm(total=len(patterns))
        while patterns:
            for result in self._pattern_analysis(patterns[:step], query, **kw):
                yield result
            patterns = patterns[step:]
            self._progress and pbar.update(step)

    def sequence_analysis(self, sequences, query, step=20):
        return list(self.iter_sequence_analysis(sequences, query, step))

    def pattern_analysis(self, patterns, query, step=20, **kw):
        return list(self.iter_pattern_analysis(patterns, query, step, **kw))

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
