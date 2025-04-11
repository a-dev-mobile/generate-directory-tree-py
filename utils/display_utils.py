"""
Display utilities for directory structure analysis.
"""

from prettytable import PrettyTable

def create_directory_count_table(dir_file_count):
    """
    Create a PrettyTable for directory file counts.
    
    Args:
        dir_file_count (list): List of tuples (directory_path, file_count)
        
    Returns:
        PrettyTable: Formatted table
    """
    table = PrettyTable(["File Count", "Directory"])
    table.align["File Count"] = "r"
    table.align["Directory"] = "l"
    
    for dir_path, file_count in dir_file_count:
        table.add_row([file_count, dir_path])
        
    return table

def create_character_count_table(file_char_counts):
    """
    Create a PrettyTable for file character counts.
    
    Args:
        file_char_counts (list): List of tuples (char_count, file_path)
        
    Returns:
        PrettyTable: Formatted table
    """
    table = PrettyTable(["Character Count", "File Path"])
    table.align["Character Count"] = "r"
    table.align["File Path"] = "l"
    
    for char_count, file_path in file_char_counts:
        table.add_row([char_count, file_path])
        
    return table