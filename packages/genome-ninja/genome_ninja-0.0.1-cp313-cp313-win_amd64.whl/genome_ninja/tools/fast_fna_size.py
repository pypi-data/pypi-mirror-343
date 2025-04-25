# -----------------------------------------------------------------------------
# src/genome_ninja/tools/fast_fna_size.py
# first built‑in ninja trick – estimate uncompressed bytes of *.fna.gz
# -----------------------------------------------------------------------------

"""fast_fna_size – recursively sum the uncompressed size of *.fna.gz files.

Usage:
    genome-ninja fna-size <directory> [--threads 8]
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import typer

from genome_ninja.core.io import smart_open
from genome_ninja.core.utils import parallel_map

try:
    # optional C++ accelerator (will be None if wheel built w/o C++ toolchain)
    from genome_ninja._fast_reader import (
        uncompressed_bytes as _fast_count,  # type: ignore
    )
except ImportError:
    _fast_count = None  # fallback to pure python


# ---------------------------- pure‑python fallback ---------------------------


def _py_count(files: Iterable[Path]) -> int:
    def one(p: Path) -> int:
        with smart_open(p, "rb") as fh:
            return sum(len(chunk) for chunk in iter(lambda: fh.read(1 << 20), b""))

    return sum(parallel_map(one, files))


def count_bytes(files: Iterable[Path], threads: int = 8) -> int:
    if _fast_count is not None:
        return _fast_count(list(files), threads)
    return _py_count(files)


# --------------------------- CLI glue ---------------------------------------


def register(cli: typer.Typer) -> None:
    @cli.command(
        "fna-size", help="Recursively sum uncompressed bytes of *.fna.gz files."
    )
    def fna_size(
        path: Path = typer.Argument(exists=True, dir_okay=True, help="Root directory"),
        threads: int = typer.Option(
            8, "--threads", "-t", show_default=True, help="Thread count"
        ),
    ) -> None:
        total = count_bytes(path.rglob("*.fna.gz"), threads)
        typer.echo(f"Total uncompressed bytes: {total:,}")
