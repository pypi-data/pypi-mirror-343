"""
Utility functions for RepoDex tools.
"""

import argparse
import sys
from . import __version__

def add_common_arguments(parser):
    """Add common arguments to an ArgumentParser."""
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version information and exit"
    )
    parser.add_argument(
        "--help",
        action="store_true",
        help="Show this help message and exit"
    )
    return parser

def handle_common_arguments(args, tool_name, description):
    """Handle common arguments like --version and --help."""
    if hasattr(args, "version") and args.version:
        print(f"{tool_name} v{__version__}")
        sys.exit(0)

    if hasattr(args, "help") and args.help:
        print(f"{tool_name} - {description}")
        print(f"\nUsage: {tool_name} [options]")
        print("\nOptions:")
        print("  --version     Show version information and exit")
        print("  --help        Show this help message and exit")
        # Add tool-specific help here if needed
        sys.exit(0)
