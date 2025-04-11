# Directory Structure Analyzer

A flexible Python tool for analyzing and visualizing directory structures, counting files, and examining file contents.

## Features

- Generate visual directory tree structures
- Count files within directories
- Read and display file contents based on patterns
- Filter out specific directories, files, or content
- Generate detailed statistics about files
- Comprehensive logging
- Formatted output via PrettyTable

## Installation

### Prerequisites

- Python 3.6 or higher
- pip package manager

### Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/dirstructure.git
cd dirstructure
```

2. Create a virtual environment:

```bash
# Create virtual environment
python -m venv .venv

# Activate on Linux/Mac
source .venv/bin/activate

# Activate on Windows
# .venv\Scripts\activate
```

3. Install the package in development mode:

```bash
pip install -e .
```

## Usage

### Command Line Interface

```bash
python -m dirstructure.main --path /path/to/analyze [options]
```

### Basic Options

| Option | Description |
|--------|-------------|
| `--path PATH` | Path to the directory to analyze (required) |
| `--display {structure,count,content,all}` | What to display (default: all) |
| `--exclude [PATTERNS ...]` | Patterns to exclude (e.g., `*.log`, `.git`) |
| `--file-names [PATTERNS ...]` | File names or extensions to include content from (e.g., `*.py`, `README.md`) |
| `--exclude-strings [STRINGS ...]` | Substrings to exclude from file contents |
| `--log-file [FILE]` | Log file path (empty for default location) |
| `--log-level LEVEL` | Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: INFO) |
| `--output-file [FILE]` | Save output to file (empty for default location) |

### Examples

Display directory structure only:
```bash
python -m dirstructure.main --path ./my_project --display structure
```

Count files excluding common directories:
```bash
python -m dirstructure.main --path ./my_project --display count --exclude "__pycache__" "*.pyc" ".git"
```

Show content of Python files:
```bash
python -m dirstructure.main --path ./my_project --display content --file-names "*.py"
```

Complete analysis with verbose logging:
```bash
python -m dirstructure.main --path ./my_project --exclude "__pycache__" "*.pyc" ".git" --file-names "*.py" "*.md" --log-level DEBUG
```

## Development

### Project Structure

```
dirstructure/
├── __init__.py
├── main.py
├── utils/
│   ├── __init__.py
│   ├── logging_utils.py
│   ├── file_utils.py
│   └── display_utils.py
├── processors/
│   ├── __init__.py
│   ├── directory_processor.py
│   ├── file_processor.py
│   └── content_processor.py
```

### VS Code Integration

For VS Code users, the repository includes:
- Launch configurations for different scenarios
- Workspace settings for Python environment
- Recommended extensions

To use with VS Code:

1. Open the project in VS Code
2. Select the Python interpreter from your virtual environment (Ctrl+Shift+P → "Python: Select Interpreter")
3. Use the Run and Debug panel (Ctrl+Shift+D) to execute predefined launch configurations

## Troubleshooting

- **"Import could not be resolved" errors in VS Code**: Make sure you've installed the package in development mode and selected the correct interpreter.
- **Permission issues when saving output**: Make sure you have write permissions for the output directory.
- **Character encoding errors**: The tool assumes UTF-8 encoding for all files. Use the `--exclude` option for binary files.

## License

This project is licensed under the MIT License - see the LICENSE file for details.