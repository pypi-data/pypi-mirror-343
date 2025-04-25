# -----------------------------------------------------------------------------
# src/genome_ninja/core/utils.py
# misc helpers (thread‑pool map, progress wrapper etc.)
# -----------------------------------------------------------------------------

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Iterable, List, TypeVar

T = TypeVar("T")
R = TypeVar("R")


def parallel_map(
    func: Callable[[T], R], items: Iterable[T], threads: int = 4
) -> List[R]:
    with ThreadPoolExecutor(max_workers=threads) as pool:
        return list(pool.map(func, items))
