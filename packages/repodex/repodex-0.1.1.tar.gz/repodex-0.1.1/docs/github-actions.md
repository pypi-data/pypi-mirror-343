# RepoDex - Automated Updates

This document explains how to set up the automated GitHub Actions workflow for updating README collections.

- [`cello-repos`](../github-project-readmes-shane/github-project-readmes-cello/README.md)
- [`shane-repos`](../github-project-readmes-shane/README.md)

## Overview

Two Python scripts collect README files from GitHub repositories:

- `github_readme_fetcher_cello.py` - Collects READMEs from Cello Communications repositories authored by you
- `github_readme_fetcher_shane.py` - Collects READMEs from your personal repositories

A GitHub Actions workflow has been set up to run these scripts monthly and update the README collections automatically.

## Setup Instructions

### 1. Create a GitHub Personal Access Token (PAT)

You need a Personal Access Token with appropriate permissions:

1. Go to GitHub → Settings → Developer settings → [Personal access tokens](https://github.com/settings/tokens) → Tokens (classic)
2. Click "Generate new token" → "Generate new token (classic)"
3. Add a note like "RepoDex"
4. Set expiration (recommended: 90+ days)
5. Select these scopes:
    - `repo` (full control of private repositories)
    - `read:org` (read organization information)
6. Click "Generate token"
7. **IMPORTANT**: Copy the token immediately - you won't see it again!

### 2. Add the PAT as a Repository Secret

Use the provided Python tool to add your PAT as a repository secret named `GH_PAT` (or as specified):

```sh
# Option 1: Run with token as argument (less secure)
python3 tools/gh_repo_setup_secret.py --token YOUR_TOKEN_HERE

# Option 2: Run without token argument and enter when prompted (more secure)
python3 tools/gh_repo_setup_secret.py

# You can also specify the repository and secret name if needed:
# python3 tools/gh_repo_setup_secret.py -R owner/repo -s SECRET_NAME
```

This tool securely prompts for the token if not provided via the `--token` argument.

### 3. GitHub Actions Workflow

The workflow is configured to:

- Run automatically on the 1st of each month
- Be triggered manually when needed
- Update both README collections
- Commit and push any changes back to the repository

To manually trigger the workflow:

1. Go to the "Actions" tab in your repository
2. Select the "Update GitHub README Collections" workflow
3. Click "Run workflow" on the main branch

## Troubleshooting

If the workflow fails:

1. Check the GitHub Actions logs for error messages
2. Verify your PAT has the correct permissions and hasn't expired
3. Ensure the GitHub CLI authentication step is successful
4. Check if there are any issues with the Python scripts themselves

## Maintenance

- Update your PAT before it expires to ensure continuous operation
- If you change repository names or structure, update the scripts accordingly
