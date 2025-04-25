"""
Command-line interface for RepoDex.
"""

import argparse
import sys
import importlib
from . import __version__

def main():
    """Main entry point for the repodex command."""
    parser = argparse.ArgumentParser(
        description="RepoDex: GitHub Repository Catalog tools",
        prog="repodex"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"RepoDex v{__version__}"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        help="Command to run"
    )

    # Add subcommands
    add_fetch_shane_parser(subparsers)
    add_fetch_cello_parser(subparsers)
    add_release_initial_shane_parser(subparsers)
    add_release_initial_cello_parser(subparsers)
    add_release_latest_shane_parser(subparsers)
    add_release_latest_cello_parser(subparsers)
    add_update_readmes_parser(subparsers)
    add_setup_secret_parser(subparsers)

    # Parse arguments
    args = parser.parse_args()

    # If no command is specified, show help
    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Import and run the appropriate module
    try:
        if args.command == "fetch-shane":
            from tools import gh_repo_fetch_index_shane
            gh_repo_fetch_index_shane.main()
        elif args.command == "fetch-cello":
            from tools import gh_repo_fetch_index_cello
            gh_repo_fetch_index_cello.main()
        elif args.command == "release-initial-shane":
            from tools import gh_repo_release_initial_shane
            gh_repo_release_initial_shane.main()
        elif args.command == "release-initial-cello":
            from tools import gh_repo_release_initial_cello
            gh_repo_release_initial_cello.main()
        elif args.command == "release-latest-shane":
            from tools import gh_repo_release_latest_shane
            gh_repo_release_latest_shane.main()
        elif args.command == "release-latest-cello":
            from tools import gh_repo_release_latest_cello
            gh_repo_release_latest_cello.main()
        elif args.command == "update-readmes":
            from tools import gh_repo_update_readmes
            gh_repo_update_readmes.main()
        elif args.command == "setup-secret":
            from tools import gh_repo_setup_secret
            gh_repo_setup_secret.main()
    except ImportError as e:
        print(f"Error: Could not import module: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def add_fetch_shane_parser(subparsers):
    """Add parser for fetch-shane command."""
    parser = subparsers.add_parser(
        "fetch-shane",
        help="Fetch READMEs from personal GitHub repositories"
    )

def add_fetch_cello_parser(subparsers):
    """Add parser for fetch-cello command."""
    parser = subparsers.add_parser(
        "fetch-cello",
        help="Fetch READMEs from Cello organization repositories"
    )

def add_release_initial_shane_parser(subparsers):
    """Add parser for release-initial-shane command."""
    parser = subparsers.add_parser(
        "release-initial-shane",
        help="Create initial v0.1.0 release for untagged personal repositories"
    )

def add_release_initial_cello_parser(subparsers):
    """Add parser for release-initial-cello command."""
    parser = subparsers.add_parser(
        "release-initial-cello",
        help="Create initial v0.1.0 release for untagged Cello repositories"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without making changes"
    )

def add_release_latest_shane_parser(subparsers):
    """Add parser for release-latest-shane command."""
    parser = subparsers.add_parser(
        "release-latest-shane",
        help="Create releases for latest tags on personal repositories"
    )

def add_release_latest_cello_parser(subparsers):
    """Add parser for release-latest-cello command."""
    parser = subparsers.add_parser(
        "release-latest-cello",
        help="Create releases for latest tags on Cello repositories"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without making changes"
    )

def add_update_readmes_parser(subparsers):
    """Add parser for update-readmes command."""
    parser = subparsers.add_parser(
        "update-readmes",
        help="Update README files across multiple repositories"
    )
    parser.add_argument(
        "-c", "--csv",
        help="Path to CSV file with repository names"
    )
    parser.add_argument(
        "-d", "--dir",
        help="Path to directory with local README files"
    )

def add_setup_secret_parser(subparsers):
    """Add parser for setup-secret command."""
    parser = subparsers.add_parser(
        "setup-secret",
        help="Setup GitHub PAT as a repository secret"
    )

if __name__ == "__main__":
    main()
