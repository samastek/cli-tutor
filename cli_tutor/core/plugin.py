"""Plugin system for CLI Tutor."""

from typing import Dict, Any, Optional
import json
from pathlib import Path
from .progress_tracker import ProgressTracker


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
    
    def __init__(self, json_file: Path, progress_tracker: Optional[ProgressTracker] = None):
        self.json_file = json_file
        self.name = json_file.stem
        self.tasks = []
        self.current_task_index = 0
        self.metadata = {}
        self.progress_tracker = progress_tracker
        self._load_from_json()
        
        # Initialize progress tracking if available
        if self.progress_tracker:
            self._load_progress()
    
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
    
    def _load_progress(self):
        """Load progress from the progress tracker."""
        if not self.progress_tracker:
            return
            
        # Get the next incomplete task index
        next_task_index = self.progress_tracker.get_next_incomplete_task_index(
            self.name, len(self.tasks)
        )
        self.current_task_index = next_task_index
        
        # Update plugin progress in database
        completed_count = len(self.progress_tracker.get_completed_task_ids(self.name))
        self.progress_tracker.update_plugin_progress(
            self.name, len(self.tasks), completed_count, self.current_task_index
        )
    
    @property
    def current_task(self) -> Optional[Task]:
        """Get the current task."""
        if self.current_task_index < len(self.tasks):
            return self.tasks[self.current_task_index]
        return None
    
    def complete_current_task(self) -> bool:
        """Mark current task as completed and move to next. Returns True if more tasks available."""
        if not self.current_task:
            return False
            
        current_task = self.current_task
        
        # Mark task as completed in progress tracker
        if self.progress_tracker:
            self.progress_tracker.mark_task_completed(
                self.name, current_task.id, current_task.title
            )
        
        # Move to next incomplete task
        return self._advance_to_next_incomplete_task()
    
    def _advance_to_next_incomplete_task(self) -> bool:
        """Move to the next incomplete task. Returns True if more tasks available."""
        if not self.progress_tracker:
            # Fallback to simple sequential progression
            self.current_task_index += 1
            return self.current_task_index < len(self.tasks)
        
        # Find next incomplete task
        completed_ids = self.progress_tracker.get_completed_task_ids(self.name)
        
        for i in range(self.current_task_index + 1, len(self.tasks)):
            task_id = self.tasks[i].id
            if task_id not in completed_ids:
                self.current_task_index = i
                self._update_progress()
                return True
        
        # No more incomplete tasks
        self.current_task_index = len(self.tasks)
        self._update_progress()
        return False
    
    def _update_progress(self):
        """Update progress in the tracker."""
        if self.progress_tracker:
            completed_count = len(self.progress_tracker.get_completed_task_ids(self.name))
            self.progress_tracker.update_plugin_progress(
                self.name, len(self.tasks), completed_count, self.current_task_index
            )
    
    def next_task(self) -> bool:
        """Move to next task. Returns True if more tasks available."""
        # This method is kept for backward compatibility but now uses complete_current_task
        return self.complete_current_task()
    
    def reset(self):
        """Reset to first incomplete task."""
        if self.progress_tracker:
            # Reset to first incomplete task
            next_task_index = self.progress_tracker.get_next_incomplete_task_index(
                self.name, len(self.tasks)
            )
            self.current_task_index = next_task_index
            self._update_progress()
        else:
            # Fallback to simple reset
            self.current_task_index = 0
    
    def reset_progress(self):
        """Reset all progress for this plugin."""
        if self.progress_tracker:
            self.progress_tracker.reset_plugin_progress(self.name)
        self.current_task_index = 0
    
    @property
    def is_complete(self) -> bool:
        """Check if all tasks are completed."""
        if self.progress_tracker:
            completed_ids = self.progress_tracker.get_completed_task_ids(self.name)
            return len(completed_ids) >= len(self.tasks)
        return self.current_task_index >= len(self.tasks)
    
    @property
    def progress(self) -> str:
        """Get progress string."""
        if self.progress_tracker:
            completed_count = len(self.progress_tracker.get_completed_task_ids(self.name))
            return f"{completed_count}/{len(self.tasks)}"
        return f"{self.current_task_index}/{len(self.tasks)}"
    
    @property
    def completed_task_count(self) -> int:
        """Get number of completed tasks."""
        if self.progress_tracker:
            return len(self.progress_tracker.get_completed_task_ids(self.name))
        return self.current_task_index
    
    def get_progress_summary(self) -> Dict:
        """Get detailed progress summary."""
        completed_count = self.completed_task_count
        total_count = len(self.tasks)
        
        return {
            "plugin_name": self.name,
            "completed_tasks": completed_count,
            "total_tasks": total_count,
            "progress_percentage": (completed_count / total_count * 100) if total_count > 0 else 0,
            "is_complete": self.is_complete,
            "current_task_index": self.current_task_index,
            "current_task_title": self.current_task.title if self.current_task else None
        }
    
    def get_command_info(self) -> Dict[str, str]:
        """Return basic information about the command."""
        return {
            "name": self.metadata["command"],
            "description": self.metadata["description"], 
            "category": self.metadata["category"]
        }