# -*- coding: utf-8 -*-

QUERY_SEQUENCE_ANALYSIS = """
    inputSequence { header },
    subtypeText,
    validationResults {
        level,
        message
    },
    alignedGeneSequences {
        firstAA, lastAA,
        gene { name },
        mutations {
            consensus,
            position,
            AAs,
            isInsertion,
            isDeletion,
            isApobecDRM
        },
        SDRMs:mutations(filterOptions:[SDRM]) {
            text
        },
        prettyPairwise {
            positionLine,
            refAALine,
            alignedNAsLine,
            mutationLine
        }
    },
    drugResistance {
        gene { name },
        drugScores {
            drugClass { name },
            drug {
                name,
                displayAbbr,
            },
            score,
            partialScores {
                mutations {
                    text,
                    primaryType,
                    comments { type, text }
                },
                score
            },
            text
        }
    }
"""
QUERY_MUTATIONS_ANALYSIS = """
    validationResults {
        level,
        message
    },
    drugResistance {
        gene { name },
        drugScores {
            drugClass { name },
            drug {
                name,
                displayAbbr,
            },
            score,
            partialScores {
                mutations {
                    consensus,
                    position,
                    AAs,
                    text,
                    primaryType,
                    comments { type, text }
                },
                score
            },
            text
        }
    }
"""
