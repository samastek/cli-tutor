"""Main tutor class for managing learning sessions."""

from typing import Optional
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.rule import Rule
from rich.text import Text

from .plugin_manager import PluginManager
from .plugin import Plugin
from .progress_tracker import ProgressTracker


class CLITutor:
    """Main tutor class for interactive learning sessions."""
    
    def __init__(self, plugins_dir: Path):
        self.console = Console()
        self.progress_tracker = ProgressTracker()
        self.plugin_manager = PluginManager(plugins_dir, self.progress_tracker)
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
        
        # Show overall stats
        stats = self.progress_tracker.get_overall_stats()
        if stats["total_tasks_completed"] > 0:
            stats_text = (
                f"📊 [dim]Your Progress:[/dim] "
                f"[green]{stats['total_tasks_completed']}[/green] tasks completed • "
                f"[cyan]{stats['commands_completed']}[/cyan] commands mastered • "
                f"[yellow]{stats['commands_started']}[/yellow] commands started"
            )
            self.console.print(Panel.fit(stats_text, border_style="dim"))
            self.console.print()
        
        # Clear visual separation
        self._print_section_separator("📚 Available Commands", "bright_magenta")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("🔧 Command", style="cyan", width=15)
        table.add_column("📝 Description", style="white")
        table.add_column("📈 Progress", style="green", width=12)
        
        for plugin_name in plugins:
            info = self.plugin_manager.get_plugin_info(plugin_name)
            
            # Get progress for this plugin
            progress_info = self.progress_tracker.get_plugin_progress(plugin_name)
            if progress_info:
                completed = progress_info["completed_tasks"]
                total = progress_info["total_tasks"]
                progress_text = f"{completed}/{total}"
                if progress_info["is_completed"]:
                    progress_text += " ✅"
                elif completed > 0:
                    progress_text += " 🔄"
                else:
                    progress_text = "New"
            else:
                progress_text = "New"
            
            # Check if this is a madness mode plugin
            plugin = self.plugin_manager.load_plugin(plugin_name)
            if plugin.is_madness_mode:
                # Special styling for madness mode plugins
                command_display = f"🔥 {plugin_name} 🔥"
                description_display = f"[red]{info.get('description', 'No description')}[/red] [bold red](MADNESS MODE - 100 exercises!)[/bold red]"
                if progress_info and progress_info["completed_tasks"] >= 50:
                    progress_text += " ⚡"
                elif progress_info and progress_info["completed_tasks"] >= 25:
                    progress_text += " 🚀"
                elif progress_info and progress_info["completed_tasks"] >= 10:
                    progress_text += " 💪"
            else:
                command_display = plugin_name
                description_display = info.get("description", "No description")
            
            table.add_row(command_display, description_display, progress_text)
        
        table.add_row("📊 progress", "[dim]View detailed progress report[/dim]", "")
        table.add_row("🗑️ reset", "[dim]Reset progress for a command[/dim]", "")
        table.add_row("❌ quit", "[dim]Exit CLI Tutor[/dim]", "")
        self.console.print(table)
        
        self.console.print()
        while True:
            choice = Prompt.ask(
                "[bold]Choose a command to learn",
                default="quit"
            )
            
            # Validate the choice
            valid_choices = plugins + ["progress", "reset", "quit"]
            if choice in valid_choices:
                break
            else:
                self.console.print(f"[red]Invalid choice: '{choice}'. Please choose from the table above.[/red]")
                self.console.print()
        
        if choice == "quit":
            self._print_section_separator("👋 Goodbye", "bright_yellow")
            self.console.print(Panel.fit(
                "[yellow]Happy learning! Come back anytime to master more commands.[/yellow]",
                border_style="yellow"
            ))
            exit(0)
        elif choice == "progress":
            self._show_progress_report()
        elif choice == "reset":
            self._show_reset_menu()
        else:
            self.current_plugin = self.plugin_manager.load_plugin(choice)
            self.current_plugin.reset()  # This now resets to first incomplete task
    
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
        
        # Show enhanced progress for madness mode (like Vim)
        if self.current_plugin.is_madness_mode:
            self._show_madness_mode_progress()
        else:
            self._show_standard_progress()
        
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
        elif user_input.lower() in ["reset", "r"]:
            self._reset_current_plugin()
            return
        elif user_input.lower() in ["progress", "p"] and self.current_plugin.is_madness_mode:
            self._show_chapter_progress()
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
        
        # Add chapter info for madness mode
        if self.current_plugin.is_madness_mode and hasattr(task, 'chapter'):
            task_header.append(f" (Ch {task.chapter})", style="dim cyan")
        
        task_header.append(": ", style="bold white")
        task_header.append(task.title, style="bold green")
        
        # Add difficulty indicator for madness mode
        if self.current_plugin.is_madness_mode:
            difficulty_colors = {
                "beginner": "green",
                "intermediate": "yellow", 
                "advanced": "red",
                "legendary": "magenta"
            }
            difficulty_color = difficulty_colors.get(task.difficulty, "white")
            task_header.append(f" [{difficulty_color}][{task.difficulty.upper()}][/{difficulty_color}]", style=difficulty_color)
        
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
        if self.current_plugin.is_madness_mode:
            commands_help = (
                "[dim italic]💡 Commands:[/dim italic] "
                "[yellow]'hint'[/yellow] for help • "
                "[yellow]'skip'[/yellow] to skip • "
                "[yellow]'progress'[/yellow] for chapter progress • "
                "[yellow]'reset'[/yellow] to restart • "
                "[yellow]'quit'[/yellow] to return to menu"
            )
        else:
            commands_help = (
                "[dim italic]💡 Commands:[/dim italic] "
                "[yellow]'hint'[/yellow] for help • "
                "[yellow]'skip'[/yellow] to skip • "
                "[yellow]'reset'[/yellow] to restart this command • "
                "[yellow]'quit'[/yellow] to return to menu"
            )
        self.console.print(Panel.fit(
            commands_help,
            border_style="dim",
            padding=(0, 1)
        ))
    
    def _show_madness_mode_progress(self):
        """Show enhanced progress for madness mode plugins like Vim."""
        progress_summary = self.current_plugin.get_progress_summary()
        completed = progress_summary["completed_tasks"]
        total = progress_summary["total_tasks"]
        current_task = self.current_plugin.current_task
        
        # Main progress bar
        completed_blocks = int((completed / total) * 30) if total > 0 else 0
        remaining_blocks = 30 - completed_blocks
        progress_bar = "█" * completed_blocks + "░" * remaining_blocks
        
        # Current task info with chapter
        task_info = f"Task {current_task.id}/100"
        if hasattr(current_task, 'chapter'):
            task_info += f" • Chapter {current_task.chapter}"
        task_info += f" • {current_task.difficulty.title()}"
        
        progress_text = (
            f"[bold red]🔥 VIM MADNESS MODE 🔥[/bold red]\n"
            f"[bold cyan]Progress: {completed}/{total}[/bold cyan] {progress_bar}\n"
            f"[dim]{task_info}[/dim]"
        )
        
        if progress_summary["is_complete"]:
            progress_text += "\n[green]🏆 MADNESS CONQUERED! 🏆[/green]"
        elif completed >= 50:
            progress_text += "\n[yellow]⚡ Vim Warrior Level! ⚡[/yellow]"
        elif completed >= 25:
            progress_text += "\n[blue]🚀 Getting Dangerous! 🚀[/blue]"
        elif completed >= 10:
            progress_text += "\n[green]💪 Building Skills! 💪[/green]"
        
        progress_panel = Panel(
            progress_text,
            title=f"[bold red]VIM MASTERY JOURNEY[/bold red]",
            title_align="center",
            border_style="red",
            padding=(1, 2)
        )
        self.console.print(progress_panel)
    
    def _show_standard_progress(self):
        """Show standard progress display for regular plugins."""
        progress_summary = self.current_plugin.get_progress_summary()
        completed = progress_summary["completed_tasks"]
        total = progress_summary["total_tasks"]
        progress_ratio = f"{completed}/{total}"
        
        # Create a more detailed progress bar
        completed_blocks = int((completed / total) * 20) if total > 0 else 0
        remaining_blocks = 20 - completed_blocks
        progress_bar = "█" * completed_blocks + "░" * remaining_blocks
        
        progress_text = f"[bold cyan]Progress: {progress_ratio}[/bold cyan] {progress_bar}"
        if progress_summary["is_complete"]:
            progress_text += " [green]✅ Complete![/green]"
        elif completed > 0:
            progress_text += f" [yellow]🔄 Resume at task {self.current_plugin.current_task_index + 1}[/yellow]"
        
        progress_panel = Panel.fit(
            progress_text,
            title=f"[bold]{self.current_plugin.name.upper()} Learning Session[/bold]",
            border_style="cyan"
        )
        self.console.print(progress_panel)
    
    def _show_chapter_progress(self):
        """Show detailed chapter progress for madness mode."""
        if not self.current_plugin.is_madness_mode:
            return
            
        self._print_section_separator("📚 Chapter Progress", "bright_magenta")
        
        chapter_progress = self.current_plugin.get_chapter_progress()
        if not chapter_progress:
            self.console.print("[dim]No chapter information available.[/dim]")
            return
        
        # Chapter mapping for Vim
        chapter_names = {
            1: "Starting & Basics",
            2: "Buffers, Windows, Tabs", 
            4: "Vim Grammar",
            5: "Moving in Files",
            6: "Insert Mode",
            7: "The Dot Command",
            8: "Registers",
            9: "Macros",
            10: "Undo",
            11: "Visual Mode",
            12: "Search & Substitute",
            13: "Global Commands",
            14: "External Commands",
            17: "Folding",
            22: "Configuration",
            99: "Mastery"
        }
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Chapter", style="cyan", width=8)
        table.add_column("Topic", style="white", width=25)
        table.add_column("Progress", style="green", width=12)
        table.add_column("Status", style="yellow", width=15)
        
        for chapter_num in sorted(chapter_progress.keys()):
            progress_data = chapter_progress[chapter_num]
            chapter_name = chapter_names.get(chapter_num, "Advanced Topics")
            
            progress_text = f"{progress_data['completed']}/{progress_data['total']}"
            percentage = f"{progress_data['percentage']:.0f}%"
            
            if progress_data['is_complete']:
                status = "✅ Complete"
            elif progress_data['completed'] > 0:
                status = "🔄 In Progress"
            else:
                status = "⭐ Not Started"
            
            table.add_row(
                f"Ch {chapter_num}",
                chapter_name,
                f"{progress_text} ({percentage})",
                status
            )
        
        self.console.print(table)
        self.console.print()
        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")
    
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
        
        if self.current_plugin.is_madness_mode:
            # Special celebration for madness mode
            celebration_messages = [
                "🔥 VIM POWER! 🔥",
                "⚡ LIGHTNING FAST! ⚡", 
                "🚀 UNSTOPPABLE! 🚀",
                "💪 VIM STRONG! 💪",
                "🧙‍♂️ WIZARD MOVE! 🧙‍♂️",
                "🏆 CHAMPION! 🏆"
            ]
            import random
            celebration = random.choice(celebration_messages)
            
            self.console.print(Panel.fit(
                f"✅ [bold green]Correct![/bold green] {celebration}",
                border_style="green",
                padding=(0, 2)
            ))
        else:
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
                "[cyan]Moving to next challenge...[/cyan]" if self.current_plugin.is_madness_mode else "[cyan]Moving to next incomplete task...[/cyan]",
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
                "[cyan]Moving to next incomplete task...[/cyan]",
                border_style="cyan"
            ))
        else:
            self._session_complete()
    
    def _session_complete(self):
        """Handle session completion."""
        # Major visual separator for session completion
        if self.current_plugin.is_madness_mode:
            self._print_section_separator("� VIM MADNESS CONQUERED! 🏆", "bright_red")
            
            completion_message = (
                f"[bold red]🔥 INCREDIBLE! 🔥[/bold red]\n\n"
                f"You've conquered all [bold yellow]100 Vim exercises[/bold yellow] in [bold red]MADNESS MODE[/bold red]!\n\n"
                f"[bold green]You are now a VIM MASTER![/bold green]\n\n"
                f"[dim]From basic movements to advanced text objects, macros, and beyond...\n"
                f"You've mastered the ancient art of Vim wizardry!\n\n"
                f"hjkl will never be the same again. 🧙‍♂️✨[/dim]"
            )
            
            title = "🧙‍♂️ VIM WIZARD ACHIEVED 🧙‍♂️"
            border_style = "bright_red"
        else:
            self._print_section_separator("�🎉 SESSION COMPLETE", "bright_green")
            
            completion_message = (
                f"[bold green]Congratulations![/bold green]\n\n"
                f"You've successfully completed all tasks for the "
                f"[bold cyan]'{self.current_plugin.name}'[/bold cyan] command!\n\n"
                f"[dim]You're now ready to use this command confidently in real scenarios.[/dim]"
            )
            
            title = "🏆 Achievement Unlocked"
            border_style = "bright_green"
        
        self.console.print(Panel(
            completion_message,
            title=title,
            title_align="center",
            border_style=border_style,
            padding=(2, 4)
        ))
        
        self.current_plugin = None
        
        # Separator before returning to menu
        self._print_section_separator("Returning to Main Menu", "bright_blue")
    
    def _show_progress_report(self):
        """Show detailed progress report."""
        self._print_section_separator("📊 Progress Report", "bright_cyan")
        
        stats = self.progress_tracker.get_overall_stats()
        summary = self.progress_tracker.get_plugin_summary()
        
        # Overall stats
        overall_panel = Panel(
            f"[green]Total Tasks Completed:[/green] {stats['total_tasks_completed']}\n"
            f"[cyan]Commands Started:[/cyan] {stats['commands_started']}\n"
            f"[yellow]Commands Mastered:[/yellow] {stats['commands_completed']}",
            title="🏆 Overall Statistics",
            title_align="center",
            border_style="bright_cyan",
            padding=(1, 2)
        )
        self.console.print(overall_panel)
        
        if summary:
            self.console.print()
            
            # Progress table
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Command", style="cyan", width=15)
            table.add_column("Progress", style="white", width=12)
            table.add_column("Percentage", style="green", width=12)
            table.add_column("Status", style="yellow", width=12)
            table.add_column("Last Accessed", style="dim", width=20)
            
            for plugin_info in summary:
                status = "✅ Complete" if plugin_info["is_completed"] else "🔄 In Progress"
                progress = f"{plugin_info['completed_tasks']}/{plugin_info['total_tasks']}"
                percentage = f"{plugin_info['progress_percentage']:.1f}%"
                
                table.add_row(
                    plugin_info["plugin_name"],
                    progress,
                    percentage,
                    status,
                    plugin_info["last_accessed"][:16] if plugin_info["last_accessed"] else "Never"
                )
            
            self.console.print(table)
        
        self.console.print()
        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")
    
    def _show_reset_menu(self):
        """Show reset options menu."""
        self._print_section_separator("🗑️ Reset Progress", "bright_red")
        
        self.console.print("[yellow]⚠️  Warning: This will permanently delete progress data![/yellow]")
        self.console.print()
        
        # Get plugins with progress
        summary = self.progress_tracker.get_plugin_summary()
        if not summary:
            self.console.print(Panel.fit(
                "[dim]No progress to reset.[/dim]",
                border_style="dim"
            ))
            return
        
        table = Table(show_header=True, header_style="bold red")
        table.add_column("Option", style="cyan", width=20)
        table.add_column("Description", style="white")
        
        for plugin_info in summary:
            table.add_row(
                plugin_info["plugin_name"],
                f"Reset {plugin_info['completed_tasks']} completed tasks"
            )
        
        table.add_row("all", "[red]Reset ALL progress (nuclear option)[/red]")
        table.add_row("cancel", "[dim]Cancel and return to menu[/dim]")
        
        self.console.print(table)
        self.console.print()
        
        choices = [p["plugin_name"] for p in summary] + ["all", "cancel"]
        choice = Prompt.ask(
            "[bold red]What would you like to reset?",
            choices=choices,
            default="cancel"
        )
        
        if choice == "cancel":
            return
        elif choice == "all":
            if Confirm.ask("[bold red]Are you absolutely sure you want to reset ALL progress?"):
                self.progress_tracker.reset_all_progress()
                self.console.print(Panel.fit(
                    "[green]✅ All progress has been reset.[/green]",
                    border_style="green"
                ))
        else:
            if Confirm.ask(f"[red]Reset progress for '{choice}'?"):
                self.progress_tracker.reset_plugin_progress(choice)
                self.console.print(Panel.fit(
                    f"[green]✅ Progress for '{choice}' has been reset.[/green]",
                    border_style="green"
                ))
        
        self.console.print()
        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")
    
    def _reset_current_plugin(self):
        """Reset progress for the current plugin."""
        if not self.current_plugin:
            return
        
        self.console.print()
        if Confirm.ask(f"[yellow]Reset all progress for '{self.current_plugin.name}'?"):
            self.current_plugin.reset_progress()
            self.current_plugin.reset()
            self.console.print(Panel.fit(
                f"[green]✅ Progress for '{self.current_plugin.name}' has been reset.[/green]",
                border_style="green"
            ))
        else:
            self.console.print(Panel.fit(
                "[dim]Reset cancelled.[/dim]",
                border_style="dim"
            ))