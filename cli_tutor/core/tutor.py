"""Main tutor class for managing learning sessions."""

from typing import Optional
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.rule import Rule
from rich.text import Text

from .plugin_manager import PluginManager
from .plugin import Plugin


class CLITutor:
    """Main tutor class for interactive learning sessions."""
    
    def __init__(self, plugins_dir: Path):
        self.console = Console()
        self.plugin_manager = PluginManager(plugins_dir)
        self.current_plugin: Optional[Plugin] = None
    
    def _print_section_separator(self, title: str = "", style: str = "bright_blue"):
        """Print a visual separator between sections."""
        self.console.print()
        if title:
            self.console.print(Rule(title, style=style))
        else:
            self.console.print(Rule(style=style))
        self.console.print()
    
    def start(self):
        """Start the interactive learning session."""
        # Clear welcome with visual separation
        self.console.print()
        welcome_text = (
            "[bold blue]Welcome to CLI Tutor![/bold blue]\n\n"
            "[white]Master command-line utilities through interactive practice.[/white]\n"
            "[dim]Learn at your own pace with hints, explanations, and real examples.[/dim]"
        )
        
        self.console.print(Panel(
            welcome_text,
            title="🚀 CLI Tutor",
            title_align="center",
            border_style="bright_blue",
            padding=(2, 4)
        ))
        
        while True:
            if not self.current_plugin:
                self._show_plugin_selection()
            else:
                self._run_current_session()
    
    def _show_plugin_selection(self):
        """Display available plugins and let user choose."""
        plugins = self.plugin_manager.get_available_plugins()
        
        if not plugins:
            self.console.print("[red]No plugins found! Please add some plugin modules.[/red]")
            return
        
        # Clear visual separation
        self._print_section_separator("📚 Available Commands", "bright_magenta")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("🔧 Command", style="cyan", width=15)
        table.add_column("📝 Description", style="white")
        
        for plugin_name in plugins:
            info = self.plugin_manager.get_plugin_info(plugin_name)
            table.add_row(plugin_name, info.get("description", "No description"))
        
        table.add_row("❌ quit", "[dim]Exit CLI Tutor[/dim]")
        self.console.print(table)
        
        self.console.print()
        choice = Prompt.ask(
            "[bold]Choose a command to learn",
            choices=plugins + ["quit"],
            default="quit"
        )
        
        if choice == "quit":
            self._print_section_separator("👋 Goodbye", "bright_yellow")
            self.console.print(Panel.fit(
                "[yellow]Happy learning! Come back anytime to master more commands.[/yellow]",
                border_style="yellow"
            ))
            exit(0)
        else:
            self.current_plugin = self.plugin_manager.load_plugin(choice)
            self.current_plugin.reset()
    
    def _run_current_session(self):
        """Run the learning session for current plugin."""
        if not self.current_plugin or self.current_plugin.is_complete:
            self._session_complete()
            return
        
        task = self.current_plugin.current_task
        if not task:
            self._session_complete()
            return
        
        # Clear visual separation before new task
        self._print_section_separator()
        
        # Show progress with enhanced formatting
        progress_ratio = f"{self.current_plugin.current_task_index}/{len(self.current_plugin.tasks)}"
        progress_bar = "█" * self.current_plugin.current_task_index + "░" * (len(self.current_plugin.tasks) - self.current_plugin.current_task_index)
        
        progress_panel = Panel.fit(
            f"[bold cyan]Progress: {progress_ratio}[/bold cyan] {progress_bar}",
            title=f"[bold]{self.current_plugin.name.upper()} Learning Session[/bold]",
            border_style="cyan"
        )
        self.console.print(progress_panel)
        
        # Display task with clear separation
        self._display_task(task)
        
        # Get user input
        user_input = Prompt.ask("[bold green]Your answer")
        
        # Handle special commands
        if user_input.lower() in ["quit", "q"]:
            self.current_plugin = None
            return
        elif user_input.lower() in ["hint", "h"]:
            self._show_hint(task)
            return
        elif user_input.lower() in ["skip", "s"]:
            self._skip_task()
            return
        
        # Check answer
        if task.check_answer(user_input):
            self._correct_answer(task)
        else:
            self._incorrect_answer(task, user_input)
    
    def _display_task(self, task):
        """Display the current task."""
        # Task header with clear formatting
        task_header = Text()
        task_header.append("Task ", style="bold white")
        task_header.append(str(task.id), style="bold yellow")
        task_header.append(": ", style="bold white")
        task_header.append(task.title, style="bold green")
        
        self.console.print()
        self.console.print(task_header)
        
        # Task description in a prominent panel
        self.console.print(Panel(
            task.description,
            title="📋 Task Description",
            title_align="left",
            border_style="blue",
            padding=(1, 2)
        ))
        
        # Commands help in a subtle panel
        commands_help = (
            "[dim italic]💡 Commands:[/dim italic] "
            "[yellow]'hint'[/yellow] for help • "
            "[yellow]'skip'[/yellow] to skip • "
            "[yellow]'quit'[/yellow] to return to menu"
        )
        self.console.print(Panel.fit(
            commands_help,
            border_style="dim",
            padding=(0, 1)
        ))
    
    def _show_hint(self, task):
        """Show hint for current task."""
        if task.hints:
            # Show the first hint, or join multiple hints with newlines
            if len(task.hints) == 1:
                hint_text = task.hints[0]
            else:
                hint_text = "\n".join(f"• {hint}" for hint in task.hints)
            
            self.console.print()
            self.console.print(Panel(
                hint_text,
                title="💡 Hint",
                title_align="left",
                border_style="yellow",
                padding=(1, 2)
            ))
        else:
            self.console.print()
            self.console.print(Panel.fit(
                "[yellow]No hints available for this task.[/yellow]",
                border_style="yellow"
            ))
    
    def _correct_answer(self, task):
        """Handle correct answer."""
        # Visual separator and success message
        self.console.print()
        self.console.print(Panel.fit(
            "✅ [bold green]Correct![/bold green]",
            border_style="green",
            padding=(0, 2)
        ))
        
        if task.explanation:
            self.console.print(Panel(
                task.explanation,
                title="💡 Explanation",
                title_align="left",
                border_style="green",
                padding=(1, 2)
            ))
        
        if self.current_plugin.next_task():
            self.console.print(Panel.fit(
                "[cyan]Moving to next task...[/cyan]",
                border_style="cyan"
            ))
        else:
            self._session_complete()
    
    def _incorrect_answer(self, task, user_input):
        """Handle incorrect answer."""
        # Visual separator and error message
        self.console.print()
        self.console.print(Panel.fit(
            "❌ [bold red]Incorrect.[/bold red]",
            border_style="red",
            padding=(0, 2)
        ))
        
        # Show comparison in a clear format
        comparison_text = (
            f"[red]Your answer:[/red] [white]{user_input}[/white]\n"
            f"[green]Expected:[/green] [white]{task.command}[/white]"
        )
        self.console.print(Panel(
            comparison_text,
            title="📝 Answer Comparison",
            title_align="left",
            border_style="red",
            padding=(1, 2)
        ))
        
        # Show first hint automatically
        if task.hints:
            self.console.print(Panel(
                task.hints[0],
                title="💡 Hint",
                title_align="left",
                border_style="yellow",
                padding=(1, 2)
            ))
    
    def _skip_task(self):
        """Skip current task."""
        self.console.print()
        self.console.print(Panel.fit(
            "[yellow]⏭️ Task skipped[/yellow]",
            border_style="yellow"
        ))
        
        if self.current_plugin.next_task():
            self.console.print(Panel.fit(
                "[cyan]Moving to next task...[/cyan]",
                border_style="cyan"
            ))
        else:
            self._session_complete()
    
    def _session_complete(self):
        """Handle session completion."""
        # Major visual separator for session completion
        self._print_section_separator("🎉 SESSION COMPLETE", "bright_green")
        
        completion_message = (
            f"[bold green]Congratulations![/bold green]\n\n"
            f"You've successfully completed all tasks for the "
            f"[bold cyan]'{self.current_plugin.name}'[/bold cyan] command!\n\n"
            f"[dim]You're now ready to use this command confidently in real scenarios.[/dim]"
        )
        
        self.console.print(Panel(
            completion_message,
            title="🏆 Achievement Unlocked",
            title_align="center",
            border_style="bright_green",
            padding=(2, 4)
        ))
        
        self.current_plugin = None
        
        # Separator before returning to menu
        self._print_section_separator("Returning to Main Menu", "bright_blue")