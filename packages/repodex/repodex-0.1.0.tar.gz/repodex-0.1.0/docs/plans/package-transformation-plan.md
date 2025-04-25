# RepoDex Transformation Plan

This document outlines the plan to transform RepoDex from a personal tool into a flexible, configurable application that anyone can use with their own GitHub accounts and organizations.

## Configuration System

1. **YAML Configuration File**:
    - Create a `.repodex.yml` configuration file that can be:
        - Project-based (in the current directory)
        - User-based (in the user's home directory)
        - System-wide (in a global config location)
    - Support cascading configuration with local overriding global

2. **Authentication Fallbacks**:
    - Use GitHub CLI authentication if available
    - Fall back to Git configuration if GitHub CLI is not authenticated
    - Prompt for GitHub username/organization if neither is available
    - Support personal access token (PAT) configuration

3. **Organization Support**:
    - Allow specifying multiple organizations in the config
    - Provide interactive prompts for organization selection when not specified

## Configuration Schema

```yaml
# .repodex.yml
github:
    username: "username"  # Optional, detected from gh CLI or git config if not specified
    organizations:        # Optional list of organizations to work with
        - name: "org1"
            # Optional org-specific settings
        - name: "org2"

repositories:
    output_dir: "github-readmes"  # Base directory for README storage
    exclude_forks: true           # Whether to exclude forked repositories
    include_private: true         # Whether to include private repositories

releases:
    initial_tag: "v0.1.0"         # Tag to use for initial releases
    auto_create: false            # Whether to automatically create releases

formatting:
    readme_filename_format: "{}-readme.md"  # Format for saved README files
    index_title: "GitHub Projects README Index"  # Title for index file
```

## CLI Improvements

1. **Command Structure**:

    ```sh
    repodex [command] [options]
    ```

    Commands:
    - `fetch` - Fetch repositories and READMEs
    - `release` - Manage releases
    - `update` - Update remote READMEs
    - `config` - Manage configuration

2. **Interactive Mode**:
    - Add a fully interactive mode with prompts for all required information
    - Support both CLI arguments and interactive prompts

## Package Structure

1. **Core Package**:

    ```tree
    repodex/
    ├── __init__.py
    ├── cli.py            # Command-line interface
    ├── config.py         # Configuration management
    ├── auth.py           # Authentication handling
    ├── github/           # GitHub API interactions
    │   ├── __init__.py
    │   ├── repos.py      # Repository operations
    │   ├── releases.py   # Release operations
    │   └── readmes.py    # README operations
    ├── utils/            # Utility functions
    │   ├── __init__.py
    │   ├── formatting.py # Output formatting
    │   └── logging.py    # Logging utilities
    └── templates/        # Template files
        └── config.yml    # Default configuration template
    ```

2. **Entry Points**:
    - Main CLI entry point
    - Potential for library usage

## Implementation Plan

1. **Phase 1: Configuration System**
    - Implement YAML configuration loading/saving
    - Create authentication fallback chain
    - Add interactive prompts for missing configuration

2. **Phase 2: Refactor Existing Scripts**
    - Convert current scripts to use the new configuration system
    - Modularize functionality into proper Python modules
    - Maintain backward compatibility

3. **Phase 3: CLI Improvements**
    - Implement command structure
    - Add argument parsing with help text
    - Create interactive mode

4. **Phase 4: Packaging**
    - Create proper Python package structure
    - Add setup.py/pyproject.toml
    - Publish to PyPI

## Additional Features to Consider

1. **Template System**:
    - Allow customizing the format of generated index files
    - Support different output formats (Markdown, HTML, JSON)

2. **Filtering and Searching**:
    - Advanced filtering of repositories by various criteria
    - Search functionality within cached READMEs

3. **Web Interface**:
    - Optional simple web UI for browsing repositories and READMEs

4. **Webhooks**:
    - Support for webhook notifications when repositories are updated
