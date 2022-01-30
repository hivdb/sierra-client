from typing import TextIO, Generator, Optional
from .common_types import Sequence


def load(fp: TextIO) -> Generator[Sequence, None, None]:
    header: Optional[str] = None
    curseq: bytearray = bytearray()
    for line in fp:
        if line.startswith('>'):
            if header and curseq:
                yield {
                    'header': header,
                    'sequence': curseq.upper().decode('U8')
                }
            header = line[1:].strip()
            curseq = bytearray()
        elif line.startswith('#'):
            continue
        else:
            curseq.extend(
                line.strip()
                .encode('ASCII', errors='ignore')
            )
    if header and curseq:
        yield {
            'header': header,
            'sequence': curseq.upper().decode('U8')
        }
