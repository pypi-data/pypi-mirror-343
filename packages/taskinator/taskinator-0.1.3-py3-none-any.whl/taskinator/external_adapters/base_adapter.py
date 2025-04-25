"""Base adapter for external integrations."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union

from taskinator.constants import ExternalSystem, SyncStatus


class ExternalAdapter(ABC):
    """Base class for external adapters.
    
    This abstract class defines the interface that all external adapters must implement.
    It provides methods for synchronizing tasks between Taskinator and external systems.
    """
    
    @property
    @abstractmethod
    def system_id(self) -> str:
        """Get the ID of the external system.
        
        Returns:
            System ID string
        """
        pass
        
    @property
    @abstractmethod
    def system_name(self) -> str:
        """Get the name of the external system.
        
        Returns:
            System name string
        """
        pass
        
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the adapter.
        
        Returns:
            True if initialization was successful, False otherwise
        """
        pass
        
    @abstractmethod
    async def close(self) -> None:
        """Close the adapter and release resources."""
        pass
        
    @abstractmethod
    async def sync_task(self, task: Dict[str, Any], direction: str = "bidirectional") -> Dict[str, Any]:
        """Synchronize a task with the external system.
        
        Args:
            task: Task to synchronize
            direction: Sync direction (bidirectional, push, pull)
            
        Returns:
            Updated task with sync metadata
        """
        pass
        
    @abstractmethod
    async def get_external_task(self, external_id: str) -> Optional[Any]:
        """Get a task from the external system by its ID.
        
        Args:
            external_id: External ID of the task
            
        Returns:
            External task if found, None otherwise
        """
        pass
        
    @abstractmethod
    def map_local_to_remote(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Map a local task to a remote task.
        
        Args:
            task: Local task
            
        Returns:
            Remote task
        """
        pass
        
    @abstractmethod
    def map_remote_to_local(self, remote_task: Any) -> Dict[str, Any]:
        """Map a remote task to a local task.
        
        Args:
            remote_task: Remote task
            
        Returns:
            Local task
        """
        pass
        
    @abstractmethod
    async def find_tasks_by_query(self, query: Dict[str, Any]) -> List[Any]:
        """Find tasks in the external system by query.
        
        Args:
            query: Query parameters
            
        Returns:
            List of matching tasks
        """
        pass
