#!/usr/bin/env python3
# MalinaPet - Configuration settings

import os
import json
import time

class Config:
    def __init__(self):
        self.config_path = "/home/anna/Desktop/MalinaPet/config.json"
        self.default_config = {
            "openai_api_key": "",
            "first_run": True,
            "last_pet_type": None,
            "last_pet_name": None
        }
        self.config = self.default_config.copy()
        self.load()
        
    def load(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                    # Update config with loaded values
                    for key, value in loaded_config.items():
                        if key in self.config:
                            self.config[key] = value
        except Exception as e:
            print(f"Error loading config: {e}")
            # Use default config if loading fails
            self.config = self.default_config.copy()
            
    def save(self):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f)
        except Exception as e:
            print(f"Error saving config: {e}")
            
    def get(self, key, default=None):
        """Get a configuration value"""
        return self.config.get(key, default)
        
    def set(self, key, value):
        """Set a configuration value and save to file"""
        if key in self.config:
            self.config[key] = value
            self.save()
            
    def check_api_key(self):
        """Check if an OpenAI API key is set"""
        return bool(self.config.get("openai_api_key", ""))
