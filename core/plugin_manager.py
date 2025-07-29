"""Plugin manager for dynamically loading and managing utility plugins."""

import os
import importlib.util
import inspect
from typing import Dict, List, Optional
from pathlib import Path

from .base_plugin import BasePlugin


class PluginManager:
    """Manages loading and access to utility plugins."""
    
    def __init__(self, plugins_dir: str = "plugins"):
        self.plugins_dir = Path(plugins_dir)
        self.plugins: Dict[str, BasePlugin] = {}
        self._load_plugins()
    
    def _load_plugins(self) -> None:
        """Dynamically load all plugins from the plugins directory."""
        if not self.plugins_dir.exists():
            print(f"Plugins directory '{self.plugins_dir}' not found.")
            return
        
        for plugin_file in self.plugins_dir.glob("*_plugin.py"):
            try:
                self._load_plugin_file(plugin_file)
            except Exception as e:
                print(f"Error loading plugin {plugin_file}: {e}")
    
    def _load_plugin_file(self, plugin_file: Path) -> None:
        """Load a single plugin file."""
        spec = importlib.util.spec_from_file_location(
            plugin_file.stem, plugin_file
        )
        if spec is None or spec.loader is None:
            return
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find plugin classes in the module
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if (obj != BasePlugin and 
                issubclass(obj, BasePlugin) and 
                obj.__module__ == module.__name__):
                
                plugin_instance = obj()
                self.plugins[plugin_instance.utility_name] = plugin_instance
                print(f"Loaded plugin: {plugin_instance.name}")
    
    def get_plugin(self, utility_name: str) -> Optional[BasePlugin]:
        """Get a plugin by utility name."""
        return self.plugins.get(utility_name)
    
    def get_available_utilities(self) -> List[str]:
        """Get list of available utility names."""
        return list(self.plugins.keys())
    
    def get_plugin_info(self) -> Dict[str, str]:
        """Get information about all loaded plugins."""
        return {
            name: plugin.description 
            for name, plugin in self.plugins.items()
        }
    
    def reload_plugins(self) -> None:
        """Reload all plugins."""
        self.plugins.clear()
        self._load_plugins()
