# OmniBase Project

[[toc]]

BootStrap your Claude Desktop App with this project prompt that remembers your personal context across projects. Useful for anyone that is constantly reminding Claude about your personal context and operating preferences

> [!IMPORTANT]
> This a very busy prompt. At first, it will want to write lot which could annoy some users
>
>Until such time we can auto approve Claude to write to our personal Knowledge graph we will have to manually approve Claude for each write. This is a security feature. However, `reads` can be auto-approved for the entire chat.

![alt text](img/readme-01.png)

The `project-prompt.xml` file is the core of this repository, as it defines the structure and initialization process for a Model Context Protocol (MCP) project. This prompt provides a comprehensive and extensible framework for integrating MCP capabilities into applications, ensuring a consistent and robust initialization process.

## Requirements

## Overview

The prompt outlines a three-layer architecture for MCP-enabled applications:

1. **Base Layer**: Anthropic's system prompt, which defines Claude's core behaviors and capabilities.
2. **Middle Layer**: The user's project-specific customizations, including the user prompt and associated files.
3. **Top Layer**: A persistent, structured knowledge graph that stores user context and preferences, accessible across projects.

This multi-layered approach allows for project-specific requirements while maintaining user-level context persistence and consistency.

## Features

1. **Systematic Initialization**: The prompt defines a detailed, deterministic process for initializing the MCP environment, ensuring parity between the XML structure and the knowledge graph.
2. **Context Evolution**: The prompt outlines a comprehensive set of observation directives, learning patterns, and persistence rules for maintaining and evolving the user's personal, health, dietary, and professional context.
3. **Validation Framework**: The prompt includes a robust validation system to ensure the integrity of the context evolution, pattern recognition, and service integration.
4. **Fallback Strategies**: The prompt defines graceful degradation strategies to handle service failures and maintain a basic level of operation.
5. **Subject Domain Integration**: The prompt allows for the integration of subject-specific configurations and validation rules, enabling domain-specific functionality.

## Usage

This `project-prompt.xml` file is intended to be used as a starting point for developers building MCP-enabled applications. By incorporating this prompt, developers can leverage the established architecture and initialization process, allowing them to focus on building their application-specific features and functionality.

### Inform Claude

Where your config file is located.

Set this in the prompt so Claude knows where to find your configuration file. This is important for Claude to remember your personal context across projects in case you may need Claude to help you troubleshoot any MCP initialization issues.

> [!IMPORTANT]
> MCP File Service will need path availability to read that configuration file.

```xml
        <mcp-initialization>
            <claude-desktop-config>
                Here is the configuration file location for the Claude Desktop App which contains all MCP services initialization parameters: "C:\Users\shane\AppData\Roaming\Claude\claude_desktop_config.json"
            </claude-desktop-config>
```

## CRITICAL CONCEPT

[Critical Concept](./CRITICAL.md)

## Related Documentation

The following documents in this repository provide additional context and guidance for understanding and utilizing the `project-prompt.xml`:

- `docs/mcp-knowledge-graph-enhanced-chat-initialization.md`: Detailed information on the knowledge graph-based initialization process.
- `docs/understanding-the-knowledge-graph-schema.md`: In-depth explanation of the knowledge graph schema and best practices.
- `docs/setting-up-personal-context-with-mcp-in-claude-desktop-app.md`: Guide on setting up personal context using the MCP in the Claude Desktop application.

For more general information on the Model Context Protocol, please refer to the [official MCP documentation](https://modelcontextprotocol.io).
