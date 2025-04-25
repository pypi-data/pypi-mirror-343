# GitHub Workflow Management Tools

A command-line utility for managing GitHub Actions and workflows across repositories.

## Usage

```bash
./gh-workflow-tools.sh COMMAND [OPTIONS]
```

### Commands

- `delete-fails` - Delete all failed workflow runs
- `disable-workflows` - Disable individual workflows
- `disable-actions` - Disable GitHub Actions at repository level
- `enable-actions` - Enable GitHub Actions at repository level

### Options

- `--repo REPO_NAME` - Specify a repository (default: all repos)
- `--limit NUMBER` - Limit number of repositories (default: 1300)
- `--help` - Show help message

### Examples

```bash
# Delete all failed workflow runs
./gh-workflow-tools.sh delete-fails

# Disable all workflows in a specific repository
./gh-workflow-tools.sh disable-workflows --repo my-repo

# Disable GitHub Actions for all repositories
./gh-workflow-tools.sh disable-actions

# Enable GitHub Actions for a specific repository
./gh-workflow-tools.sh enable-actions --repo my-repo

# Process only the first 50 repositories
./gh-workflow-tools.sh delete-fails --limit 50
```

## Requirements

- GitHub CLI (`gh`) installed and authenticated
- Bash shell environment
- Appropriate GitHub permissions

## Features

- Color-coded output with text-based status indicators ([PASS], [FAIL], [INFO])
- Progress reporting for operations across multiple repositories
- Error handling for failed API calls
- Safe handling of repository names with proper owner verification

## Setup

1. Make sure the script is executable:

    ```bash
    chmod +x gh-workflow-tools.sh
    ```

2. Authenticate with GitHub if not already done:

    ```bash
    gh auth login
    ```

## Future Development

For details on planned future enhancements focused on mass repository management with non-destructive operations, see the [Future Ideas Document](gh-workflow-tools-future-ideas.md). This document includes:

- Validated GitHub CLI commands for working with workflow data
- Detailed implementations for analyzing workflows across repositories
- Ideas for monitoring, reporting, and optimization features
- All proposed features are read-only and will not modify repository content
