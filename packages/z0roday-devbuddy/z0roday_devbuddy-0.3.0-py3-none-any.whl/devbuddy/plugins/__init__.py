"""
Plugin system for DevBuddy.
Plugins can extend the core functionality with custom commands.
"""

import os
import importlib
import sys

def discover_plugins():
    """Discover all installed plugins."""
    plugin_dir = os.path.dirname(__file__)
    plugins = []
    
    # Look for plugin directories (excluding __pycache__ etc.)
    for name in os.listdir(plugin_dir):
        if name.startswith('__'):
            continue
            
        plugin_path = os.path.join(plugin_dir, name)
        if os.path.isdir(plugin_path) and os.path.exists(os.path.join(plugin_path, '__init__.py')):
            plugins.append(name)
            
    return plugins

def load_plugin(plugin_name):
    """Load a plugin by name."""
    try:
        module_path = f"devbuddy.plugins.{plugin_name}"
        return importlib.import_module(module_path)
    except ImportError as e:
        print(f"Error loading plugin {plugin_name}: {e}")
        return None

def register_plugin_commands(cli_group):
    """Register commands from all available plugins with the CLI."""
    plugins = discover_plugins()
    
    for plugin_name in plugins:
        plugin = load_plugin(plugin_name)
        if plugin and hasattr(plugin, 'register_commands'):
            try:
                plugin.register_commands(cli_group)
                print(f"Loaded plugin: {plugin_name}")
            except Exception as e:
                print(f"Error registering commands from plugin {plugin_name}: {e}") 