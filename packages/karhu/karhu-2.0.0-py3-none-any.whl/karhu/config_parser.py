# src/config_parser.py
import json
import yaml
from termcolor import colored

class ConfigParser:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config_data = self.load_config()

    def load_config(self):
        try:
            if self.config_file.endswith('.json'):
                with open(self.config_file, 'r', encoding='utf-8') as file:
                    return json.load(file)
            elif self.config_file.endswith('.yaml') or self.config_file.endswith('.yml'):
                with open(self.config_file, 'r', encoding='utf-8') as file:
                    return yaml.safe_load(file)
            else:
                raise ValueError("Unsupported configuration file format")
        except Exception as e:
            print(f"Error loading configuration file: {str(e)}")
            return {}

    def get_profile(self, profile_name):
        """
        Retrieve the profile data for the given profile name.

        Args:
            profile_name (str): The name of the profile to retrieve.

        Returns:
            dict: The profile data if found, otherwise an empty dictionary.
        """
        cleaned_profile_name = profile_name.strip()
        profiles = self.config_data.get('profiles', {})
        if cleaned_profile_name not in profiles:
            print(colored(f"\n ⅹ Profile '{cleaned_profile_name}' does not exist.", "red"))
            return {}
        return profiles.get(cleaned_profile_name, {})