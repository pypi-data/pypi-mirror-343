# Notebook Foundry

A learning lab and repurposing engine for running Jupyter notebooks locally using three distinct workflows. This project not only provides a systematic approach to preserve full original functionality while enabling code reuse, but also produces fully functional, reusable modules from each notebook ingestion. Each conversion step is rigorously validated to ensure quality outcomes, creating a reliable pipeline from exploratory notebooks to production-ready code.

> [!CAUTION]
> Not all workflows are fully validated yet... standby for this message to go away before using.

## Learning Progression

This project is designed as a learning lab with three distinct levels of notebook conversion mastery:

1. **Notebook-to-Notebook**: The foundation level
   - "Does it work as advertised?" - Basic functionality testing
   - Minimal changes, focused on getting things running
   - Entry point for beginners to understand dependency management and env vars

2. **Notebook-to-Package**: The intermediate level
   - "Can we systematically repurpose it?" - Structured transformation
   - Teaches software engineering principles and package design
   - Shows how to preserve original functionality while adding structure

3. **Notebook-to-Automated**: The advanced level
   - "Can we programmatically automate it?" - Full automation
   - Scripts and tools to handle the conversion process
   - The culmination where manual learning becomes automated process

This progression follows the exact pattern of mature automation development:

1. First, do it manually to understand the process
2. Then, structure it into reusable components
3. Finally, automate the whole workflow

Using a single notebook across all three approaches provides a consistent point of comparison, allowing users to directly see how the same content transforms through each stage of sophistication.

## Project Structure

This project is organized as follows:

```sh
notebook-conversions/
├── projects/                           # All notebook implementations
│   ├── anthropic-think-tool-notebook/  # Notebook-to-Notebook example
│   ├── anthropic-think-tool-package/   # Notebook-to-Package example
│   └── anthropic-think-tool-automated/ # Notebook-to-Automated example
├── workflows/                          # Detailed workflow documentation
│   ├── notebook-to-notebook-workflow.md
│   ├── notebook-to-package-workflow.md
│   └── notebook-to-automated-workflow.md
├── docs/                               # Reference documentation
│   ├── reference-uv-commands.md        # UV dependency management reference
│   └── validation-instructions.md      # Workflow validation guidelines
├── assets/                             # Asset files and resources
├── memory-bank/                        # Project documentation
├── tools/                              # Helper tools and scripts
├── README.md                           # Core documentation
└── .clinerules                         # Project rules
```

## Purpose

This project provides three well-defined workflows for adapting Jupyter notebooks (often from online sources like GitHub Gists) to run locally on your machine:

1. **Notebook-to-Notebook**: Minimal adjustments to run notebooks in their original format
2. **Notebook-to-Package**: Full conversion to structured Python packages with both complete original functionality and reusable components
3. **Notebook-to-Automated**: Automated conversion process producing the same dual implementation

All workflows address common challenges like dependency management, environment variables, and authentication that typically prevent notebooks from running locally, while ensuring complete preservation of original notebook functionality.

## Dual Implementation Philosophy

A key principle of this project is the **dual implementation approach**:

1. **One-to-One Implementation**: Preserves ALL original notebook functionality with minimal changes
   - Only modifications are for dependency management (UV/pyproject.toml) and environment variables
   - All original examples, tools, and demonstration code remain intact
   - Functionally identical to the original notebook

2. **Structured Implementation**: Refactors code for reusability (where applicable)
   - Proper Python package structure with clean, modular design
   - Reusable components that can be imported in other projects
   - Same core functionality in a more maintainable format

This approach ensures you get the best of both worlds - complete original functionality AND reusable components.

## Key Differences Between Workflows

| Feature           | [Notebook-to-Notebook](./workflows/notebook-to-notebook-workflow.md) | [Notebook-to-Package](./workflows/notebook-to-package-workflow.md) | [Notebook-to-Automated](./workflows/notebook-to-automated-workflow.md) |
| ----------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| **End Result**    | Executable .ipynb file                                               | Python package with dual implementation                             | Python package with dual implementation                                 |
| **Modifications** | Minimal (env vars, auth)                                             | Complete + structured refactoring                                   | Automated conversion with both implementations                          |
| **Interactive?**  | Yes, preserves Jupyter experience                                    | Partially (original.py) + structured modules                        | Partially (original.py) + structured modules                            |
| **Reusability**   | Limited to Jupyter                                                   | Dual approach: original + reusable modules                          | Dual approach: original + reusable modules                              |
| **Complexity**    | Simpler, fewer changes                                               | More complex, dual implementation                                   | Automated process with helper scripts                                   |
| **Execution**     | Via Jupyter notebook interface                                       | Via Python interpreter                                              | Via Python interpreter                                                  |

