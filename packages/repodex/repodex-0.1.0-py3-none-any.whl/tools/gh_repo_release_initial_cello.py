#!/usr/bin/env python3

import subprocess
import json
import sys
import platform
import argparse

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
GITHUB_ORG = "CelloCommunications" # Changed
GITHUB_AUTHOR_USERNAME = "shaneholloman" # Added
# CSV_FILE = "github-project-readmes-shane/repositories.csv" # Removed
# REPO_COLUMN_NAME = "Repository"  # Removed
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


# Added function to fetch authored repos using GraphQL
def get_authored_repositories():
    """Get list of repositories from organization that were authored by GITHUB_AUTHOR_USERNAME using GraphQL for efficiency"""
    # Note: GITHUB_AUTHOR_USERNAME is used for author checking, GITHUB_ORG for repo fetching
    print(f"{INDICATOR_INFO} Fetching repositories from {COLOR_BLUE}{GITHUB_ORG}{COLOR_RESET} authored by {COLOR_BLUE}{GITHUB_AUTHOR_USERNAME}{COLOR_RESET}...")

    authored_repo_names = [] # Just need names for this script
    cursor = None
    has_next_page = True
    page_count = 0
    repo_limit = 2500 # Use a reasonable limit, similar to fetcher script

    # Paginate through all repos
    while has_next_page and page_count < repo_limit // 100 + 1:
        page_count += 1
        print(f"{INDICATOR_INFO} Fetching page {page_count}...") # Simplified message

        # Prepare cursor parameter for pagination
        cursor_param = f', after: "{cursor}"' if cursor else ""

        # GraphQL query to get repos and first commit author in one call
        query = f"""
        query {{
          organization(login: "{GITHUB_ORG}") {{
            repositories(first: 100{cursor_param}) {{
              pageInfo {{
                hasNextPage
                endCursor
              }}
              nodes {{
                name
                isFork
                defaultBranchRef {{
                  target {{
                    ... on Commit {{
                      history(first: 1) {{
                        nodes {{
                          author {{
                            user {{
                              login
                            }}
                          }}
                        }}
                      }}
                    }}
                  }}
                }}
              }}
            }}
          }}
        }}
        """

        # Execute GraphQL query
        cmd = ["gh", "api", "graphql", "-f", f"query={query}"]

        try:
            result = run_gh_command(cmd, check=True, capture_output=True) # Use helper
        except subprocess.CalledProcessError: # Removed unused 'e' assignment
             # Error already logged by run_gh_command
             print(f"{INDICATOR_FAIL} Error during GraphQL API call on page {page_count}. Stopping fetch.")
             # Return what we have so far, or handle differently? For now, stop.
             break
        except Exception as e: # Keep 'e' here as it's used in the message
             print(f"{INDICATOR_FAIL} Unexpected error during GraphQL API call on page {page_count}: {e}. Stopping fetch.")
             break


        # Parse JSON response
        try:
             data = json.loads(result.stdout)
        except json.JSONDecodeError:
             print(f"{INDICATOR_FAIL} Error parsing GraphQL JSON response on page {page_count}. Stopping fetch.")
             break

        # Extract repository data and pagination info
        try:
            repos = data["data"]["organization"]["repositories"]["nodes"]
            page_info = data["data"]["organization"]["repositories"]["pageInfo"]
            has_next_page = page_info["hasNextPage"]
            cursor = page_info["endCursor"]
        except (KeyError, TypeError) as e: # Keep 'e' here as it's used in the message
            print(f"{INDICATOR_FAIL} Error extracting data from GraphQL response on page {page_count}: {e}. Stopping fetch.")
            print(f"Response data: {data}") # Log response data for debugging
            break


        # Filter for non-fork repos authored by GITHUB_AUTHOR_USERNAME
        for repo in repos:
            if repo.get("isFork", False):
                continue

            # Get author of first commit if available
            try:
                # Check if defaultBranchRef and target exist before accessing history
                if repo.get("defaultBranchRef") and repo["defaultBranchRef"].get("target") and repo["defaultBranchRef"]["target"].get("history"):
                    first_commit = repo["defaultBranchRef"]["target"]["history"]["nodes"][0]
                    # Check if author and user exist
                    if first_commit.get("author") and first_commit["author"].get("user"):
                         first_author = first_commit["author"]["user"]["login"]
                         # Check if authored by target user
                         if first_author == GITHUB_AUTHOR_USERNAME:
                             # print(f"{INDICATOR_SUCCESS} Repository {COLOR_BLUE}{repo['name']}{COLOR_RESET} was authored by {GITHUB_AUTHOR_USERNAME}") # Keep less verbose
                             authored_repo_names.append(repo["name"])
                         # else: # Keep less verbose
                         #     print(f"{INDICATOR_FAIL} Repository {COLOR_BLUE}{repo['name']}{COLOR_RESET} was not authored by {GITHUB_AUTHOR_USERNAME} (first commit by {first_author})")
                    else:
                         # Handle cases where author/user might be null (e.g., commit by deleted user)
                         print(f"{INDICATOR_WARN} Could not determine authorship for {COLOR_BLUE}{repo['name']}{COLOR_RESET} (author/user missing in commit data).")
                else:
                     # Handle cases where default branch might not exist or have commits
                     print(f"{INDICATOR_WARN} Could not determine authorship for {COLOR_BLUE}{repo['name']}{COLOR_RESET} (missing branch/commit history).")

            except (KeyError, TypeError, IndexError):
                 # Catch potential errors accessing nested data
                 print(f"{INDICATOR_WARN} Could not determine authorship for {COLOR_BLUE}{repo['name']}{COLOR_RESET} (data structure error).")


    print(f"{INDICATOR_INFO} Found {len(authored_repo_names)} repositories authored by {GITHUB_AUTHOR_USERNAME} after checking {page_count} page(s).")
    return authored_repo_names


