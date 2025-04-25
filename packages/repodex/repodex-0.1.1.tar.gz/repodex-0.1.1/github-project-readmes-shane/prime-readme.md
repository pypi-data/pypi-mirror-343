# Prime

A CLI host application that enables Large Language Models (LLMs) to interact with external tools through the Model Context Protocol (MCP). Named with a nod to Star Trek's guiding principles, Prime functions as a universal interface between AI models and their tools. Currently supports Claude 3.5 Sonnet, OpenAI, and Ollama models.

## Installation

```bash
go install github.com/shaneholloman/prime@latest

# run the application
prime --help
```

## Overview

Prime acts as a host in the MCP client-server architecture, where:

- **Hosts** (like Prime) are LLM applications that manage connections and interactions
- **Clients** maintain 1:1 connections with MCP servers
- **Servers** provide context, tools, and capabilities to the LLMs

This architecture allows language models to:

- Access external tools and data sources
- Maintain consistent context across interactions
- Execute commands and retrieve information safely

Current model support:

- Claude 3.5 Sonnet (claude-3-5-sonnet-20240620)
- OpenAI GPT-4 and compatible models
- Ollama-compatible models with function calling support

## Core Capabilities

- Interactive conversations with Claude, OpenAI, and Ollama models
- Support for multiple concurrent MCP servers
- Dynamic tool discovery and integration
- Tool calling capabilities for both model types
- Configurable MCP server locations and arguments
- Consistent command interface across model types
- Configurable message history window for context management

## Technical Requirements

- Go 1.23 or later
- For Claude: An Anthropic API key
- For OpenAI: An OpenAI API key
- For Ollama: Local Ollama installation with desired models
- One or more MCP-compatible tool servers

## Environment Configuration

1. API Authentication:

    ```bash
    # For Claude
    export ANTHROPIC_API_KEY='your-anthropic-key'

    # For OpenAI
    export OPENAI_API_KEY='your-openai-key'
    ```

2. API Endpoints (Optional):
    - Custom Anthropic API endpoint: Use `--anthropic-url` flag
    - Custom OpenAI API endpoint: Use `--openai-url` flag

3. Ollama Setup:
    - Install from <https://ollama.ai>
    - Pull your desired model:

    ```bash
    ollama pull mistral
    ```

    - Ensure Ollama is running:

    ```bash
    ollama serve
    ```

## Configuration

Prime will automatically create a configuration file at `~/.mcp.json` if it doesn't exist. You can also specify a custom location using the `--config` flag:

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uvx",
      "args": [
        "mcp-server-sqlite",
        "--db-path",
        "/tmp/foo.db"
      ]
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/tmp"
      ]
    }
  }
}
```

Each MCP server entry requires:

- `command`: The command to run (e.g., `uvx`, `npx`)
- `args`: Array of arguments for the command:
  - For SQLite server: `mcp-server-sqlite` with database path
  - For filesystem server: `@modelcontextprotocol/server-filesystem` with directory path

## Usage

Prime is a CLI tool that allows you to interact with various AI models through a unified interface. It supports various tools through MCP servers and provides streaming responses.

### Available Models

Models can be specified using the `--model` (`-m`) flag:

- Anthropic Claude (default): `anthropic:claude-3-5-sonnet-latest`
- OpenAI: `openai:gpt-4`
- Ollama models: `ollama:modelname`

### Examples

```bash
# Use Ollama with Qwen model
prime -m ollama:qwen2.5:3b

# Use OpenAI's GPT-4
prime -m openai:gpt-4
```

### Command Line Flags

- `--anthropic-url string`: Base URL for Anthropic API (defaults to api.anthropic.com)
- `--anthropic-api-key string`: Anthropic API key (can also be set via ANTHROPIC_API_KEY environment variable)
- `--config string`: Config file location (default is $HOME/mcp.json)
- `--debug`: Enable debug logging
- `--message-window int`: Number of messages to keep in context (default: 10)
- `-m, --model string`: Model to use (format: provider:model) (default "anthropic:claude-3-5-sonnet-latest")
- `--openai-url string`: Base URL for OpenAI API (defaults to api.openai.com)
- `--openai-api-key string`: OpenAI API key (can also be set via OPENAI_API_KEY environment variable)

### Interactive Commands

While chatting, you can use:

- `/help`: Show available commands
- `/tools`: List all available tools
- `/servers`: List configured MCP servers
- `/history`: Display conversation history
- `/quit`: Exit the application
- `Ctrl+C`: Exit at any time

### Global Flags

- `--config`: Specify custom config file location
- `--message-window`: Set number of messages to keep in context (default: 10)

## MCP Server Compatibility

Prime can work with any MCP-compliant server. For examples and reference implementations, see the [MCP Servers Repository](https://github.com/modelcontextprotocol/servers).

## Contributing

Contributions are welcome! Feel free to:

- Submit bug reports or feature requests through issues
- Create pull requests for improvements
- Share your custom MCP servers
- Improve documentation

Please ensure your contributions follow good coding practices and include appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Anthropic: Claude development and MCP specification
- Ollama: Local model runtime implementation
- Community contributors
