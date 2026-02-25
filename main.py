
import logging
from mcp.server.fastmcp import FastMCP
from typing import  Any
from src.utils.types import AddToMemoryAttributes, SearchFilter
from src.memory.mem0.mem0_factory import mem0_factory
from config.app import app_config

# Configure logging to show in terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


mcp = FastMCP("company-tools", port=app_config.APP_PORT)

mem0_client = mem0_factory.create() # Initialize the Mem0 client using the factory

@mcp.tool()
def get_contextual_memory(user_input: str, filter_attributes: SearchFilter) -> dict[str, Any]:
    """Fetch relevant contextual memory based on the user input and filter attributes.
    
    Args:
        - user_input: The input text to search for relevant memory
        - filter_attributes: A dictionary containing optional filter keys:
            - user_id: Filter by user identifier
            - run_id: Filter by conversation/run identifier
            - agent_id: Filter by agent identifier
    """
    return mem0_client.search(user_input, filter_attributes)

@mcp.tool()
def add_to_memory(message: Any, attributes: AddToMemoryAttributes):
    """Add a message to memory with specified attributes.
    
    Args:
        - message: The message/memory content to store
        - attributes: A dictionary containing the following keys:
            - user_id: User identifier to associate with the memory
            - run_id: Conversation/run identifier for grouping related memories
            - agent_id: Agent/application identifier that created the memory
            - metadata: Optional additional key-value pairs to store with the memory
    """
    mem0_client.add(message, **attributes)

if __name__ == "__main__":
    try:
        mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        pass