def get_tags(repo_name: str) -> list | None:
    """Fetch tags for a repository. Returns None if fetch fails."""
    # print(f"--- Fetching tags for {repo_name} ---") # Less verbose for this script
    command = ["gh", "api", f"repos/{GITHUB_ORG}/{repo_name}/tags"] # Use GITHUB_ORG
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


def create_initial_release(repo_name: str, tag: str, dry_run: bool):
    """Create the initial v0.1.0 release, respecting dry_run flag."""
    full_repo = f"{GITHUB_ORG}/{repo_name}" # Use GITHUB_ORG
    command = ["gh", "release", "create", tag, "--generate-notes", "-R", full_repo]

    if dry_run:
        print(f"{INDICATOR_INFO} [DRY RUN] Would execute: {' '.join(command)}")
        # Simulate success for dry run counting
        print(f"{INDICATOR_SUCCESS} [DRY RUN] Simulated creation of initial release for tag {COLOR_YELLOW}{tag}{COLOR_RESET}.")
        return True

    print(f"Attempting to create initial release {COLOR_YELLOW}{tag}{COLOR_RESET}...")
    # Use --generate-notes, it might be empty but harmless
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
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description=f"Create initial v0.1.0 release for untagged {GITHUB_AUTHOR_USERNAME}'s repos in the {GITHUB_ORG} org.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what actions would be taken without actually creating releases."
    )
    args = parser.parse_args()

    if args.dry_run:
        print(f"{INDICATOR_WARN} --- DRY RUN MODE ENABLED ---")
        print(f"{INDICATOR_WARN} No releases will actually be created.")
        print("-" * 30)

    # --- Get Authored Repositories ---
    repos_to_process = get_authored_repositories()

    if not repos_to_process:
        print(f"{INDICATOR_WARN} No repositories authored by {GITHUB_AUTHOR_USERNAME} found in {GITHUB_ORG} or error fetching list.")
        return

    print(f"{INDICATOR_INFO} Found {len(repos_to_process)} authored repositories. Checking for initial tag/release...")
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
                # Pass dry_run flag to creation function
                if create_initial_release(repo_name, INITIAL_TAG, args.dry_run):
                    created_count += 1
                else:
                    # Creation failed, was skipped (dry run), or release/tag already existed
                    # Increment error count only if it wasn't a dry run skip or known skip condition
                    if not args.dry_run:
                         # Check stderr from create_initial_release if needed, but for now, count as error
                         error_count += 1 # Count actual failures or unexpected skips
            else:  # Tags already exist
                print(f"{INDICATOR_WARN} Repository already has tags ({len(tags)} found). Skipping.")
                skipped_tagged_count += 1

        except Exception as e: # Keep 'e' here as it's used in the message
            print(f"{INDICATOR_FAIL} An critical error occurred processing {repo_name}: {e}", file=sys.stderr)
            error_count += 1
        finally:
            print("-" * 30)

    print("\n--- Initial Release Processing Complete ---")
    print(f"Repositories Processed: {len(repos_to_process)}")
    print(f"{INDICATOR_SUCCESS} Initial Releases ({INITIAL_TAG}) {'Simulated' if args.dry_run else 'Successfully Created'}: {created_count}")
    print(f"{INDICATOR_WARN} Repositories Skipped (already had tags): {skipped_tagged_count}")
    print(f"{INDICATOR_FAIL} Errors/Skipped during processing (fetch/creation issues): {error_count}")


if __name__ == "__main__":
    main()
