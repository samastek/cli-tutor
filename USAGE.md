# Utility Master - Educational CLI Learning Tool

## Overview

Utility Master is a Python-based interactive CLI learning tool designed for educational purposes. It helps users learn command-line utilities through repetitive interaction and hands-on practice with immediate feedback.

## Features

- **Interactive Learning**: Learn through hands-on practice with real command examples
- **Modular Plugin System**: Easy to extend with new utilities
- **Progressive Difficulty**: Tasks organized by beginner, intermediate, and advanced levels
- **Immediate Feedback**: Get instant feedback on your commands with scoring
- **Rich Interface**: Beautiful terminal interface (with fallback for simple environments)
- **Multiple Utilities**: Currently supports `ls` and `grep` commands with more to come

## Quick Start

### Installation

1. Clone or download the project
2. Run the setup script:
   ```bash
   python setup.py
   ```

### Running the Application

```bash
python utility_master.py
```

### Testing

To verify everything is working correctly:
```bash
python test_utility_master.py
```

## Usage Example

When you run the application, you'll see:

1. **Welcome Screen**: Introduction to Utility Master
2. **Utility Selection**: Choose which command to learn (ls, grep, etc.)
3. **Difficulty Selection**: Pick your skill level (beginner, intermediate, advanced, all)
4. **Interactive Tasks**: Complete tasks with immediate feedback
5. **Progress Tracking**: See your score and completion rate

### Sample Workflow

```
🚀 Welcome to Utility Master!
Available Utilities:
• ls         - Learn the ls command for listing directory contents
• grep       - Learn the grep command for searching text patterns

Select a utility: ls
Select difficulty: beginner

Task 1/3 - Beginner
Objective: List the contents of the current directory
💻 Enter your command: ls
✅ Correct! Score: 100/100
```

## Supported Commands

### ls Command
Learn to use the `ls` command with various options:
- Basic listing: `ls`
- Long format: `ls -l`
- Show hidden files: `ls -a`
- Human-readable sizes: `ls -lh`
- Sort by time: `ls -t`
- And more...

### grep Command
Learn to search text with `grep`:
- Basic search: `grep pattern file`
- Case-insensitive: `grep -i pattern file`
- Line numbers: `grep -n pattern file`
- Invert match: `grep -v pattern file`
- Word boundaries: `grep -w pattern file`
- And more...

## Creating New Plugins

To add support for a new command, create a plugin in the `plugins/` directory:

```python
# plugins/find_plugin.py
from core.base_plugin import BasePlugin, Task, TaskResult

class FindPlugin(BasePlugin):
    def get_name(self) -> str:
        return "Find Command Learning Plugin"
    
    def get_utility_name(self) -> str:
        return "find"
    
    def get_description(self) -> str:
        return "Learn the find command for searching files and directories"
    
    def get_tasks(self, difficulty: str = "all") -> List[Task]:
        # Define your tasks here
        pass
    
    def validate_task(self, task: Task, user_input: str) -> TaskResult:
        # Implement validation logic
        pass
```

## Project Structure

```
utility-master/
├── utility_master.py          # Main CLI entry point
├── setup.py                   # Setup and installation script
├── test_utility_master.py     # Test suite
├── requirements.txt           # Python dependencies
├── core/                      # Core framework
│   ├── __init__.py
│   ├── plugin_manager.py      # Plugin loading and management
│   ├── base_plugin.py         # Base plugin class
│   ├── task_manager.py        # Task execution and validation
│   ├── ui.py                  # Rich-based UI components
│   └── simple_ui.py          # Fallback simple UI
├── plugins/                   # Utility plugins
│   ├── __init__.py
│   ├── ls_plugin.py          # ls command plugin
│   └── grep_plugin.py        # grep command plugin
└── data/
    └── test_files/           # Test files for practice
```

## Technical Details

### Architecture

- **Plugin Manager**: Dynamically loads plugins from the `plugins/` directory
- **Base Plugin**: Abstract base class that all plugins must inherit from
- **Task Manager**: Handles task execution, environment setup, and validation
- **UI System**: Provides both Rich-enhanced and simple fallback interfaces

### Dependencies

- **Rich**: For enhanced terminal interface (optional, falls back to simple UI)
- **Standard Library**: Most functionality uses Python standard library

### Platform Support

- **Linux/Unix**: Full support with all features
- **macOS**: Full support with all features
- **Windows**: Basic support (some commands may behave differently)

## Educational Benefits

1. **Hands-on Learning**: Learn by doing, not just reading
2. **Immediate Feedback**: Get instant validation and tips
3. **Progressive Difficulty**: Start simple and advance gradually
4. **Repetitive Practice**: Reinforce learning through repetition
5. **Safe Environment**: Practice without fear of breaking anything

## Contributing

To add new plugins or improve existing ones:

1. Follow the plugin architecture defined in `core/base_plugin.py`
2. Add comprehensive tasks for different difficulty levels
3. Include helpful hints and detailed feedback
4. Test your plugin thoroughly

## Future Enhancements

- Support for more utilities (find, awk, sed, curl, etc.)
- Progress tracking and user profiles
- Adaptive difficulty based on performance
- Command history and replay
- Integration with real file systems for practice

## License

This project is intended for educational purposes. Feel free to modify and extend it for your learning needs.
