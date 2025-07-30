# CLI Tutor - AI Coding Instructions

## Project Overview
CLI Tutor is an interactive educational tool built with Python that teaches command-line utilities through hands-on practice. The architecture follows a modular plugin system where each CLI command is implemented as a JSON-defined plugin.

## Core Architecture

### Plugin-Based Learning System
- **Plugin Manager** (`cli_tutor/core/plugin_manager.py`): Discovers and loads JSON plugin files from `cli_tutor/plugins/`
- **Plugin Class** (`cli_tutor/core/plugin.py`): Wraps JSON plugin data into Python objects with Task and Plugin classes
- **Tutor Engine** (`cli_tutor/core/tutor.py`): Orchestrates the interactive learning session using Rich for UI

### Key Design Patterns

**JSON-Driven Configuration**: All learning content is defined in JSON files (e.g., `ls.json`, `grep.json`) rather than hardcoded Python. This enables easy content addition without code changes.

**Progressive Task Flow**: Each plugin contains ordered tasks with increasing difficulty levels (`beginner` → `intermediate` → `advanced`). The tutor tracks progress through `current_task_index`.

**Rich Console Integration**: All user interaction uses the Rich library for enhanced terminal output with panels, tables, and colored text. Never use plain `print()` statements.

## Development Workflows

### Adding New Commands
1. Create `cli_tutor/plugins/[command].json` following the schema:
   ```json
   {
     "command": "command_name",
     "description": "Brief description",
     "category": "file_system|text_processing|system|networking",
     "tasks": [
       {
         "id": 1,
         "title": "Task Name",
         "description": "What user needs to do",
         "command": "expected_command",
         "difficulty": "beginner|intermediate|advanced",
         "hints": ["hint1", "hint2"],
         "explanation": "Why this command works"
       }
     ]
   }
   ```

### Running the Application
- **Development**: `poetry run cli-tutor start`
- **Plugin listing**: `poetry run cli-tutor list-plugins`
- **Custom plugins**: `poetry run cli-tutor start --plugins-dir /path/to/plugins`

### Code Quality
- **Formatting**: `poetry run black cli_tutor/`
- **Linting**: `poetry run flake8 cli_tutor/`
- **Testing**: `poetry run pytest` (test framework configured but no tests implemented yet)

## Project-Specific Conventions

### Task Validation Logic
The `Task.check_answer()` method compares user input against either:
- `command` field (exact command match)
- `expected_output` field (when checking command output rather than command syntax)

### State Management
- `CLITutor.current_plugin`: Tracks active learning session
- `Plugin.current_task_index`: Tracks progress within a plugin
- Session state resets when switching between plugins

### Error Handling Pattern
```python
if not plugins_path.exists():
    typer.echo(f"Error: Plugins directory '{plugins_path}' not found!", err=True)
    raise typer.Exit(1)
```

### CLI Command Structure
Entry point uses Typer with two main commands:
- `start`: Begin interactive learning session
- `list-plugins`: Display available command plugins

## Integration Points

### Dependencies
- **Typer**: CLI framework for command parsing and option handling
- **Rich**: Terminal UI library for all console output formatting
- **Poetry**: Dependency management and script execution

### Plugin Discovery
The system auto-discovers plugins by scanning `*.json` files in the plugins directory. No manual registration required.

### File Structure Requirements
```
cli_tutor/
├── main.py              # Typer CLI entry point
├── core/
│   ├── tutor.py         # Main session orchestrator
│   ├── plugin_manager.py # Plugin discovery & loading
│   └── plugin.py        # Task & Plugin data models
└── plugins/
    ├── ls.json          # Example: file system commands
    ├── grep.json        # Example: text processing
    └── [command].json   # Add new commands here
```

## Common Pitfalls to Avoid
- Don't use `print()` - always use `self.console.print()` with Rich formatting
- Plugin JSON must have sequential task IDs starting from 1
- The `tasks/` directory exists but is unused - all content goes in `plugins/`
- Command validation is strict - exact string matching including whitespace
