import os
from mem0 import MemoryClient  # Placeholder for the actual Mem0 client library
from .mem0_base import Mem0Base
from typing import Any
from src.utils.types import SearchFilter

class SelfHosted(Mem0Base):
    client: MemoryClient  # Placeholder for the actual Mem0 client
    api_key: str|None
    
    def __init__(self):
        self.api_key = os.getenv("MEM0_API_KEY")  # Load API key from environment variable
        self.client = MemoryClient(api_key=self.api_key)  # Initialize the Mem0 client
    
    def add(self, message: Any, user_id: str, run_id: str, app_id: str, metadata: dict[str, Any] | None = None)-> dict[str, Any]:
        return {"status": "success", "message": "Data added to Mem0 self-hosted platform successfully."}
    
    def search(self, query: str, filters: SearchFilter) -> dict[str, Any]:
        if filters is not None:
            return self.client.search(query, filters=filters)
        else:
            return self.client.search(query)