
import logging
from mcp.server.fastmcp import FastMCP
from typing import  Any
from src.utils.types import SearchFilter
from src.memory.mem0.mem0_factory import mem0_factory

# Configure logging to show in terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

mcp = FastMCP("company-tools", port=5002)

mem0_client = mem0_factory.create() # Initialize the Mem0 client using the factory

@mcp.tool()
def get_contextual_memory(query: str, filters: SearchFilter) -> dict[str, Any]:
    """Fetch relevant contextual memory based on the query and optional filters."""
    context = mem0_client.search(query, filters)  # Use the Mem0 client to search for relevant memory
    logger.info(f"Fetching contextual memory for query: {query}")
    logger.info(f"Contextual memory results: {context}")
    return {"results": context}

@mcp.tool()
def add_to_memory(message: str, user_id: str, run_id: str, app_id: str, metadata: dict[str, Any] | None = None):
    """Add a message to memory with optional metadata."""
    response = mem0_client.add(message, user_id, run_id, app_id, metadata)  # Use the Mem0 client to add data to memory
    logger.info(f"Added message to memory: {message} with metadata: {metadata}")
    logger.info(f"Response from Mem0 client: {response}")
    return response

if __name__ == "__main__":
    mcp.run(transport="streamable-http")