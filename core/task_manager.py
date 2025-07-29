"""Task manager for executing and validating learning tasks."""

import subprocess
import os
import tempfile
from typing import List, Optional
from pathlib import Path

from .base_plugin import Task, TaskResult, BasePlugin


class TaskManager:
    """Manages task execution and validation."""
    
    def __init__(self, work_dir: Optional[str] = None):
        self.work_dir = Path(work_dir) if work_dir else Path.cwd()
        self.temp_dir = None
    
    def setup_task_environment(self, task: Task) -> bool:
        """Setup environment for a task."""
        try:
            # Create temporary directory for task execution
            self.temp_dir = tempfile.mkdtemp(prefix="utility_master_")
            os.chdir(self.temp_dir)
            
            # Run setup commands if any
            if task.setup_commands:
                for cmd in task.setup_commands:
                    result = subprocess.run(
                        cmd, shell=True, capture_output=True, text=True
                    )
                    if result.returncode != 0:
                        print(f"Setup command failed: {cmd}")
                        return False
            
            return True
        except Exception as e:
            print(f"Error setting up task environment: {e}")
            return False
    
    def cleanup_task_environment(self) -> None:
        """Cleanup task environment."""
        try:
            if self.temp_dir and os.path.exists(self.temp_dir):
                os.chdir(self.work_dir)
                import shutil
                shutil.rmtree(self.temp_dir)
                self.temp_dir = None
        except Exception as e:
            print(f"Error cleaning up task environment: {e}")
    
    def execute_command(self, command: str) -> tuple[int, str, str]:
        """Execute a command and return return code, stdout, stderr."""
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=30
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)
    
    def validate_command_syntax(self, user_input: str, expected_command: str) -> bool:
        """Basic syntax validation between user input and expected command."""
        # Remove extra whitespace and normalize
        user_normalized = ' '.join(user_input.split())
        expected_normalized = ' '.join(expected_command.split())
        
        return user_normalized == expected_normalized
    
    def run_task(self, plugin: BasePlugin, task: Task, user_input: str) -> TaskResult:
        """Run a task and validate the result."""
        # First validate using the plugin's validation method
        result = plugin.validate_task(task, user_input)
        
        # If plugin validation is successful and we have setup, test actual execution
        if result.success and task.setup_commands:
            if self.setup_task_environment(task):
                try:
                    # Execute the user's command
                    returncode, stdout, stderr = self.execute_command(user_input)
                    
                    if returncode == 0:
                        result.actual_output = stdout.strip()
                        # Additional validation can be done here
                    else:
                        result.success = False
                        result.feedback += f" Command execution failed: {stderr}"
                        result.score = max(0, result.score - 20)
                
                finally:
                    self.cleanup_task_environment()
        
        return result
    
    def get_hint(self, task: Task, attempt_count: int) -> Optional[str]:
        """Get a hint for the task based on attempt count."""
        if not task.hints or attempt_count <= 0:
            return None
        
        hint_index = min(attempt_count - 1, len(task.hints) - 1)
        return task.hints[hint_index]
