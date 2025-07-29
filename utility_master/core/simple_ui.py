"""Simple fallback UI implementation without external dependencies."""

from typing import List, Dict, Optional

from utility_master.core.base_plugin import Task, TaskResult


class SimpleUI:
    """Simple console-based user interface without external dependencies."""
    
    def __init__(self):
        pass
    
    def print_welcome(self) -> None:
        """Print welcome message."""
        print("=" * 60)
        print("🚀 Welcome to Utility Master!")
        print("=" * 60)
        print("\nAn interactive CLI learning tool that helps you master")
        print("command-line utilities through hands-on practice and")
        print("immediate feedback.\n")
    
    def show_available_utilities(self, utilities: Dict[str, str]) -> None:
        """Display available utilities in a simple format."""
        print("\n📚 Available Utilities:")
        print("-" * 40)
        for name, description in utilities.items():
            print(f"• {name:<10} - {description}")
        print()
    
    def select_utility(self, available_utilities: List[str]) -> Optional[str]:
        """Prompt user to select a utility."""
        if not available_utilities:
            print("❌ No utilities available!")
            return None
        
        print("\n🔧 Available utilities:")
        for i, utility in enumerate(available_utilities, 1):
            print(f"  {i}. {utility}")
        
        while True:
            try:
                choice = input("\nSelect a utility (number or name): ").strip()
                
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(available_utilities):
                        return available_utilities[idx]
                elif choice in available_utilities:
                    return choice
                
                print("❌ Invalid choice. Please try again.")
            except (ValueError, EOFError, KeyboardInterrupt):
                print("\n❌ Invalid input. Please try again.")
    
    def select_difficulty(self) -> str:
        """Prompt user to select difficulty level."""
        difficulties = ["beginner", "intermediate", "advanced", "all"]
        
        print("\n📊 Select difficulty level:")
        for i, diff in enumerate(difficulties, 1):
            print(f"  {i}. {diff}")
        
        while True:
            try:
                choice = input("\nEnter difficulty (number or name) [default: beginner]: ").strip()
                
                if not choice:
                    return "beginner"
                
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(difficulties):
                        return difficulties[idx]
                elif choice in difficulties:
                    return choice
                
                print("❌ Invalid choice. Please try again.")
            except (ValueError, EOFError, KeyboardInterrupt):
                return "beginner"
    
    def show_task(self, task: Task, task_number: int, total_tasks: int) -> None:
        """Display a task to the user."""
        print(f"\n{'='*60}")
        print(f"📝 Task {task_number}/{total_tasks} - {task.difficulty.title()}")
        print(f"{'='*60}")
        print(f"\n🎯 Objective: {task.description}")
        print("\n💭 Your task: Enter the correct command to complete this objective.")
        print()
    
    def get_user_input(self, prompt: str = "Enter your command") -> str:
        """Get command input from user."""
        try:
            return input(f"💻 {prompt}: ").strip()
        except (EOFError, KeyboardInterrupt):
            return ""
    
    def show_task_result(self, result: TaskResult) -> None:
        """Display task result with feedback."""
        print()
        if result.success:
            print(f"✅ Correct! Score: {result.score}/100")
        else:
            print(f"❌ Incorrect. Score: {result.score}/100")
        
        if result.feedback:
            print(f"💡 Feedback: {result.feedback}")
        
        print(f"📋 Expected: {result.expected}")
        print(f"📝 Your input: {result.user_input}")
        
        if result.actual_output:
            print(f"📤 Output: {result.actual_output}")
    
    def show_hint(self, hint: str) -> None:
        """Display a hint to the user."""
        print(f"\n💡 Hint: {hint}")
    
    def show_session_summary(self, total_tasks: int, correct_tasks: int, 
                           total_score: int, max_score: int) -> None:
        """Display session summary."""
        percentage = (correct_tasks / total_tasks * 100) if total_tasks > 0 else 0
        score_percentage = (total_score / max_score * 100) if max_score > 0 else 0
        
        print(f"\n{'='*60}")
        print("📊 Session Complete!")
        print(f"{'='*60}")
        print(f"\n📈 Tasks completed: {correct_tasks}/{total_tasks} ({percentage:.1f}%)")
        print(f"🎯 Total score: {total_score}/{max_score} ({score_percentage:.1f}%)")
        print("\n🎉 Great job learning! Keep practicing to improve your skills.")
        print()
    
    def ask_continue(self, message: str = "Continue?") -> bool:
        """Ask user if they want to continue."""
        try:
            response = input(f"\n❓ {message} (y/n) [y]: ").strip().lower()
            return response in ['', 'y', 'yes']
        except (EOFError, KeyboardInterrupt):
            return False
    
    def print_error(self, message: str) -> None:
        """Print error message."""
        print(f"❌ Error: {message}")
    
    def print_info(self, message: str) -> None:
        """Print info message."""
        print(f"ℹ️  Info: {message}")
    
    def clear_screen(self) -> None:
        """Clear the screen."""
        import os
        os.system('clear' if os.name == 'posix' else 'cls')
