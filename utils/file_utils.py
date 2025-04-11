"""
File utility functions for directory structure analysis.
"""

import os
import fnmatch

def match_pattern(patterns, name):
    """
    Check if file/directory name matches any of the given patterns.
    If pattern contains '*', use fnmatch for matching.
    Otherwise, check for exact match.
    
    Args:
        patterns (list): List of patterns to match against
        name (str): File or directory name to check
        
    Returns:
        bool: True if name matches any pattern, False otherwise
    """
    for pattern in patterns:
        if '*' in pattern:
            if fnmatch.fnmatch(name, pattern):
                return True
        else:
            if os.path.basename(name) == pattern:
                return True
    return False