## 0.1.3 (unstable)
  - expose HIValg parameters in `pattern_analysis` method

## 0.1.2 (2016-12-19)

Features:
  - new subcommand `pattern` to analyze multiple lists of mutations
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
