# `HealthBridge` - A Personal Health Tracking System

TODO: Consider renaming project to 'LifeSync' or 'LifeBridge'

## Overview

> HealthBridge is a private, patient-centric health tracking system designed for the New Zealand healthcare context. The system enables detailed health tracking through daily diary entries and supplemental notes, with future capabilities for doctor integration.

## Core Features

- Daily health diary system
- Supplemental health note tracking
- Comprehensive health tagging system
- Multi-language support (Spanish/English)
- NZ healthcare standards compliance preparation

## Project Structure

```txt
healthbridge/
├── .git/                          # Git repository data
├── .history/                      # File change history
├── docs/                          # Project documentation
│   ├── database/                  # Database documentation
│   ├── design/                    # Design decisions and diagrams
│   ├── project/                   # Project context and guidelines
│   ├── technical/                 # Technical specifications
│   └── user/                      # User instructions and guides
├── DEVOPS_GUIDE.md                # Operational guide for Claude
├── PROJECT_STATUS.md              # Current project status tracking
├── README.md                      # Project overview
├── healthbridge.db                # SQLite database
└── healthbridge-diary-prompt.xml  # System behavior configuration
```

## Technical Stack

- SQLite database
- Protected Health Information (PHI) handling
- NZ healthcare identifiers support (NHI, ACC)
- Tag-based health tracking system
- Anthropic Claude desktop App integration
- NOTE: consider pydantic for data validation!

## Database Schema

### Core Tables

> Implemented so far:

- users
- diary_entries
- supplemental_notes
- tags
- entry_tags

### Extended Schema

> Planned for future development:

- user_extended_profile
- user_contact_info
- healthcare_identifiers
- insurance_providers
- user_insurance

## Development Status

- Base implementation complete
- Extended user profiles to be check for and possibly added
- Ready for test data validation
- Prepared for diary entry examination

## Installation and Setup

> *Private project - setup instructions maintained internally*

## Usage Guidelines

> *Private project - usage guidelines maintained internally*

## Security Notice

This is a private project handling sensitive health information. All development and usage must follow appropriate PHI handling procedures and NZ healthcare data standards.

## Compliance Preparation

- Health Information Privacy Code (HIPC) 2020
- Health and Disability Commissioner (HDC) Code
- NZ Health Information Standards Organisation (HISO) guidelines
- NZ Health Information Governance Guidelines

## Future Development

- Doctor integration system
- Clinical data synchronization
- Medical professional interface
- Enhanced consultation support

## Project Status

Currently in active development with focus on:

1. Validating schema against real usage
2. Refining data structures
3. Implementing healthcare standard compliance
4. Preparing for future doctor integration

---

**Private Project Notice:** This project is private and contains sensitive health information. Not for public distribution or use.
