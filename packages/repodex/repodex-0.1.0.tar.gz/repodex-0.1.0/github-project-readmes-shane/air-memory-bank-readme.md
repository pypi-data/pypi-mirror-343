# The AIR System: AI-Agnostic Ruleset & Memory Bank

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

> **Give your AI assistant a persistent, structured memory and a standardized operational protocol.**

## The Problem: AI Assistants Keep Forgetting

Every developer who works with AI assistants faces the same frustration: **your AI helper forgets everything between sessions**. You spend time explaining your project, walking through architecture decisions, and establishing conventions - only to have that context disappear when you close your editor or start a new chat.

This fundamental limitation of Large Language Models (LLMs) creates several challenges:

- **Lost Context**: Every new session starts from scratch.
- **Repeated Explanations**: You constantly re-explain your project basics.
- **Inconsistent Implementations**: Solutions vary as context is lost and operational rules aren't consistently followed.
- **Documentation Drift**: Project knowledge exists only in your head or scattered conversations.

## Our Solution: The AIR System (AI Ruleset)

The AIR System provides a **structured external memory** (`memory-bank/`) and a **standardized operational ruleset** (`.air` file and `.air/rules/` documentation) for AI assistants.

**Key Concepts:**

1. **Portability:** AIR is designed as an AI-agnostic standard. The goal is for any sufficiently capable AI assistant to be *configured* to use it.
2. **External Memory:** A `memory-bank/` directory holds structured Markdown files containing persistent project context (brief, product context, system patterns, tech stack, progress, active work).
3. **Project Intelligence:** A root `.air` file captures project-specific patterns, user preferences, and learned insights, evolving over time.
4. **Operational Protocols:** The `.air/rules/` directory documents standardized procedures for workflow, command execution, documentation, creative phases, verification, etc.
5. **AI Configuration:** The user configures their specific AI assistant (via System Prompt, custom instructions, etc.) to **load, understand, and adhere to** the context and protocols defined within the AIR System files.

This approach avoids overwhelming the LLM with massive context dumps by strategically organizing information and defining clear operational procedures.

![Memory Bank System](./images/memory-bank-diagram.png)
*(Diagram shows core memory bank structure)*

## How It Works: Standardized Context & Protocols

The AIR System addresses AI limitations through:

### 1. Structured Documentation as Memory (`memory-bank/`)

A network of specialized documentation files serves as the AI's long-term project memory:

```tree
memory-bank/
├── projectBrief.md      # What we're building
├── productContext.md    # Why we're building it
├── activeContext.md     # What we're working on now
├── systemPatterns.md    # How we've designed it
├── techContext.md       # What technologies we're using
├── progress.md          # What we've completed
└── tasks.md             # What we're tracking (single source of truth)
```

*(An AI configured for AIR reads these files at the start of each task):*

### 2. Project Intelligence File (`.air`)

A root-level `.air` file acts as a learning journal for the project, capturing:

- Project-specific coding patterns and conventions.
- User workflow preferences.
- Known challenges and workarounds.
- Evolution of project decisions.

*(A configured AI consults and potentially updates this file):*

### 3. Documented Operational Protocols (`.air/rules/`)

Detailed Markdown files document standard procedures for:

- **Adaptive Workflow:** Scaling process based on task complexity (Levels 1-4).
- **Command Execution:** Running commands safely (one at a time) and documenting results.
- **Creative Phases:** Structured thinking for complex design decisions (inspired by Anthropic's "Think Tool").
- **Task Tracking:** Using `tasks.md` as the single source of truth.
- **Verification & Checkpoints:** Ensuring process steps are completed correctly.
- **Archiving & Cross-Linking:** Maintaining a history of completed work.

*(A configured AI references these documents to guide its actions):*

### 4. AI Assistant Configuration (User Task)

The key to making AIR work is instructing your chosen AI assistant to use it. This typically involves modifying the AI's System Prompt or custom instructions to:

- **Mandate Reading:** Instruct the AI to *always* read all `memory-bank/` files and the `.air` file at the start of any task.
- **Adhere to Protocols:** Instruct the AI to follow the workflows, command safety rules, documentation practices, etc., as defined in the `.air/rules/` documentation.
- **Utilize Tools:** Ensure the AI uses its available tools (file reading/writing, command execution) appropriately according to the protocols.

*(See `docs/INSTALLATION.md` for more detailed guidance on configuration.)*

## The Benefits: A Consistent, Context-Aware AI Partner

By implementing and configuring an AI assistant to use the AIR System, you gain:

- **Session Persistence**: Critical context is retained between sessions via the Memory Bank.
- **Standardized Workflow**: Ensures consistent, reliable processes tailored to task complexity.
- **Self-Documenting Projects**: Documentation is integrated into the workflow.
- **Improved AI Reliability**: Clear protocols reduce inconsistent or unsafe AI behavior.
- **Reduced Cognitive Load**: Stop repeating project basics and focus on building.
- **Better Design Decisions**: Enforced creative phases promote thorough design thinking.
- **Portability (Goal):** Aims for a standard that future AI assistants and IDEs could potentially support more natively.

## Getting Started: Installation & Configuration

Setting up the AIR System involves two main parts: setting up the file structure and configuring your AI assistant.

1. **Set up AIR File Structure:**
    - Clone this repository or copy the `memory-bank/`, `.air` (file), and `.air/rules/` directories into your project root.
    - Ensure the core Memory Bank files exist (or configure your AI to create them based on templates in `.air/rules/templates/`).
    - Create the `docs/archive/` directory for completed tasks.
2. **Populate Initial Context:** Fill in the core `memory-bank/` files (`projectBrief.md`, `techContext.md`, etc.) with your project's specific details.
3. **Configure Your AI Assistant:**
    - Modify your AI assistant's primary configuration (System Prompt, custom instructions file, etc.).
    - Instruct it to **always read** `memory-bank/*` and `.air` at the start of tasks.
    - Instruct it to **follow the protocols** documented in `.air/rules/*` (e.g., adaptive workflow, command safety, task tracking via `tasks.md`, reflection, archiving).
    - *(Refer to `docs/INSTALLATION.md` for more detailed configuration guidance).*
4. **Initialize & Test:** Give your configured AI a simple task and verify it follows the expected initialization process (reading files, determining complexity) and workflow.

## Detailed Documentation

For more detailed information about the AIR System:

- [Complete Architecture](./docs/architecture.md) - Comprehensive technical details and principles.
- [Optimization Journey](./docs/optimization-journey.md) - How the system evolved.
- [Rule Protocols](./.air/rules/) - Detailed documentation for specific protocols (workflow, commands, creative phases, etc.).

---

*(Note: The Technical Documentation section previously here contained Cursor-specific implementation details and has been removed or integrated into `docs/architecture.md`)*.
