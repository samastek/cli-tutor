"""Base plugin class that all utility plugins must inherit from."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Task:
    """Represents a learning task for a utility command."""
    id: str
    description: str
    expected_command: str
    expected_output: Optional[str] = None
    setup_commands: Optional[List[str]] = None
    difficulty: str = "beginner"  # beginner, intermediate, advanced
    hints: Optional[List[str]] = None


@dataclass
class TaskResult:
    """Result of executing a task."""
    success: bool
    user_input: str
    expected: str
    actual_output: Optional[str] = None
    feedback: str = ""
    score: int = 0


class BasePlugin(ABC):
    """Base class for all utility plugins."""
    
    def __init__(self):
        self.name = self.get_name()
        self.description = self.get_description()
        self.utility_name = self.get_utility_name()
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the plugin name."""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Return a description of what this plugin teaches."""
        pass
    
    @abstractmethod
    def get_utility_name(self) -> str:
        """Return the name of the utility this plugin teaches."""
        pass
    
    @abstractmethod
    def get_tasks(self, difficulty: str = "all") -> List[Task]:
        """Return available tasks for the specified difficulty level."""
        pass
    
    @abstractmethod
    def validate_task(self, task: Task, user_input: str) -> TaskResult:
        """Validate user input against the expected result."""
        pass
    
    def get_introduction(self) -> str:
        """Return an introduction to the utility."""
        return f"Welcome to {self.utility_name} learning module!"
    
    def get_help(self) -> str:
        """Return help information for the utility."""
        return f"Learn about {self.utility_name} command and its options."
    
    def setup_environment(self) -> bool:
        """Setup any required test environment. Return True if successful."""
        return True
    
    def cleanup_environment(self) -> bool:
        """Cleanup test environment. Return True if successful."""
        return True
