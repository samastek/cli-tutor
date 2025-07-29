# Utility Master - Interactive CLI Learning Tool

An educational Python CLI tool that helps users learn command-line utilities through interactive tasks and repetitive practice.

## Features

- Interactive learning sessions for various CLI utilities
- Modular plugin system for easy extension
- Task-based learning with feedback
- Progress tracking and scoring
- Support for multiple utilities (ls, grep, find, etc.)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python utility_master.py
```

## Plugin Development

Create new plugins by adding Python files to the `plugins/` directory. Each plugin should define a class that inherits from `BasePlugin` and implements the required methods.

## Project Structure

```
utility-master/
├── utility_master.py          # Main CLI entry point
├── core/
│   ├── __init__.py
│   ├── plugin_manager.py      # Plugin loading and management
│   ├── base_plugin.py         # Base plugin class
│   ├── task_manager.py        # Task execution and validation
│   └── ui.py                  # User interface components
├── plugins/
│   ├── __init__.py
│   ├── ls_plugin.py           # ls command plugin
│   └── grep_plugin.py         # grep command plugin
├── data/
│   └── test_files/            # Test files for practice
└── requirements.txt
```
