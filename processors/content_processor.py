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
    total_files = 0
    total_lines = 0
    
    # Collect all matching files first
    matching_files = []
    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if not match_pattern(exclude_patterns, os.path.join(root, d))]
        
        for file in files:
            file_path = os.path.join(root, file)
            
            if not match_pattern(exclude_patterns, file_path):
                if names_or_extensions and match_pattern(names_or_extensions, file):
                    relative_path = os.path.relpath(file_path, base_path)
                    matching_files.append((file_path, relative_path))
    
    # Sort files by path for consistent output
    matching_files.sort(key=lambda x: x[1])
    
    # Add summary header
    content += f"Base path: {base_path}\n"
    content += f"Found {len(matching_files)} files matching patterns: {', '.join(names_or_extensions)}\n\n"
    
    # Process each file
    for file_path, relative_path in matching_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if logger:
                    logger.debug(f"Reading content of {file_path}")
                
                # Read and filter content
                file_lines = []
                original_line_count = 0
                
                for line in f:
                    original_line_count += 1
                    # Check if line should be excluded
                    should_exclude = any(substring in line for substring in exclude_strings)
                    if not should_exclude:
                        file_lines.append(line.rstrip('\n\r'))
                
                filtered_line_count = len(file_lines)
                file_content = '\n'.join(file_lines)
                
                # Add file header with metadata
                content += f"\nFile: {relative_path}\n"
                content += f"Path: {file_path}\n"
                content += f"Lines: {filtered_line_count}"
                if original_line_count != filtered_line_count:
                    content += f" (filtered from {original_line_count})"
                content += f"\nSize: {len(file_content)} characters\n\n"
                
                # Add the actual content
                if file_content.strip():  # Only add non-empty files
                    content += file_content + "\n"
                else:
                    content += "[Empty file or all content filtered]\n"
                
                processed_files.append(file_path)
                total_files += 1
                total_lines += filtered_line_count
                
        except UnicodeDecodeError:
            if logger:
                logger.warning(f"Binary file skipped: {file_path}")
            content += f"\nFile: {relative_path}\n"
            content += f"[BINARY FILE - SKIPPED]\n\n"
        except Exception as e:
            if logger:
                logger.error(f"Failed to read {file_path}: {e}")
            content += f"\nFile: {relative_path}\n"
            content += f"[ERROR READING FILE: {e}]\n\n"
    
    # Add summary footer
    content += f"\nCONTENT ANALYSIS SUMMARY\n"
    content += f"Total files processed: {total_files}\n"
    content += f"Total lines: {total_lines}\n"
    content += f"Total characters: {len(content)}\n"
    if exclude_strings:
        content += f"Excluded patterns: {', '.join(exclude_strings)}\n"
    content += f"\n"
                
    return content, processed_files