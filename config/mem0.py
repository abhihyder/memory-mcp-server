import os
from typing import Any, Dict
from dotenv import load_dotenv

load_dotenv()

class Mem0Config:
    MEM0_SELF_HOSTED: Dict[str, Any] =  {
        "vector_store": {
            "provider": "pgvector",
            "config": {
                "host": os.getenv("PGVECTOR_HOST", "localhost"),
                "port": os.getenv("PGVECTOR_PORT", "5432"),
                "user": os.getenv("PGVECTOR_USER", "postgres"),
                "password": os.getenv("PGVECTOR_PASSWORD", "mysecretpassword"),
                "dbname": os.getenv("PGVECTOR_DBNAME", "mem0_db"),
                "collection_name": "agent_memories" # The table/collection name in the database
            }
        },
        "llm": {
            "provider": "openai",
            "config": {
                "model": "gpt-4o-mini", # Highly recommended for memory extraction
                "api_key": os.getenv("OPENAI_API_KEY")
            }
        },
        "embedder": {
            "provider": "openai",
            "config": {
                "model": "text-embedding-3-small", # The industry standard for embeddings
                "api_key": os.getenv("OPENAI_API_KEY")
            }
        }
    }
    
mem0_config = Mem0Config()