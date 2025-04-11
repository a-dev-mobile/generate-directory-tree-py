"""
File processing functionality for directory structure analysis.
"""

import os
from utils.file_utils import match_pattern

def count_files_in_directory(path, exclude_patterns, logger=None):
    """
    Count files in a directory and its subdirectories.
    
    Args:
        path (str): Directory path
        exclude_patterns (list): Patterns to exclude
        logger (logging.Logger): Logger for debug information
        
    Returns:
        int: Number of files
    """
    count = 0
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not match_pattern(exclude_patterns, os.path.join(root, d))]
        files = [f for f in files if not match_pattern(exclude_patterns, os.path.join(root, f))]
        count += len(files)
    
    if logger:
        logger.debug(f"Counted {count} files in {path}")
        
    return count

def get_file_character_counts(file_paths, base_path, exclude_patterns, logger=None):
    """
    Get character counts for a list of files.
    
    Args:
        file_paths (list): List of file paths
        base_path (str): Base directory for relative path calculation
        exclude_patterns (list): Patterns to exclude
        logger (logging.Logger): Logger for debug information
        
    Returns:
        tuple: (list of tuples (char_count, relative_path), total character count)
    """
    file_char_counts = []
    total_chars = 0
    
    for file_path in file_paths:
        # Check if file is excluded by patterns
        if match_pattern(exclude_patterns, file_path):
            if logger:
                logger.debug(f"Excluded from character count: {file_path}")
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                char_count = len(content)
                total_chars += char_count
                relative_path = os.path.relpath(file_path, base_path)
                file_char_counts.append((char_count, relative_path))
                
                if logger:
                    logger.debug(f"Counted {char_count} characters in {file_path}")
                    
        except Exception as e:
            if logger:
                logger.error(f"Failed to read {file_path}: {e}")
                
    return file_char_counts, total_chars