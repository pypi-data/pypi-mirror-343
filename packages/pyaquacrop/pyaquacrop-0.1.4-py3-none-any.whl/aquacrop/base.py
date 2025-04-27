import os
import re

class AquaCropFile:
    """Base class for all AquaCrop file types"""
    
    def __init__(self, name: str, description: str = ""):
        self.name = "".join(name.split())
        self.description = description
        self.version = "7.1"  # AquaCrop version (August 2023)
    
    def set_version(self, version: str):
        """Set AquaCrop version"""
        self.version = version
        return self
    
    def write(self, directory: str = "."):
        """Write file to directory"""
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, self.name)
        with open(filepath, "w") as f:
            f.write(self.to_string())
        print(f"File written to {filepath}")
        return filepath
        
    @classmethod
    def from_file(cls, filepath):
        """Create an instance from an existing file"""
        raise NotImplementedError("Subclasses must implement from_file method")
        
    def parse_version(self, line):
        """Extract AquaCrop version from a line"""
        match = re.search(r'(\d+\.\d+)\s*:\s*AquaCrop Version', line)
        if match:
            return match.group(1)
        return self.version
    
    def to_string(self):
        """Convert to string representation"""
        raise NotImplementedError("Subclasses must implement to_string method")
