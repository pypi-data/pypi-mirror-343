import json
import os
from termcolor import colored

class ModelManager:
    """Manages AI model configurations for the assistant."""
    
    MODELS_FILE = os.path.join(os.path.dirname(__file__), "config/models.json")
    
    @classmethod
    def get_models(cls):
        """Get all available models."""
        try:
            if not os.path.exists(cls.MODELS_FILE):
                cls._create_default_models()
                
            with open(cls.MODELS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("models", {})
        except Exception as e:
            print(colored(f"Error loading models: {str(e)}", "red"))
            return {}
    
    @classmethod
    def get_current_model(cls):
        """Get the name of the current model."""
        try:
            with open(cls.MODELS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("current_model", "gpt-4o")
        except Exception:
            return "gpt-4o"
    
    @classmethod
    def set_current_model(cls, model_name):
        """Set the current model."""
        try:
            with open(cls.MODELS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            data["current_model"] = model_name
            
            with open(cls.MODELS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
                
            return True
        except Exception as e:
            print(colored(f"Error setting current model: {str(e)}", "red"))
            return False
    
    @classmethod
    def add_model(cls, name, model_config):
        """Add a new model or update an existing one."""
        try:
            with open(cls.MODELS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            data["models"][name] = model_config
            
            with open(cls.MODELS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
                
            return True
        except Exception as e:
            print(colored(f"Error adding model: {str(e)}", "red"))
            return False
    
    @classmethod
    def get_model_config(cls, model_name):
        """Get configuration for a specific model."""
        models = cls.get_models()
        return models.get(model_name, None)
    
    @classmethod
    def _create_default_models(cls):
        """Create default models if the file doesn't exist."""
        default_data = {
            "current_model": "gpt-4o",
            "models": {
                "gpt-4o": {
                    "model": "gpt-4o",
                    "temp": 0.7,
                    "max_tokens": 4096,
                    "top_p": 1
                },
                "gpt-4o-mini": {
                    "model": "gpt-4o-mini",
                    "temp": 0.7,
                    "max_tokens": 4096,
                    "top_p": 1
                },
                "claude-3-5-sonnet": {
                    "model": "claude-3-5-sonnet-20240620",
                    "temp": 0.7,
                    "max_tokens": 4096,
                    "top_p": 1
                },
                "claude-3-opus": {
                    "model": "claude-3-opus-20240229",
                    "temp": 0.7,
                    "max_tokens": 4096,
                    "top_p": 1
                }
            }
        }
        
        os.makedirs(os.path.dirname(cls.MODELS_FILE), exist_ok=True)
        
        with open(cls.MODELS_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, indent=2)