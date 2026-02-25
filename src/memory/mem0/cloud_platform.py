import os
from mem0 import MemoryClient

from src.utils.types import SearchFilter  # Placeholder for the actual Mem0 client library
from .mem0_base import Mem0Base
from typing import Any

class CloudPlatform(Mem0Base):
    client: MemoryClient  # Placeholder for the actual Mem0 client
    api_key: str|None
    
    def __init__(self):
        self.api_key = os.getenv("MEM0_API_KEY")  # Load API key from environment variable
        self.client = MemoryClient(api_key=self.api_key)  # Initialize the Mem0 client
    
    def add(self, message: Any, user_id: str, run_id: str, agent_id: str, metadata: dict[str, Any] | None = None)-> dict[str, Any]:
        self.client.add(message, user_id=user_id, run_id=run_id, agent_id=agent_id, metadata=metadata)
        return {"status": "success", "message": "Data added to Mem0 cloud platform successfully."}
    
    def search(self, query: str, filters: SearchFilter) -> dict[str, Any]:
        return self.client.search(query, filters=filters)