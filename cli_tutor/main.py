"""Main entry point for CLI Tutor application."""

import typer
from pathlib import Path
from .core.tutor import CLITutor

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
    manager = PluginManager(plugins_path)
    plugins = manager.get_available_plugins()
    
    if not plugins:
        typer.echo("No plugins found!")
        return
    
    typer.echo("Available plugins:")
    for plugin_name in plugins:
        info = manager.get_plugin_info(plugin_name)
        typer.echo(f"  {plugin_name}: {info.get('description', 'No description')}")


if __name__ == "__main__":
    app()