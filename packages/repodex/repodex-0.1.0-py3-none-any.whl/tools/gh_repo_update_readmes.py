#!/usr/bin/env python3

import os
import subprocess
import json
import sys
import platform
import csv
import base64
import argparse
from pathlib import Path
from typing import Optional, Union

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
DEFAULT_USERNAME = "shaneholloman"
DEFAULT_README_DIR = "github-project-readmes-shane"
DEFAULT_CSV_FILE = os.path.join(DEFAULT_README_DIR, "repositories.csv")
REPO_COLUMN_NAME = "Repository"  # Header in the CSV for repository names
README_FILENAME_FORMAT = "{}-readme.md"
REMOTE_README_PATH = "README.md"
COMMIT_MESSAGE = "docs: update README formatting"


# --- Helper Functions ---
def run_gh_command(
    command: list, check: bool = True, capture_output: bool = True
) -> Union[subprocess.CompletedProcess, subprocess.CalledProcessError]:
    """Helper function to run GitHub CLI commands."""
    try:
        process = subprocess.run(
            command,
            text=True,
            check=check,
            capture_output=capture_output,
            encoding="utf-8",
        )
        # Avoid printing stderr noise like "Checking gh auth status"
        if process.stderr and check and "checking gh auth status" not in process.stderr.lower():
            print(f"Stderr from {' '.join(command)}:\n{process.stderr.strip()}", file=sys.stderr)
        return process
    except FileNotFoundError:
        print(
            f"{INDICATOR_FAIL} Error: '{command[0]}' command not found. Make sure GitHub CLI (gh) is installed and in your PATH.",
            file=sys.stderr,
        )
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        # Error details are useful, print them if check=False or if check=True before raising
        print(f"{INDICATOR_FAIL} Error running command: {' '.join(command)}", file=sys.stderr)
        print(f"Return Code: {e.returncode}", file=sys.stderr)
        if e.stdout:
            print(f"Stdout: {e.stdout.strip()}", file=sys.stderr)
        if e.stderr:
            print(f"Stderr: {e.stderr.strip()}", file=sys.stderr)
        if not check:
            return e  # Return error object if check=False
        raise  # Re-raise if check=True
    except Exception as e:
        print(f"{INDICATOR_FAIL} An unexpected error occurred running {' '.join(command)}: {e}", file=sys.stderr)
        sys.exit(1)


def get_readme_sha(username: str, repo_name: str) -> Optional[str]:
    """Get the SHA of the remote README.md file."""
    command = ["gh", "api", f"repos/{username}/{repo_name}/contents/{REMOTE_README_PATH}"]
    result = run_gh_command(command, check=False, capture_output=True)

    if isinstance(result, subprocess.CalledProcessError) or result.returncode != 0:
        stderr_lower = result.stderr.lower() if hasattr(result, "stderr") and result.stderr else ""
        if "not found (404)" in stderr_lower:
            print(f"{INDICATOR_WARN} Remote {REMOTE_README_PATH} not found in {repo_name}. Skipping.")
        else:
            print(f"{INDICATOR_WARN} Could not get SHA for {REMOTE_README_PATH} in {repo_name}. Skipping.")
        return None

    try:
        data = json.loads(result.stdout)
        sha = data.get("sha")
        if not sha:
            print(f"{INDICATOR_WARN} Could not parse SHA from API response for {repo_name}. Skipping.")
            return None
        return sha
    except json.JSONDecodeError:
        print(f"{INDICATOR_FAIL} Error parsing JSON response for SHA in {repo_name}. Skipping.")
        return None


def update_remote_readme(username: str, repo_name: str, sha: str, local_readme_path: str) -> bool:
    """Update the remote README file using the GitHub API."""
    try:
        with open(local_readme_path, "rb") as f:
            content_bytes = f.read()
        content_base64 = base64.b64encode(content_bytes).decode("utf-8")
    except Exception as e:
        print(f"{INDICATOR_FAIL} Error reading or encoding local file {local_readme_path}: {e}")
        return False

    command = [
        "gh",
        "api",
        "-X",
        "PUT",
        f"/repos/{username}/{repo_name}/contents/{REMOTE_README_PATH}",
        "-f",
        f"message={COMMIT_MESSAGE}",
        "-f",
        f"content={content_base64}",
        "-f",
        f"sha={sha}",
    ]

    print(f"{INDICATOR_INFO} Attempting to update {REMOTE_README_PATH} in {repo_name}...")
    result = run_gh_command(command, check=False, capture_output=True)

    if isinstance(result, subprocess.CalledProcessError) or result.returncode != 0:
        print(f"{INDICATOR_FAIL} Failed to update {REMOTE_README_PATH} for {repo_name}.")
        # Error details already printed by run_gh_command
        return False
    else:
        print(f"{INDICATOR_SUCCESS} Successfully updated {REMOTE_README_PATH} for {repo_name}.")
        return True


