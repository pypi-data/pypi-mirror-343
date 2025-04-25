"""Plugin manager for Taskinator."""

import importlib
import inspect
import os
import pkgutil
from pathlib import Path
from typing import Dict, Any, List, Optional, Type, Set, Tuple

from loguru import logger

from taskinator.external_adapters.base_adapter import ExternalAdapter


class PluginDependency:
    """Represents a dependency for a plugin."""
    
    def __init__(self, name: str, version: str = None, optional: bool = False):
        """Initialize a plugin dependency.
        
        Args:
            name: Name of the dependency
            version: Version requirement (e.g., ">=1.0.0")
            optional: Whether the dependency is optional
        """
        self.name = name
        self.version = version
        self.optional = optional
        
    def __str__(self) -> str:
        """Get a string representation of the dependency."""
        if self.version:
            return f"{self.name}{self.version}"
        return self.name


class PluginInfo:
    """Information about a plugin."""
    
    def __init__(
        self, 
        name: str, 
        version: str = "0.1.0",
        description: str = "",
        author: str = "",
        dependencies: List[PluginDependency] = None
    ):
        """Initialize plugin information.
        
        Args:
            name: Name of the plugin
            version: Version of the plugin
            description: Description of the plugin
            author: Author of the plugin
            dependencies: List of dependencies
        """
        self.name = name
        self.version = version
        self.description = description
        self.author = author
        self.dependencies = dependencies or []
        
    def __str__(self) -> str:
        """Get a string representation of the plugin info."""
        return f"{self.name} v{self.version}"


