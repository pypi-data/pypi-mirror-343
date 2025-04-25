#!/usr/bin/env python3

import csv
import subprocess
import json
import sys
import os
import platform

# --- Color Codes ---
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

# Configuration
GITHUB_USERNAME = "shaneholloman"
CSV_FILE = "github-project-readmes-shane/repositories.csv"
REPO_COLUMN_NAME = "Repository"  # Header in the CSV for repository names
INITIAL_TAG = "v0.1.0"


# Allow returning CalledProcessError when check=False
def run_gh_command(
    command: list, check: bool = True, capture_output: bool = True
) -> subprocess.CompletedProcess | subprocess.CalledProcessError:
    """Helper function to run GitHub CLI commands."""
    try:
        process = subprocess.run(command, text=True, check=check, capture_output=capture_output, encoding="utf-8")
        if process.stderr and check:  # Only print stderr on success if check=True, avoid double printing on error
            # Don't print expected "release not found" errors from stderr during checks
            stderr_lower = process.stderr.lower()
            if "release not found" not in stderr_lower and "could not find release" not in stderr_lower:
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


def get_tags(repo_name: str) -> list | None:
    """Fetch tags for a repository. Returns None if fetch fails."""
    # print(f"--- Fetching tags for {repo_name} ---") # Less verbose for this script
    command = ["gh", "api", f"repos/{GITHUB_USERNAME}/{repo_name}/tags"]
    result = run_gh_command(command, check=False)

    if isinstance(result, subprocess.CalledProcessError) or result.returncode != 0:
        # Check if it's a 404 (repo not found) or 409 (Git repo is empty)
        stderr_lower = result.stderr.lower() if hasattr(result, "stderr") and result.stderr else ""
        if "not found (404)" in stderr_lower:
            print(f"{INDICATOR_WARN} Repository {repo_name} not found (404). Skipping.")
        elif "git repository is empty (409)" in stderr_lower:
            print(f"{INDICATOR_WARN} Repository {repo_name} is empty (409). Cannot tag. Skipping.")
        else:
            print(f"{INDICATOR_WARN} Could not fetch tags for {repo_name}. Skipping.")
        return None  # Indicate failure to fetch
    try:
        tags_data = json.loads(result.stdout)
        if isinstance(tags_data, list):
            # Return the list of tag names found
            return [tag.get("name") for tag in tags_data if tag.get("name")]
        else:
            print(
                f"{INDICATOR_WARN} Unexpected format for tags data for {repo_name}. Expected list, got {type(tags_data)}. Skipping."
            )
            return None  # Indicate unexpected format
    except json.JSONDecodeError:
        print(f"{INDICATOR_FAIL} Error parsing tags JSON for {repo_name}. Skipping.")
        return None  # Indicate JSON parsing error


def create_initial_release(repo_name: str, tag: str):
    """Create the initial v0.1.0 release."""
    print(f"Attempting to create initial release {COLOR_YELLOW}{tag}{COLOR_RESET}...")
    full_repo = f"{GITHUB_USERNAME}/{repo_name}"
    # Use --generate-notes, it might be empty but harmless
    command = ["gh", "release", "create", tag, "--generate-notes", "-R", full_repo]
    try:
        result = run_gh_command(command, check=True, capture_output=True)
        print(f"{INDICATOR_SUCCESS} Successfully created initial release: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        stderr_lower = e.stderr.lower() if e.stderr else ""
        if "release already exists" in stderr_lower:
            print(f"{INDICATOR_WARN} Release for tag {COLOR_YELLOW}{tag}{COLOR_RESET} already exists.")
            return False  # Indicate skipped/already exists
        elif "reference already exists" in stderr_lower:
            print(
                f"{INDICATOR_WARN} Tag {COLOR_YELLOW}{tag}{COLOR_RESET} already exists, but release might be missing. Skipping initial creation."
            )
            # Consider adding logic here to create *only* the release if tag exists but release doesn't
            return False  # Indicate skipped/tag exists
        else:
            print(
                f"{INDICATOR_FAIL} Failed to create initial release for tag {COLOR_YELLOW}{tag}{COLOR_RESET}.",
                file=sys.stderr,
            )
            # Stderr logged by run_gh_command
            return False  # Indicate failure


def main():
    """Main script logic."""
    if not os.path.exists(CSV_FILE):
        print(f"{INDICATOR_FAIL} Error: CSV file not found at {CSV_FILE}", file=sys.stderr)
        sys.exit(1)

    repos_to_process = []
    try:
        with open(CSV_FILE, mode="r", encoding="utf-8") as infile:
            reader = csv.DictReader(infile)
            if REPO_COLUMN_NAME not in reader.fieldnames:
                print(
                    f"{INDICATOR_FAIL} Error: Column '{REPO_COLUMN_NAME}' not found in header of {CSV_FILE}",
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
                        f"{INDICATOR_WARN} Empty repository name found in row {row_number} of {CSV_FILE}",
                        file=sys.stderr,
                    )
    except Exception as e:
        print(f"{INDICATOR_FAIL} Error reading CSV file {CSV_FILE}: {e}", file=sys.stderr)
        sys.exit(1)

    if not repos_to_process:
        print(f"{INDICATOR_WARN} No valid repository names found in CSV file.")
        return

    print(
        f"{INDICATOR_INFO} Found {len(repos_to_process)} repositories in {CSV_FILE}. Checking for initial tag/release..."
    )
    print("-" * 30)

    created_count = 0
    skipped_tagged_count = 0
    error_count = 0  # Includes fetch errors and creation errors

    for repo_name in repos_to_process:
        print(f"Processing repository: {COLOR_BLUE}{repo_name}{COLOR_RESET}")
        try:
            tags = get_tags(repo_name)

            if tags is None:  # Indicates an error during fetch (e.g., 404, 409, JSON error)
                error_count += 1
                print(f"{INDICATOR_FAIL} Skipping {repo_name} due to tag fetch error.")
            elif len(tags) == 0:  # No tags exist, proceed with creation attempt
                print(f"{INDICATOR_INFO} No tags found for {repo_name}.")
                if create_initial_release(repo_name, INITIAL_TAG):
                    created_count += 1
                else:
                    # Creation failed or release/tag already existed
                    error_count += 1  # Count as error for simplicity, though might be a skip
            else:  # Tags already exist
                print(f"{INDICATOR_WARN} Repository already has tags ({len(tags)} found). Skipping.")
                skipped_tagged_count += 1

        except Exception as e:
            print(f"{INDICATOR_FAIL} An critical error occurred processing {repo_name}: {e}", file=sys.stderr)
            error_count += 1
        finally:
            print("-" * 30)

    print("\n--- Initial Release Processing Complete ---")
    print(f"Repositories Processed: {len(repos_to_process)}")
    print(f"{INDICATOR_SUCCESS} Initial Releases ({INITIAL_TAG}) Successfully Created: {created_count}")
    print(f"{INDICATOR_WARN} Repositories Skipped (already had tags): {skipped_tagged_count}")
    print(f"{INDICATOR_FAIL} Errors/Skipped during processing (fetch/creation issues): {error_count}")


if __name__ == "__main__":
    main()
