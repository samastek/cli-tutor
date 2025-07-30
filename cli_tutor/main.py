"""Main entry point for CLI Tutor application."""

import typer
from pathlib import Path
from .core.tutor import CLITutor
from .core.progress_tracker import ProgressTracker

app = typer.Typer(
    name="cli-tutor",
    help="Interactive CLI tool for learning command-line utilities"
)


@app.command()
def start(
    plugins_dir: str = typer.Option(
        None,
        "--plugins-dir",
        "-p",
        help="Path to plugins directory (default: built-in plugins)"
    )
):
    """Start the interactive CLI learning session."""
    if plugins_dir:
        plugins_path = Path(plugins_dir)
    else:
        # Use built-in plugins directory
        plugins_path = Path(__file__).parent / "plugins"
    
    if not plugins_path.exists():
        typer.echo(f"Error: Plugins directory '{plugins_path}' not found!", err=True)
        raise typer.Exit(1)
    
    tutor = CLITutor(plugins_path)
    try:
        tutor.start()
    except KeyboardInterrupt:
        typer.echo("\n\nGoodbye! Happy learning!")
        raise typer.Exit(0)


@app.command()
def list_plugins(
    plugins_dir: str = typer.Option(
        None,
        "--plugins-dir",
        "-p",
        help="Path to plugins directory (default: built-in plugins)"
    )
):
    """List available plugins."""
    if plugins_dir:
        plugins_path = Path(plugins_dir)
    else:
        plugins_path = Path(__file__).parent / "plugins"
    
    if not plugins_path.exists():
        typer.echo(f"Error: Plugins directory '{plugins_path}' not found!", err=True)
        raise typer.Exit(1)
    
    from .core.plugin_manager import PluginManager
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    
    console = Console()
    manager = PluginManager(plugins_path)
    plugins = manager.get_available_plugins()
    
    if not plugins:
        console.print("[red]No plugins found![/red]")
        return
    
    # Create a nice table for plugin listing
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Command", style="cyan", width=15)
    table.add_column("Description", style="white")
    table.add_column("Category", style="green", width=15)
    
    for plugin_name in plugins:
        info = manager.get_plugin_info(plugin_name)
        table.add_row(
            plugin_name, 
            info.get('description', 'No description'),
            info.get('category', 'general')
        )
    
    console.print(Panel(
        table,
        title="📚 Available CLI Commands",
        title_align="center",
        border_style="bright_cyan"
    ))


@app.command()
def progress(
    plugins_dir: str = typer.Option(
        None,
        "--plugins-dir",
        "-p",
        help="Path to plugins directory (default: built-in plugins)"
    )
):
    """Show detailed progress report."""
    if plugins_dir:
        plugins_path = Path(plugins_dir)
    else:
        plugins_path = Path(__file__).parent / "plugins"
    
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    
    console = Console()
    progress_tracker = ProgressTracker()
    
    stats = progress_tracker.get_overall_stats()
    summary = progress_tracker.get_plugin_summary()
    
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
    console.print(overall_panel)
    
    if summary:
        console.print()
        
        # Progress table
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Command", style="cyan", width=15)
        table.add_column("Progress", style="white", width=12)
        table.add_column("Percentage", style="green", width=12)
        table.add_column("Status", style="yellow", width=12)
        
        for plugin_info in summary:
            status = "✅ Complete" if plugin_info["is_completed"] else "🔄 In Progress"
            progress = f"{plugin_info['completed_tasks']}/{plugin_info['total_tasks']}"
            percentage = f"{plugin_info['progress_percentage']:.1f}%"
            
            table.add_row(
                plugin_info["plugin_name"],
                progress,
                percentage,
                status
            )
        
        console.print(Panel(
            table,
            title="📊 Detailed Progress",
            title_align="center",
            border_style="green"
        ))
    else:
        console.print("\n[dim]No progress recorded yet. Start learning with 'cli-tutor start'![/dim]")


@app.command()
def reset_progress(
    command: str = typer.Argument(None, help="Command to reset (or 'all' for everything)"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation prompt")
):
    """Reset progress for a specific command or all commands."""
    progress_tracker = ProgressTracker()
    
    from rich.console import Console
    from rich.prompt import Confirm
    from rich.panel import Panel
    
    console = Console()
    
    if command == "all":
        if force or Confirm.ask("[bold red]Are you sure you want to reset ALL progress?"):
            progress_tracker.reset_all_progress()
            console.print(Panel.fit(
                "[green]✅ All progress has been reset.[/green]",
                border_style="green"
            ))
        else:
            console.print("[dim]Reset cancelled.[/dim]")
    elif command:
        if force or Confirm.ask(f"[red]Reset progress for '{command}'?"):
            progress_tracker.reset_plugin_progress(command)
            console.print(Panel.fit(
                f"[green]✅ Progress for '{command}' has been reset.[/green]",
                border_style="green"
            ))
        else:
            console.print("[dim]Reset cancelled.[/dim]")
    else:
        console.print("[red]Error: Please specify a command name or 'all'[/red]")
        console.print("[dim]Example: cli-tutor reset-progress ls[/dim]")
        console.print("[dim]Example: cli-tutor reset-progress all[/dim]")


@app.command()
def export_progress(
    output_file: str = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path (default: progress_backup.json)"
    )
):
    """Export progress data for backup."""
    import json
    from datetime import datetime
    from rich.console import Console
    from rich.panel import Panel
    
    console = Console()
    progress_tracker = ProgressTracker()
    
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"cli_tutor_progress_{timestamp}.json"
    
    try:
        data = progress_tracker.export_progress()
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        console.print(Panel.fit(
            f"[green]✅ Progress exported to '{output_file}'[/green]",
            border_style="green"
        ))
        
    except Exception as e:
        console.print(f"[red]Error exporting progress: {e}[/red]")


if __name__ == "__main__":
    app()