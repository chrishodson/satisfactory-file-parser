# Python Wrapper for Satisfactory File Parser

This document provides instructions on how to use the Python wrapper for the Satisfactory File Parser.

## Installation

To use the Python wrapper, you need to install `pyodide`. You can do this using the following command:

```bash
pip install pyodide
```

## Usage

The Python wrapper allows you to parse and write Satisfactory save files and blueprints using the existing TypeScript code. Below are some examples of how to use the wrapper.

### Parsing a Save File

```python
from python_wrapper import parse_save

save = parse_save('path/to/save/file.sav')
print(save)
```

### Writing a Save File

```python
from python_wrapper import write_save

save = parse_save('path/to/save/file.sav')
write_save(save, 'path/to/output/file.sav')
```

### Parsing a Blueprint

```python
from python_wrapper import parse_blueprint

blueprint = parse_blueprint('path/to/blueprint/file.sbp', 'path/to/config/file.sbpcfg')
print(blueprint)
```

### Writing a Blueprint

```python
from python_wrapper import write_blueprint

blueprint = parse_blueprint('path/to/blueprint/file.sbp', 'path/to/config/file.sbpcfg')
write_blueprint(blueprint, 'path/to/output/file.sbp', 'path/to/output/file.sbpcfg')
```

## API Reference

### `parse_save(file_path: str) -> dict`

Parses a Satisfactory save file and returns the parsed data as a dictionary.

- `file_path`: The path to the save file.

### `write_save(save: dict, file_path: str) -> None`

Writes the parsed save data to a file.

- `save`: The parsed save data as a dictionary.
- `file_path`: The path to the output save file.

### `parse_blueprint(main_file_path: str, config_file_path: str) -> dict`

Parses a Satisfactory blueprint and returns the parsed data as a dictionary.

- `main_file_path`: The path to the main blueprint file.
- `config_file_path`: The path to the blueprint config file.

### `write_blueprint(blueprint: dict, main_file_path: str, config_file_path: str) -> None`

Writes the parsed blueprint data to files.

- `blueprint`: The parsed blueprint data as a dictionary.
- `main_file_path`: The path to the output main blueprint file.
- `config_file_path`: The path to the output blueprint config file.
