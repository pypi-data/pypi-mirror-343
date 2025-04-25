# Cello Knowledge Refactor

This repo is for discussions, tasks, requests etc regarding the Cello Knowledge Refactor project which will be replacing bookstack.

<!-- TOC -->

- [Cello Knowledge Refactor](#cello-knowledge-refactor)
  - [Proposed Site](#proposed-site)
  - [Reference](#reference)
  - [Discussions](#discussions)
  - [Issues and Requests](#issues-and-requests)
  - [GitHub Considerations](#github-considerations)
    - [GitHub Hosting](#github-hosting)
    - [GitHub Costs](#github-costs)
    - [GitHub Features](#github-features)
  - [Challenges](#challenges)
  - [Tasks](#tasks)
    - [Approval \& Review](#approval--review)
    - [Initial Demo](#initial-demo)

<!-- /TOC -->

## Proposed Site

Docs: <https://docs.cello.co.nz>

The name is up for grabs. We can change it to whatever.

The old site will forward to the new site once it's ready. Will use custom domain feature in GitHub Pages to point to new site.

## Reference

Go here for instruction [Reference](reference)

## Discussions

Go here for [Discussions](https://github.com/CelloCommunications/cello-knowledge-refactor/discussions)

## Issues and Requests

Go here for [Issues and Requests](https://github.com/CelloCommunications/cello-knowledge-refactor/issues)

## GitHub Considerations

### GitHub Hosting

Considerations for a GitHub hosted solution:

- [ ] ISO compliance discussion to be had
- [ ] 2fa Enforcement
  - Unfortunately github will kick all non 2fa users and they will need to be re-invited or make sure they have 2fa enabled before the switch
- [ ] Company wide 1password rollout
  - Not all users have a 1password account
- [ ] SSO is is only available on enterprise github
- [ ] Review current GitHub permissions, teams, owners, etc.
- [ ] Company GitHub Name Review
    - Maybe shorten to `cello.nz` or similar

### GitHub Costs

Currently **zero**,  as we use the free version.

Next step is to upgrade to team plan at $4 USD per user. See [plans](https://github.com/pricing)

### GitHub Features

- [ ] No need for a separate server (if using an enterprise GitHub account)
- [ ] GitHub edit via Gui
- [ ] GitHub Pages for hosting
- [ ] GitHub Actions for auto rebuilds
- [ ] CoPilot knowledge queries via the web gui
- [ ] Finally give engineers programmatic access to the knowledge base!

## Challenges

- [ ] Culling of old data should be done before migration
- [ ] Bookstack migrate to markdown - Bookstack export is shit and we will dont use it.
  - Is not trivial, We have a combination of methods for this
  - Is worth the effort
- [ ] Non technical staff will need to learn markdown.
  - We believe that to be doable

## Tasks

Project Tasks will be tracked in [Project Tasks](https://github.com/orgs/CelloCommunications/projects/1)

### Approval & Review

- [ ] Technical Approval for GitHub as Host
  - Assignee: @falkoweber-cello

### Initial Demo

- [ ] Bookstack to MkDocs Demo
  - Assignee: @shaneholloman
  - Components:

    ```txt
    - BookStack SmartLan Section used for demo, re: @ivanwalker request
    - Version Control System
    - Attribution & Metadata features:
      - Author/Created By
      - Creation Date
      - Last Modified Date
      - Last Modified By
      - Last Reviewed By
      - Last Review Date
      - Document Approver
    ```