## Getting Started

1. **Prerequisites**:
   - Python 3.10+ installed
   - UV for dependency management (see [UV Commands](./docs/reference-uv-commands.md))

2. **Choose a workflow**:
   - For quick execution with minimal changes: [Notebook-to-Notebook Workflow](./workflows/notebook-to-notebook-workflow.md)
   - For complete functionality + reusable code: [Notebook-to-Package Workflow](./workflows/notebook-to-package-workflow.md)
   - For automated conversion process: [Notebook-to-Automated Workflow](./workflows/notebook-to-automated-workflow.md)

3. **Follow the step-by-step instructions** in the corresponding workflow document

## Workflow Documentation

- **[notebook-to-notebook-workflow.md](./workflows/notebook-to-notebook-workflow.md)**: Detailed steps for making minimal adjustments while preserving the notebook format
- **[notebook-to-package-workflow.md](./workflows/notebook-to-package-workflow.md)**: Comprehensive guide for creating dual implementation (one-to-one + structured)
- **[notebook-to-automated-workflow.md](./workflows/notebook-to-automated-workflow.md)**: Automated approach to creating dual implementation packages
- **[reference-uv-commands.md](./docs/reference-uv-commands.md)**: Reference for UV dependency management commands
- **[validation-instructions.md](./docs/validation-instructions.md)**: Guidelines for validating workflow steps

## Core Principles

### Discovery-First Approach

A core principle of this project is treating each notebook as entirely unique. We make no assumptions about content, dependencies, or structure. The discovery process must be performed fresh for every notebook.

### Complete Functionality Preservation

We ensure all original notebook functionality is preserved in our conversions. This means examples, tools, demonstrations, and features must work exactly as in the original notebook, with only minimal changes for local execution.

## Implemented Examples

We've applied these workflows to the following same notebook: One notebook, 3 workflows!

1. **[anthropic-think-tool-notebook](./projects/anthropic-think-tool-notebook/)**: Example of the Notebook-to-Notebook workflow
   - [README.md](./projects/anthropic-think-tool-notebook/README.md): Documentation of changes
   - Original source: [GitHub Gist](https://gist.github.com/shaneholloman/0606297dd31d1fd7c83f1f859481dadf)

2. **[anthropic-think-tool-package](./projects/anthropic-think-tool-package/)**: Example of the Notebook-to-Package workflow
   - Contains both one-to-one implementation and structured modules
   - [README.md](./projects/anthropic-think-tool-package/README.md): Documentation of conversion
   - Original source: Same notebook, different approach

3. **[anthropic-think-tool-automated](./projects/anthropic-think-tool-automated/)**: Example of the Notebook-to-Automated workflow
   - Automated conversion with both implementations
   - Coming soon: Implementation of the automated workflow approach

## Project Rules

All development follows strict rules documented in [.clinerules](./.clinerules), including:

- Python 3.10+ required
- UV-only dependency management
- No pip-related commands
- pyproject.toml for all dependencies
- Consistent naming conventions

## Memory Bank

Project documentation is maintained in the Memory Bank:

- **[projectBrief.md](./memory-bank/projectBrief.md)**: Project overview and goals
- **[productContext.md](./memory-bank/productContext.md)**: Product purpose and context
- **[systemPatterns.md](./memory-bank/systemPatterns.md)**: Architecture and patterns
- **[techContext.md](./memory-bank/techContext.md)**: Technologies used
- **[activeContext.md](./memory-bank/activeContext.md)**: Current work focus
- **[progress.md](./memory-bank/progress.md)**: Project status and roadmap

## Future Work

- Validation of all workflow steps
- Cross-platform compatibility testing
- Additional example conversions
- Troubleshooting guides
