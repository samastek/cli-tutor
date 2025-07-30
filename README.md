# CLI Tutor

An interactive Python-based CLI tool designed for educational purposes. It helps users learn command-line utilities through repetitive interaction and hands-on practice with immediate feedback.

## Features

- **Modular Plugin System**: Easy addition of new command plugins
- **Interactive Learning**: Step-by-step tasks with immediate feedback
- **Rich CLI Interface**: Beautiful terminal interface using Rich library
- **Progressive Difficulty**: Tasks range from beginner to advanced
- **Hints and Explanations**: Built-in help system for learning

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd utility-master
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

## Usage

### Start Interactive Learning
```bash
poetry run cli-tutor start
```

### List Available Plugins
```bash
poetry run cli-tutor list-plugins
```

### Use Custom Plugins Directory
```bash
poetry run cli-tutor start --plugins-dir /path/to/custom/plugins
```

## Available Commands

The tool currently includes plugins for learning these commands:

- **ls**: Learn directory listing and file information
- **grep**: Master text searching and pattern matching
- **find**: Explore file and directory searching

## Creating New Plugins

To add a new command plugin, simply create a JSON file in `cli_tutor/plugins/` (e.g., `sed.json`).

### Plugin Structure

**JSON Plugin File** (`cli_tutor/plugins/command.json`):
```json
{
  "command": "command_name",
  "description": "Brief description of what the command does",
  "category": "file_system|text_processing|system|networking",
  "tasks": [
    {
      "id": 1,
      "title": "Task Title",
      "description": "What the user needs to do",
      "command": "expected_command",
      "difficulty": "beginner|intermediate|advanced",
      "hints": ["Helpful hint 1", "Helpful hint 2"],
      "explanation": "Explanation of the command"
    }
  ]
}
```

## Development

### Run Tests
```bash
poetry run pytest
```

### Code Formatting
```bash
poetry run black cli_tutor/
```

### Linting
```bash
poetry run flake8 cli_tutor/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your plugin or improvement
4. Write tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.