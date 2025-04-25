"""
RepoDex: A tool for fetching, indexing, and organizing GitHub repository metadata.
"""

from importlib import metadata

# Get version from package metadata or fallback to "unknown"
try:
    __version__ = metadata.version("repodex")
except metadata.PackageNotFoundError:
    # This happens if package is not installed (e.g., in development)
    __version__ = "unknown"
