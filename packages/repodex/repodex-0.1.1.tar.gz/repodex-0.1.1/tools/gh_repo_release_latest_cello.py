#!/usr/bin/env python3

import subprocess
import json
import sys
import platform
import argparse

# Attempt to import packaging, provide guidance if missing
try:
    from packaging import version
except ImportError:
    print("Error: 'packaging' library not found.")
    print("Please install it: pip install packaging")
    sys.exit(1)

# --- Color Codes ---
# Check if running on Windows, which might not support ANSI codes directly
# in all terminals without extra configuration (like colorama or WT).
# Basic check, might need refinement for specific Windows terminal emulators.
IS_WINDOWS = platform.system() == "Windows"

if IS_WINDOWS:
    # Simple output for Windows without ANSI codes
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
    # ANSI escape codes for other terminals (Linux, macOS, modern Windows Terminal)
    COLOR_GREEN = "\033[32m"
    COLOR_RED = "\033[31m"
    COLOR_YELLOW = "\033[33m"
    COLOR_BLUE = "\033[34m"  # Added for info
    COLOR_RESET = "\033[0m"
    INDICATOR_SUCCESS = f"{COLOR_GREEN}[x]{COLOR_RESET}"
    INDICATOR_FAIL = f"{COLOR_RED}[ ]{COLOR_RESET}"
    INDICATOR_WARN = f"{COLOR_YELLOW}[-]{COLOR_RESET}"
    INDICATOR_INFO = f"{COLOR_BLUE}[i]{COLOR_RESET}"


# Configuration
GITHUB_ORG = "CelloCommunications" # Changed from GITHUB_USERNAME
GITHUB_AUTHOR_USERNAME = "shaneholloman" # Added for clarity in fetching
# CSV_FILE = "github-project-readmes-shane/repositories.csv" # Removed
# REPO_COLUMN_NAME = "Repository"  # Removed


# Allow returning CalledProcessError when check=False
def run_gh_command(
    command: list, check: bool = True, capture_output: bool = True
) -> subprocess.CompletedProcess | subprocess.CalledProcessError:
    """Helper function to run GitHub CLI commands."""
    try:
        # Using shell=False is generally safer, command should be a list
        process = subprocess.run(
            command,
            text=True,
            check=check,
            capture_output=capture_output,
            encoding="utf-8",  # Explicitly set encoding
        )
        # Log stderr even on success for potential warnings
        if process.stderr:
            print(f"Stderr from {' '.join(command)}:\n{process.stderr.strip()}", file=sys.stderr)
        return process
    except FileNotFoundError:
        print(
            f"Error: '{command[0]}' command not found. Make sure GitHub CLI (gh) is installed and in your PATH.",
            file=sys.stderr,
        )
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        # Log more details on error
        print(f"Error running command: {' '.join(command)}", file=sys.stderr)
        print(f"Return Code: {e.returncode}", file=sys.stderr)
        if e.stdout:
            print(f"Stdout: {e.stdout.strip()}", file=sys.stderr)
        if e.stderr:
            print(f"Stderr: {e.stderr.strip()}", file=sys.stderr)
        # If check=False was intended, return the error object instead of raising
        if not check:
            return e
        # Re-raise the error if check=True (default)
        raise
    except Exception as e:
        print(f"An unexpected error occurred running {' '.join(command)}: {e}", file=sys.stderr)
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
        except subprocess.CalledProcessError: # Removed unused 'as e'
             # Error already logged by run_gh_command
             print(f"{INDICATOR_FAIL} Error during GraphQL API call on page {page_count}. Stopping fetch.")
             # Return what we have so far, or handle differently? For now, stop.
             break
        except Exception as e:
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
        except (KeyError, TypeError) as e:
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

            except (KeyError, TypeError, IndexError): # Removed unused 'e' assignment
                 # Catch potential errors accessing nested data
                 print(f"{INDICATOR_WARN} Could not determine authorship for {COLOR_BLUE}{repo['name']}{COLOR_RESET} (data structure error).")


    print(f"{INDICATOR_INFO} Found {len(authored_repo_names)} repositories authored by {GITHUB_AUTHOR_USERNAME} after checking {page_count} page(s).")
    return authored_repo_names


