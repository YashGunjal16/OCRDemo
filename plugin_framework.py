from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import importlib
import os
import json

class DocumentProcessorPlugin(ABC):
    """Base class for document processor plugins."""
    
    @abstractmethod
    def can_process(self, file_path: str) -> bool:
        """Check if this plugin can process the given file."""
        pass
    
    @abstractmethod
    def process(self, file_path: str) -> List[Dict[str, Any]]:
        """Process the document and return structured content."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of the plugin."""
        pass
    
    @property
    @abstractmethod
    def supported_extensions(self) -> List[str]:
        """Get the list of file extensions this plugin supports."""
        pass

class PluginManager:
    """Manager for document processor plugins."""
    
    def __init__(self, plugins_dir: str = "plugins"):
        """Initialize the plugin manager."""
        self.plugins_dir = plugins_dir
        self.plugins: List[DocumentProcessorPlugin] = []
        self.load_plugins()
    
    def load_plugins(self):
        """Load all plugins from the plugins directory."""
        if not os.path.exists(self.plugins_dir):
            os.makedirs(self.plugins_dir)
            return
        
        # Get all Python files in the plugins directory
        for file_name in os.listdir(self.plugins_dir):
            if file_name.endswith(".py") and not file_name.startswith("__"):
                module_name = file_name[:-3]  # Remove .py extension
                try:
                    # Import the module
                    module_path = f"{self.plugins_dir}.{module_name}"
                    module = importlib.import_module(module_path)
                    
                    # Find all classes that inherit from DocumentProcessorPlugin
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (isinstance(attr, type) and 
                            issubclass(attr, DocumentProcessorPlugin) and 
                            attr is not DocumentProcessorPlugin):
                            # Create an instance of the plugin
                            plugin = attr()
                            self.plugins.append(plugin)
                            print(f"Loaded plugin: {plugin.name}")
                except Exception as e:
                    print(f"Error loading plugin {module_name}: {e}")
    
    def get_plugin_for_file(self, file_path: str) -> Optional[DocumentProcessorPlugin]:
        """Get the appropriate plugin for the given file."""
        for plugin in self.plugins:
            if plugin.can_process(file_path):
                return plugin
        return None
    
    def process_document(self, file_path: str) -> Optional[List[Dict[str, Any]]]:
        """Process a document using the appropriate plugin."""
        plugin = self.get_plugin_for_file(file_path)
        if plugin:
            print(f"Processing {file_path} with plugin: {plugin.name}")
            return plugin.process(file_path)
        else:
            print(f"No plugin found for {file_path}")
            return None

# Example plugin implementation
class ExamplePlugin(DocumentProcessorPlugin):
    """Example plugin for demonstration purposes."""
    
    @property
    def name(self) -> str:
        return "Example Plugin"
    
    @property
    def supported_extensions(self) -> List[str]:
        return [".txt"]
    
    def can_process(self, file_path: str) -> bool:
        return file_path.lower().endswith(".txt")
    
    def process(self, file_path: str) -> List[Dict[str, Any]]:
        content = []
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line.strip():
                    content.append({
                        "text": line.strip(),
                        "line_num": i,
                        "type": "text"
                    })
        return content

# Example usage
if __name__ == "__main__":
    # Create a plugin manager
    manager = PluginManager()
    
    # Register an example plugin
    example_plugin = ExamplePlugin()
    manager.plugins.append(example_plugin)
    
    # Process a sample text file
    sample_file = "sample.txt"
    
    # Create a sample file if it doesn't exist
    if not os.path.exists(sample_file):
        with open(sample_file, 'w') as f:
            f.write("This is a sample text file.\nIt has multiple lines.\nEach line will be processed separately.")
    
    # Process the file
    result = manager.process_document(sample_file)
    
    if result:
        print(json.dumps(result, indent=2))