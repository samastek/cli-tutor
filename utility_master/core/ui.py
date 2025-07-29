"""User interface components using Rich for enhanced CLI experience."""

from typing import List, Dict, Optional
from utility_master.core.base_plugin import Task, TaskResult

# Try to import rich, fall back to simple UI if not available
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.text import Text
    from rich.syntax import Syntax
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


if RICH_AVAILABLE:
    class RichUI:
        """Rich-based user interface for the application."""
        
        def __init__(self):
            self.console = Console()
        
        def print_welcome(self) -> None:
            """Print welcome message."""
            welcome_text = """
    [bold blue]Welcome to Utility Master![/bold blue]
            
    An interactive CLI learning tool that helps you master command-line utilities
    through hands-on practice and immediate feedback.
            """
            self.console.print(Panel(welcome_text, title="🚀 Utility Master", expand=False))
        
        def show_available_utilities(self, utilities: Dict[str, str]) -> None:
            """Display available utilities in a table."""
            table = Table(title="Available Utilities")
            table.add_column("Utility", style="cyan")
            table.add_column("Description", style="white")
            
            for name, description in utilities.items():
                table.add_row(name, description)
            
            self.console.print(table)
        
        def select_utility(self, available_utilities: List[str]) -> Optional[str]:
            """Prompt user to select a utility."""
            if not available_utilities:
                self.console.print("[red]No utilities available![/red]")
                return None
            
            self.console.print("\n[bold]Available utilities:[/bold]")
            for i, utility in enumerate(available_utilities, 1):
                self.console.print(f"  {i}. {utility}")
            
            while True:
                try:
                    choice = Prompt.ask("\nSelect a utility (number or name)", 
                                      choices=[str(i) for i in range(1, len(available_utilities) + 1)] + available_utilities)
                    
                    if choice.isdigit():
                        return available_utilities[int(choice) - 1]
                    else:
                        return choice if choice in available_utilities else None
                except (ValueError, IndexError):
                    self.console.print("[red]Invalid choice. Please try again.[/red]")
        
        def select_difficulty(self) -> str:
            """Prompt user to select difficulty level."""
            return Prompt.ask(
                "\nSelect difficulty level",
                choices=["beginner", "intermediate", "advanced", "all"],
                default="beginner"
            )
        
        def show_task(self, task: Task, task_number: int, total_tasks: int) -> None:
            """Display a task to the user."""
            title = f"Task {task_number}/{total_tasks} - {task.difficulty.title()}"
            
            task_content = f"""
    [bold]Objective:[/bold] {task.description}

    [bold]Your task:[/bold] Enter the correct command to complete this objective.
            """
            
            self.console.print(Panel(task_content, title=title, expand=False))
        
        def get_user_input(self, prompt: str = "Enter your command") -> str:
            """Get command input from user."""
            return Prompt.ask(f"\n💻 {prompt}")
        
        def show_task_result(self, result: TaskResult) -> None:
            """Display task result with feedback."""
            if result.success:
                self.console.print(f"\n[green]✅ Correct! Score: {result.score}/100[/green]")
            else:
                self.console.print(f"\n[red]❌ Incorrect. Score: {result.score}/100[/red]")
            
            if result.feedback:
                self.console.print(f"[yellow]Feedback:[/yellow] {result.feedback}")
            
            self.console.print(f"[blue]Expected:[/blue] {result.expected}")
            self.console.print(f"[blue]Your input:[/blue] {result.user_input}")
            
            if result.actual_output:
                self.console.print(f"[blue]Output:[/blue] {result.actual_output}")
        
        def show_hint(self, hint: str) -> None:
            """Display a hint to the user."""
            self.console.print(f"\n[yellow]💡 Hint:[/yellow] {hint}")
        
        def show_session_summary(self, total_tasks: int, correct_tasks: int, 
                               total_score: int, max_score: int) -> None:
            """Display session summary."""
            percentage = (correct_tasks / total_tasks * 100) if total_tasks > 0 else 0
            score_percentage = (total_score / max_score * 100) if max_score > 0 else 0
            
            summary = f"""
    [bold]Session Complete![/bold]

    Tasks completed: {correct_tasks}/{total_tasks} ({percentage:.1f}%)
    Total score: {total_score}/{max_score} ({score_percentage:.1f}%)

    Great job learning! Keep practicing to improve your skills.
            """
            
            self.console.print(Panel(summary, title="📊 Session Summary", expand=False))
        
        def ask_continue(self, message: str = "Continue?") -> bool:
            """Ask user if they want to continue."""
            return Confirm.ask(f"\n{message}")
        
        def print_error(self, message: str) -> None:
            """Print error message."""
            self.console.print(f"[red]Error:[/red] {message}")
        
        def print_info(self, message: str) -> None:
            """Print info message."""
            self.console.print(f"[blue]Info:[/blue] {message}")
        
        def clear_screen(self) -> None:
            """Clear the screen."""
            self.console.clear()


# Import SimpleUI class
from utility_master.core.simple_ui import SimpleUI


def UI():
    """Factory function that returns the appropriate UI implementation."""
    if RICH_AVAILABLE:
        return RichUI()
    else:
        print("Rich library not available, using simple UI.")
        return SimpleUI()
