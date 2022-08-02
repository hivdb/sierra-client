SierraPy
========
[![install with pypi](https://img.shields.io/pypi/v/sierrapy.svg)](https://pypi.python.org/pypi/sierrapy)
[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat-square)](https://bioconda.github.io/recipes/sierrapy/README.html)
[![donation](https://img.shields.io/badge/Donate-Stanford_Giving-green.svg)][donation]

SierraPy package contains a client and a command line program for
[HIVDB][hivdb] Sierra GraphQL Webservice.


Installation
------------

With the Python package installation tool [pip][pip] one can easily install
this package using the command below:

```shell
pip install sierrapy
```

To install the latest version (unstable) from Github:

```shell
pip install -e "git+https://github.com/hivdb/sierra-client.git#egg=sierrapy&subdirectory=python"
```


Usage
-----

Once installed, a command `sierrapy` is available from the command line. The
command currently support three main methods to fetch JSON-format
drug-resistance report from backend service.

### Select a virus

By default, SierraPy send queries to our HIV-1 analysis server. This behavior
can be changed by specify `--virus` after the sierrapy command:

```shell
# For HIV-2 analysis
sierrapy --virus HIV2 ...

For SARS-CoV-2 analysis
sierrapy --virus SARS2 ...
```

### Specify GraphQL entry-point

By default, SierraPy send queries to Sierra production servers maintained by
HIVDB team. If users wish to host their own [Sierra
server](https://github.com/hivdb/sierra), they must specify the entry-point of
Sierra GraphQL. For example:

```shell
sierrapy --url http://localhost:8080/WebApplications/rest/graphql ...
```

### Input Sequences (FASTA File)

This method is corresponding to the [HIVDB "Input sequences"][hivdb-seqinput]
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
[graphql.org/learn][graphql-learn]. For API reference and a playground of HIVDB
GraphQL service, please visit [hivdb.stanford.edu/page/graphiql][graphiql].

### Input Sequence Reads (CodFreq File)

This method is corresponding to the [HIVDB "Input sequence
reads"][hivdb-seqreadsinput] tab. It can accept a list of CodFreq files or
directories that containing CodFreq files. JSON format reports will be
generated for each CodFreq files when the analysis completed.

```shell
sierrapy seqreads path/to/codfreq/dir/ additional.codfreq.gz
```

The reports will be placed in the same directory of the input CodFreq file and
named with suffix ".report.json".

Users can customize the GraphQL by defining the query. A parameter `-q` or
`--query` can be specified for defining the query fragment on
`SequenceReadsAnalysis` object. An example and the default query is located [in
the "fragments" folder][seqreads-query].


### Input Mutations

This method is corresponding to the [HIVDB "Input mutations"][hivdb-mutinput]
tab. It accepts PR, RT, and/or IN mutations based on
[HIV-1 subtype B consensus][consensus]. The format of the mutations is not
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

### Input Patterns
A pattern is a set (list) of mutations. With this method, you can analyze
mutations derived from different samples at the same time. The method accepts
one or more files contained mutations. Each row in the files represents a
pattern. Here's an example of a file contained 2 patterns:

```
> patient 1
RT:M41L + RT:M184V + RT:L210W + RT:T215Y
> patient 2
PR:L24I + PR:M46L + PR:I54V + PR:V82A
```

These delimiters are supported: commas (`,`), plus signs(`+`), semicolon(`;`),
whitespaces and tabs. The output result of this method is a list of
`MutationsAnalysis` object, in the same order as the input.

Here's a command example. It output the JSON result to the current console:

```shell
sierrapy patterns /path/to/pattern/file.txt
```

This one output the JSON result to a file:

```shell
sierrapy patterns /path/to/pattern/file.txt -o output.json
```

Custom query fragment on object `MutationsAnalysis` can be also specified by
parameter `-q` or `--query`. As we described in the above section.

Donation
--------

If you find SierraPy useful and wish to donate to the HIVDB team, you can do
so through [Stanford Make a Gift][donation] form. Your contribution will be
greatly appreciated.


[hivdb]: https://hivdb.stanford.edu/
[pip]: https://github.com/pypa/get-pip
[hivdb-seqinput]: https://hivdb.stanford.edu/hivdb/by-sequences/
[hivdb-seqreadsinput]: https://hivdb.stanford.edu/hivdb/by-reads/
[hivdb-mutinput]: https://hivdb.stanford.edu/hivdb/by-mutations/
[seq-query]: https://raw.githubusercontent.com/hivdb/sierra-client/master/python/sierrapy/fragments/hiv1_sequence_analysis_default.gql
[seqreads-query]: https://raw.githubusercontent.com/hivdb/sierra-client/master/python/sierrapy/fragments/hiv1_sequence_reads_analysis_default.gql
[graphql-learn]: http://graphql.org/learn/
[graphiql]: https://hivdb.stanford.edu/page/graphiql/
[consensus]: https://hivdb.stanford.edu/page/release-notes/#appendix.1.consensus.b.sequences
[donation]: https://makeagift.stanford.edu/goto/shafergift
