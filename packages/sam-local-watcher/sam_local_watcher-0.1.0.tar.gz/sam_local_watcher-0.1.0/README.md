# SAM Local Watcher

A utility for watching and syncing AWS SAM local development files.

## Overview

SAM Local Watcher monitors your AWS SAM project files and automatically syncs changes to the `.aws-sam/build` directory. This eliminates the need to rebuild your SAM application after every code change, making local development faster and more efficient.

## Installation

```bash
pip install sam-local-watcher
```

## Usage

### Command Line

```bash
# Watch the current directory using the default template.yaml
sam-watcher

# Watch a specific directory
sam-watcher --path /path/to/sam/project

# Use a different template file
sam-watcher --template sam-template.yaml
```

### Python API

```python
from sam_local_watcher import watch_folder

# Watch the current directory
watch_folder(".", "template.yaml")

# Watch a specific directory with a custom template
watch_folder("/path/to/sam/project", "/path/to/template.yaml")
```

## How It Works

1. SAM Local Watcher parses your SAM template to identify all Lambda functions
2. It creates a mapping between your source code directories and the corresponding functions
3. When a file is modified, it automatically copies the changes to the appropriate location in the `.aws-sam/build` directory

## Supported File Types

Currently, the watcher syncs files with the following extensions:
- `.py` (Python)
- `.js` (JavaScript)
- `.json` (JSON)
- `.txt` (Text)

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
