# GitHub README Fetcher

[![Update GitHub README Collections](https://github.com/shaneholloman/github-readme-fetcher/actions/workflows/update_github_readmes.yml/badge.svg)](https://github.com/shaneholloman/github-readme-fetcher/actions/workflows/update_github_readmes.yml)

Tools for fetching READMEs from GitHub repositories and generating a searchable index.

- [`cello-repos`](./github-project-readmes-cello/README.md)
- [`shane-repos`](./github-project-readmes-shane/README.md)

## Scripts

This repository contains several Python scripts for managing repository information:

**README Fetching & Indexing:**

- `gh_repo_fetch_index_shane.py`: Fetches READMEs from your personal GitHub repositories (public and private, excluding forks) and generates an index file (`github-project-readmes-shane/README.md`) with repository metadata and statistics.
- `gh_repo_fetch_index_cello.py`: Fetches READMEs from the `CelloCommunications` organization repositories authored by you (based on the first commit) and generates a similar index file (`github-project-readmes-cello/README.md`).

**Release Management (for personal repos):**

- `gh_repo_release_latest_shane.py`: Reads `github-project-readmes-shane/repositories.csv`, finds the latest semantic version tag for each personal repository, and creates a GitHub Release with auto-generated notes if one doesn't already exist for that tag.
- `gh_repo_release_initial_shane.py`: Reads `github-project-readmes-shane/repositories.csv` and creates an initial `v0.1.0` tag and release for any personal repository that currently has no tags.
- `gh_repo_release_latest_cello.py`: Fetches repositories authored by you in the `CelloCommunications` org, finds the latest semantic version tag for each, and creates a GitHub Release with auto-generated notes if one doesn't already exist. Includes a `--dry-run` option.
- `gh_repo_release_initial_cello.py`: Fetches repositories authored by you in the `CelloCommunications` org and creates an initial `v0.1.0` tag and release for any that currently have no tags. Includes a `--dry-run` option.

**Utility Shell Scripts:**

- `scripts/find_authored_repos.sh`: A shell script showing how to find repos authored by a specific user using GraphQL.
- `scripts/find_all_authored_repos.sh`: An enhanced version with pagination and detailed output formatting.

## Features

- Fetches READMEs from GitHub repositories
- Filters by authorship (first commit author)
- Generates a Markdown index with links to all fetched READMEs
- Includes creation and update dates for each repository

## Performance Optimization

A significant optimization has been implemented using GitHub's GraphQL API to reduce API calls and improve efficiency. See [optimization.md](docs/optimization.md) for details on:

- The original vs. optimized approach
- Technical implementation with GraphQL
- Performance benefits
- Implementation considerations

## Development Approach

### Terminal Testing First

**IMPORTANT:** Before implementing any scripting solution, ALWAYS test your approach directly in the terminal first. This principle was critical to discovering the GraphQL optimization in this project.

For example, before implementing the GraphQL solution in Python:

1. Basic GraphQL query was tested directly with GitHub CLI:

   ```bash
   gh api graphql -f query='query { organization(login: "CelloCommunications") { ... } }'
   ```

2. Once the query worked, it was refined interactively:

   ```bash
   gh api graphql -f query='...' | jq '.data.organization.repositories.nodes[] | select(...)'
   ```

3. Only after confirming the approach worked in the terminal was it implemented in Python.

This terminal-first approach allows you to:

- Verify API responses without writing complex code
- Iterate quickly on query structure
- Identify potential issues early
- Understand exactly what data you're working with

### Usage

Clone this repository:

```bash
git clone https://github.com/shaneholloman/github-readme-fetcher.git
cd github-readme-fetcher
```

Run the desired script from the `tools/` directory:

```bash
# Fetch/Index personal READMEs
python3 tools/gh_repo_fetch_index_shane.py

# Fetch/Index Cello READMEs authored by you
python3 tools/gh_repo_fetch_index_cello.py

# Create releases for latest tags on personal repos (if missing)
python3 tools/gh_repo_release_latest_shane.py

# Create initial v0.1.0 release for untagged personal repos
python3 tools/gh_repo_release_initial_shane.py

# Create latest releases for Cello repos (Dry Run)
python3 tools/gh_repo_release_latest_cello.py --dry-run

# Create initial v0.1.0 release for untagged Cello repos (Dry Run)
python3 tools/gh_repo_release_initial_cello.py --dry-run
```

The fetcher scripts will:

1. Fetch repositories from GitHub
2. Filter by authorship (for the Cello script)
3. Download READMEs from each repository
4. Generate an index file with links to all fetched READMEs

## Requirements

- Python 3.8+ (due to type hints like `|`)
- GitHub CLI (gh) installed and authenticated
- `packaging` library for Python (`pip install packaging`) for release scripts
- Optional: jq (for shell scripts)

## Output

The scripts will create subdirectories with fetched READMEs and an index file:

- `github-project-readmes-shane/`: For personal repositories
- `github-project-readmes-cello/`: For organization repositories

Each directory contains:

- Individual README files renamed according to repository
- An `index.md` file with links to all READMEs and metadata

## License

MIT
