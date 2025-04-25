# -----------------------------------------------------------------------------
# src/genome_ninja/core/io.py
# generic I/O helpers – gzip aware, streaming friendly
# -----------------------------------------------------------------------------

from __future__ import annotations

import gzip
from pathlib import Path
from typing import Iterator, Tuple, Union

PathLike = Union[str, Path]


def smart_open(path: PathLike, mode: str = "rt", **kw):
    """Open local file transparently handling .gz compression."""
    path = Path(path)
    if path.suffix == ".gz":
        return gzip.open(path, mode, **kw)
    return open(path, mode, **kw)


# extremely light‑weight FASTA iterator; good enough for small helper tasks


def iter_fasta(path: PathLike) -> Iterator[Tuple[str, str]]:
    header: str | None = None
    seq_parts: list[str] = []
    with smart_open(path, "rt") as fh:
        for line in fh:
            if line.startswith(">"):
                if header is not None:
                    yield header, "".join(seq_parts)
                header = line[1:].strip()
                seq_parts.clear()
            else:
                seq_parts.append(line.rstrip())
    if header is not None:
        yield header, "".join(seq_parts)
