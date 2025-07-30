"""Main tutor class for managing learning sessions."""

from typing import Optional
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from .plugin_manager import PluginManager
from .plugin import Plugin


class CLITutor:
    """Main tutor class for interactive learning sessions."""
    
    def __init__(self, plugins_dir: Path):
        self.console = Console()
        self.plugin_manager = PluginManager(plugins_dir)
        self.current_plugin: Optional[Plugin] = None
    
    def start(self):
        """Start the interactive learning session."""
        self.console.print(Panel.fit(
            "[bold blue]Welcome to CLI Tutor![/bold blue]\n"
            "Learn command-line utilities through interactive practice.",
            title="CLI Tutor"
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
        
        self.console.print("\n[bold]Available Commands:[/bold]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Command", style="cyan")
        table.add_column("Description", style="white")
        
        for plugin_name in plugins:
            info = self.plugin_manager.get_plugin_info(plugin_name)
            table.add_row(plugin_name, info.get("description", "No description"))
        
        table.add_row("quit", "Exit CLI Tutor")
        self.console.print(table)
        
        choice = Prompt.ask(
            "\n[bold]Choose a command to learn",
            choices=plugins + ["quit"],
            default="quit"
        )
        
        if choice == "quit":
            self.console.print("[yellow]Goodbye! Happy learning![/yellow]")
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
        
        # Show progress
        progress_text = f"[bold cyan]Progress: {self.current_plugin.progress}[/bold cyan]"
        progress_bar = "█" * self.current_plugin.current_task_index + "░" * (len(self.current_plugin.tasks) - self.current_plugin.current_task_index)
        self.console.print(f"\n{progress_text} {progress_bar}")
        
        # Display task
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
        self.console.print(f"\n[bold]Task {task.id}: {task.title}[/bold]")
        self.console.print(Panel(
            task.description,
            title="Task Description",
            border_style="blue"
        ))
        
        self.console.print("\n[dim]Commands: 'hint' for help, 'skip' to skip, 'quit' to return to menu[/dim]")
    
    def _show_hint(self, task):
        """Show hint for current task."""
        if task.hints:
            # Show the first hint, or join multiple hints with newlines
            if len(task.hints) == 1:
                hint_text = task.hints[0]
            else:
                hint_text = "\n".join(f"• {hint}" for hint in task.hints)
            
            self.console.print(Panel(
                hint_text,
                title="💡 Hint",
                border_style="yellow"
            ))
        else:
            self.console.print("[yellow]No hints available for this task.[/yellow]")
    
    def _correct_answer(self, task):
        """Handle correct answer."""
        self.console.print("[bold green]✓ Correct![/bold green]")
        
        if task.explanation:
            self.console.print(Panel(
                task.explanation,
                title="Explanation",
                border_style="green"
            ))
        
        if self.current_plugin.next_task():
            self.console.print("[cyan]Moving to next task...[/cyan]")
        else:
            self._session_complete()
    
    def _incorrect_answer(self, task, user_input):
        """Handle incorrect answer."""
        self.console.print(f"[bold red]✗ Incorrect.[/bold red]")
        self.console.print(f"[red]Your answer:[/red] {user_input}")
        self.console.print(f"[green]Expected:[/green] {task.command}")
        
        # Show first hint automatically
        if task.hints:
            self.console.print(Panel(
                task.hints[0],
                title="💡 Hint",
                border_style="yellow"
            ))
    
    def _skip_task(self):
        """Skip current task."""
        if self.current_plugin.next_task():
            self.console.print("[yellow]Task skipped. Moving to next task...[/yellow]")
        else:
            self._session_complete()
    
    def _session_complete(self):
        """Handle session completion."""
        self.console.print(Panel.fit(
            f"[bold green]🎉 Congratulations![/bold green]\n"
            f"You've completed all tasks for the '{self.current_plugin.name}' command!",
            title="Session Complete"
        ))
        self.current_plugin = None