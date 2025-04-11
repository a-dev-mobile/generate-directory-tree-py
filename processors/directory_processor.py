"""
Directory processing functionality for directory structure analysis.
"""

import os
from utils.file_utils import match_pattern

def generate_directory_structure(path, exclude_patterns, indent="", is_last=True, logger=None):
    """
    Generate a text representation of directory structure.
    
    Args:
        path (str): Directory path to analyze
        exclude_patterns (list): Patterns to exclude
        indent (str): Current indentation level
        is_last (bool): Whether this is the last item at this level
        logger (logging.Logger): Logger for debug information
        
    Returns:
        str: Formatted directory structure as text
    """
    structure = ""
    try:
        items = sorted(os.listdir(path))
    except Exception as e:
        if logger:
            logger.error(f"Cannot list directory {path}: {e}")
        return structure

    for index, item in enumerate(items):
        item_path = os.path.join(path, item)
        
        if match_pattern(exclude_patterns, item_path):
            if logger:
                logger.debug(f"Excluded {item_path}")
            continue
            
        connector = "└── " if index == len(items) - 1 else "├── "
        
        if os.path.isdir(item_path):
            structure += indent + connector + item + "/\n"
            sub_indent = indent + ("    " if index == len(items) - 1 else "│   ")
            structure += generate_directory_structure(
                item_path, 
                exclude_patterns, 
                sub_indent, 
                index == len(items) - 1,
                logger
            )
        else:
            structure += indent + connector + item + "\n"
            
    if logger:
        logger.debug(f"Generated structure for {path}")
        
    return structure