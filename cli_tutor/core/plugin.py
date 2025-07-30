"""Plugin system for CLI Tutor."""

from typing import Dict, Any, Optional
import json
from pathlib import Path


class Task:
    """Represents a single learning task."""
    
    def __init__(self, data: Dict[str, Any]):
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.command = data["command"]
        self.expected_output = data.get("expected_output")
        self.hints = data.get("hints", [])
        self.explanation = data.get("explanation", "")
        self.difficulty = data.get("difficulty", "beginner")
        
    def check_answer(self, user_input: str) -> bool:
        """Check if user input matches expected command or output."""
        if self.expected_output:
            return user_input.strip() == self.expected_output.strip()
        return user_input.strip() == self.command.strip()


class Plugin:
    """Represents a command learning plugin loaded from JSON."""
    
    def __init__(self, json_file: Path):
        self.json_file = json_file
        self.name = json_file.stem
        self.tasks = []
        self.current_task_index = 0
        self.metadata = {}
        self._load_from_json()
    
    def _load_from_json(self):
        """Load plugin data from JSON file."""
        with open(self.json_file, 'r') as f:
            data = json.load(f)
            
        # Load metadata
        self.metadata = {
            "command": data.get("command", self.name),
            "description": data.get("description", ""),
            "category": data.get("category", "general"),
            "author": data.get("author", ""),
            "version": data.get("version", "1.0")
        }
        
        # Load tasks
        self.tasks = [Task(task_data) for task_data in data.get("tasks", [])]
    
    @property
    def current_task(self) -> Optional[Task]:
        """Get the current task."""
        if self.current_task_index < len(self.tasks):
            return self.tasks[self.current_task_index]
        return None
    
    def next_task(self) -> bool:
        """Move to next task. Returns True if more tasks available."""
        self.current_task_index += 1
        return self.current_task_index < len(self.tasks)
    
    def reset(self):
        """Reset to first task."""
        self.current_task_index = 0
    
    @property
    def is_complete(self) -> bool:
        """Check if all tasks are completed."""
        return self.current_task_index >= len(self.tasks)
    
    @property
    def progress(self) -> str:
        """Get progress string."""
        return f"{self.current_task_index}/{len(self.tasks)}"
    
    def get_command_info(self) -> Dict[str, str]:
        """Return basic information about the command."""
        return {
            "name": self.metadata["command"],
            "description": self.metadata["description"], 
            "category": self.metadata["category"]
        }