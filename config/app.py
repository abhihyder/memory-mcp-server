
import os
from dotenv import load_dotenv

from src.utils.enums import MemorySearchDriver

load_dotenv()

class AppConfig:
    APP_PORT: int = int(os.getenv("APP_PORT", 5000))
    
    MEM0_PROVIDER: str | None = os.getenv("MEM0_PROVIDER")
    
    MEM0_API_KEY: str | None = os.getenv("MEM0_API_KEY")
    
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    
    MEMORY_SEARCH_DRIVER: MemorySearchDriver = MemorySearchDriver(os.getenv("MEMORY_SEARCH_DRIVER", "mem0"))  # Default to mem0 if not set
    
app_config = AppConfig()