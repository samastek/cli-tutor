"""Plugin discovery and management."""

from pathlib import Path
from typing import Dict, List
from .plugin import Plugin


class PluginManager:
    """Manages plugin discovery and loading."""
    
    def __init__(self, plugins_dir: Path):
        self.plugins_dir = plugins_dir
        self.plugin_files: Dict[str, Path] = {}
        self.loaded_plugins: Dict[str, Plugin] = {}
        self._discover_plugins()
    
    def _discover_plugins(self):
        """Discover all available plugin JSON files."""
        if not self.plugins_dir.exists():
            return
            
        # Find all JSON files in the plugins directory
        for json_file in self.plugins_dir.glob("*.json"):
            plugin_name = json_file.stem
            self.plugin_files[plugin_name] = json_file
    
    def get_available_plugins(self) -> List[str]:
        """Get list of available plugin names."""
        return list(self.plugin_files.keys())
    
    def load_plugin(self, name: str) -> Plugin:
        """Load and return a plugin instance."""
        if name not in self.loaded_plugins:
            if name in self.plugin_files:
                self.loaded_plugins[name] = Plugin(self.plugin_files[name])
            else:
                raise ValueError(f"Plugin '{name}' not found")
        return self.loaded_plugins[name]
    
    def get_plugin_info(self, name: str) -> Dict[str, str]:
        """Get basic information about a plugin."""
        if name in self.plugin_files:
            plugin = self.load_plugin(name)
            return plugin.get_command_info()
        return {}