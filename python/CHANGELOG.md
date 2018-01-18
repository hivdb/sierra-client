## 0.2.2dev
TODO

## 0.2.1 (2018-01-18)
Features:
  - add support for Python 3.6

Bugfix:
  - fix broken subcommand `patterns`

## 0.2.0 (2017-11-14)
Features:
  - expose HIValg parameters in `pattern_analysis` method
  - refactor command line tool mainly by replacing `argparse` with `click`
  - new subcommand `recipe` to support customized post-process
  - new recipe `alignment` to output aligned sequences (FASTA)

Bugfix:
  - fix a bug that sequence header was accidently prepended to the sequence

## 0.1.2 (2016-12-19)

Features:
  - new subcommand `patterns` to analyze multiple lists of mutations
  - new methods `iter_pattern_analysis` and `pattern_analysis` to support
    multiple lists of mutations
  - new method `iter_sequence_analysis` available in `SierraClient`
  - by default return version object in DrugResistance object
  - adjust dependencies
  - new method `toggle_progress` in `SierraClient` to allow progress meter
    being switch on and off

## 0.1.1 (2016-09-22)

Features:
  - add support to fetch lastest HIVdb version
  - allow to query versions with `sierrapy --version`

## 0.1.0 (2016-09-21)

Features:
  - create SierraPy project
  - support to analyze HIV pol sequences in FASTA files
  - support to analyze HIV pol mutations
  - support to fetch introspection
  - a command line entry point
