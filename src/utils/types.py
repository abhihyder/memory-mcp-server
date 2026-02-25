
from typing import Any
from typing_extensions import TypedDict

class SearchFilter(TypedDict):
    user_id: Any|None
    run_id: Any|None
    agent_id: Any|None

class AddToMemoryAttributes(TypedDict):
    user_id: str
    run_id: str
    agent_id: str
    metadata: dict[str, Any]|None