# --- Main Function ---
def main():
    """Main script logic."""
    parser = argparse.ArgumentParser(description="Update README files in GitHub repositories from local files.")
    parser.add_argument(
        "-u",
        "--username",
        default=DEFAULT_USERNAME,
        help=f"GitHub username (default: {DEFAULT_USERNAME})",
    )
    parser.add_argument(
        "-c",
        "--csv-file",
        default=DEFAULT_CSV_FILE,
        help=f"Path to the CSV file containing repository names (default: {DEFAULT_CSV_FILE})",
    )
    parser.add_argument(
        "-d",
        "--readme-dir",
        default=DEFAULT_README_DIR,
        help=f"Directory containing local README files (default: {DEFAULT_README_DIR})",
    )
    args = parser.parse_args()

    # --- Check Prerequisites ---
    print(f"{INDICATOR_INFO} Checking GitHub CLI authentication...")
    auth_check = run_gh_command(["gh", "auth", "status"], check=False)
    if isinstance(auth_check, subprocess.CalledProcessError) or auth_check.returncode != 0:
        print(f"{INDICATOR_FAIL} GitHub CLI not authenticated. Please run 'gh auth login'.")
        sys.exit(1)
    print(f"{INDICATOR_SUCCESS} GitHub CLI authenticated.")

    csv_file_path = Path(args.csv_file)
    readme_dir_path = Path(args.readme_dir)

    if not csv_file_path.is_file():
        print(f"{INDICATOR_FAIL} Error: CSV file not found at {csv_file_path}", file=sys.stderr)
        sys.exit(1)
    if not readme_dir_path.is_dir():
        print(f"{INDICATOR_FAIL} Error: Local README directory not found at {readme_dir_path}", file=sys.stderr)
        sys.exit(1)

    # --- Read Repositories from CSV ---
    repos_to_process = []
    try:
        with open(csv_file_path, mode="r", encoding="utf-8", newline="") as infile:
            reader = csv.DictReader(infile)
            if REPO_COLUMN_NAME not in reader.fieldnames:
                print(
                    f"{INDICATOR_FAIL} Error: Column '{REPO_COLUMN_NAME}' not found in header of {csv_file_path}",
                    file=sys.stderr,
                )
                print(f"Available columns: {reader.fieldnames}", file=sys.stderr)
                sys.exit(1)
            for row_number, row in enumerate(reader, start=2):
                repo_name = row.get(REPO_COLUMN_NAME)
                if repo_name and repo_name.strip():
                    repos_to_process.append(repo_name.strip())
                else:
                    print(
                        f"{INDICATOR_WARN} Empty repository name found in row {row_number} of {csv_file_path}",
                        file=sys.stderr,
                    )
    except Exception as e:
        print(f"{INDICATOR_FAIL} Error reading CSV file {csv_file_path}: {e}", file=sys.stderr)
        sys.exit(1)

    if not repos_to_process:
        print(f"{INDICATOR_WARN} No valid repository names found in CSV file.")
        return

    print(f"{INDICATOR_INFO} Found {len(repos_to_process)} repositories in {csv_file_path}. Starting update process...")
    print("-" * 30)

    # --- Process Each Repository ---
    success_count = 0
    failure_count = 0
    skipped_count = 0

    for repo_name in repos_to_process:
        print(f"Processing repository: {COLOR_BLUE}{repo_name}{COLOR_RESET}")
        local_readme_filename = README_FILENAME_FORMAT.format(repo_name)
        local_readme_path = readme_dir_path / local_readme_filename

        if not local_readme_path.is_file():
            print(f"{INDICATOR_WARN} Local README file not found: {local_readme_path}. Skipping.")
            skipped_count += 1
            print("-" * 30)
            continue

        sha = get_readme_sha(args.username, repo_name)
        if not sha:
            # Error/skip message already printed by get_readme_sha
            failure_count += 1
            print("-" * 30)
            continue

        if update_remote_readme(args.username, repo_name, sha, str(local_readme_path)):
            success_count += 1
        else:
            # Error message already printed by update_remote_readme
            failure_count += 1

        print("-" * 30)

    # --- Summary ---
    print("\n--- README Update Process Complete ---")
    print(f"Repositories Processed: {len(repos_to_process)}")
    print(f"{INDICATOR_SUCCESS} Successfully updated: {success_count}")
    print(f"{INDICATOR_FAIL} Failed updates: {failure_count}")
    print(f"{INDICATOR_WARN} Skipped (local file missing/remote check failed): {skipped_count}")


if __name__ == "__main__":
    main()
