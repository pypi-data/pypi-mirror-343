# slurp (TypeScript Version)

`slurp` is a command-line tool, rebuilt in TypeScript, that automatically scrapes web-based documentation from a given URL, converts it into clean Markdown partials, applies standard linting fixes, and optionally compiles these partials into a single file. It's designed to provide structured documentation suitable for AI consumption.

## Features

-   **Modular TypeScript Architecture**: Core logic (fetching, parsing, converting, linting, saving) is separated into distinct modules under `src/scraper/`.
-   **Direct URL Scraping**: Fetches content directly from a starting URL (`slurp <url>`).
-   **Targeted Fetching**: Fetches content and saves partials without immediate compilation (`slurp fetch <url> [version]`).
-   **Markdown Conversion**: Transforms HTML documentation into clean, structured markdown using Turndown and the GFM plugin (for tables, etc.).
-   **Standard Linting**: Applies `markdownlint` fixes based on `.markdownlint.jsonc` configuration.
-   **Compilation**: Combines scraped partials into a single output file (`slurp compile [options]`).
-   **Configurable**: Options can be set via a `.env` file or command-line flags.
-   **Asynchronous**: Uses `p-queue` for managing concurrent scraping tasks.

## Installation

```sh
# Clone the repository (replace with actual URL)
# git clone https://github.com/yourusername/slurp.git
cd slurp

# Install dependencies
npm install

# Build the TypeScript code
npm run build # (Requires a 'build' script in package.json, e.g., "build": "tsc")

# Link the command for global access (optional)
# This typically links the compiled JS entry point specified in package.json's "bin" field
npm link

# Copy and configure environment variables
cp .env.example .env
# Edit .env to customize settings (see Configuration below)
```

## Usage

After building (`npm run build`), you can run `slurp` using Node.js directly on the compiled output (`dist/cli.js`) or via `npm run` if you add a script to `package.json`. If linked globally, you might be able to use `slurp` directly.

**1. Direct URL Mode (Scrape & Compile)**

This is the simplest way to get a single compiled document. It scrapes, saves partials temporarily, compiles them, and then deletes the partials (by default).

```sh
node dist/cli.js https://example.com/docs/v1/
# or (if npm script "slurp" is configured like "slurp": "node dist/cli.js")
npm run slurp -- https://example.com/docs/v1/
```

**2. Fetch Mode (Scrape Only)**

This scrapes the content and saves the individual Markdown partials to the output directory (default: `slurp_partials/<site_name>/[version]/`).

```sh
node dist/cli.js fetch https://example.com/docs/v1/ 1.0.0
# or
npm run slurp -- fetch https://example.com/docs/v1/ 1.0.0
```
*   The `[version]` argument is optional but recommended for organizing different documentation versions.

**3. Compile Mode**

This compiles existing Markdown partials from a specified directory into a single file.

```sh
# Compile specific directory
node dist/cli.js compile --input ./slurp_partials/example/1.0.0 --output ./compiled/example_v1.md
# or
npm run slurp -- compile --input ./slurp_partials/example/1.0.0 --output ./compiled/example_v1.md

# Compile using default/env directories
node dist/cli.js compile
# or
npm run slurp -- compile
```

## Configuration

Customize behavior via a `.env` file (copy `.env.example`). Key options:

| Variable                      | Default                        | Description                                                              |
| :---------------------------- | :----------------------------- | :----------------------------------------------------------------------- |
| `SLURP_PARTIALS_DIR`          | `slurp_partials`               | Root directory for intermediate scraped markdown files                   |
| `SLURP_COMPILED_DIR`          | `compiled`                     | Output directory for the final compiled markdown file                    |
| `SLURP_MAX_PAGES_PER_SITE`    | `0` (unlimited)                | Maximum pages to scrape per site                                         |
| `SLURP_CONCURRENCY`           | `10`                           | Number of pages to process concurrently                                  |
| `SLURP_USE_HEADLESS`          | `true`                         | Use headless browser (Puppeteer) for JS-rendered content                 |
| `SLURP_ENFORCE_BASE_PATH`     | `true`                         | Only follow links containing the base path of the starting URL           |
| `SLURP_PRESERVE_QUERY_PARAMS` | (See defaults in code)         | Comma-separated list of query params to keep in URLs                     |
| `SLURP_DELETE_PARTIALS`       | `true`                         | Delete partials directory after successful compilation (in direct URL mode or via compile command) |
| `SLURP_DEBUG`                 | `false`                        | Enable detailed debug logging                                            |
| `SLURP_TIMEOUT`               | `60000` (ms)                   | Network timeout for fetching pages                                       |
| `SLURP_PRESERVE_METADATA`     | `true`                         | Keep YAML frontmatter during compilation                                 |
| `SLURP_REMOVE_NAVIGATION`     | `true`                         | Attempt to remove common nav elements during compilation                 |
| `SLURP_REMOVE_DUPLICATES`     | `true`                         | Remove duplicate content sections during compilation                     |

Command-line flags (e.g., `--max 50`, `--output ./my_partials`) override `.env` variables.

## Development

1.  **Install Dependencies:** `npm install`
2.  **Build:** `npm run build` (Compiles TypeScript to JavaScript in `dist/`)
3.  **Run:** `node dist/cli.js <command> [args]`

## License

ISC
