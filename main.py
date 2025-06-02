#!/usr/bin/env python3

import os
import argparse
from datetime import datetime

from utils.logging_utils import setup_logging
from processors.directory_processor import generate_directory_structure
from processors.file_processor import count_files_in_directory, get_file_character_counts
from processors.content_processor import read_files_with_names_or_extensions
from utils.display_utils import create_directory_count_table, create_character_count_table

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Generate directory structure")
    parser.add_argument("--path", required=True, help="Path to the directory")
    parser.add_argument("--exclude", nargs='*', default=[], help="List of patterns to exclude directories/files")
    parser.add_argument("--file-names", nargs='*', default=[], help="List of specific file names or extensions to include content from")
    parser.add_argument("--exclude-strings", nargs='*', default=[], help="List of substrings to exclude lines containing them from file contents")
    parser.add_argument("--log-file", nargs='?', const="", help="File to save log to, if not specified logs to console, if specified but empty logs to default file in the parsed directory")
    parser.add_argument("--log-level", default="INFO", help="Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
    parser.add_argument("--output-file", nargs='?', const="", help="File to save output to, if specified but empty saves to default file in the parsed directory")
    parser.add_argument("--display", choices=['structure', 'count', 'content', 'all'], default='all', help="Display Directory Structure, Directory File Count, Files Content, or all")
    return parser.parse_args()



def format_output_header(args):
    """Create a formatted header for the output."""
    header = f"""
DIRECTORY STRUCTURE ANALYSIS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Analysis Path: {os.path.abspath(args.path)}
Display Mode: {args.display}
"""
    if args.file_names:
        header += f"File Patterns: {', '.join(args.file_names)}\n"
    if args.exclude:
        header += f"Excluded Patterns: {', '.join(args.exclude)}\n"
    if args.exclude_strings:
        header += f"Content Filters: {', '.join(args.exclude_strings)}\n"
    
    header += f"\n"
    return header

def format_section_divider(title):
    """Create a formatted section divider."""
    return f"\n\n{title.upper()}\n"
def main():
    """
    Main function to run the directory structure analyzer.
    """
    args = parse_arguments()

    directory = args.path if os.path.isdir(args.path) else os.path.dirname(args.path)
    log_file = args.log_file
    if args.log_file == "":
        log_file = os.path.join(directory, f"directory_structure_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    logger = setup_logging(log_file, directory, args.log_level)

    logger.info(f"Selected path for scanning: {args.path}")
    if args.file_names:
        logger.info(f"File names or extensions to include: {', '.join(args.file_names)}")
    if args.exclude_strings:
        logger.info(f"Substrings to exclude from file contents: {', '.join(args.exclude_strings)}")

    if not os.path.isdir(args.path):
        logger.error(f"{args.path} is not a valid directory")
        print(f"Error: {args.path} is not a valid directory.")
        if log_file:
            print(f"Please check the log file at {os.path.abspath(log_file)} for more details.")
        return

    output = format_output_header(args)
    processed_files = []

    try:
        exclude_patterns = args.exclude
        exclude_strings = args.exclude_strings

        # Generate directory structure if requested
        if args.display in ['structure', 'all']:
            last_folder_name = os.path.basename(os.path.normpath(args.path))
            logger.info(f"Generating directory structure for {args.path}")
            directory_structure = f"{last_folder_name}/\n" + generate_directory_structure(args.path, exclude_patterns, "    ", logger=logger)
            output += format_section_divider("Directory Structure")
            output += directory_structure

        # Read file contents if requested
        if args.display in ['content', 'all'] and args.file_names:
            logger.info("Reading files with specified names or extensions")
            file_content, processed_files = read_files_with_names_or_extensions(args.path, args.file_names, exclude_patterns, exclude_strings, logger)
            output += format_section_divider("Files Content")
            output += file_content

        # Count files in directories if requested
        if args.display in ['count', 'all']:
            dir_file_count = []
            total_files = 0
            for root, dirs, files in os.walk(args.path):
                from utils.file_utils import match_pattern
                dirs[:] = [d for d in dirs if not match_pattern(exclude_patterns, os.path.join(root, d))]
                for d in dirs:
                    dir_path = os.path.join(root, d)
                    file_count = count_files_in_directory(dir_path, exclude_patterns, logger)
                    dir_file_count.append((dir_path, file_count))
                    total_files += file_count

            dir_file_count.sort(key=lambda x: x[1], reverse=True)
            table = create_directory_count_table(dir_file_count)
            output += format_section_divider(f"Directory File Count (Total: {total_files})")
            output += str(table) + "\n"

        # Generate character counts for processed files if in 'all' mode
        if args.display == 'all':
            if processed_files:
                logger.info("Generating file character count table for processed files")
                file_char_counts, total_chars = get_file_character_counts(processed_files, args.path, exclude_patterns, logger=logger)
                file_char_counts.sort(key=lambda x: x[0], reverse=True)

                table = create_character_count_table(file_char_counts)
                output += format_section_divider(f"File Character Counts (Total: {total_chars:,} characters)")
                output += str(table)
            else:
                logger.info("No files processed for character counts.")
                output += format_section_divider("File Character Counts")
                output += "\nNo files matched the specified file names or extensions."
        output += f"\nANALYSIS COMPLETED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        # Save output to file if requested
        if args.output_file is not None:
            if args.output_file == "":
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_filename = f"directory_structure_{timestamp}.txt"
            else:
                output_filename = args.output_file

            output_file_path = output_filename if os.path.isabs(output_filename) else os.path.join(args.path, output_filename)

            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(output)
            
            # Use absolute paths for better clickability
            abs_output_path = os.path.abspath(output_file_path)
            print(f"Output saved to {abs_output_path}")
            logger.info(f"Output saved to {abs_output_path}")
        else:
            print(output)

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print(f"An error occurred.")
        if log_file:
            abs_log_path = os.path.abspath(log_file)
            print(f"Please check the log file at {abs_log_path} for more details.")
    finally:
        logger.info("Script has finished execution.")
        if log_file:
            abs_log_path = os.path.abspath(log_file)
            print(f"Log file saved to {abs_log_path}")

if __name__ == "__main__":
    main()