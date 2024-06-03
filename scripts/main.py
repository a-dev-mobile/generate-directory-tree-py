import os
import argparse
import re
import logging
from prettytable import PrettyTable

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def count_files_in_directory(path, exclude_patterns):
    count = 0
    for root, dirs, files in os.walk(path):
        # Check if directory or file matches exclude patterns
        dirs[:] = [d for d in dirs if not any(re.search(pattern, os.path.join(root, d)) for pattern in exclude_patterns)]
        files = [f for f in files if not any(re.search(pattern, os.path.join(root, f)) for pattern in exclude_patterns)]
        count += len(files)
    logger.debug(f"Counted {count} files in {path}")
    return count

def generate_directory_structure(path, exclude_patterns, indent="", is_last=True):
    structure = ""
    items = sorted(os.listdir(path))
    for index, item in enumerate(items):
        item_path = os.path.join(path, item)
        if any(re.search(pattern, item_path) for pattern in exclude_patterns):
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

def main():
    parser = argparse.ArgumentParser(description="Generate directory structure")
    parser.add_argument("--path", required=True, help="Path to the directory")
    parser.add_argument("--exclude", nargs='*', default=[], help="List of regex patterns to exclude directories/files")
    parser.add_argument("--log-level", default="INFO", help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
    args = parser.parse_args()

    # Set logging level based on user input
    logger.setLevel(args.log_level.upper())

    if not os.path.isdir(args.path):
        logger.error(f"{args.path} is not a valid directory")
        return

    try:
        exclude_patterns = [pattern.replace("\\", "\\\\") for pattern in args.exclude]  # Escape backslashes
        logger.info(f"Generating directory structure for {args.path}")
        directory_structure = "root/\n" + generate_directory_structure(args.path, exclude_patterns, "    ")
        print("Directory Structure:\n")
        print(directory_structure)

        dir_file_count = []
        for root, dirs, files in os.walk(args.path):
            # Check if directory matches exclude patterns
            dirs[:] = [d for d in dirs if not any(re.search(pattern, os.path.join(root, d)) for pattern in exclude_patterns)]
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

        print("\nDirectory File Count:\n")
        print(table)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        logger.info("Script has finished execution.")

if __name__ == "__main__":
    main()
