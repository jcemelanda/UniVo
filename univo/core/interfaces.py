"""Core interfaces for dependency inversion in UniVo.

Defines protocols to decouple domain logic from data source implementations.
"""
from typing import Any, Protocol


class PictogramRepository(Protocol):
    """Protocol for fetching pictogram and category data.
    
    Implementations must provide raw access to the database or 
    persistence layer.
    """
    
    def get_connection(self) -> Any:
        """Context manager yielding a database connection or equivalent.
        
        Must support a context manager interface and return an object 
        capable of executing queries.
        """
        ...
