# src/genome_ninja/__init__.py
"""GenomeNinja: package initialisation and version getter."""
from importlib.metadata import version

__version__: str = version("genome-ninja")

__all__ = ["__version__"]
