# MCPx - MCP Agent REPL Interface

A command-line REPL (Read-Eval-Print Loop) interface for interacting with AI agents powered by the Model Context Protocol (MCP) framework.

## Version
0.0.1

## Features

- Command-line interface for interacting with AI agents
- Persistent conversation history across sessions
- Web browsing capabilities via Playwright
- Customizable system prompts and configuration
- Command history navigation
- Rich terminal output with markdown rendering
- Real-time tool usage streaming during agent thinking

## Installation

### Using uv (recommended)

```bash
uv tool install .
```

### Using pip

```bash
pip install .
```

## Usage

Once installed, you can use the `mcpx` command:

```bash
# Start the REPL interface
mcpx run

# Open the configuration directory
mcpx config

# Edit the configuration file directly
mcpx edit

# Edit the system prompt 
mcpx prompt
```

### Chat Commands

While in the REPL interface, you can use the following chat commands:

- `/clear` - Clear the conversation history
- `/help` - Show available commands
- `/tools` - List all available MCP tools (with robust detection across various agent structures)
- `/fix` - Fix corrupted conversation history by removing empty messages
- `/init` - Re-initialize the agent and MCP servers (useful when tools stop working or you've started new servers)

These commands support tab-completion.

## Real-time Tool Usage Streaming

MCPx displays real-time information about what tools the agent is using while it's thinking. This helps you:

- See which tools are being called and with what inputs
- Understand the agent's reasoning process
- Monitor progress during longer tasks
- Debug when tools are failing or giving unexpected results

The tool usage is displayed inline during the "thinking" phase with the following information:
- Tool name and sequence number
- Tool input (truncated for readability)
- Tool result or error (if any)
- Final tool usage count

## Configuration

Configuration is stored in the user's config directory:
- macOS: `~/Library/Application Support/mcp-agent-x/`
- Linux: `~/.config/mcp-agent-x/`
- Windows: `C:\Users\<username>\AppData\Roaming\mcp-agent-x\`

The following files are available in the configuration directory:
- `config.json` - Main configuration for MCPx including LLM and agent settings
- `system_prompt.md` - System prompt that controls the agent's behavior

## Requirements

- Python 3.11+
- Google API key (for Gemini model)
- Node.js (for Playwright)

## Environment Variables

Create a `.env` file in your project directory with:

```
GOOGLE_API_KEY=your_google_api_key
```

## Development

### Running Tests

To run the tests:

```bash
# Install development dependencies
uv tool install -e ".[dev]"

# Run tests
python run_tests.py

# Or directly using pytest
pytest -v tests
```

The test suite includes:
- Configuration management tests
- Conversation history tests
- REPL functionality tests

### Debugging

If you encounter issues with conversation history, check the following:
- Use the `/fix` command to repair corrupted history with empty messages
- Ensure the history file is properly formatted JSON
- Check file permissions for the config directory
- Review the error messages for specific issues

If MCP tools stop working:
- Use the `/init` command to reconnect to MCP servers and refresh available tools
- Check that required servers (like Playwright) are running
- Verify your internet connection

### Error Messages

The application provides helpful error messages for common issues:
- **Empty message content**: If this error occurs, run the `/fix` command to remove empty messages from your conversation history.
- **API rate limit exceeded**: Wait a moment and try again.
- **Agent not properly initialized**: Use the `/init` command to re-initialize the agent.

## License

MIT
