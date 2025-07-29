"""Plugin for teaching the 'ls' command and its various options."""

import re
from typing import List

from core.base_plugin import BasePlugin, Task, TaskResult


class LsPlugin(BasePlugin):
    """Plugin for learning the ls command."""
    
    def get_name(self) -> str:
        return "LS Command Learning Plugin"
    
    def get_description(self) -> str:
        return "Learn the ls command for listing directory contents with various options"
    
    def get_utility_name(self) -> str:
        return "ls"
    
    def get_tasks(self, difficulty: str = "all") -> List[Task]:
        """Return ls learning tasks."""
        all_tasks = [
            # Beginner tasks
            Task(
                id="ls_basic",
                description="List the contents of the current directory",
                expected_command="ls",
                difficulty="beginner",
                hints=["Use the basic ls command without any options"]
            ),
            Task(
                id="ls_long",
                description="List directory contents in long format showing detailed information",
                expected_command="ls -l",
                difficulty="beginner",
                hints=["Use the -l option for long format", "The -l flag shows permissions, ownership, size, and date"]
            ),
            Task(
                id="ls_all",
                description="List all files including hidden files (those starting with .)",
                expected_command="ls -a",
                difficulty="beginner",
                hints=["Hidden files start with a dot (.)", "Use the -a option to show all files"]
            ),
            Task(
                id="ls_human",
                description="List files in long format with human-readable file sizes",
                expected_command="ls -lh",
                difficulty="intermediate",
                hints=["Combine -l and -h options", "The -h flag makes file sizes human-readable (KB, MB, GB)"]
            ),
            Task(
                id="ls_all_long",
                description="List all files (including hidden) in long format",
                expected_command="ls -la",
                difficulty="intermediate",
                hints=["Combine the -l and -a options", "You can combine options like -la or -l -a"]
            ),
            Task(
                id="ls_reverse",
                description="List files in reverse alphabetical order",
                expected_command="ls -r",
                difficulty="intermediate",
                hints=["Use the -r option for reverse order"]
            ),
            Task(
                id="ls_time_sort",
                description="List files sorted by modification time (newest first)",
                expected_command="ls -t",
                difficulty="intermediate",
                hints=["Use the -t option to sort by time", "Newest files will appear first"]
            ),
            Task(
                id="ls_size_sort",
                description="List files in long format sorted by file size (largest first)",
                expected_command="ls -lS",
                difficulty="advanced",
                hints=["Combine -l and -S options", "Capital S sorts by size"]
            ),
            Task(
                id="ls_time_reverse",
                description="List files sorted by modification time with oldest first",
                expected_command="ls -tr",
                difficulty="advanced",
                hints=["Combine -t and -r options", "Use both time sort and reverse order"]
            ),
            Task(
                id="ls_recursive",
                description="List files recursively showing subdirectory contents",
                expected_command="ls -R",
                difficulty="advanced",
                hints=["Use the -R option for recursive listing", "Capital R will show contents of subdirectories too"]
            )
        ]
        
        if difficulty == "all":
            return all_tasks
        else:
            return [task for task in all_tasks if task.difficulty == difficulty]
    
    def validate_task(self, task: Task, user_input: str) -> TaskResult:
        """Validate user input for ls tasks."""
        user_input = user_input.strip()
        expected = task.expected_command
        
        # Normalize the commands for comparison
        user_normalized = self._normalize_ls_command(user_input)
        expected_normalized = self._normalize_ls_command(expected)
        
        success = user_normalized == expected_normalized
        score = 100 if success else 0
        feedback = ""
        
        if not success:
            feedback = self._generate_feedback(task, user_input, expected)
            # Partial credit for close attempts
            if user_input.startswith("ls"):
                score = 20
                if self._has_correct_options(user_input, expected):
                    score = 60
        
        return TaskResult(
            success=success,
            user_input=user_input,
            expected=expected,
            feedback=feedback,
            score=score
        )
    
    def _normalize_ls_command(self, command: str) -> str:
        """Normalize ls command for comparison."""
        # Remove extra spaces
        command = ' '.join(command.split())
        
        # Handle combined options (e.g., -la vs -l -a)
        if command.startswith('ls '):
            parts = command.split()
            cmd = parts[0]
            options = []
            
            for part in parts[1:]:
                if part.startswith('-') and len(part) > 1:
                    # Separate combined options
                    for char in part[1:]:
                        if char not in options:
                            options.append(char)
            
            if options:
                options.sort()
                return f"{cmd} -{' '.join(options)}"
            else:
                return cmd
        
        return command
    
    def _has_correct_options(self, user_input: str, expected: str) -> bool:
        """Check if user input has the correct options, regardless of order."""
        user_options = set()
        expected_options = set()
        
        # Extract options from both commands
        for cmd in [user_input, expected]:
            parts = cmd.split()
            for part in parts[1:]:
                if part.startswith('-'):
                    user_options.update(part[1:]) if cmd == user_input else expected_options.update(part[1:])
        
        return user_options == expected_options
    
    def _generate_feedback(self, task: Task, user_input: str, expected: str) -> str:
        """Generate helpful feedback for incorrect answers."""
        if not user_input.startswith('ls'):
            return "Remember to start with the 'ls' command."
        
        expected_options = set()
        user_options = set()
        
        # Extract options
        exp_parts = expected.split()
        user_parts = user_input.split()
        
        for part in exp_parts[1:]:
            if part.startswith('-'):
                expected_options.update(part[1:])
        
        for part in user_parts[1:]:
            if part.startswith('-'):
                user_options.update(part[1:])
        
        missing_options = expected_options - user_options
        extra_options = user_options - expected_options
        
        feedback_parts = []
        
        if missing_options:
            feedback_parts.append(f"Missing options: -{', -'.join(sorted(missing_options))}")
        
        if extra_options:
            feedback_parts.append(f"Extra options: -{', -'.join(sorted(extra_options))}")
        
        if not feedback_parts:
            feedback_parts.append("Check your command syntax.")
        
        return ". ".join(feedback_parts) + "."
    
    def get_introduction(self) -> str:
        """Return introduction to ls command."""
        return """
The 'ls' command is used to list directory contents. It's one of the most commonly used commands in Unix/Linux systems.

Common options:
- ls        : List files and directories
- ls -l     : Long format (detailed information)
- ls -a     : Show all files (including hidden)
- ls -h     : Human-readable file sizes
- ls -t     : Sort by modification time
- ls -r     : Reverse order
- ls -S     : Sort by file size
- ls -R     : Recursive listing

You can combine options, for example: ls -la, ls -lth, etc.
        """
