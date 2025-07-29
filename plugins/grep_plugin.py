"""Plugin for teaching the 'grep' command and its various options."""

import re
from typing import List

from core.base_plugin import BasePlugin, Task, TaskResult


class GrepPlugin(BasePlugin):
    """Plugin for learning the grep command."""
    
    def get_name(self) -> str:
        return "GREP Command Learning Plugin"
    
    def get_description(self) -> str:
        return "Learn the grep command for searching text patterns in files"
    
    def get_utility_name(self) -> str:
        return "grep"
    
    def get_tasks(self, difficulty: str = "all") -> List[Task]:
        """Return grep learning tasks."""
        all_tasks = [
            # Beginner tasks
            Task(
                id="grep_basic",
                description="Search for the word 'hello' in a file called 'test.txt'",
                expected_command="grep hello test.txt",
                difficulty="beginner",
                setup_commands=[
                    "echo 'hello world' > test.txt",
                    "echo 'goodbye' >> test.txt",
                    "echo 'hello again' >> test.txt"
                ],
                hints=["Use grep followed by the pattern and filename", "Basic syntax: grep pattern filename"]
            ),
            Task(
                id="grep_case_insensitive",
                description="Search for 'HELLO' in test.txt ignoring case differences",
                expected_command="grep -i HELLO test.txt",
                difficulty="beginner",
                setup_commands=[
                    "echo 'hello world' > test.txt",
                    "echo 'HELLO there' >> test.txt",
                    "echo 'Hello again' >> test.txt"
                ],
                hints=["Use the -i option for case-insensitive search"]
            ),
            Task(
                id="grep_line_numbers",
                description="Search for 'world' in test.txt and show line numbers",
                expected_command="grep -n world test.txt",
                difficulty="beginner",
                setup_commands=[
                    "echo 'hello world' > test.txt",
                    "echo 'goodbye' >> test.txt",
                    "echo 'world of code' >> test.txt"
                ],
                hints=["Use the -n option to show line numbers"]
            ),
            Task(
                id="grep_invert",
                description="Show all lines that do NOT contain 'error' from log.txt",
                expected_command="grep -v error log.txt",
                difficulty="intermediate",
                setup_commands=[
                    "echo 'info: starting application' > log.txt",
                    "echo 'error: file not found' >> log.txt",
                    "echo 'info: processing data' >> log.txt",
                    "echo 'error: connection failed' >> log.txt",
                    "echo 'info: task completed' >> log.txt"
                ],
                hints=["Use the -v option to invert the match", "This shows lines that don't match the pattern"]
            ),
            Task(
                id="grep_count",
                description="Count how many lines contain 'info' in log.txt",
                expected_command="grep -c info log.txt",
                difficulty="intermediate",
                setup_commands=[
                    "echo 'info: starting application' > log.txt",
                    "echo 'error: file not found' >> log.txt",
                    "echo 'info: processing data' >> log.txt",
                    "echo 'warning: low memory' >> log.txt",
                    "echo 'info: task completed' >> log.txt"
                ],
                hints=["Use the -c option to count matching lines"]
            ),
            Task(
                id="grep_word_boundary",
                description="Search for the whole word 'cat' (not 'category' or 'catch') in animals.txt",
                expected_command="grep -w cat animals.txt",
                difficulty="intermediate",
                setup_commands=[
                    "echo 'cat' > animals.txt",
                    "echo 'dog' >> animals.txt",
                    "echo 'category' >> animals.txt",
                    "echo 'catch the cat' >> animals.txt"
                ],
                hints=["Use the -w option for whole word matching"]
            ),
            Task(
                id="grep_recursive",
                description="Search for 'function' recursively in all files in the current directory",
                expected_command="grep -r function .",
                difficulty="advanced",
                setup_commands=[
                    "mkdir -p subdir",
                    "echo 'function test() {' > code.js",
                    "echo 'var x = 1;' >> code.js",
                    "echo 'def function()' > subdir/script.py",
                    "echo 'normal text' > readme.txt"
                ],
                hints=["Use the -r option for recursive search", "Use . to search in current directory"]
            ),
            Task(
                id="grep_extended_regex",
                description="Search for lines containing either 'cat' or 'dog' using extended regular expressions",
                expected_command="grep -E 'cat|dog' animals.txt",
                difficulty="advanced",
                setup_commands=[
                    "echo 'cat' > animals.txt",
                    "echo 'bird' >> animals.txt",
                    "echo 'dog' >> animals.txt",
                    "echo 'fish' >> animals.txt"
                ],
                hints=["Use -E for extended regex", "Use | for OR operator in regex"]
            ),
            Task(
                id="grep_multiple_options",
                description="Search recursively for 'error' in all files, ignoring case and showing line numbers",
                expected_command="grep -rin error .",
                difficulty="advanced",
                setup_commands=[
                    "mkdir -p logs",
                    "echo 'INFO: start' > app.log",
                    "echo 'ERROR: failed' >> app.log",
                    "echo 'Error in processing' > logs/debug.log",
                    "echo 'All good' >> logs/debug.log"
                ],
                hints=["Combine -r, -i, and -n options", "You can write them as -rin or -r -i -n"]
            )
        ]
        
        if difficulty == "all":
            return all_tasks
        else:
            return [task for task in all_tasks if task.difficulty == difficulty]
    
    def validate_task(self, task: Task, user_input: str) -> TaskResult:
        """Validate user input for grep tasks."""
        user_input = user_input.strip()
        expected = task.expected_command
        
        # Normalize the commands for comparison
        user_normalized = self._normalize_grep_command(user_input)
        expected_normalized = self._normalize_grep_command(expected)
        
        success = user_normalized == expected_normalized
        score = 100 if success else 0
        feedback = ""
        
        if not success:
            feedback = self._generate_feedback(task, user_input, expected)
            # Partial credit for close attempts
            if user_input.startswith("grep"):
                score = 20
                if self._has_correct_options(user_input, expected):
                    score = 60
                if self._has_correct_pattern(user_input, expected):
                    score = max(score, 40)
        
        return TaskResult(
            success=success,
            user_input=user_input,
            expected=expected,
            feedback=feedback,
            score=score
        )
    
    def _normalize_grep_command(self, command: str) -> str:
        """Normalize grep command for comparison."""
        # Remove extra spaces
        command = ' '.join(command.split())
        
        if command.startswith('grep '):
            parts = command.split()
            cmd = parts[0]
            options = []
            non_options = []
            
            for part in parts[1:]:
                if part.startswith('-') and len(part) > 1:
                    # Handle combined options
                    for char in part[1:]:
                        if char not in options:
                            options.append(char)
                else:
                    non_options.append(part)
            
            # Rebuild command with sorted options
            result = [cmd]
            if options:
                options.sort()
                result.append(f"-{''.join(options)}")
            result.extend(non_options)
            
            return ' '.join(result)
        
        return command
    
    def _has_correct_options(self, user_input: str, expected: str) -> bool:
        """Check if user input has the correct options."""
        user_options = set()
        expected_options = set()
        
        for cmd in [user_input, expected]:
            parts = cmd.split()
            for part in parts[1:]:
                if part.startswith('-'):
                    if cmd == user_input:
                        user_options.update(part[1:])
                    else:
                        expected_options.update(part[1:])
        
        return user_options == expected_options
    
    def _has_correct_pattern(self, user_input: str, expected: str) -> bool:
        """Check if user input has the correct search pattern."""
        user_parts = user_input.split()
        expected_parts = expected.split()
        
        # Find the pattern (first non-option argument)
        user_pattern = None
        expected_pattern = None
        
        for part in user_parts[1:]:
            if not part.startswith('-') and user_pattern is None:
                user_pattern = part
                break
        
        for part in expected_parts[1:]:
            if not part.startswith('-') and expected_pattern is None:
                expected_pattern = part
                break
        
        return user_pattern == expected_pattern
    
    def _generate_feedback(self, task: Task, user_input: str, expected: str) -> str:
        """Generate helpful feedback for incorrect answers."""
        if not user_input.startswith('grep'):
            return "Remember to start with the 'grep' command."
        
        user_parts = user_input.split()
        expected_parts = expected.split()
        
        feedback_parts = []
        
        # Check options
        if not self._has_correct_options(user_input, expected):
            expected_options = set()
            for part in expected_parts[1:]:
                if part.startswith('-'):
                    expected_options.update(part[1:])
            
            if expected_options:
                feedback_parts.append(f"Missing or incorrect options. Expected: -{' -'.join(sorted(expected_options))}")
        
        # Check pattern
        if not self._has_correct_pattern(user_input, expected):
            expected_pattern = None
            for part in expected_parts[1:]:
                if not part.startswith('-'):
                    expected_pattern = part
                    break
            
            if expected_pattern:
                feedback_parts.append(f"Check your search pattern. Expected: {expected_pattern}")
        
        if not feedback_parts:
            feedback_parts.append("Check your command syntax and arguments.")
        
        return ". ".join(feedback_parts) + "."
    
    def get_introduction(self) -> str:
        """Return introduction to grep command."""
        return """
The 'grep' command searches for patterns in text files. It's a powerful tool for finding specific content.

Common options:
- grep pattern file     : Search for pattern in file
- grep -i pattern file  : Case-insensitive search
- grep -n pattern file  : Show line numbers
- grep -v pattern file  : Invert match (show non-matching lines)
- grep -c pattern file  : Count matching lines
- grep -w pattern file  : Match whole words only
- grep -r pattern dir   : Recursive search in directory
- grep -E pattern file  : Extended regular expressions

You can combine options, for example: grep -rn, grep -iv, etc.
        """
