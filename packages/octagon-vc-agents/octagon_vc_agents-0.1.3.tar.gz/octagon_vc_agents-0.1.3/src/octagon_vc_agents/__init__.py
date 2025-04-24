"""
Octagon VC Agents - AI-driven venture capitalist agents powered by Octagon Private Markets
"""

__version__ = "0.1.0"

from .cli import main
from .server import run_server

__all__ = ["main", "run_server"]
