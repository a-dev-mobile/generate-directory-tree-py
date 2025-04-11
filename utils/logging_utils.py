"""
Logging utilities for directory structure analysis.
"""

import os
import logging
from datetime import datetime

def setup_logging(log_file, directory, log_level):
    """
    Setup logging configuration.
    
    Args:
        log_file (str): Path to log file, if None logs to console
        directory (str): Directory to save default log file in if log_file is empty string
        log_level (str): Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        logging.Logger: Configured logger
    """
    if log_file == "":
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(directory, f"directory_structure_log_{timestamp}.log")
    
    log_level = getattr(logging, log_level.upper(), logging.INFO)
    
    if log_file:
        logging.basicConfig(level=log_level, 
                          format='%(asctime)s - %(levelname)s - %(message)s', 
                          filename=log_file, 
                          filemode='w')
    else:
        logging.basicConfig(level=log_level, 
                          format='%(asctime)s - %(levelname)s - %(message)s')
    
    logger = logging.getLogger(__name__)
    return logger