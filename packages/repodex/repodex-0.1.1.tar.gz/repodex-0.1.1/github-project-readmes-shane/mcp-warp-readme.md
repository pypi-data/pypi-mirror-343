# MCP Warp

A simple CLI program to run AI prompts and implement [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) client.

You can use any [MCP-compatible servers](https://github.com/punkpeye/awesome-mcp-servers) from the convenience of your terminal.

This acts as an alternative client beside Claude Desktop. Additionally you can use any language model provider like OpenAI, Groq, or local models via [llama](https://github.com/ggerganov/llama.cpp).

![C4 Diagram](c4_diagram.png)

## Usage

### Basic Usage

```bash
warp What is the capital city of North Sumatra?
The capital city of North Sumatra is Medan.
```

You can omit the quotes, but be careful with bash special characters like `&`, `|`, `;` that might be interpreted by your shell.

You can also pipe input from other commands or files:

```bash
echo "What is the capital city of North Sumatra?" | warp
The capital city of North Sumatra is Medan.

echo "Given a location, tell me its capital city." > instructions.txt
cat instruction.txt | warp "West Java"
The capital city of West Java is Bandung.
```

### Image Input

You can pipe image files to analyze them with multimodal models:

```bash
cat image.jpg | warp "What do you see in this image?"
[The AI will analyze and describe the image]

cat screenshot.png | warp "Is there any error in this screenshot?"
[The AI will analyze the screenshot and point out any errors]
```

### Using Prompt Templates

You can use predefined prompt templates by using the `p` prefix followed by the template name and its arguments:

```bash
# List available prompt templates
warp --list-prompts

# Use a template
warp p review  # Review git changes
warp p commit  # Generate commit message
warp p yt url=https://youtube.com/...  # Summarize YouTube video
```

### Triggering a tool

```bash
warp What is the top article on hackernews today?

================================== Ai Message ==================================
Tool Calls:
  brave_web_search (call_eXmFQizLUp8TKBgPtgFo71et)
 Call ID: call_eXmFQizLUp8TKBgPtgFo71et
  Args:
    query: site:news.ycombinator.com
    count: 1
Brave Search MCP Server running on stdio

# If the tool requires confirmation, you'll be prompted:
Confirm tool call? [y/n]: y

================================== Ai Message ==================================
Tool Calls:
  fetch (call_xH32S0QKqMfudgN1ZGV6vH1P)
 Call ID: call_xH32S0QKqMfudgN1ZGV6vH1P
  Args:
    url: https://news.ycombinator.com/
================================= Tool Message =================================
Name: fetch

[TextContent(type='text', text='Contents [REDACTED]]
================================== Ai Message ==================================

The top article on Hacker News today is:

### [Why pipes sometimes get "stuck": buffering](https://jvns.ca)
- **Points:** 31
- **Posted by:** tanelpoder
- **Posted:** 1 hour ago

You can view the full list of articles on [Hacker News](https://news.ycombinator.com/)
```

To bypass tool confirmation requirements, use the `--no-confirmations` flag:

```bash
warp --no-confirmations "What is the top article on hackernews today?"
```

### Continuation

Add a `c` prefix to your message to continue the last conversation.

```bash
warp asldkfjasdfkl
It seems like your message might have been a typo or an error. Could you please clarify or provide more details about what you need help with?
warp c what did i say previously?
You previously typed "asldkfjasdfkl," which appears to be a random string of characters. If you meant to ask something specific or if you have a question, please let me know!
```

### Clipboard Support

You can use content from your clipboard using the `cb` command:

```bash
# After copying text to clipboard
warp cb
[The AI will process the clipboard text]

warp cb "What language is this code written in?"
[The AI will analyze the clipboard text with your question]

# After copying an image to clipboard
warp cb "What do you see in this image?"
[The AI will analyze the clipboard image]

# You can combine it with continuation
warp cb c "Tell me more about what you see"
[The AI will continue the conversation about the clipboard content]
```

The clipboard feature works in:

- Native Windows/macOS/Linux environments
  - Windows: Uses PowerShell
  - macOS: Uses `pbpaste` for text, `pngpaste` for images (optional)
  - Linux: Uses `xclip` (required for clipboard support)
- Windows Subsystem for Linux (WSL)
  - Accesses the Windows clipboard through PowerShell
  - Works with both text and images
  - Make sure you have access to `powershell.exe` from WSL

Required tools for clipboard support:

- Windows: PowerShell (built-in)
- macOS:
  - `pbpaste` (built-in) for text
  - `pngpaste` (optional) for images: `brew install pngpaste`
- Linux:
  - `xclip`: `sudo apt install xclip` or equivalent

The CLI automatically detects if the clipboard content is text or image and handles it appropriately.

### Additional Options

```bash
warp --list-tools                # List all available tools
warp --list-prompts              # List available prompt templates
warp --no-tools                  # Run without any tools
warp --force-refresh             # Force refresh tool capabilities cache
warp --text-only                 # Output raw text without markdown formatting
warp --show-memories             # Show user memories
```

## Setup

1. Clone the repository:

   ```bash
   pip install git+https://github.com/shaneholloman/mcp-warp.git
   ```

2. Create a `~/.warp/config.json` file to configure your Warp and MCP servers:

   ```json
   {
     "systemPrompt": "You are an AI assistant helping a software engineer...",
     "warp": {
       "provider": "openai",
       "model": "gpt-4",
       "api_key": "your-openai-api-key",
       "temperature": 0.7,
       "base_url": "https://api.openai.com/v1"  // Optional, for OpenRouter or other providers
     },
     "mcpServers": {
       "fetch": {
         "command": "uvx",
         "args": ["mcp-server-fetch"],
         "requires_confirmation": ["fetch"],
         "enabled": true,  // Optional, defaults to true
         "exclude_tools": []  // Optional, list of tool names to exclude
       },
       "brave-search": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-brave-search"],
         "env": {
           "BRAVE_API_KEY": "your-brave-api-key"
         },
         "requires_confirmation": ["brave_web_search"]
       },
       "youtube": {
         "command": "uvx",
         "args": ["--from", "git+https://github.com/shaneholloman/mcp-youtube", "mcp-youtube"]
       }
     }
   }
   ```

   Note:
   - Use `requires_confirmation` to specify which tools need user confirmation before execution
   - The Warp API key can also be set via environment variables `WARP_API_KEY` or `OPENAI_API_KEY`
   - The config file can be placed in either `~/.warp/config.json` or `$PWD/.warp/config.json`
   - You can comment the JSON config file with `//` if you like to switch around the configuration

3. Run the CLI:

   ```bash
   warp "What is the capital city of North Sumatra?"
   ```

## Contributing

Feel free to submit issues and pull requests for improvements or bug fixes.
