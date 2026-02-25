# Memory MCP Server

An MCP (Model Context Protocol) server that provides contextual memory capabilities using [Mem0](https://mem0.ai/) with support for both direct Mem0 API and raw PGVector database queries.

## Features

- **Contextual Memory Search** - Retrieve relevant memories based on semantic queries
- **Memory Storage** - Add messages to memory with user/session context
- **Multiple Providers** - Support for both Mem0 Cloud Platform and Self-Hosted deployments
- **Dual Search Drivers** - Choose between Mem0 API or direct PGVector database queries
- **Similarity Threshold** - Filter results based on semantic similarity scores
- **Flexible Filtering** - Filter by user_id, run_id, agent_id, and custom metadata fields

## Prerequisites

- Python >= 3.11
- Mem0 API key (for cloud platform) or self-hosted Mem0 instance with PGVector database

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
# ====================
# APPLICATION
# ====================
# Optional: Application port (default: 5000)
APP_PORT=5000

# ====================
# MEM0 CONFIGURATION
# ====================
# Required: Choose provider - "cloud_platform" or "self_hosted"
MEM0_PROVIDER=self_hosted

# Required for Cloud Platform: Your Mem0 API key
MEM0_API_KEY=your-mem0-api-key-here

# Required for Self-Hosted: OpenAI API key (for embeddings and LLM)
# Get your key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your-openai-api-key-here

# ====================
# SEARCH DRIVER
# ====================
# Required for Self-Hosted only: Choose search driver - "mem0" or "pgvector"
# Note: This setting has no effect when MEM0_PROVIDER=cloud_platform
# - mem0: Uses Mem0 client API for search (default)
# - pgvector: Direct SQL queries to PGVector database
MEMORY_SEARCH_DRIVER=mem0

# ====================
# PGVECTOR DATABASE
# ====================
# PGVector Database Configuration (for self-hosted with pgvector driver)
PGVECTOR_HOST=localhost
PGVECTOR_PORT=5432
PGVECTOR_USER=postgres
PGVECTOR_PASSWORD=mysecretpassword
PGVECTOR_DBNAME=mem0_db
```

## Search Drivers

**Note:** Search drivers only apply when `MEM0_PROVIDER=self_hosted`. For cloud platform deployments, Mem0's built-in search is always used regardless of the `MEMORY_SEARCH_DRIVER` setting.

### MEM0 Driver
Uses the Mem0 client API for semantic search. This is the default and recommended approach as it handles all the complexity internally.

### PGVECTOR Driver
Performs direct SQL queries against the PGVector database for more control and customization:
- Direct access to vector similarity search
- Configurable similarity threshold (default: 0.2)
- Custom filtering on JSONB payload fields
- Returns similarity scores with results

**Database Schema:**
```sql
Table: agent_memories
- id: uuid (primary key)
- vector: vector (pgvector embeddings)
- payload: jsonb {
    data: string,
    hash: string,
    user_id: string,
    agent_id: string,
    run_id: string,
    created_at: timestamp,
    updated_at: timestamp
  }
```

## Usage

### Running the Server

```bash
uv run main.py
```

The server runs on the configured port (default: 5000) using streamable HTTP transport.

Press `Ctrl+C` to stop the server gracefully.

### MCP Tools

The server exposes two MCP tools:

#### `get_contextual_memory`

Fetch relevant contextual memory based on a semantic query.

**Parameters:**
- `user_input` (str): The search query
- `filters` (SearchFilter): Optional filter object containing:
  - `user_id`: Filter by user identifier
  - `run_id`: Filter by conversation/run identifier
  - `agent_id`: Filter by agent identifier
  - `app_id`: Filter by application identifier (automatically mapped to agent_id)
  - Any custom fields in the payload JSONB

**Filter Behavior:**
- If both `app_id` and `agent_id` are provided, `agent_id` takes precedence
- All non-null filter values are applied with AND logic
- For PGVECTOR driver: Only returns results with similarity > 0.2 (configurable)

**Returns:** 
```json
{
  "results": {
    "status": "success",
    "results": [
      {
        "id": "uuid",
        "memory": "memory content",
        "user_id": "user1",
        "agent_id": "app1",
        "run_id": "run1",
        "similarity": 0.85  // Only in pgvector mode
      }
    ]
  }
}
```

#### `add_to_memory`

Add a message to memory with context.

**Parameters:**
- `message` (str): The message/memory content to store
- `user_id` (str): User identifier to associate with the memory
- `run_id` (str): Conversation/run identifier for grouping related memories
- `agent_id` (str): Agent/application identifier that created the memory
- `metadata` (dict, optional): Additional key-value pairs to store with the memory

**Returns:** None (logs success internally)

## Project Structure

```
memory-mcp/
├── main.py                        # MCP server entry point
├── config/
│   ├── app.py                     # Application configuration
│   └── mem0.py                    # Mem0 specific configuration
├── src/
│   ├── memory/
│   │   └── mem0/
│   │       ├── mem0_base.py       # Abstract base class
│   │       ├── mem0_factory.py    # Factory for provider selection
│   │       ├── cloud_platform.py  # Mem0 Cloud implementation
│   │       └── self_hosted.py     # Self-hosted with dual search drivers
│   └── utils/
│       ├── types.py               # Type definitions
│       └── enums.py               # Enumerations (MemorySearchDriver)
├── pyproject.toml
└── README.md
```

## Architecture

### Provider Selection
The system uses a factory pattern to select between Cloud Platform and Self-Hosted implementations based on `MEM0_PROVIDER` environment variable.

### Search Driver Selection
For Self-Hosted deployments, you can choose between:
1. **MEM0 Driver**: Uses Mem0's built-in search (`client.search()`)
2. **PGVECTOR Driver**: Direct PGVector queries with:
   - OpenAI embeddings for query vectorization
   - Cosine similarity search with `<=>` operator
   - Similarity threshold filtering
   - Dynamic JSONB field filtering

## Examples

### Using with Claude Desktop

Add to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "memory": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/memory-mcp",
        "run",
        "main.py"
      ]
    }
  }
}
```

### Search Examples

**Basic search:**
```python
filters = {"user_id": "user123"}
result = get_contextual_memory("What is my profession?", filters)
```

**Multi-filter search:**
```python
filters = {
    "user_id": "user123",
    "agent_id": "assistant_v1",
    "run_id": "session_001"
}
result = get_contextual_memory("previous conversation", filters)
```

## Testing with MCP Inspector

```bash
npx @modelcontextprotocol/inspector uv --directory /path/to/memory-mcp run main.py
```

## Dependencies

- `mem0ai` - Mem0 client library
- `psycopg2-binary` - PostgreSQL adapter (for pgvector)
- `openai` - OpenAI API client (for embeddings)
- `mcp` - Model Context Protocol server
- `python-dotenv` - Environment variable management

## Troubleshooting

### PGVector Connection Issues
- Ensure PostgreSQL with pgvector extension is installed and running
- Verify database credentials in `.env`
- Check that the `agent_memories` table exists

### Embedding Generation Errors
- Verify `OPENAI_API_KEY` is valid
- Check OpenAI API quota and rate limits

### Search Returns No Results
- Lower the `similarity_threshold` in `self_hosted.py` (default: 0.2)
- Verify data exists in the database for the given filters
- Check that embeddings are properly generated and stored

## License

MIT
