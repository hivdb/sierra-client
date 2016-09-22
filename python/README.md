SierraPy
========

SierraPy package contains a client and a command line program for
[HIVdb][hivdb] Sierra GraphQL Webservice.


Installation
------------

With the Python package installation tool [pip][pip] one can easily install
this package using the command below:

```shell
pip install sierrapy
```

To install the latest version (unstable) from Github:

```shell
pip install -e "git+https://github.com/hivdb/sierra-client.git#egg=master&subdirectory=python"
```


Usage
-----

Once installed, a command `sierrapy` is available in the command line. The
command currently support two main methods to fetch JSON-format drug-resistance
report from backend service.

### Input Sequences (FASTA File)

This method is corresponding to the [HIVdb "Input Sequences"][hivdb-seqinput]
tab. It can accept any large number of files and sequences as long as you
don't blow up your computer. The input FASTA files should contain at least one
HIV/SIV pol DNA sequence.

You can specify one or more FASTA-format files to method `sierrapy fasta`.
Use the following command to output the result to your console:

```shell
sierrapy fasta fasta1.fasta fasta2.fasta
```

You may redirect the output to a file using `-o` or `--output` parameter:

```shell
sierrapy fasta fasta1.fasta fasta2.fasta -o output.json
```

GraphQL allows users to customize the structure of output result by defining
the query. The `sierrapy fasta` method accepts an optional parameter `-q` or
`--query` which enabling users to define a custom query fragment on object
`SequenceAnalysis`. An example and the default query is located
[in the "fragments" folder][seq-query]. Once you have your custom query,
assume it saved at `path/to/your/query/file.gql`, use this command to get
the customized result:

```shell
sierrapy fasta fasta1.fasta fasta2.fasta -q path/to/your/query/file.gql
```

For further infomations on how to write queries in GraphQL, please visit
[graphql.org/learn][graphql-learn].

### Input Mutations

This method is corresponding to the [HIVdb "Input Mutations"][hivdb-mutinput]
tab. It accepts PR, RT, and/or IN mutations based on
[HIV-1 type B consensus][consensus]. The format of the mutations is not
strictly required. Here's a list of examples for valid mutations:

- `PR:E35E_D`, `PRE35_`, `PR:35Insertion`, and `PR35ins` are all valid
  insertions at PR codon 35 position.
- `RT:T67-`, `RT67Deletion`, `RT67d`, and `RT69del` are all valid deletions
  at RT codon 67 position.
- `IN:M50MI`, a mutation at IN codon 50 position and contains mixture.
- `IN:M50*`, a mutation at IN codon 50 position and is a stop codon.

You can specify one or more mutations to method `sierrapy mutations`.
Use the following command to output the result to your console:

```shell
sierrapy mutations PR:E35E_D RT:T67- IN:M50MI
```

You may redirect the output to a file using `-o` or `--output` parameter:

```shell
sierrapy mutations PR:E35E_D RT:T67- IN:M50MI -o output.json
```

You can also specify a custom query fragment on object `MutationsAnalysis`.
Use the similar command like previous section to retrieve custom result.


[hivdb]: https://hivdb.stanford.edu/
[pip]: https://github.com/pypa/get-pip
[hivdb-seqinput]: https://hivdb.stanford.edu/hivdb/by-sequences/
[seq-query]: https://raw.githubusercontent.com/hivdb/sierra-client/master/python/sierrapy/fragments/sequence_analysis_default.gql
[graphql-learn]: http://graphql.org/learn/
[consensus]: https://hivdb.stanford.edu/page/release-notes/#appendix.1.consensus.b.sequences
