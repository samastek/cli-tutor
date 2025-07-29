"""Plugin for teaching the 'find' command and its various options."""

import re
from typing import List

from utility_master.core.base_plugin import BasePlugin, Task, TaskResult


class FindPlugin(BasePlugin):
    """Plugin for learning the find command."""
    
    def get_name(self) -> str:
        return "FIND Command Learning Plugin"
    
    def get_description(self) -> str:
        return "Learn the find command for searching files and directories based on various criteria"
    
    def get_utility_name(self) -> str:
        return "find"
    
    def get_tasks(self, difficulty: str = "all") -> List[Task]:
        """Return find learning tasks."""
        all_tasks = [
            # Beginner tasks
            Task(
                id="find_basic",
                description="Find all files in the current directory",
                expected_command="find .",
                difficulty="beginner",
                setup_commands=[
                    "touch file1.txt",
                    "touch file2.txt",
                    "mkdir subdir",
                    "touch subdir/file3.txt"
                ],
                hints=["Use find followed by the directory path", "Use . for current directory"]
            ),
            Task(
                id="find_by_name",
                description="Find all files named 'test.txt' in the current directory and subdirectories",
                expected_command="find . -name test.txt",
                difficulty="beginner",
                setup_commands=[
                    "touch test.txt",
                    "touch other.txt",
                    "mkdir subdir",
                    "touch subdir/test.txt"
                ],
                hints=["Use -name option to search by filename", "Put the filename after -name"]
            ),
            Task(
                id="find_name_pattern",
                description="Find all .txt files in the current directory and subdirectories",
                expected_command="find . -name '*.txt'",
                difficulty="beginner",
                setup_commands=[
                    "touch file1.txt",
                    "touch file2.py",
                    "touch document.txt",
                    "mkdir subdir",
                    "touch subdir/notes.txt"
                ],
                hints=["Use wildcard * to match any characters", "Don't forget quotes around the pattern"]
            ),
            Task(
                id="find_type_file",
                description="Find only regular files (not directories) in the current directory",
                expected_command="find . -type f",
                difficulty="intermediate",
                setup_commands=[
                    "touch file1.txt",
                    "touch file2.txt",
                    "mkdir dir1",
                    "mkdir dir2",
                    "touch dir1/file3.txt"
                ],
                hints=["Use -type f to find only files", "f stands for regular files"]
            ),
            Task(
                id="find_type_directory",
                description="Find only directories in the current directory and subdirectories",
                expected_command="find . -type d",
                difficulty="intermediate",
                setup_commands=[
                    "touch file1.txt",
                    "mkdir dir1",
                    "mkdir dir2",
                    "mkdir dir1/subdir"
                ],
                hints=["Use -type d to find only directories", "d stands for directories"]
            ),
            Task(
                id="find_size_greater",
                description="Find files larger than 100 bytes in the current directory",
                expected_command="find . -size +100c",
                difficulty="intermediate",
                setup_commands=[
                    "echo 'small' > small.txt",
                    "head -c 200 /dev/zero > large.txt",
                    "echo 'medium content here' > medium.txt"
                ],
                hints=["Use -size +100c for files larger than 100 bytes", "c means bytes, + means greater than"]
            ),
            Task(
                id="find_maxdepth",
                description="Find .txt files only in the current directory (not subdirectories)",
                expected_command="find . -maxdepth 1 -name '*.txt'",
                difficulty="intermediate",
                setup_commands=[
                    "touch file1.txt",
                    "touch file2.py",
                    "mkdir subdir",
                    "touch subdir/deep.txt"
                ],
                hints=["Use -maxdepth 1 to limit search to current directory only", "Combine with -name for filename pattern"]
            ),
            Task(
                id="find_newer",
                description="Find files newer than reference.txt",
                expected_command="find . -newer reference.txt",
                difficulty="advanced",
                setup_commands=[
                    "touch reference.txt",
                    "sleep 1",
                    "touch newer1.txt",
                    "touch newer2.txt"
                ],
                hints=["Use -newer to find files modified after another file", "Specify the reference file after -newer"]
            ),
            Task(
                id="find_exec",
                description="Find all .log files and display their contents using cat",
                expected_command="find . -name '*.log' -exec cat {} \\;",
                difficulty="advanced",
                setup_commands=[
                    "echo 'log entry 1' > app.log",
                    "echo 'error occurred' > error.log",
                    "touch other.txt",
                    "mkdir logs",
                    "echo 'debug info' > logs/debug.log"
                ],
                hints=["Use -exec to execute commands on found files", "Use {} as placeholder for filename", "End with \\;"]
            ),
            Task(
                id="find_multiple_conditions",
                description="Find .txt files that are larger than 50 bytes",
                expected_command="find . -name '*.txt' -size +50c",
                difficulty="advanced",
                setup_commands=[
                    "echo 'short' > small.txt",
                    "echo 'this is a longer text file with more content to make it bigger than 50 bytes' > large.txt",
                    "touch empty.py"
                ],
                hints=["Combine multiple conditions by listing them", "Both -name and -size conditions must be true"]
            ),
            Task(
                id="find_exclude_directory",
                description="Find all .txt files but exclude the 'backup' directory",
                expected_command="find . -name '*.txt' -not -path './backup/*'",
                difficulty="advanced",
                setup_commands=[
                    "touch file1.txt",
                    "touch file2.txt",
                    "mkdir backup",
                    "touch backup/old.txt",
                    "mkdir other",
                    "touch other/new.txt"
                ],
                hints=["Use -not -path to exclude directories", "Use pattern './backup/*' to exclude backup directory"]
            )
        ]
        
        if difficulty == "all":
            return all_tasks
        else:
            return [task for task in all_tasks if task.difficulty == difficulty]
    
    def validate_task(self, task: Task, user_input: str) -> TaskResult:
        """Validate user input for find tasks."""
        user_input = user_input.strip()
        expected = task.expected_command
        
        # Normalize the commands for comparison
        user_normalized = self._normalize_find_command(user_input)
        expected_normalized = self._normalize_find_command(expected)
        
        success = user_normalized == expected_normalized
        score = 100 if success else 0
        feedback = ""
        
        if not success:
            feedback = self._generate_feedback(task, user_input, expected)
            # Partial credit for close attempts
            if user_input.startswith("find"):
                score = 20
                if self._has_correct_path(user_input, expected):
                    score = 40
                if self._has_correct_options(user_input, expected):
                    score = max(score, 60)
        
        return TaskResult(
            success=success,
            user_input=user_input,
            expected=expected,
            feedback=feedback,
            score=score
        )
    
    def _normalize_find_command(self, command: str) -> str:
        """Normalize find command for comparison."""
        # Remove extra spaces
        command = ' '.join(command.split())
        
        # Handle quoted arguments consistently
        command = re.sub(r"'([^']*)'", r'"\1"', command)
        
        return command
    
    def _has_correct_path(self, user_input: str, expected: str) -> bool:
        """Check if user input has the correct search path."""
        user_parts = user_input.split()
        expected_parts = expected.split()
        
        if len(user_parts) >= 2 and len(expected_parts) >= 2:
            return user_parts[1] == expected_parts[1]
        
        return False
    
    def _has_correct_options(self, user_input: str, expected: str) -> bool:
        """Check if user input has similar options to expected."""
        user_parts = user_input.split()
        expected_parts = expected.split()
        
        # Extract option-value pairs
        user_options = self._extract_options(user_parts)
        expected_options = self._extract_options(expected_parts)
        
        # Check if major options are present
        common_options = 0
        for opt in expected_options:
            if opt in user_options:
                common_options += 1
        
        return common_options >= len(expected_options) * 0.7  # 70% match
    
    def _extract_options(self, parts: List[str]) -> List[str]:
        """Extract option names from command parts."""
        options = []
        for i, part in enumerate(parts):
            if part.startswith('-') and not part.startswith('--'):
                options.append(part)
        return options
    
    def _generate_feedback(self, task: Task, user_input: str, expected: str) -> str:
        """Generate helpful feedback for incorrect answers."""
        if not user_input.startswith('find'):
            return "Remember to start with the 'find' command."
        
        user_parts = user_input.split()
        expected_parts = expected.split()
        
        feedback_parts = []
        
        # Check search path
        if not self._has_correct_path(user_input, expected):
            if len(expected_parts) >= 2:
                feedback_parts.append(f"Check your search path. Expected: {expected_parts[1]}")
        
        # Check for missing key options
        expected_options = self._extract_options(expected_parts)
        user_options = self._extract_options(user_parts)
        
        missing_options = []
        for opt in expected_options:
            if opt not in user_options:
                missing_options.append(opt)
        
        if missing_options:
            feedback_parts.append(f"Missing options: {', '.join(missing_options)}")
        
        # Check for specific patterns in expected command
        if '-name' in expected and '-name' not in user_input:
            feedback_parts.append("Use -name option to search by filename")
        
        if '-type' in expected and '-type' not in user_input:
            feedback_parts.append("Use -type option to specify file type (f for files, d for directories)")
        
        if '-size' in expected and '-size' not in user_input:
            feedback_parts.append("Use -size option to search by file size")
        
        if '-exec' in expected and '-exec' not in user_input:
            feedback_parts.append("Use -exec option to execute commands on found files")
        
        if not feedback_parts:
            feedback_parts.append("Check your command syntax and arguments.")
        
        return ". ".join(feedback_parts) + "."
    
    def get_introduction(self) -> str:
        """Return introduction to find command."""
        return """
The 'find' command searches for files and directories based on various criteria. It's extremely powerful for locating files.

Common options:
- find path                    : Find all files in path
- find . -name filename        : Find files by exact name
- find . -name '*.ext'         : Find files by pattern (use quotes!)
- find . -type f               : Find only files (not directories)
- find . -type d               : Find only directories
- find . -size +100c           : Find files larger than 100 bytes
- find . -size -100c           : Find files smaller than 100 bytes
- find . -maxdepth 1           : Limit search depth
- find . -newer file           : Find files newer than reference file
- find . -name '*.txt' -exec cat {} \\; : Execute command on found files

Tips:
- Use quotes around patterns with wildcards
- Combine multiple criteria for precise searches
- Use {} as placeholder in -exec commands
- End -exec commands with \\;
        """