def get_tags(repo_name: str) -> list:
    """Fetch tags for a repository."""
    print(f"--- Fetching tags for {repo_name} ---")
    command = ["gh", "api", f"repos/{GITHUB_ORG}/{repo_name}/tags"] # Use GITHUB_ORG
    # Don't exit if tags fetch fails (e.g., repo deleted or no tags)
    result = run_gh_command(command, check=False)
    # Check if the result object is an error or a success
    if isinstance(result, subprocess.CalledProcessError) or result.returncode != 0:
        print(f"{INDICATOR_WARN} Could not fetch tags for {repo_name} (Maybe no tags or repo deleted?). Skipping.")
        return []
    try:
        tags_data = json.loads(result.stdout)
        # Ensure tags_data is a list before proceeding
        if isinstance(tags_data, list):
            return [tag.get("name") for tag in tags_data if tag.get("name")]
        else:
            print(
                f"{INDICATOR_WARN} Unexpected format for tags data for {repo_name}. Expected a list, got {type(tags_data)}. Skipping."
            )
            return []
    except json.JSONDecodeError:
        print(f"{INDICATOR_FAIL} Error parsing tags JSON for {repo_name}. Skipping.")
        return []


def find_latest_semver_tag(tags: list) -> str | None:
    """Find the latest semantic version tag from a list, preferring non-prereleases."""
    latest_stable_v = None
    latest_stable_tag_str = None
    latest_prerelease_v = None
    latest_prerelease_tag_str = None

    # print(f"Analyzing tags: {tags}") # Keep this less verbose unless debugging

    for tag_str in tags:
        try:
            # Allow optional 'v' prefix
            current_v_str = tag_str.lstrip("v")
            # Check if string is empty after stripping 'v'
            if not current_v_str:
                print(f"Skipping empty tag string derived from '{tag_str}'")
                continue
            current_v = version.parse(current_v_str)

            # Ensure it's a valid Version object (handles legacy versions too)
            if not isinstance(current_v, version.Version):
                print(f"Skipping tag '{tag_str}' - parsed as non-standard version type: {type(current_v)}")
                continue

            if current_v.is_prerelease:
                if latest_prerelease_v is None or current_v > latest_prerelease_v:
                    latest_prerelease_v = current_v
                    latest_prerelease_tag_str = tag_str
            else:  # Stable release
                if latest_stable_v is None or current_v > latest_stable_v:
                    latest_stable_v = current_v
                    latest_stable_tag_str = tag_str

        except version.InvalidVersion:
            # Ignore tags that are not valid versions
            # print(f"Ignoring invalid version tag: {tag_str}") # Less verbose
            continue
        except Exception as e:
            print(f"{INDICATOR_WARN} Unexpected error parsing tag '{tag_str}': {e}")
            continue

    # Prefer the latest stable tag if found
    if latest_stable_tag_str:
        print(f"{INDICATOR_INFO} Latest SemVer tag found: {COLOR_YELLOW}{latest_stable_tag_str}{COLOR_RESET} (stable)")
        return latest_stable_tag_str
    elif latest_prerelease_tag_str:
        print(
            f"{INDICATOR_INFO} Latest SemVer tag found: {COLOR_YELLOW}{latest_prerelease_tag_str}{COLOR_RESET} (pre-release)"
        )
        return latest_prerelease_tag_str
    else:
        print(f"{INDICATOR_WARN} No valid SemVer tags found.")
        return None


def check_release_exists(repo_name: str, tag: str) -> bool:
    """Check if a release exists for a given tag."""
    print(f"Checking for existing release for tag {tag}...")
    # Use full repo path with ORG
    full_repo = f"{GITHUB_ORG}/{repo_name}" # Use GITHUB_ORG
    command = ["gh", "release", "view", tag, "-R", full_repo]
    # Run with check=False as non-existence is expected
    result = run_gh_command(command, check=False, capture_output=True)

    # `gh release view` exits with 0 if found, non-zero (usually 1) if not found
    # Check if the result object is an error or a success
    is_error = isinstance(result, subprocess.CalledProcessError)
    return_code = result.returncode if not is_error else -1  # Use -1 or similar if it's an error obj

    exists = return_code == 0
    if exists:
        print(f"{INDICATOR_WARN} Release already exists for tag {COLOR_YELLOW}{tag}{COLOR_RESET}.")
    else:
        # Check stderr specifically for "release not found" to be sure
        stderr_lower = result.stderr.lower() if hasattr(result, "stderr") and result.stderr else ""
        if "release not found" in stderr_lower or "could not find release" in stderr_lower:
            print(f"{INDICATOR_INFO} Release does not exist for tag {COLOR_YELLOW}{tag}{COLOR_RESET}.")
        else:
            # Log unexpected error but treat as "not found" to potentially retry later
            print(
                f"{INDICATOR_WARN} Could not confirm release status for tag {COLOR_YELLOW}{tag}{COLOR_RESET}. `gh release view` failed with unexpected error. Assuming not found.",
                file=sys.stderr,
            )
            if hasattr(result, "stderr") and result.stderr:
                print(f"Stderr: {result.stderr.strip()}", file=sys.stderr)
            # Return False, allowing the script to attempt creation.
            # If creation fails due to existence, gh release create will handle it.
            return False
    return exists


