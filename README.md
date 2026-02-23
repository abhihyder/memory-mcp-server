# Memory MCP Server

An MCP (Model Context Protocol) server that provides contextual memory capabilities using [Mem0](https://mem0.ai/).

## Features

- **Contextual Memory Search** - Retrieve relevant memories based on semantic queries
- **Memory Storage** - Add messages to memory with user/session context
- **Multiple Providers** - Support for both Mem0 Cloud Platform and Self-Hosted deployments

## Prerequisites

- Python >= 3.11
- Mem0 API key (for cloud platform) or self-hosted Mem0 instance

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd memory-mcp

# Install dependencies using uv
uv sync
```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
# Required: Choose provider - "cloud_platform" or "self_hosted"
MEM0_PROVIDER=cloud_platform

# Required: Your Mem0 API key
MEM0_API_KEY=your_api_key_here

# Optional: OpenAI API key (if using OpenAI-based features)
OPENAI_API_KEY=your_openai_key_here
```

## Usage

### Running the Server

```bash
uv run main.py
```

The server runs on port 5002 using streamable HTTP transport.

### MCP Tools

The server exposes two MCP tools:

#### `get_contextual_memory`

Fetch relevant contextual memory based on a query.

**Parameters:**
- `query` (str): The search query
- `filters` (SearchFilter): Filter object containing:
  - `user_id`: Filter by user ID
  - `run_id`: Filter by run/session ID
  - `app_id`: Filter by application ID

**Returns:** Dictionary with search results

#### `add_to_memory`

Add a message to memory with context.

**Parameters:**
- `message` (str): The message to store
- `user_id` (str): User identifier
- `run_id` (str): Run/session identifier
- `app_id` (str): Application identifier
- `metadata` (dict, optional): Additional metadata

**Returns:** Response from Mem0 client

## Project Structure

```
memory-mcp/
├── main.py                 # MCP server entry point
├── config/
│   └── app.py              # Application configuration
├── src/
│   ├── memory/
│   │   └── mem0/
│   │       ├── mem0_base.py       # Abstract base class
│   │       ├── mem0_factory.py    # Factory for provider selection
│   │       ├── cloud_platform.py  # Mem0 Cloud implementation
│   │       └── self_hosted.py     # Self-hosted implementation
│   └── utils/
│       └── types.py        # Type definitions
├── pyproject.toml
└── README.md
```

## Testing with MCP Inspector

```bash
npx @modelcontextprotocol/inspector
```

## License

MIT
