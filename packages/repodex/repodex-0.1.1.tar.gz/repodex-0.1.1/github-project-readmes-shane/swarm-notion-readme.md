# Swarm-Notion Integration

A powerful integration that combines the Swarm framework with Notion's API to create an AI-powered Notion assistant. This application enables natural language interactions to manage Notion pages and content through a multi-agent system.

## Features

- **Page Management**: Create new Notion pages with specified titles
- **Rich Content Blocks**: Add various types of content blocks including:

    - Headings (multiple levels)
    - Paragraphs
    - Code blocks with syntax highlighting
    - Embedded content
    - YouTube videos
    - Images
    - Bookmarks
    - Numbered lists
    - Bulleted lists
    - To-do lists

## Architecture

The application uses a multi-agent system with three specialized agents:

1. **Notion Delegate Agent**: Routes requests to appropriate specialized agents
2. **Notion Page Agent**: Handles page creation and management
3. **Notion Block Agent**: Manages block-level content creation and formatting

## Setup

For detailed setup instructions using `uv` package installer on Windows (PowerShell) and Linux/macOS (Bash), please refer to [SETUP.md](SETUP.md).

Quick start:

1. Clone the repository
2. Install dependencies:

    ```bash
    uv pip install -r requirements.txt
    ```

3. Create a `.env` file with the following variables:

    ```ini
    NOTION_API_KEY=your_notion_api_key
    OPENAI_API_KEY_=your_openai_api_key
    NOTION_ENDPOINT=https://api.notion.com/v1
    NOTION_PAGE_ID=your_notion_page_id
    ```

## Usage

Run the application:

```bash
python app.py
```

### Example Commands

1. Create a new page:

    ```txt
    Create a new page titled "Meeting Notes"
    ```

2. Add content to existing page:

    ```txt
    Add a bullet list with "Task 1, Task 2, Task 3" in my notion page
    ```

3. Add code block:

    ```txt
    Add a Python code block with a simple hello world program in my notion page
    ```

## Technical Details

### Dependencies

- swarm: OpenAI's Swarm framework for multi-agent systems (installed from GitHub)
- httpx: HTTP client for API requests
- python-dotenv: Environment variable management
- openai: OpenAI API client for GPT-4 integration

### Agent System

- Uses GPT-4 for natural language understanding
- Implements a hierarchical agent system for task delegation
- Each agent has specific responsibilities and capabilities
- Agents can transfer control to other agents based on task requirements

### Notion API Integration

- Supports all major Notion block types
- Implements proper error handling and timeouts
- Uses Notion API v2022-06-28
- Handles rich text formatting and block-specific properties

## Error Handling

The system includes comprehensive error handling for:

- Invalid block types
- Missing parameters
- Authorization issues
- API timeouts
- Invalid YouTube URLs
- Malformed list inputs

## Best Practices

1. Use clear, specific commands
2. Specify block types explicitly when needed
3. Use commas to separate list items
4. Ensure proper authorization setup before use
5. Monitor API rate limits

## Limitations

- Requires valid Notion API key and page access
- Some block types have specific formatting requirements
- API rate limits apply
- YouTube embeds require valid YouTube URLs
