"""
Content processing functionality for directory structure analysis.
"""

import os
from utils.file_utils import match_pattern

def read_files_with_names_or_extensions(base_path, names_or_extensions, exclude_patterns, exclude_strings, logger=None):
    """
    Read contents of files matching specified names or extensions.
    
    Args:
        base_path (str): Base directory path
        names_or_extensions (list): File names or extensions to match
        exclude_patterns (list): Patterns to exclude files/directories
        exclude_strings (list): Substrings to exclude from file content
        logger (logging.Logger): Logger for debug information
        
    Returns:
        tuple: (formatted content string, list of processed file paths)
    """
    content = ""
    processed_files = []
    
    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if not match_pattern(exclude_patterns, os.path.join(root, d))]
        
        for file in files:
            file_path = os.path.join(root, file)
            
            if not match_pattern(exclude_patterns, file_path):
                if names_or_extensions:
                    if match_pattern(names_or_extensions, file):
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                relative_path = os.path.relpath(file_path, base_path)
                                
                                if logger:
                                    logger.debug(f"Reading content of {file_path}")
                                    
                                content += f"\n{'='*40}\nContent of {relative_path}:\n{'='*40}\n"
                                
                                # Read file line by line and filter lines
                                for line in f:
                                    if not any(substring in line for substring in exclude_strings):
                                        content += line
                                        
                                content += "\n"
                                processed_files.append(file_path)
                                
                        except Exception as e:
                            if logger:
                                logger.error(f"Failed to read {file_path}: {e}")
                                
    return content, processed_files