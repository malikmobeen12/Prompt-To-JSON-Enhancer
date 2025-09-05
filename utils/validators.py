"""
Validation utilities for prompt processing
"""

import hashlib


def validate_prompt(prompt):
    """
    Validate the input prompt for basic requirements.
    
    Args:
        prompt (str): The input prompt to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if not prompt or not isinstance(prompt, str):
        return False, "Prompt must be a non-empty string"
    
    if len(prompt.strip()) < 3:
        return False, "Prompt must be at least 3 characters long"
    
    if len(prompt) > 5000:
        return False, "Prompt must be less than 5000 characters"
    
    return True, None


def get_cache_key(prompt):
    """
    Generate a cache key for the prompt.
    
    Args:
        prompt (str): The input prompt
        
    Returns:
        str: MD5 hash of the normalized prompt
    """
    return hashlib.md5(prompt.lower().strip().encode()).hexdigest()
