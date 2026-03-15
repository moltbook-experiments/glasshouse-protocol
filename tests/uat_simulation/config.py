import yaml
import os
from typing import Dict, Any, Optional
from pathlib import Path

class SimulationConfig:
    """Configuration manager for UAT simulation parameters."""

    DEFAULT_CONFIG = {
        'simulation': {
            'duration_seconds': 300,
            'num_requesters': 5,
            'num_workers': 10,
            'num_verifiers': 3,
            'concurrency_level': 10
        },
        'agents': {
            'base_url': 'http://127.0.0.1:8000',
            'api_tokens': [],  # List of tokens for different agents
            'proficiency_distribution': {
                'beginner': 0.3,
                'intermediate': 0.5,
                'expert': 0.2
            }
        },
        'jobs': {
            'types': [
                {'name': 'data_analysis', 'complexity': 2.0, 'payment': 10},
                {'name': 'content_generation', 'complexity': 1.5, 'payment': 8},
                {'name': 'code_development', 'complexity': 3.0, 'payment': 15},
                {'name': 'financial_modeling', 'complexity': 2.5, 'payment': 12}
            ],
            'posting_interval_seconds': 5,
            'max_concurrent_jobs': 20
        },
        'logging': {
            'level': 'INFO',
            'format': 'json',
            'file': 'uat_simulation.log'
        }
    }

    def __init__(self, config_file: Optional[str] = None):
        self.config = self.DEFAULT_CONFIG.copy()
        if config_file:
            self.load_config(config_file)

    def load_config(self, config_file: str) -> None:
        """Load configuration from YAML file."""
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file not found: {config_file}")

        with open(config_file, 'r') as f:
            user_config = yaml.safe_load(f)

        # Deep merge user config with defaults
        self._deep_merge(self.config, user_config)

    def _deep_merge(self, base: Dict[str, Any], update: Dict[str, Any]) -> None:
        """Deep merge update dict into base dict."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-separated key."""
        keys = key.split('.')
        value = self.config
        try:
            for k in keys:
                value = value[k]
            return value
        except KeyError:
            return default

    def set(self, key: str, value: Any) -> None:
        """Set configuration value by dot-separated key."""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value

    def save_config(self, config_file: str) -> None:
        """Save current configuration to YAML file."""
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)

    def create_default_config(self, config_file: str) -> None:
        """Create a default configuration file."""
        self.save_config(config_file)

# Global config instance
config = SimulationConfig()