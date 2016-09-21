# -*- coding: utf-8 -*-

from tqdm import tqdm
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from requests.exceptions import HTTPError

VERSION = '0.1'
DEFAULT_URL = 'http://localhost:8080/graphql'


class ResponseError(Exception):
    pass


class SierraClient(object):

    def __init__(self, url=DEFAULT_URL):
        transport = RequestsHTTPTransport(url, use_json=True, timeout=300)
        transport.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'sierra-client (python)/{}'.format(VERSION)
        }
        self._client = Client(
            transport=transport,
            fetch_schema_from_transport=True)

    def execute(self, document, variable_values):
        try:
            return self._client.execute(
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
        return self._client.introspection

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

    def sequence_analysis(self, sequences, query, step=20):
        result = []
        pbar = tqdm(total=len(sequences))
        while sequences:
            result.extend(self._sequence_analysis(sequences[:step], query))
            sequences = sequences[step:]
            pbar.update(step)
        return result

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
