#!/usr/bin/env python3
"""
Image Configuration Manager - Separation of data and procedures
Procedural Programming Paradigm: Data separate from logic
"""

import json
import os
import logging
from typing import Dict, Optional, Tuple
from urllib.parse import unquote

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageConfig:
    """
    Manages image mappings and configuration separately from business logic
    Follows procedural programming: data structure separate from procedures
    """
    
    def __init__(self, config_path: str = None):
        """Initialize with config file path"""
        if config_path is None:
            # Default path relative to this file
            base_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(base_dir, 'image_mappings.json')
        
        self.config_path = config_path
        self._mappings_cache = None
        self._settings_cache = None
        self._patterns_cache = None
        self._load_time = None
        
        logger.info(f"ImageConfig initialized with: {config_path}")
    
    def load_config(self) -> bool:
        """
        Load configuration from JSON file
        Returns True if successful, False otherwise
        """
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Separate data into logical groups
            self._mappings_cache = self._flatten_mappings(config)
            self._settings_cache = config.get('settings', {})
            self._patterns_cache = config.get('patterns', {})
            self._load_time = os.path.getmtime(self.config_path)
            
            logger.info(f"Configuration loaded: {len(self._mappings_cache)} mappings")
            return True
            
        except FileNotFoundError:
            logger.error(f"Config file not found: {self.config_path}")
            return False
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            return False
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return False
    
    def _flatten_mappings(self, config: Dict) -> Dict[str, str]:
        """
        Flatten nested mapping structure to flat dictionary
        Improves lookup performance from O(n*m) to O(1)
        """
        flat_mappings = {}
        
        # Process each category
        categories = ['profile_images', 'project_images', 'ui_images', 'blog_images']
        
        for category in categories:
            if category in config:
                for original, optimized in config[category].items():
                    # Add original mapping
                    flat_mappings[original] = optimized
                    
                    # Add Projects/ prefix for project images
                    if category == 'project_images':
                        flat_mappings[f"Projects/{original}"] = optimized
                        
                        # Add space version for compatibility
                        spaced_original = original.replace('_', ' ')
                        flat_mappings[f"Projects/{spaced_original}"] = optimized
        
        return flat_mappings
    
    def get_mapping(self, image_path: str) -> Optional[str]:
        """
        Get optimized image path for original image path
        Uses efficient O(1) lookup with caching
        """
        # Check if cache needs refresh
        if self._needs_refresh():
            self.load_config()
        
        if not self._mappings_cache:
            return None
        
        # Try direct lookup first (fastest)
        if image_path in self._mappings_cache:
            return self._mappings_cache[image_path]
        
        # Try with URL decoding
        decoded_path = unquote(image_path)
        if decoded_path in self._mappings_cache:
            return self._mappings_cache[decoded_path]
        
        # Try pattern-based matching (fallback)
        return self._pattern_match(image_path)
    
    def _pattern_match(self, image_path: str) -> Optional[str]:
        """
        Pattern-based matching for dynamic image resolution
        More efficient than hardcoded mappings for predictable patterns
        """
        if not self._patterns_cache:
            return None
        
        # Project pattern: Projects/Name_Cover.png -> images/optimized/projects/name.jpg
        if image_path.startswith('Projects/'):
            filename = image_path.replace('Projects/', '')
            if filename.endswith('_COVER.png'):
                base_name = filename.replace('_COVER.png', '').lower()
                return f"images/optimized/projects/{base_name}.jpg"
        
        # Blog pattern: Name_Cover.png -> images/optimized/blog/Name.jpg
        if image_path.endswith('_Cover.png'):
            base_name = image_path.replace('_Cover.png', '')
            return f"images/optimized/blog/{base_name}.jpg"
        
        return None
    
    def _needs_refresh(self) -> bool:
        """Check if configuration needs to be reloaded"""
        if not self._load_time:
            return True
        
        try:
            current_mtime = os.path.getmtime(self.config_path)
            return current_mtime > self._load_time
        except OSError:
            return True
    
    def get_all_mappings(self) -> Dict[str, str]:
        """Get all mappings (for debugging/reporting)"""
        if self._needs_refresh():
            self.load_config()
        return self._mappings_cache.copy() if self._mappings_cache else {}
    
    def validate_mappings(self, static_root: str) -> Tuple[int, int]:
        """
        Validate that optimized files exist
        Returns: (total_mappings, valid_mappings)
        """
        if not self._mappings_cache:
            self.load_config()
        
        total = len(self._mappings_cache)
        valid = 0
        
        for original, optimized in self._mappings_cache.items():
            optimized_path = os.path.join(static_root, optimized)
            if os.path.exists(optimized_path):
                valid += 1
            else:
                logger.warning(f"Missing optimized file: {optimized}")
        
        return total, valid
    
    def get_settings(self) -> Dict:
        """Get configuration settings"""
        if self._needs_refresh():
            self.load_config()
        return self._settings_cache.copy() if self._settings_cache else {}
    
    def get_patterns(self) -> Dict:
        """Get pattern definitions"""
        if self._needs_refresh():
            self.load_config()
        return self._patterns_cache.copy() if self._patterns_cache else {}


# Global instance for singleton pattern (efficient for web requests)
_image_config = None

def get_image_config() -> ImageConfig:
    """Get global image configuration instance"""
    global _image_config
    if _image_config is None:
        _image_config = ImageConfig()
        _image_config.load_config()
    return _image_config