class PluginManager:
    """Manager for Taskinator plugins.
    
    This class provides methods for loading, unloading, and managing plugins.
    It discovers plugins in the external_adapters package and registers them
    for use in the application.
    """
    
    def __init__(self):
        """Initialize the plugin manager."""
        self.adapters: Dict[str, Type[ExternalAdapter]] = {}
        self.adapter_instances: Dict[str, ExternalAdapter] = {}
        self.loaded_plugins: Set[str] = set()
        self.plugin_info: Dict[str, PluginInfo] = {}
        self.dependency_graph: Dict[str, List[str]] = {}
        
    def discover_plugins(self, package_name: str = "taskinator.external_adapters") -> List[str]:
        """Discover available plugins in the specified package.
        
        Args:
            package_name: Name of the package to search for plugins
            
        Returns:
            List of discovered plugin names
        """
        discovered_plugins = []
        package = importlib.import_module(package_name)
        
        # Get the package directory
        if hasattr(package, "__path__"):
            for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
                if not is_pkg and name != "base_adapter" and not name.startswith("__"):
                    discovered_plugins.append(name)
        
        logger.info(f"Discovered plugins: {discovered_plugins}")
        return discovered_plugins
        
    def load_plugin(self, plugin_name: str, package_name: str = "taskinator.external_adapters") -> bool:
        """Load a plugin by name.
        
        Args:
            plugin_name: Name of the plugin to load
            package_name: Name of the package containing the plugin
            
        Returns:
            True if the plugin was loaded successfully, False otherwise
        """
        if plugin_name in self.loaded_plugins:
            logger.info(f"Plugin {plugin_name} is already loaded")
            return True
            
        try:
            # Import the module
            module_name = f"{package_name}.{plugin_name}"
            module = importlib.import_module(module_name)
            
            # Get plugin info if available
            plugin_info = None
            if hasattr(module, "PLUGIN_INFO"):
                plugin_info = module.PLUGIN_INFO
            else:
                # Create default plugin info
                plugin_info = PluginInfo(
                    name=plugin_name,
                    description=getattr(module, "__doc__", ""),
                    author=getattr(module, "__author__", "")
                )
                
            # Store plugin info
            self.plugin_info[plugin_name] = plugin_info
            
            # Check dependencies
            if not self._check_dependencies(plugin_info):
                logger.error(f"Failed to load plugin {plugin_name} due to missing dependencies")
                return False
            
            # Find adapter classes in the module
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and 
                    issubclass(obj, ExternalAdapter) and 
                    obj != ExternalAdapter):
                    
                    # Register the adapter
                    adapter_id = obj.system_id if hasattr(obj, "system_id") else plugin_name
                    self.adapters[adapter_id] = obj
                    logger.info(f"Registered adapter {name} for system {adapter_id}")
            
            # Mark the plugin as loaded
            self.loaded_plugins.add(plugin_name)
            
            # Update dependency graph
            self._update_dependency_graph()
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading plugin {plugin_name}: {e}")
            return False
            
    def _check_dependencies(self, plugin_info: PluginInfo) -> bool:
        """Check if all dependencies for a plugin are satisfied.
        
        Args:
            plugin_info: Plugin information
            
        Returns:
            True if all dependencies are satisfied, False otherwise
        """
        if not plugin_info.dependencies:
            return True
            
        for dependency in plugin_info.dependencies:
            # Skip optional dependencies
            if dependency.optional:
                continue
                
            # Check if the dependency is loaded
            if dependency.name not in self.loaded_plugins:
                # Try to load the dependency
                if not self.load_plugin(dependency.name):
                    logger.error(f"Failed to load dependency {dependency.name}")
                    return False
                    
            # Check version if specified
            if dependency.version and dependency.name in self.plugin_info:
                # TODO: Implement version checking
                pass
                
        return True
        
    def _update_dependency_graph(self):
        """Update the dependency graph based on loaded plugins."""
        self.dependency_graph = {}
        
        for plugin_name, plugin_info in self.plugin_info.items():
            if plugin_name not in self.dependency_graph:
                self.dependency_graph[plugin_name] = []
                
            for dependency in plugin_info.dependencies:
                if dependency.name not in self.dependency_graph:
                    self.dependency_graph[dependency.name] = []
                    
                # Add dependency relationship
                self.dependency_graph[plugin_name].append(dependency.name)
                
    def get_plugin_info(self, plugin_name: str) -> Optional[PluginInfo]:
        """Get information about a plugin.
        
        Args:
            plugin_name: Name of the plugin
            
        Returns:
            Plugin information if found, None otherwise
        """
        return self.plugin_info.get(plugin_name)
        
    def get_plugin_dependencies(self, plugin_name: str) -> List[str]:
        """Get dependencies for a plugin.
        
        Args:
            plugin_name: Name of the plugin
            
        Returns:
            List of dependency names
        """
        return self.dependency_graph.get(plugin_name, [])
        
    def get_dependent_plugins(self, plugin_name: str) -> List[str]:
        """Get plugins that depend on the specified plugin.
        
        Args:
            plugin_name: Name of the plugin
            
        Returns:
            List of plugin names that depend on the specified plugin
        """
        dependents = []
        for name, dependencies in self.dependency_graph.items():
            if plugin_name in dependencies:
                dependents.append(name)
                
        return dependents
        
    def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a plugin by name.
        
        Args:
            plugin_name: Name of the plugin to unload
            
        Returns:
            True if the plugin was unloaded successfully, False otherwise
        """
        if plugin_name not in self.loaded_plugins:
            logger.info(f"Plugin {plugin_name} is not loaded")
            return True
            
        try:
            # Check for dependent plugins
            dependents = self.get_dependent_plugins(plugin_name)
            if dependents:
                logger.error(f"Cannot unload plugin {plugin_name} because it is required by: {', '.join(dependents)}")
                return False
                
            # Find adapters from this plugin
            adapters_to_remove = []
            for adapter_id, adapter_class in self.adapters.items():
                module_name = adapter_class.__module__.split(".")[-1]
                if module_name == plugin_name:
                    adapters_to_remove.append(adapter_id)
            
            # Remove adapter instances
            for adapter_id in adapters_to_remove:
                if adapter_id in self.adapter_instances:
                    # Close the adapter instance
                    adapter = self.adapter_instances[adapter_id]
                    try:
                        # Run close method if it's synchronous
                        if not inspect.iscoroutinefunction(adapter.close):
                            adapter.close()
                    except Exception as e:
                        logger.error(f"Error closing adapter {adapter_id}: {e}")
                        
                    # Remove the instance
                    del self.adapter_instances[adapter_id]
                
                # Remove the adapter class
                if adapter_id in self.adapters:
                    del self.adapters[adapter_id]
            
            # Remove plugin info
            if plugin_name in self.plugin_info:
                del self.plugin_info[plugin_name]
                
            # Mark the plugin as unloaded
            self.loaded_plugins.remove(plugin_name)
            
            # Update dependency graph
            self._update_dependency_graph()
            
            return True
            
        except Exception as e:
            logger.error(f"Error unloading plugin {plugin_name}: {e}")
            return False
            
    def get_adapter_class(self, system_id: str) -> Optional[Type[ExternalAdapter]]:
        """Get an adapter class by system ID.
        
        Args:
            system_id: ID of the system to get the adapter for
            
        Returns:
            Adapter class if found, None otherwise
        """
        return self.adapters.get(system_id)
        
    async def get_adapter_instance(self, system_id: str, **kwargs) -> Optional[ExternalAdapter]:
        """Get or create an adapter instance by system ID.
        
        Args:
            system_id: ID of the system to get the adapter for
            **kwargs: Additional arguments to pass to the adapter constructor
            
        Returns:
            Adapter instance if found or created, None otherwise
        """
        # Check if we already have an instance
        if system_id in self.adapter_instances:
            return self.adapter_instances[system_id]
            
        # Get the adapter class
        adapter_class = self.get_adapter_class(system_id)
        if not adapter_class:
            logger.error(f"No adapter found for system {system_id}")
            return None
            
        try:
            # Create a new instance
            adapter = adapter_class(**kwargs)
            
            # Initialize the adapter
            success = False
            if inspect.iscoroutinefunction(adapter.initialize):
                success = await adapter.initialize()
            else:
                success = adapter.initialize()
                
            if not success:
                logger.error(f"Failed to initialize adapter for system {system_id}")
                return None
                
            # Store the instance
            self.adapter_instances[system_id] = adapter
            return adapter
            
        except Exception as e:
            logger.error(f"Error creating adapter instance for system {system_id}: {e}")
            return None
            
    async def close_adapter(self, system_id: str) -> bool:
        """Close an adapter instance by system ID.
        
        Args:
            system_id: ID of the system to close the adapter for
            
        Returns:
            True if the adapter was closed successfully, False otherwise
        """
        if system_id not in self.adapter_instances:
            logger.info(f"No adapter instance found for system {system_id}")
            return True
            
        try:
            # Get the adapter instance
            adapter = self.adapter_instances[system_id]
            
            # Close the adapter
            if inspect.iscoroutinefunction(adapter.close):
                await adapter.close()
            else:
                adapter.close()
                
            # Remove the instance
            del self.adapter_instances[system_id]
            return True
            
        except Exception as e:
            logger.error(f"Error closing adapter for system {system_id}: {e}")
            return False
            
    async def close_all_adapters(self) -> bool:
        """Close all adapter instances.
        
        Returns:
            True if all adapters were closed successfully, False otherwise
        """
        success = True
        for system_id in list(self.adapter_instances.keys()):
            if not await self.close_adapter(system_id):
                success = False
                
        return success
        
    def get_available_systems(self) -> List[str]:
        """Get a list of available system IDs.
        
        Returns:
            List of system IDs
        """
        return list(self.adapters.keys())
