# Tech Context: RepoDex

## Core Technologies

1. **Python:** The primary language for all tooling (`tools/` directory).
    - **Version:** Requires Python 3.10+ (as defined in `pyproject.toml`). This is necessary for modern type hint syntax (`|`) used in some scripts.
    - **Standard Libraries:** Uses `subprocess`, `os`, `sys`, `json`, `csv`, `base64`, `argparse`, `pathlib`, `getpass`, `typing`.
2. **GitHub CLI (`gh`):** Used extensively via `subprocess` calls for interacting with the GitHub API (REST and GraphQL), managing releases, and handling secrets. Assumed to be installed and authenticated in the execution environment.
3. **GitHub API:** The underlying API accessed via the `gh` CLI. Both REST and GraphQL endpoints are used.
    - REST API used for fetching repo contents (READMEs, tags), user repos, creating/viewing releases, setting secrets.
    - GraphQL API used for optimized fetching of organization repositories with authorship information.
4. **Markdown:** Used for documentation (`README.md`, `docs/`, `memory-bank/`) and generated index files. Specific linting rules apply (see `.clinerules`).
5. **TOML:** Used for project configuration (`pyproject.toml`) to define Python version requirements and project metadata.
6. **Shell (Bash):** Previously used for scripting (`scripts/` directory), but now deprecated and removed in favor of Python tools.
7. **GitHub Actions:** Used for automating the execution of the `gh_repo_fetch_index_*.py` scripts for scheduled updates.

## External Libraries/Dependencies

1. **`packaging` (Python):** Required by `gh_repo_release_latest_*.py` scripts for parsing and comparing semantic version tags. Needs to be installed (`pip install packaging`).

## Development Environment & Tooling

1. **Ruff:** Used for Python linting and formatting, configured via `.clinerules` (eventually potentially `pyproject.toml`). Enforces PEP 8, line length, import order, etc., targeting Python 3.10.
2. **Mypy:** Used for static type checking (implicitly, as errors were reported). Project now targets Python 3.10, resolving previous type hint syntax issues.
3. **Git & GitHub:** Essential for version control and hosting.
4. **Text Editor/IDE:** (e.g., VS Code) for development.

## Technical Constraints

1. **Requires `gh` CLI:** The core functionality relies entirely on the GitHub CLI being installed and properly authenticated. The tools will fail without it.
2. **Network Access:** Requires internet connectivity to interact with the GitHub API.
3. **API Rate Limits:** While the GraphQL optimization significantly reduces API calls for the Cello use case, GitHub's API rate limits still apply. Extremely large numbers of repositories could potentially hit limits, although the current implementation is efficient.
4. **PAT Security:** The GitHub Actions workflow relies on a securely stored Personal Access Token (PAT) with appropriate permissions. Token expiration requires manual updates.
