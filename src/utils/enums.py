from enum import Enum

class MemorySearchDriver(str, Enum):
    MEM0 = "mem0"
    PGVECTOR = "pgvector"