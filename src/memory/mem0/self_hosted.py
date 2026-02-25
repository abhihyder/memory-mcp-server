import logging
from mem0 import Memory  # Placeholder for the actual Mem0 client library
from .mem0_base import Mem0Base
from typing import Any
import psycopg2
from psycopg2.extras import RealDictCursor

from src.utils.types import SearchFilter
from src.utils.enums import MemorySearchDriver
from config.mem0 import mem0_config
from config.app import app_config


# Configure logging to show in terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class SelfHosted(Mem0Base):
    client: Memory  # Placeholder for the actual Mem0 client
    
    def __init__(self):
        self.client = Memory.from_config(mem0_config.MEM0_SELF_HOSTED)  # Initialize the Mem0 client
    
    def add(self, message: Any, user_id: str, run_id: str, agent_id: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        self.client.add(message, user_id=user_id, run_id=run_id, agent_id=agent_id, metadata=metadata)
        return {"status": "success", "message": "Data added to Mem0 self-hosted platform successfully."}
    
    def search(self, query: str, filters: SearchFilter) -> dict[str, Any]:
        """
        Search memories based on the configured search driver.
        - MEM0: Uses the mem0 client for semantic search
        - PGVECTOR: Performs raw SQL query against pgvector database
        """
        search_driver = app_config.MEMORY_SEARCH_DRIVER
        
        if search_driver == MemorySearchDriver.MEM0:
            return self._search_with_mem0(query, filters)
        elif search_driver == MemorySearchDriver.PGVECTOR:
            return self._search_with_pgvector(query, filters)
        else:
            raise ValueError(f"Unsupported search driver: {search_driver}")
    
    def _search_with_mem0(self, query: str, filters: SearchFilter) -> dict[str, Any]:
        """Search using the mem0 client."""
        return self.client.search(query, **filters)
    
    def _search_with_pgvector(self, query: str, filters: SearchFilter) -> dict[str, Any]:
        """
        Search directly against pgvector database using raw SQL.
        Uses the embedding model to convert query to vector for similarity search.
        """
        try:
            # Get embedding for the query
            query_embedding = self._get_query_embedding(query)
            
            # Build and execute the pgvector search query
            results = self._execute_pgvector_search(query_embedding, filters)
            
            return {
                "status": "success",
                "results": results
            }
        except Exception as e:
            logger.error(f"Error during pgvector search: {e}")
            return {
                "status": "error",
                "results": []
            }
    
    def _get_pgvector_connection(self):
        """Create a connection to the pgvector database."""
        pg_config = mem0_config.MEM0_SELF_HOSTED["vector_store"]["config"]
        return psycopg2.connect(
            host=pg_config["host"],
            port=pg_config["port"],
            user=pg_config["user"],
            password=pg_config["password"],
            dbname=pg_config["dbname"]
        )
    
    def _get_query_embedding(self, query: str) -> list[float]:
        """
        Get embedding vector for the query using OpenAI embeddings.
        Uses the same embedder configuration as mem0.
        """
        import openai
        
        embedder_config = mem0_config.MEM0_SELF_HOSTED["embedder"]["config"]
        client = openai.OpenAI(api_key=embedder_config["api_key"])
        
        response = client.embeddings.create(
            model=embedder_config["model"],
            input=query
        )
        return response.data[0].embedding
    
    def _execute_pgvector_search(
        self, 
        query_embedding: list[float], 
        filters: SearchFilter,
        limit: int = 10,
        similarity_threshold: float = 0.2
    ) -> list[dict[str, Any]]:
        """
        Execute similarity search against pgvector database.
        
        Table schema:
        - id: uuid (primary key)
        - vector: vector (pgvector type)
        - payload: jsonb containing {data, hash, user_id, agent_id, run_id, created_at, updated_at}
        
        Args:
            similarity_threshold: Minimum similarity score (0-1). Only returns matches above this threshold.
        """
        collection_name = mem0_config.MEM0_SELF_HOSTED["vector_store"]["config"]["collection_name"]
        
        # Convert embedding to pgvector format
        embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"
        
        # Build WHERE clause based on filters (payload is JSONB)
        where_clauses = []
        params = [embedding_str, similarity_threshold]  # For the similarity threshold condition
        
        # Dynamically add all filter keys to WHERE clause
        if filters is not None:
            for key, value in filters.items():
                if value is not None:
                    where_clauses.append(f"payload->>'{key}' = %s")
                    params.append(value)
        
        # Always include similarity threshold filter
        similarity_condition = "1 - (vector <=> %s::vector) > %s"
        
        if where_clauses:
            where_sql = f"WHERE {similarity_condition} AND {' AND '.join(where_clauses)}"
        else:
            where_sql = f"WHERE {similarity_condition}"
        
        query = f"""
            SELECT 
                id,
                payload->>'data' AS memory,
                1 - (vector <=> %s::vector) AS similarity
            FROM {collection_name}
            {where_sql}
            ORDER BY similarity DESC
            LIMIT %s
        """
        
        params = [embedding_str] + params + [limit]
        
        conn = self._get_pgvector_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
                return [dict(row) for row in results]
        finally:
            conn.close()