import os
import yaml
from typing import Dict, Any, Optional

class Config:
    """Configuration management for the SEA system."""
    
    DEFAULT_CONFIG_PATH = "config/config.yaml"
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration from file."""
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not os.path.exists(self.config_path):
            return self._create_default_config()
            
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create and save default configuration."""
        default_config = {
            "llm": {
                "default_provider": "openai",
                "providers": {
                    "openai": {
                        "model": "gpt-4",
                        "temperature": 0.7
                    },
                    "anthropic": {
                        "model": "claude-2",
                        "temperature": 0.7
                    },
                    "mistral": {
                        "model": "mistral-large",
                        "temperature": 0.7
                    },
                    "groq": {
                        "model": "groq-large",
                        "temperature": 0.7
                    },
                    "gemini": {
                        "model": "gemini-pro",
                        "temperature": 0.7
                    }
                }
            },
            "tools": {
                "code_analysis": {
                    "default_language": "python",
                    "linting_rules": "strict"
                },
                "simulation": {
                    "default_engine": "numpy",
                    "precision": "double"
                },
                "documentation": {
                    "default_format": "markdown",
                    "auto_generate": True
                }
            },
            "security": {
                "api_key_env_prefix": "SEA_",
                "encryption_enabled": True
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        }
        
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            yaml.dump(default_config, f)
            
        return default_config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
                
        return value if value is not None else default
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            config = config.setdefault(k, {})
            
        config[keys[-1]] = value
        
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f)
