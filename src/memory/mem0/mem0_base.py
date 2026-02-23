from abc import abstractmethod, ABC
from typing import Any

from src.utils.types import SearchFilter

class Mem0Base(ABC):
    
    @abstractmethod
    def add(self, message: Any, user_id: str, run_id: str, app_id: str, metadata: dict[str, Any]| None = None)-> dict[str, Any]:
        pass
    
    @abstractmethod
    def search(self, query: str, filters: SearchFilter) -> dict[str, Any]:
        pass