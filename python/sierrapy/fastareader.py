# -*- coding: utf-8 -*-


def load(fp):
    sequences = []
    header = None
    curseq = ''
    for line in fp:
        if line.startswith('>'):
            if header and curseq:
                sequences.append({
                    'header': header,
                    'sequence': curseq
                })
            header = line[1:].strip()
            curseq = ''
        if line.startswith('#'):
            continue
        else:
            curseq += line.strip()
    if header and curseq:
        sequences.append({
            'header': header,
            'sequence': curseq
        })
    return sequences
