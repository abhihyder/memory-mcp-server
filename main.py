
import logging
from mcp.server.fastmcp import FastMCP
from typing import  Any
from src.utils.types import SearchFilter
from src.memory.mem0.mem0_factory import mem0_factory
from config.app import app_config

# Configure logging to show in terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


mcp = FastMCP("company-tools", port=app_config.APP_PORT)

mem0_client = mem0_factory.create() # Initialize the Mem0 client using the factory

@mcp.tool()
def get_contextual_memory(user_input: str, filters: SearchFilter) -> dict[str, Any]:
    """Fetch relevant contextual memory based on the user input and optional filters.
    
    Filter keys:
        - user_id: Filter by user identifier
        - run_id: Filter by conversation/run identifier
        - agent_id: Filter by agent identifier (takes precedence over app_id if both provided)
    """
    context = mem0_client.search(user_input, filters)
    return {"results": context}

@mcp.tool()
def add_to_memory(message: str, user_id: str, run_id: str, agent_id: str, metadata: dict[str, Any] | None = None):
    """Add a message to memory with optional metadata.
    
    Args:
        - message: The message/memory content to store
        - user_id: User identifier to associate with the memory
        - run_id: Conversation/run identifier for grouping related memories
        - agent_id: Agent/application identifier that created the memory
        - metadata: Optional additional key-value pairs to store with the memory
    """
    mem0_client.add(message, user_id, run_id, agent_id, metadata)

if __name__ == "__main__":
    try:
        mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        pass