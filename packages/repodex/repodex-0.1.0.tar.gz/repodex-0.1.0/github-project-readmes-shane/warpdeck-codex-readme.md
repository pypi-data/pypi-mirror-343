# WarpDeck Codex: Platform Investigation & Rebuild

## Objective

This project involves investigating the original Upstash Context7 platform components and building **WarpDeck Codex**, an open-source replacement for its core functionality (API server and Vector DB). The primary goal is to create a self-hostable platform for providing real-time documentation context to AI agents and developers within the WarpDeck ecosystem.

A secondary, long-term goal is to refactor the platform's identity, replacing "Upstash" and "Context7" references with "WarpDeck" throughout the codebase and documentation.

## Project Status

- **Current Phase:** Initial Implementation (API Server Build)
- **Status:** Planning and housekeeping complete. Ready to begin building the `warpdeck-codex-api` server.

## Memory Bank

Detailed context, decisions, and ongoing progress are tracked within the `memory-bank/` directory. Key documents include:

- `projectBrief.md`: Overall goals and scope.
- `productContext.md`: The "why" behind the project.
- `systemPatterns.md`: High-level architecture.
- `techContext.md`: Technology stack details.
- `activeContext.md`: Current focus and recent decisions.
- `progress.md`: Build progress and blockers.

## Current Understanding of the Workflow

Based on analysis of the `upstash/context7`, `upstash/context7-legacy`, `upstash/docs2vector`, and `upstash/vector-js` repositories, along with the `https://context7.com` website, the target workflow is as follows (visualized in `docs/warpdeck-codex-workflow.md`, with detailed plans in `docs/plans/api-server-plan.md` and `docs/plans/vector-db-plan.md`):

1. **Data Processing (`upstash/docs2vector`):**

   - Clones documentation from a specified GitHub repository.
   - Parses Markdown (`.md`, `.mdx`) files.
   - Chunks the text content using LangChain.
   - Generates vector embeddings (optionally using OpenAI, otherwise Upstash's service).
   - Stores text chunks, embeddings, and metadata in an Upstash Vector database, organized by namespace.

2. **Context Retrieval:**
   - A client (like the `context7` MCP server) sends a request to the API server (`https://context7.com/api`).
   - The API server receives the request (e.g., for a specific library ID and topic).
   - It queries the Upstash Vector database using the `@upstash/vector` SDK (likely using the `query` method with vector similarity search for topics).
   - The API server retrieves relevant text chunks and metadata from the database.
   - It formats the retrieved chunks into a single string context, respecting token limits.
   - The API server returns the formatted context to the client.

## Identified Components

- **`context7` (MCP Client):** The `@upstash/context7-mcp` package. User-facing client for MCP environments. (Repo: `upstash/context7`, Cloned: `components/context7/`)
- **`docs2vector` (Data Processor):** Tool for processing docs and populating the vector DB. (Repo: `upstash/docs2vector`, Cloned: `components/docs2vector/`)
- **`vector-js` (Vector DB SDK):** The `@upstash/vector` package used for DB interaction. (Repo: `upstash/vector-js`, Cloned: `components/vector-js/`)
- **`context7-legacy`:** Contains legacy configurations and potentially older code/ideas. (Repo: `upstash/context7-legacy`, Cloned: `components/context7-legacy/`)
- **Upstash Vector Database:** The cloud service storing the processed data. (External Service - _Initial Target_)
- **Qdrant:** Open-source vector database. (Self-Hosted - _Long-Term Target_)
- **Embedding Services:** Pluggable services (e.g., OpenAI API, Google Gemini API, Anthropic API). (External Services)
- **`context7.com/api` (API Server):** **[Missing Public Component]** The intermediary server connecting the MCP client and the Vector DB. Appears to be private/closed-source. This is the primary component we aim to rebuild.

## Documentation

- **Workflow Diagram:** `docs/warpdeck-codex-workflow.md`
- **API Server Plan:** `docs/plans/api-server-plan.md`
- **Vector DB Plan:** `docs/plans/vector-db-plan.md`

## Next Steps

1. **Build API Server:** Implement the replacement API server based on the plan outlined in `docs/plans/api-server-plan.md`, using Next.js and initially targeting the Upstash Vector database via a DAL.
2. **Modify `docs2vector`:** Update the `docs2vector` tool (in `components/docs2vector/`) to store the `embeddingModel` identifier in the metadata when upserting to the vector database, as detailed in the plans.
3. **(Future) Migrate to Qdrant:** Implement the Qdrant DAL in the API server and update `docs2vector` to use the Qdrant client, following the plan in `docs/plans/vector-db-plan.md`.
4. **(Future) Refactor Namespace:** Rename components, packages, and references from "Upstash"/"Context7" to "WarpDeck" across the platform.
