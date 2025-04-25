#!/usr/bin/env python3

import os
import subprocess
import json
import sys
import base64
import datetime
import platform
from pathlib import Path
from typing import Dict, List, Optional

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

# Configuration variables
GITHUB_USERNAME = "shaneholloman"
OUTPUT_DIR = "github-project-readmes-shane"
INDEX_FILENAME = "README.md"  # Changed from index.md to README.md
CSV_FILENAME = "repositories.csv"  # CSV export filename
README_FILENAME = "README.md"
FILE_FORMAT = "{}-readme.md"
INDEX_TITLE = "# GitHub Projects README Index"
INDEX_INTRO = "This is an index of README files from my GitHub repositories (excluding forks).\n\n"
REPO_LIMIT = 2500  # Maximum number of repositories to fetch (Increased from 1500)


def check_gh_cli():
    """Check if GitHub CLI is installed and authenticated"""
    try:
        result = subprocess.run(
            ["gh", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            print(f"{INDICATOR_FAIL} Error: GitHub CLI (gh) is not installed or not in PATH")
            print(f"{INDICATOR_INFO} Please install it from: https://cli.github.com/")
            sys.exit(1)

        # Check if authenticated
        result = subprocess.run(
            ["gh", "auth", "status"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            print(f"{INDICATOR_FAIL} Error: Not authenticated with GitHub")
            print(f"{INDICATOR_INFO} Please run: gh auth login")
            sys.exit(1)

        print(f"{INDICATOR_SUCCESS} GitHub CLI is installed and authenticated")
    except Exception as e:
        print(f"{INDICATOR_FAIL} Error checking GitHub CLI: {e}")
        sys.exit(1)


def create_output_directory():
    """Create the output directory if it doesn't exist"""
    output_path = Path(OUTPUT_DIR)
    if not output_path.exists():
        try:
            output_path.mkdir(parents=True)
            print(f"{INDICATOR_SUCCESS} Created directory: {OUTPUT_DIR}")
        except Exception as e:
            print(f"{INDICATOR_FAIL} Error creating directory {OUTPUT_DIR}: {e}")
            sys.exit(1)
    else:
        print(f"{INDICATOR_INFO} Directory already exists: {OUTPUT_DIR}")


def get_repositories():
    """Get list of non-forked repositories for the user using pagination"""
    try:
        print(f"{INDICATOR_INFO} Fetching repositories (up to {REPO_LIMIT})...")

        all_repos = []
        page = 1
        per_page = 100  # GitHub API default and maximum
        max_pages = REPO_LIMIT // per_page + 1

        while page <= max_pages:
            print(f"{INDICATOR_INFO} Fetching page {page} of repositories...")

            # Use GitHub API directly with pagination - user/repos endpoint to include private repos
            cmd = [
                "gh",
                "api",
                f"user/repos?per_page={per_page}&page={page}&affiliation=owner",
            ]

            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )

            # Parse the JSON output
            page_repos = json.loads(result.stdout)

            if not page_repos:  # No more repositories
                print(f"{INDICATOR_INFO} No more repositories found.")
                break

            print(f"{INDICATOR_INFO} Retrieved {len(page_repos)} repositories on page {page}")
            all_repos.extend(page_repos)

            # Break if we hit the repo limit
            if len(all_repos) >= REPO_LIMIT:
                all_repos = all_repos[:REPO_LIMIT]
                break

            page += 1

        print(f"{INDICATOR_INFO} Retrieved {len(all_repos)} total repositories from API.")

        # Convert GitHub API format to our expected format
        converted_repos = []
        for repo in all_repos:
            converted_repos.append(
                {
                    "name": repo.get("name", ""),
                    "isFork": repo.get("fork", False),
                    "description": repo.get("description", ""),
                    "createdAt": repo.get("created_at", ""),
                    "updatedAt": repo.get("updated_at", ""),
                    "isPrivate": repo.get("private", False),  # Track if repository is private
                }
            )

        # Filter out forks
        non_fork_repos = [repo for repo in converted_repos if not repo.get("isFork", False)]

        print(f"{INDICATOR_INFO} Found {len(non_fork_repos)} non-forked repositories out of {len(all_repos)} total repositories fetched.")

        # Verify how many ansible-role repositories we found
        ansible_roles = [repo for repo in non_fork_repos if "ansible-role" in repo["name"]]
        print(f"{INDICATOR_INFO} Found {len(ansible_roles)} ansible-role repositories.")

        return non_fork_repos
    except subprocess.CalledProcessError as e:
        print(f"{INDICATOR_FAIL} Error fetching repositories: {e}")
        print(f"{INDICATOR_FAIL} Error output: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(f"{INDICATOR_FAIL} Error processing repositories: {e}")
        sys.exit(1)


def fetch_readme(repo_name):
    """Fetch README content for a repository"""
    try:
        cmd = [
            "gh",
            "api",
            f"repos/{GITHUB_USERNAME}/{repo_name}/contents/{README_FILENAME}",
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)

        if result.returncode != 0:
            # Check if it's a 404 error specifically
            stderr_lower = result.stderr.lower() if result.stderr else ""
            if "not found (404)" in stderr_lower:
                print(f"{INDICATOR_WARN} README not found for {repo_name} (404).")
            else:
                print(f"{INDICATOR_WARN} Error checking README for {repo_name} (Return code: {result.returncode}).")
                if result.stderr:
                    print(f"Stderr: {result.stderr.strip()}", file=sys.stderr)
            return None

        content_data = json.loads(result.stdout)
        if content_data.get("encoding") == "base64" and content_data.get("content"):
            content = base64.b64decode(content_data["content"]).decode("utf-8")
            return content
        else:
            print(f"{INDICATOR_WARN} Unexpected content format for {repo_name}")
            return None
    except Exception as e:
        print(f"{INDICATOR_FAIL} Error fetching README for {repo_name}: {e}")
        return None


def format_date(date_string):
    """Format a date string to a more readable format"""
    if not date_string:
        return "Unknown"
    try:
        # GitHub date format: 2020-01-15T00:00:00Z
        date_obj = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
        return date_obj.strftime("%Y-%m-%d")
    except Exception:
        return date_string


def save_readme(repo_name, content):
    """Save README content to a file"""
    if content is None:
        return False

    filename = FILE_FORMAT.format(repo_name)
    file_path = os.path.join(OUTPUT_DIR, filename)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        # Keep this less verbose, success is implied if no error
        # print(f"{INDICATOR_SUCCESS} Saved README for {repo_name}")
        return True
    except Exception as e:
        print(f"{INDICATOR_FAIL} Error saving README for {repo_name}: {e}")
        return False


def fetch_latest_release(repo_name: str) -> Optional[Dict]:
    """Fetch latest release information for a repository"""
    try:
        cmd = [
            "gh",
            "release",
            "list",
            "-R",
            f"{GITHUB_USERNAME}/{repo_name}",
            "-L",
            "1",
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)

        if result.returncode != 0 or "no releases found" in result.stdout.lower():
            # print(f"{INDICATOR_INFO} No releases found for {repo_name}") # Less verbose
            return None

        # Parse the output which is in format: TITLE TYPE TAG_NAME PUBLISHED
        parts = result.stdout.strip().split()
        if len(parts) >= 3:
            tag_name = parts[-2]  # TAG_NAME is second to last
            return {
                "tag": tag_name,
                "url": f"https://github.com/{GITHUB_USERNAME}/{repo_name}/releases/tag/{tag_name}",
            }
        return None
    except Exception as e:
        print(f"{INDICATOR_FAIL} Error fetching release for {repo_name}: {e}")
        return None


def fetch_tags(repo_name: str) -> List[str]:
    """Fetch tags for a repository"""
    try:
        cmd = ["gh", "api", f"repos/{GITHUB_USERNAME}/{repo_name}/tags"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)

        if result.returncode != 0:
            # print(f"{INDICATOR_WARN} Error fetching tags for {repo_name}") # Less verbose
            return []

        tags_data = json.loads(result.stdout)
        if not tags_data:
            return []

        # Return list of tag names
        return [tag.get("name") for tag in tags_data]
    except Exception as e:
        print(f"{INDICATOR_FAIL} Error processing tags for {repo_name}: {e}")
        return []


def export_to_csv(readme_info):
    """Export repository information to a CSV file"""
    if not readme_info:
        print(f"{INDICATOR_WARN} No READMEs found to export to CSV")
        return

    csv_path = os.path.join(OUTPUT_DIR, CSV_FILENAME)

    try:
        # Sort alphabetically by repository name
        sorted_readmes = sorted(readme_info, key=lambda x: x["name"].lower())

        with open(csv_path, "w", encoding="utf-8") as f:
            # Write CSV header
            f.write("Repository,DateCreated,DateUpdated,Visibility,Release,Tags\n")

            # Add each repository as a CSV row
            for item in sorted_readmes:
                repo_name = item["name"]
                created_at = format_date(item.get("createdAt", ""))
                updated_at = format_date(item.get("updatedAt", ""))
                visibility = "Private" if item.get("isPrivate", False) else "Public"
                release = item.get("release", {}).get("tag", "None") if item.get("release") else "None"

                # Get just the latest tag for the CSV
                tags = item.get("tags", [])
                latest_tag = tags[0] if tags else "None"

                # Write CSV row
                f.write(f"{repo_name},{created_at},{updated_at},{visibility},{release},{latest_tag}\n")

        print(f"{INDICATOR_SUCCESS} Generated CSV file: {csv_path}")
    except Exception as e:
        print(f"{INDICATOR_FAIL} Error generating CSV: {e}")


def generate_index(readme_info):
    """Generate an index file with links to all READMEs formatted as a table"""
    if not readme_info:
        print(f"{INDICATOR_WARN} No READMEs found to index")
        return

    index_path = os.path.join(OUTPUT_DIR, INDEX_FILENAME)

    try:
        # Sort alphabetically by repository name
        sorted_readmes = sorted(readme_info, key=lambda x: x["name"].lower())

        with open(index_path, "w", encoding="utf-8") as f:
            f.write(INDEX_TITLE + "\n\n")
            f.write(INDEX_INTRO)

            # Calculate statistics
            total_repos = len(sorted_readmes)
            private_repos = sum(1 for item in sorted_readmes if item.get("isPrivate", False))
            public_repos = total_repos - private_repos
            released_repos = sum(1 for item in sorted_readmes if item.get("release"))

            # Add summary line
            summary_line = (
                f"Total Repositories: {total_repos} Private: {private_repos} "
                f"Public: {public_repos} Released: {released_repos}\n\n"
            )
            f.write(summary_line)

            # Create table header
            f.write("| Repository | Date Created | Date Updated | Visibility | Release | Tags |\n")
            f.write("|------------|--------------|--------------|------------|---------|------|\n")

            # Add each repository as a table row
            for item in sorted_readmes:
                repo_name = item["name"]
                created_at = format_date(item.get("createdAt", ""))
                updated_at = format_date(item.get("updatedAt", ""))
                visibility_status = "Private" if item.get("isPrivate", False) else "Public"
                filename = FILE_FORMAT.format(repo_name)

                # Create GitHub URL for the repository
                github_url = f"https://github.com/{GITHUB_USERNAME}/{repo_name}"

                # Create markdown link for the repository name
                link_text = f"[{repo_name}](./{filename})"

                # Create markdown link for the visibility that points to GitHub
                visibility_link = f"[{visibility_status}]({github_url})"

                # Format release information (with link if available)
                release_info = item.get("release")
                if release_info:
                    release_text = f"[{release_info['tag']}]({release_info['url']})"
                else:
                    release_text = "None"

                # Format tag information (with link to the latest tag release page)
                tags = item.get("tags", [])
                if tags:
                    latest_tag = tags[0]
                    tag_url = f"{github_url}/releases/tag/{latest_tag}"
                    tag_text = f"[{latest_tag}]({tag_url})"
                else:
                    tag_text = "None"

                # Write table row
                f.write(
                    f"| {link_text} | {created_at} | {updated_at} | {visibility_link} | {release_text} | {tag_text} |\n"
                )

        print(f"{INDICATOR_SUCCESS} Generated index file: {index_path}")
    except Exception as e:
        print(f"{INDICATOR_FAIL} Error generating index: {e}")


def main():
    """Main function to process repositories and fetch READMEs"""
    print(f"{INDICATOR_INFO} Fetching READMEs for GitHub user: {GITHUB_USERNAME}")

    # Check prerequisites
    check_gh_cli()
    create_output_directory()

    # Get repositories
    repositories = get_repositories()

    # Track successfully fetched READMEs
    readme_info = []

    fetched_readme_count = 0
    # Process each repository
    for repo in repositories:
        repo_name = repo["name"]
        print(f"Processing repository: {COLOR_BLUE}{repo_name}{COLOR_RESET}")

        # Fetch and save README
        readme_content = fetch_readme(repo_name)
        if readme_content:
            if save_readme(repo_name, readme_content):
                fetched_readme_count += 1 # Count only if saved successfully
                # Fetch releases and tags for the repository
                release_info = fetch_latest_release(repo_name)
                tags = fetch_tags(repo_name)

                # Add all information to the readme_info list
                readme_info.append(
                    {
                        "name": repo_name,
                        "createdAt": repo.get("createdAt", ""),
                        "updatedAt": repo.get("updatedAt", ""),
                        "isPrivate": repo.get("isPrivate", False),
                        "release": release_info,
                        "tags": tags,
                    }
                )
            # else: error saving already printed by save_readme
        # else: error fetching already printed by fetch_readme

    # Generate index and export to CSV (using readme_info which only contains successfully fetched/saved ones)
    generate_index(readme_info)
    export_to_csv(readme_info)

    # Summary
    print("\n--- Processing Complete ---")
    print(f"{INDICATOR_INFO} Found {len(repositories)} non-forked repositories")
    print(f"{INDICATOR_SUCCESS} Successfully fetched and saved {len(readme_info)} READMEs") # Use len(readme_info) for accurate count
    print(f"{INDICATOR_INFO} Files saved in: {os.path.abspath(OUTPUT_DIR)}")
    print(f"{INDICATOR_INFO} Index file: {os.path.join(os.path.abspath(OUTPUT_DIR), INDEX_FILENAME)}")
    print(f"{INDICATOR_INFO} CSV file: {os.path.join(os.path.abspath(OUTPUT_DIR), CSV_FILENAME)}")


if __name__ == "__main__":
    main()
