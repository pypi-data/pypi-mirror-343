#!/usr/bin/env python3

import subprocess
import sys
import platform
import argparse
import getpass
from typing import Union, Optional

# --- Color Codes & Indicators (from .clinerules) ---
IS_WINDOWS = platform.system() == "Windows"

if IS_WINDOWS:
    COLOR_GREEN = ""
    COLOR_RED = ""
    COLOR_YELLOW = ""
    COLOR_BLUE = ""
    COLOR_RESET = ""
    INDICATOR_SUCCESS = "[x]"
    INDICATOR_FAIL = "[ ]"
    INDICATOR_WARN = "[-]"
    INDICATOR_INFO = "[i]"
else:
    COLOR_GREEN = "\033[32m"
    COLOR_RED = "\033[31m"
    COLOR_YELLOW = "\033[33m"
    COLOR_BLUE = "\033[34m"
    COLOR_RESET = "\033[0m"
    INDICATOR_SUCCESS = f"{COLOR_GREEN}[x]{COLOR_RESET}"
    INDICATOR_FAIL = f"{COLOR_RED}[ ]{COLOR_RESET}"
    INDICATOR_WARN = f"{COLOR_YELLOW}[-]{COLOR_RESET}"
    INDICATOR_INFO = f"{COLOR_BLUE}[i]{COLOR_RESET}"

# --- Configuration ---
DEFAULT_REPO = "shaneholloman/repodex"
DEFAULT_SECRET_NAME = "GH_PAT"


# --- Helper Functions ---
def run_gh_command(
    command: list,
    check: bool = True,
    capture_output: bool = True,
    input_str: Optional[str] = None,
) -> Union[subprocess.CompletedProcess, subprocess.CalledProcessError]:
    """Helper function to run GitHub CLI commands, optionally piping input."""
    try:
        process = subprocess.run(
            command,
            text=True,
            check=check,
            capture_output=capture_output,
            encoding="utf-8",
            input=input_str,
        )
        # Avoid printing stderr noise like "Checking gh auth status"
        # Also avoid printing the success message from `gh secret set` as we print our own
        if (
            process.stderr
            and check
            and "checking gh auth status" not in process.stderr.lower()
            and "updated secret" not in process.stderr.lower()
            and "created secret" not in process.stderr.lower()
        ):
            print(f"Stderr from {' '.join(command)}:\n{process.stderr.strip()}", file=sys.stderr)
        return process
    except FileNotFoundError:
        print(
            f"{INDICATOR_FAIL} Error: '{command[0]}' command not found. Make sure GitHub CLI (gh) is installed and in your PATH.",
            file=sys.stderr,
        )
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"{INDICATOR_FAIL} Error running command: {' '.join(command)}", file=sys.stderr)
        print(f"Return Code: {e.returncode}", file=sys.stderr)
        if e.stdout:
            print(f"Stdout: {e.stdout.strip()}", file=sys.stderr)
        if e.stderr:
            print(f"Stderr: {e.stderr.strip()}", file=sys.stderr)
        if not check:
            return e
        raise
    except Exception as e:
        print(f"{INDICATOR_FAIL} An unexpected error occurred running {' '.join(command)}: {e}", file=sys.stderr)
        sys.exit(1)


# --- Main Function ---
def main():
    """Main script logic."""
    parser = argparse.ArgumentParser(description="Add a GitHub Personal Access Token (PAT) as a repository secret.")
    parser.add_argument(
        "-t",
        "--token",
        help="GitHub Personal Access Token (if not provided, will be prompted securely).",
        default=None,
    )
    parser.add_argument(
        "-R",
        "--repo",
        default=DEFAULT_REPO,
        help=f"Target repository (owner/repo) (default: {DEFAULT_REPO})",
    )
    parser.add_argument(
        "-s",
        "--secret-name",
        default=DEFAULT_SECRET_NAME,
        help=f"Name for the repository secret (default: {DEFAULT_SECRET_NAME})",
    )
    args = parser.parse_args()

    # --- Check Prerequisites ---
    print(f"{INDICATOR_INFO} Checking GitHub CLI authentication...")
    auth_check = run_gh_command(["gh", "auth", "status"], check=False)
    if isinstance(auth_check, subprocess.CalledProcessError) or auth_check.returncode != 0:
        print(f"{INDICATOR_FAIL} GitHub CLI not authenticated. Please run 'gh auth login'.")
        sys.exit(1)
    print(f"{INDICATOR_SUCCESS} GitHub CLI authenticated.")

    # --- Get Token ---
    token = args.token
    if not token:
        try:
            token = getpass.getpass("Enter your GitHub Personal Access Token: ")
        except EOFError:
            print(f"\n{INDICATOR_FAIL} Error: Could not read token from input.", file=sys.stderr)
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.", file=sys.stderr)
            sys.exit(1)

    if not token:
        print(f"{INDICATOR_FAIL} Error: Token is required.", file=sys.stderr)
        sys.exit(1)

    # --- Add Secret ---
    print(f"{INDICATOR_INFO} Adding secret {args.secret_name} to repository {args.repo}...")
    command = ["gh", "secret", "set", args.secret_name, "-R", args.repo]

    # Pass token via stdin for security
    result = run_gh_command(command, check=False, capture_output=True, input_str=token)

    if isinstance(result, subprocess.CalledProcessError) or result.returncode != 0:
        print(f"{INDICATOR_FAIL} Failed to add secret {args.secret_name} to repository {args.repo}.")
        # Specific error details already printed by run_gh_command helper
        sys.exit(1)
    else:
        # Check stderr for success message from gh cli as stdout might be empty
        success_msg = ""
        if result.stderr:
            lines = result.stderr.strip().splitlines()
            if lines:
                # Get the last line which usually contains the success status
                last_line = lines[-1].lower()
                if f"updated secret {args.secret_name.lower()}" in last_line:
                    success_msg = f"updated secret {args.secret_name}"
                elif f"created secret {args.secret_name.lower()}" in last_line:
                    success_msg = f"created secret {args.secret_name}"

        if success_msg:
            print(f"{INDICATOR_SUCCESS} Successfully {success_msg} for repository {args.repo}.")
        else:
            # Fallback if stderr parsing failed but command succeeded
            print(
                f"{INDICATOR_SUCCESS} Secret operation completed for {args.secret_name} in {args.repo} (check details above)."
            )

    print(f"{INDICATOR_INFO} Setup complete! Your GitHub workflow can now use this secret.")


if __name__ == "__main__":
    main()
