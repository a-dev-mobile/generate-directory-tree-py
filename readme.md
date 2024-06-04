# Directory Structure Generator

This script generates a directory structure, counts files in directories with specified exclusion patterns, and can read content from files with specified extensions. Additionally, it supports logging of its actions and saving output to a file.

## Requirements

---

Python 3.6+  
`prettytable` module

Install the required module using:

    pip install prettytable

## Usage

The script can be used to generate a directory structure, count files, and read file contents based on extensions. The following arguments are available:

- `--path`: Path to the directory (required).
- `--exclude`: List of regex patterns to exclude directories/files (optional).
- `--extensions`: List of file extensions to include content from (optional).
- `--log-file`: File to save log to. If not specified, logs to console. If specified but empty, logs to a default file in the parsed directory (optional).
- `--log-level`: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL) (optional).
- `--output-file`: File to save output to. If specified but empty, saves to a default file in the parsed directory (optional).

## Examples

**1\. Generate directory structure and log to console:**

    python directory_structure.py --path /path/to/directory

**2\. Generate directory structure with exclusions:**

    python directory_structure.py --path /path/to/directory --exclude 'pattern1' 'pattern2'

**3\. Read content from files with specified extensions:**

    python directory_structure.py --path /path/to/directory --extensions .txt .md

**4\. Save log to a file:**

    python directory_structure.py --path /path/to/directory --log-file /path/to/logfile.log

**5\. Save output to a file:**

    python directory_structure.py --path /path/to/directory --output-file /path/to/output.txt

### Full Example

    python directory_structure.py --path /path/to/directory --exclude 'pattern1' 'pattern2' --extensions .txt .md --log-file --output-file

This will:

- Generate the directory structure for `/path/to/directory`.
- Exclude files and directories matching `pattern1` and `pattern2`.
- Include contents of `.txt` and `.md` files.
- Save logs to a default file in the directory.
- Save output to a default file in the directory.

## Example Output

```
Directory Structure:

my_project/
    ├── README.md
    ├── src/
    │   ├── main.py
    │   ├── utils.py
    │   └── __init__.py
    ├── tests/
    │   ├── test_main.py
    │   └── __init__.py
    └── requirements.txt

Directory File Count:

+------------+-------------------------------+
| File Count | Directory                     |
+------------+-------------------------------+
| 3          | /path/to/directory/src        |
| 2          | /path/to/directory/tests      |
| 1          | /path/to/directory            |
+------------+-------------------------------+

Files Content:

========================================
Content of README.md:
========================================
# My Project

This is the README file for My Project.

========================================
Content of requirements.txt:
========================================
prettytable

```

## Logging

The script logs its actions, including errors and debug information. By default, logs are printed to the console. If a log file is specified, logs are saved to that file.

### Example Log File Setup

    python directory_structure.py --path /path/to/directory --log-file /path/to/logfile.log --log-level DEBUG

### Example Output File Setup

    python directory_structure.py --path /path/to/directory --output-file /path/to/output.txt

## Error Handling

If an error occurs, the script will log the error and print an error message. If a log file is specified, more details can be found in the log file.

## Script Execution

To execute the script, run:

    python directory_structure.py --path /path/to/directory

Replace `/path/to/directory` with the actual path of the directory you want to process.
