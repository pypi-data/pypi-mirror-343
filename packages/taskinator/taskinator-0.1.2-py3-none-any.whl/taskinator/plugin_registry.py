"""Plugin registry for Taskinator."""

import asyncio
from typing import Dict, Any, List, Optional, Type, Set

from loguru import logger

from taskinator.plugin_manager import PluginManager, PluginInfo, PluginDependency
from taskinator.external_adapters.base_adapter import ExternalAdapter


class PluginRegistry:
    """Registry for Taskinator plugins.
    
    This class provides a singleton registry for plugins and adapters.
    It's used to access plugins throughout the application.
    """
    
    _instance = None
    
    def __new__(cls):
        """Create a new instance or return the existing one."""
        if cls._instance is None:
            cls._instance = super(PluginRegistry, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
        
    def __init__(self):
        """Initialize the plugin registry."""
        if self._initialized:
            return
            
        self.plugin_manager = PluginManager()
        self._initialized = True
        
    def discover_plugins(self) -> List[str]:
        """Discover available plugins.
        
        Returns:
            List of discovered plugin names
        """
        return self.plugin_manager.discover_plugins()
        
    def load_plugin(self, plugin_name: str) -> bool:
        """Load a plugin by name.
        
        Args:
            plugin_name: Name of the plugin to load
            
        Returns:
            True if the plugin was loaded successfully, False otherwise
        """
        return self.plugin_manager.load_plugin(plugin_name)
        
    def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a plugin by name.
        
        Args:
            plugin_name: Name of the plugin to unload
            
        Returns:
            True if the plugin was unloaded successfully, False otherwise
        """
        return self.plugin_manager.unload_plugin(plugin_name)
        
    def get_adapter_class(self, system_id: str) -> Optional[Type[ExternalAdapter]]:
        """Get an adapter class by system ID.
        
        Args:
            system_id: ID of the system to get the adapter for
            
        Returns:
            Adapter class if found, None otherwise
        """
        return self.plugin_manager.get_adapter_class(system_id)
        
    async def get_adapter_instance(self, system_id: str, **kwargs) -> Optional[ExternalAdapter]:
        """Get or create an adapter instance by system ID.
        
        Args:
            system_id: ID of the system to get the adapter for
            **kwargs: Additional arguments to pass to the adapter constructor
            
        Returns:
            Adapter instance if found or created, None otherwise
        """
        return await self.plugin_manager.get_adapter_instance(system_id, **kwargs)
        
    async def close_adapter(self, system_id: str) -> bool:
        """Close an adapter instance by system ID.
        
        Args:
            system_id: ID of the system to close the adapter for
            
        Returns:
            True if the adapter was closed successfully, False otherwise
        """
        return await self.plugin_manager.close_adapter(system_id)
        
    async def close_all_adapters(self) -> bool:
        """Close all adapter instances.
        
        Returns:
            True if all adapters were closed successfully, False otherwise
        """
        return await self.plugin_manager.close_all_adapters()
        
    def get_available_systems(self) -> List[str]:
        """Get a list of available system IDs.
        
        Returns:
            List of system IDs
        """
        return self.plugin_manager.get_available_systems()
        
    def load_all_plugins(self) -> bool:
        """Load all available plugins.
        
        Returns:
            True if all plugins were loaded successfully, False otherwise
        """
        success = True
        for plugin_name in self.discover_plugins():
            if not self.load_plugin(plugin_name):
                success = False
                
        return success
        
    def get_plugin_info(self, plugin_name: str) -> Optional[PluginInfo]:
        """Get information about a plugin.
        
        Args:
            plugin_name: Name of the plugin
            
        Returns:
            Plugin information if found, None otherwise
        """
        return self.plugin_manager.get_plugin_info(plugin_name)
        
    def get_plugin_dependencies(self, plugin_name: str) -> List[str]:
        """Get dependencies for a plugin.
        
        Args:
            plugin_name: Name of the plugin
            
        Returns:
            List of dependency names
        """
        return self.plugin_manager.get_plugin_dependencies(plugin_name)
        
    def get_dependent_plugins(self, plugin_name: str) -> List[str]:
        """Get plugins that depend on the specified plugin.
        
        Args:
            plugin_name: Name of the plugin
            
        Returns:
            List of plugin names that depend on the specified plugin
        """
        return self.plugin_manager.get_dependent_plugins(plugin_name)


# Create a singleton instance
registry = PluginRegistry()
