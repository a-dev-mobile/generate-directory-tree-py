import os
import argparse
import re
import logging
from datetime import datetime
from prettytable import PrettyTable

def setup_logging(log_file, directory, log_level):
    if log_file == "":
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(directory, f"directory_structure_log_{timestamp}.log")
    
    log_level = getattr(logging, log_level.upper(), logging.INFO)
    
    if log_file:
        logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s', filename=log_file, filemode='w')
    else:
        logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    
    logger = logging.getLogger(__name__)
    return logger

def count_files_in_directory(path, exclude_patterns):
    count = 0
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not any(re.search(f"^{pattern}$", os.path.join(root, d)) for pattern in exclude_patterns)]
        files = [f for f in files if not any(re.search(f"^{pattern}$", os.path.join(root, f)) for pattern in exclude_patterns)]
        count += len(files)
    logger.debug(f"Counted {count} files in {path}")
    return count

def generate_directory_structure(path, exclude_patterns, indent="", is_last=True):
    structure = ""
    items = sorted(os.listdir(path))
    for index, item in enumerate(items):
        item_path = os.path.join(path, item)
        if any(re.search(f"^{pattern}$", item_path) for pattern in exclude_patterns):
            logger.debug(f"Excluded {item_path}")
            continue
        connector = "└── " if index == len(items) - 1 else "├── "
        if os.path.isdir(item_path):
            structure += indent + connector + item + "/\n"
            sub_indent = indent + ("    " if index == len(items) - 1 else "│   ")
            structure += generate_directory_structure(item_path, exclude_patterns, sub_indent, index == len(items) - 1)
        else:
            structure += indent + connector + item + "\n"
    logger.debug(f"Generated structure for {path}")
    return structure

def read_files_with_names_or_extensions(base_path, names_or_extensions, exclude_patterns):
    content = ""
    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if not any(re.search(f"^{pattern}$", os.path.join(root, d)) for pattern in exclude_patterns)]
        for file in files:
            file_path = os.path.join(root, file)
            if not any(re.search(f"^{pattern}$", file_path) for pattern in exclude_patterns):
                if names_or_extensions:
                    if any(file == name for name in names_or_extensions) or any(file.endswith(ext) for ext in names_or_extensions):
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                relative_path = os.path.relpath(file_path, base_path)
                                logger.debug(f"Reading content of {file_path}")
                                content += f"\n{'='*40}\nContent of {relative_path}:\n{'='*40}\n"
                                content += f.read() + "\n"
                        except Exception as e:
                            logger.error(f"Failed to read {file_path}: {e}")
                else:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            relative_path = os.path.relpath(file_path, base_path)
                            logger.debug(f"Reading content of {file_path}")
                            content += f"\n{'='*40}\nContent of {relative_path}:\n{'='*40}\n"
                            content += f.read() + "\n"
                    except Exception as e:
                        logger.error(f"Failed to read {file_path}: {e}")
    return content

def main():
    parser = argparse.ArgumentParser(description="Generate directory structure")
    parser.add_argument("--path", required=True, help="Path to the directory")
    parser.add_argument("--exclude", nargs='*', default=[], help="List of regex patterns to exclude directories/files")
    parser.add_argument("--file-names", nargs='*', default=[], help="List of specific file names or extensions to include content from")
    parser.add_argument("--log-file", nargs='?', const="", help="File to save log to, if not specified logs to console, if specified but empty logs to default file in the parsed directory")
    parser.add_argument("--log-level", default="INFO", help="Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
    parser.add_argument("--output-file", nargs='?', const="", help="File to save output to, if specified but empty saves to default file in the parsed directory")
    parser.add_argument("--display", choices=['structure', 'count', 'content', 'all'], default='all', help="Display Directory Structure, Directory File Count, Files Content, or all")
    args = parser.parse_args()

    directory = args.path if os.path.isdir(args.path) else os.path.dirname(args.path)
    log_file = args.log_file if args.log_file else None
    if args.log_file == "":
        log_file = os.path.join(directory, f"directory_structure_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    global logger
    logger = setup_logging(log_file, directory, args.log_level)

    logger.info(f"Selected path for scanning: {args.path}")
    if args.file_names:
        logger.info(f"File names or extensions to include: {', '.join(args.file_names)}")

    if not os.path.isdir(args.path):
        logger.error(f"{args.path} is not a valid directory")
        print(f"Error: {args.path} is not a valid directory.")
        if log_file:
            print(f"Please check the log file at {os.path.abspath(logger.handlers[0].baseFilename)} for more details.")
        return

    output = ""

    try:
        exclude_patterns = [pattern.replace("\\", "\\\\") for pattern in args.exclude]  # Escape backslashes
        if exclude_patterns:
            logger.info(f"Exclude patterns: {', '.join(exclude_patterns)}")

        if args.display in ['structure', 'all']:
            last_folder_name = os.path.basename(os.path.normpath(args.path))
            logger.info(f"Generating directory structure for {args.path}")
            directory_structure = f"{last_folder_name}/\n" + generate_directory_structure(args.path, exclude_patterns, "    ")
            output += "Directory Structure:\n\n"
            output += directory_structure

        if args.display in ['content', 'all'] and args.file_names:
            logger.info("Reading files with specified names or extensions")
            file_content = read_files_with_names_or_extensions(args.path, args.file_names, exclude_patterns)
            output += "\nFiles Content:\n"
            output += file_content

        if args.display in ['count', 'all']:
            dir_file_count = []
            for root, dirs, files in os.walk(args.path):
                # Check if directory matches exclude patterns
                dirs[:] = [d for d in dirs if not any(re.search(f"^{pattern}$", os.path.join(root, d)) for pattern in exclude_patterns)]
                for d in dirs:
                    dir_path = os.path.join(root, d)
                    file_count = count_files_in_directory(dir_path, exclude_patterns)
                    dir_file_count.append((dir_path, file_count))

            dir_file_count.sort(key=lambda x: x[1], reverse=True)

            table = PrettyTable(["File Count", "Directory"])
            table.align["File Count"] = "l"
            table.align["Directory"] = "l"
            for dir_path, file_count in dir_file_count:
                table.add_row([file_count, dir_path])

            output += "\nDirectory File Count:\n\n"
            output += str(table)

        if args.output_file is not None:
            if args.output_file == "":
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_filename = f"directory_structure_{timestamp}.txt"
            else:
                output_filename = args.output_file

            output_file_path = output_filename if os.path.isabs(output_filename) else os.path.join(args.path, output_filename)

            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Output saved to {output_file_path}")
            logger.info(f"Output saved to {output_file_path}")
        else:
            print(output)

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print(f"An error occurred.")
        if log_file:
            print(f"Please check the log file at {os.path.abspath(logger.handlers[0].baseFilename)} for more details.")
    finally:
        logger.info("Script has finished execution.")
        if log_file:
            print(f"Log file saved to {log_file}")

if __name__ == "__main__":
    main()