def create_release(repo_name: str, tag: str):
    """Create a release for the given tag with auto-generated notes."""
    print(f"Attempting to create release for tag {tag}...")
    # Use full repo path with ORG
    full_repo = f"{GITHUB_ORG}/{repo_name}" # Use GITHUB_ORG
    command = ["gh", "release", "create", tag, "--generate-notes", "-R", full_repo]
    # Run with check=True, will raise CalledProcessError if creation fails
    try:
        result = run_gh_command(command, check=True, capture_output=True)
        print(f"{INDICATOR_SUCCESS} Successfully created release: {result.stdout.strip()}")
        return True  # Indicate success
    except subprocess.CalledProcessError as e:
        # Check if the error is because the release already exists (race condition?)
        stderr_lower = e.stderr.lower() if e.stderr else ""
        if "release already exists" in stderr_lower:
            print(
                f"{INDICATOR_WARN} Release for tag {COLOR_YELLOW}{tag}{COLOR_RESET} already exists (detected during creation attempt)."
            )
            return False  # Indicate skipped/already exists
        else:
            # Log other creation errors
            print(
                f"{INDICATOR_FAIL} Failed to create release for tag {COLOR_YELLOW}{tag}{COLOR_RESET}.", file=sys.stderr
            )
            # Stderr was logged by run_gh_command
            return False  # Indicate failure (explicit return for mypy)


def main():
    """Main script logic."""

    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description=f"Create latest releases for {GITHUB_AUTHOR_USERNAME}'s repos in the {GITHUB_ORG} org.")
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
        print(f"{INDICATOR_WARN} No repositories authored by {GITHUB_AUTHOR_USERNAME} found in {GITHUB_ORG} or error fetching list.") # Updated message
        return

    print(f"{INDICATOR_INFO} Found {len(repos_to_process)} repositories to process. Starting release checks...") # Updated message
    print("-" * 30)

    created_count = 0
    skipped_exist_count = 0
    skipped_no_tag_count = 0
    error_count = 0

    for repo_name in repos_to_process:
        print(f"Processing repository: {COLOR_BLUE}{repo_name}{COLOR_RESET}")
        try:
            tags = get_tags(repo_name)
            if not tags:
                # Already logged in get_tags if fetch failed
                skipped_no_tag_count += 1
                print("-" * 30)  # Separator
                continue

            latest_tag = find_latest_semver_tag(tags)
            if not latest_tag:
                # Already logged in find_latest_semver_tag
                skipped_no_tag_count += 1
                print("-" * 30)  # Separator
                continue

            if not check_release_exists(repo_name, latest_tag):
                # --- Dry Run Check ---
                if args.dry_run:
                    print(f"{INDICATOR_INFO} [DRY RUN] Would attempt to create release for tag {COLOR_YELLOW}{latest_tag}{COLOR_RESET}.")
                    # Simulate success for dry run counting, actual creation is skipped
                    created_count += 1 # Increment count as if created
                elif create_release(repo_name, latest_tag): # Only run if not dry run
                    created_count += 1
                else:
                    # If create_release returned False, it might be due to race condition or other error
                    # Check again if it exists now, maybe it was created between check and create
                    if check_release_exists(repo_name, latest_tag):
                        # Message already printed by check_release_exists if it exists now
                        skipped_exist_count += 1
                    else:
                        # Message already printed by create_release if it failed
                        error_count += 1
            else:
                # Release already existed based on initial check (message printed by check_release_exists)
                skipped_exist_count += 1

        except Exception as e:
            # Catch unexpected errors during the loop for a specific repo
            print(f"{INDICATOR_FAIL} An critical error occurred processing {repo_name}: {e}", file=sys.stderr)
            error_count += 1
        finally:
            # Ensure separator prints even if an error occurs mid-processing
            print("-" * 30)

    print("\n--- Processing Complete ---")
    print(f"Repositories Processed: {len(repos_to_process)}")
    print(f"{INDICATOR_SUCCESS} Releases Successfully Created: {created_count}")
    print(f"{INDICATOR_WARN} Releases Skipped (already existed): {skipped_exist_count}")
    print(f"{INDICATOR_WARN} Releases Skipped (no valid tag found): {skipped_no_tag_count}")
    print(f"{INDICATOR_FAIL} Errors during processing: {error_count}")


if __name__ == "__main__":
    main()
