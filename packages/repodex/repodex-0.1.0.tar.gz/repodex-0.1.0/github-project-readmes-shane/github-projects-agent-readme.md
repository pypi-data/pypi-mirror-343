# GitHub Projects Agent

An intelligent agent that helps you manage GitHub Projects using natural language. Built with LangGraph and Claude AI.

> [!CAUTION]
> Entirely untested and doesn't work yet. This is a concept only.

## Features

- **Natural Language Interface**: Interact with GitHub Projects using plain English
- **Project Management**: Create projects, add items, organize boards
- **Tagging System**: Automatically tag issues based on configurable rules
- **Flexible Deployment**: Use as a CLI, import as a library, or deploy as a service
- **Context Preservation**: Maintains context throughout conversations

## Installation

1. Clone the repository

   ```bash
   git clone https://github.com/yourusername/github-projects-agent.git
   cd github-projects-agent
   ```

2. Set up a virtual environment

   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies

   ```bash
   # Install all dependencies including development dependencies
   uv sync --all-extras

   # OR to install only main dependencies (without dev tools)
   uv sync

   # OR to install only dev dependencies
   uv sync --extra dev
   ```

3. Set up your environment variables

   ```bash
   # Create a .env file
   echo "GITHUB_TOKEN=your_github_token" > .env
   echo "GITHUB_ORG=your_default_org" >> .env
   echo "GITHUB_USER=your_github_username" >> .env
   ```

## Usage

### Command Line Interface

The agent can be used as a command-line tool:

```bash
# Run a single command
python github_projects_agent.py "Show me all projects in the techcorp organization"

# Run in interactive mode
python github_projects_agent.py --interactive

# Run with context (useful for commands that need project IDs, etc.)
python github_projects_agent.py --context '{"project_id": "PVT_123"}' "Add a new draft issue titled 'Fix login bug'"

# Load context from a file
python github_projects_agent.py --context-file my_context.json --interactive

# Save context to a file after running
python github_projects_agent.py --interactive --save-context session.json
```

### API Usage

You can also use the agent as a library in your Python code:

```python
from github_projects_agent import process_request

# Simple request
response = process_request("Show me all projects in the techcorp organization")
print(response)

# With context
context = {"project_id": "PVT_123"}
response = process_request("Add a new draft issue titled 'Fix login bug'", context)
print(response)
```

## Example Commands

Here are some examples of what you can do with the agent:

```
# Project management
Show me all projects in the techcorp organization
Create a new project called "Q2 Roadmap" for our organization
Add a draft issue titled "Implement OAuth login" to the Q2 Roadmap project

# Item management
List all items in the Q2 Roadmap project
Update the status of the OAuth login issue to "In Progress"
Move the bug fix task to the "Done" column

# Tagging and organization
Tag the OAuth login issue as high-priority
Create a new tag called "tech-debt" with red color
Find all issues tagged as "bug" in the Q2 Roadmap project
```

## Automatic Tagging

The agent can automatically tag issues based on configurable rules. Create a `tagging_rules.json` file:

```json
{
  "rules": [
    {
      "name": "High Priority Bugs",
      "tag_id": "47fc9ee4",
      "conditions": [
        {
          "type": "keyword",
          "keywords": ["critical", "urgent", "high priority"],
          "field": "title",
          "match_all": false
        }
      ]
    },
    {
      "name": "Frontend Tasks",
      "tag_id": "98236657",
      "conditions": [
        {
          "type": "keyword",
          "keywords": ["ui", "frontend", "css", "react", "vue"],
          "field": "body",
          "match_all": false
        }
      ]
    }
  ]
}
```

Then use it with the agent:

```python
from github_projects_agent import load_tagging_rules, auto_tag_item

# Load rules
rules = load_tagging_rules("tagging_rules.json")

# Apply rules to an item
auto_tag_item("PVT_123", "PVTI_456", item_content, rules)
```

## Webhook Integration

You can set up a webhook server to automatically tag new issues:

```python
from flask import Flask, request
from github_projects_agent import process_webhook_event, load_tagging_rules

app = Flask(__name__)
rules = load_tagging_rules("tagging_rules.json")

@app.route("/webhook", methods=["POST"])
def github_webhook():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json
    process_webhook_event(event_type, payload, rules)
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

## Configuration

The agent uses the following configuration sources (in order of precedence):

1. Command-line arguments
2. Configuration file (~/.github-projects-agent.json)
3. Environment variables

You can create a configuration file:

```json
{
  "github_token": "your_token",
  "github_base_url": "https://api.github.com",
  "llm_model": "claude-3-7-sonnet-20250219",
  "default_org": "your-org",
  "default_user": "your-username"
}
```

## Requirements

- Python 3.9+
- GitHub Personal Access Token with repo and project scopes
- Anthropic API Key (for Claude)

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
