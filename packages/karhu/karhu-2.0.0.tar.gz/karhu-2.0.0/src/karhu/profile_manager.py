import json
import os
from termcolor import colored

class ProfileManager:
    """Manages system prompt profiles for the assistant."""
    
    PROFILES_FILE = os.path.join(os.path.dirname(__file__), "config/profiles.json")
    
    @classmethod
    def get_profiles(cls):
        """Get all available profiles."""
        try:
            if not os.path.exists(cls.PROFILES_FILE):
                cls._create_default_profiles()
                
            with open(cls.PROFILES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("profiles", {})
        except Exception as e:
            print(colored(f"Error loading profiles: {str(e)}", "red"))
            return {}
    
    @classmethod
    def get_current_profile(cls):
        """Get the name of the current profile."""
        try:
            with open(cls.PROFILES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("current_profile", "default")
        except Exception:
            return "default"
    
    @classmethod
    def set_current_profile(cls, profile_name):
        """Set the current profile."""
        try:
            with open(cls.PROFILES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            data["current_profile"] = profile_name
            
            with open(cls.PROFILES_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
                
            return True
        except Exception as e:
            print(colored(f"Error setting current profile: {str(e)}", "red"))
            return False
    
    @classmethod
    def add_profile(cls, name, system_prompt):
        """Add a new profile or update an existing one."""
        try:
            with open(cls.PROFILES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            data["profiles"][name] = {
                "system_prompt": system_prompt
            }
            
            with open(cls.PROFILES_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
                
            return True
        except Exception as e:
            print(colored(f"Error adding profile: {str(e)}", "red"))
            return False

    @staticmethod
    def create_profile(profile_name, system_prompt):
        """Create a new profile with the given name and system prompt"""
        try:
            profiles_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config/profiles.json")
            
            with open(profiles_file, 'r', encoding='utf-8') as f:
                profiles_data = json.load(f)
                
            # Add the new profile
            profiles_data["profiles"][profile_name] = {
                "system_prompt": system_prompt
            }
            
            # Write back to file
            with open(profiles_file, 'w', encoding='utf-8') as f:
                json.dump(profiles_data, f, indent=2)
                
            return True
        except Exception as e:
            print(f"Error creating profile: {str(e)}")
            return False

    @classmethod
    def _create_default_profiles(cls):
        """Create default profiles if the file doesn't exist."""
        default_data = {
            "current_profile": "default",
            "profiles": {
                "default": {
                    "system_prompt": "You are a helpful assistant."
                },
                "coder": {
                    "system_prompt": "You are a coding assistant. Provide code examples and explain technical concepts clearly."
                },
                "creative": {
                    "system_prompt": "You are a creative writing assistant. Help with storytelling, creative ideas, and expressive language."
                },
                "academic": {
                    "system_prompt": "You are an academic assistant. Provide well-researched information with citations when possible."
                }
            }
        }
        
        os.makedirs(os.path.dirname(cls.PROFILES_FILE), exist_ok=True)
        
        with open(cls.PROFILES_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, indent=2)