# MkDocs Template

[![docs-build](https://github.com/CelloCommunications/mkdocs-template-enterprise/actions/workflows/docs-build.yml/badge.svg)](https://github.com/CelloCommunications/mkdocs-template-enterprise/actions/workflows/docs-build.yml) [![docs-sync](https://github.com/CelloCommunications/mkdocs-template-enterprise/actions/workflows/docs-sync.yml/badge.svg)](https://github.com/CelloCommunications/mkdocs-template-enterprise/actions/workflows/docs-sync.yml)

> [!IMPORTANT]
> Pleased note this repository is a template for creating a new repository.
> It is not intended to be used directly. Please dont dump random content here as it will be overwritten.
> While working on our KB refactor this template is used for work in progress and testing.

---

> [!CAUTION]
> Also this repo must be public just for now so be careful what is added to it!

[[toc]]

## Default Deployment Location

View doc output here:

```txt
https://<username>.github.io/<repository-name>
```

<https://cellocommunications.github.io/mkdocs-template-enterprise/>

## Private Pages Configuration

Configure GitHub Pages for private access, restricting it to organization members only.

[privacy](notes/notes-privacy.md)

## Workflow Concepts

Workflow concepts for managing documentation with GitHub Pages with more advanced features.

[workflows](notes/notes-workflows.md)

## CoPilot Instructions

Your Copilot preferences are set via concise plain language instructions here.

[copilot](.github/copilot-instructions.md)

## Prerequisites

### Installing UV

Before running the documentation server, you need to install `uv` - the extremely fast Python package manager. Choose the installation method for your operating system:

#### macOS and Linux

Using the standalone installer:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Alternatively, with Homebrew:

```sh
brew install uv
```

#### Windows

Using the standalone installer:

```sh
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Alternatively, with WinGet:

```sh
winget install --id=astral-sh.uv -e
```

#### Other installation methods

You can also install with pipx (works on all platforms):

```sh
pipx install uv
```

For more installation options and detailed instructions, see the [official documentation](https://docs.astral.sh/uv/getting-started/installation/).

## Local Development

### Running the documentation server locally

Start the MkDocs development server with a single command:

```sh
uv run mkdocs serve
```

This command:

- Creates a Python virtual environment (if it doesn't exist)
- Installs all dependencies from `pyproject.toml`
- Starts the MkDocs server in development mode

When the server is running, you can view the documentation at <http://127.0.0.1:8000/>
