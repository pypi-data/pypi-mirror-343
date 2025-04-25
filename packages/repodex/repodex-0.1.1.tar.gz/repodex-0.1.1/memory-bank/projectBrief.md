# Project Brief: RepoDex

## Core Goal

To create and maintain a system for fetching, indexing, organizing, and managing metadata (including READMEs and releases) for specified GitHub repositories.

## Scope

- **Repository Targets:**
    - User's personal repositories (`shaneholloman`).
    - Repositories within the `CelloCommunications` organization authored by `shaneholloman`.
- **Core Functionality:**
    - Fetch repository metadata (name, description, dates, visibility).
    - Fetch README content from target repositories.
    - Fetch release and tag information.
    - Filter repositories based on criteria (non-forked, authorship for org repos).
    - Store fetched READMEs locally in organized directories.
    - Generate index files (`README.md`, `repositories.csv`) summarizing fetched data.
    - Manage GitHub releases:
        - Create initial `v0.1.0` releases for untagged repositories.
        - Create releases corresponding to the latest semantic version tag if missing.
- **Automation:** Provide mechanisms for automated updates (e.g., via GitHub Actions).
- **Technology:** Implement tooling primarily in Python, leveraging the GitHub CLI (`gh`).

## Non-Goals (Implicit)

- Providing a web UI for browsing repositories.
- Direct interaction with Git repositories beyond what `gh` provides for metadata/releases.
- Managing repository *code* content (focus is on metadata and READMEs).
