import yaml
from typing import Dict, Any, List, Tuple
import os

class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """Load configuration from YAML file."""
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
    
    @property
    def marker_color(self) -> Tuple[int, int, int]:
        """Get the marker color."""
        return tuple(self.config['marker']['color'])
    
    @property
    def color_tolerance(self) -> int:
        """Get the color matching tolerance."""
        return self.config['marker']['tolerance']
    
    @property
    def supported_extensions(self) -> List[str]:
        """Get supported image extensions."""
        return self.config['image']['supported_extensions']
    
    @property
    def json_version(self) -> str:
        """Get JSON export version."""
        return self.config['export']['json']['version']
    
    @property
    def json_indent(self) -> int:
        """Get JSON export indentation."""
        return self.config['export']['json']['indent']
    
    @property
    def motion_error_threshold(self) -> float:
        """Get motion error threshold."""
        return self.config['motion']['error_threshold']
