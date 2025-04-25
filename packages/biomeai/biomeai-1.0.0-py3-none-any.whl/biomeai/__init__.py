"""
BiomeAI - Easy NVIDIA AI Integration Package
==========================================

This package provides simplified interfaces for NVIDIA AI capabilities,
including ColabFold MSA search functionality.
"""

__version__ = "0.1.0"

from .core import BiomeAI
from .colabfold import ColabFoldMSA

__all__ = ["BiomeAI", "ColabFoldMSA"]
