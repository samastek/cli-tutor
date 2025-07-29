#!/usr/bin/env python3
"""
Utility Master - Interactive CLI Learning Tool

An educational tool that helps users learn command-line utilities through
interactive tasks and immediate feedback.
"""

import sys
import os
from pathlib import Path
from typing import List, Optional

# Add the current directory to the Python path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

from core.plugin_manager import PluginManager
from core.task_manager import TaskManager
from core.ui import UI
from core.base_plugin import Task, BasePlugin


class UtilityMaster:
    """Main application class for Utility Master."""
    
    def __init__(self):
        self.ui = UI()
        self.plugin_manager = PluginManager()
        self.task_manager = TaskManager()
        self.current_plugin: Optional[BasePlugin] = None
    
    def run(self) -> None:
        """Main application loop."""
        try:
            self.ui.print_welcome()
            
            while True:
                # Check if any plugins are available
                available_utilities = self.plugin_manager.get_available_utilities()
                
                if not available_utilities:
                    self.ui.print_error("No utility plugins found. Please check the plugins directory.")
                    break
                
                # Show available utilities
                plugin_info = self.plugin_manager.get_plugin_info()
                self.ui.show_available_utilities(plugin_info)
                
                # Let user select a utility
                selected_utility = self.ui.select_utility(available_utilities)
                
                if not selected_utility:
                    self.ui.print_error("Invalid selection.")
                    continue
                
                # Get the plugin and start learning session
                plugin = self.plugin_manager.get_plugin(selected_utility)
                if plugin:
                    self.start_learning_session(plugin)
                
                # Ask if user wants to continue with another utility
                if not self.ui.ask_continue("Would you like to learn another utility?"):
                    break
            
            self.ui.print_info("Thank you for using Utility Master! Keep practicing!")
        
        except KeyboardInterrupt:
            self.ui.print_info("\nGoodbye! Thanks for using Utility Master!")
        except Exception as e:
            self.ui.print_error(f"An unexpected error occurred: {e}")
    
    def start_learning_session(self, plugin: BasePlugin) -> None:
        """Start a learning session for a specific utility."""
        self.current_plugin = plugin
        
        # Show introduction
        self.ui.console.print(f"\n[bold cyan]{plugin.get_introduction()}[/bold cyan]")
        
        # Select difficulty
        difficulty = self.ui.select_difficulty()
        
        # Get tasks for the selected difficulty
        tasks = plugin.get_tasks(difficulty)
        
        if not tasks:
            self.ui.print_error(f"No tasks found for difficulty: {difficulty}")
            return
        
        # Setup plugin environment
        if not plugin.setup_environment():
            self.ui.print_error("Failed to setup plugin environment.")
            return
        
        try:
            self.run_tasks(plugin, tasks)
        finally:
            # Cleanup plugin environment
            plugin.cleanup_environment()
    
    def run_tasks(self, plugin: BasePlugin, tasks: List[Task]) -> None:
        """Run through all tasks in a learning session."""
        total_tasks = len(tasks)
        correct_tasks = 0
        total_score = 0
        max_score = total_tasks * 100
        
        for i, task in enumerate(tasks, 1):
            self.ui.show_task(task, i, total_tasks)
            
            attempt_count = 0
            max_attempts = 3
            task_completed = False
            
            while attempt_count < max_attempts and not task_completed:
                attempt_count += 1
                
                # Get user input
                user_input = self.ui.get_user_input()
                
                # Skip task if user enters empty string
                if not user_input.strip():
                    self.ui.print_info("Task skipped.")
                    break
                
                # Special commands
                if user_input.lower() in ['quit', 'exit']:
                    return
                elif user_input.lower() == 'hint':
                    hint = self.task_manager.get_hint(task, attempt_count)
                    if hint:
                        self.ui.show_hint(hint)
                    else:
                        self.ui.print_info("No hints available for this task.")
                    continue
                elif user_input.lower() == 'skip':
                    self.ui.print_info("Task skipped.")
                    break
                
                # Validate the task
                result = self.task_manager.run_task(plugin, task, user_input)
                self.ui.show_task_result(result)
                
                if result.success:
                    correct_tasks += 1
                    total_score += result.score
                    task_completed = True
                else:
                    total_score += result.score
                    
                    if attempt_count < max_attempts:
                        remaining = max_attempts - attempt_count
                        self.ui.print_info(f"Try again! {remaining} attempt(s) remaining.")
                        self.ui.print_info("Type 'hint' for a hint, 'skip' to skip this task.")
                    else:
                        self.ui.print_info(f"Max attempts reached. The correct answer was: {task.expected_command}")
            
            # Ask if user wants to continue to next task
            if i < total_tasks:
                if not self.ui.ask_continue("Continue to next task?"):
                    break
        
        # Show session summary
        self.ui.show_session_summary(total_tasks, correct_tasks, total_score, max_score)


def main():
    """Entry point for the application."""
    # Change to the script directory to ensure relative imports work
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    app = UtilityMaster()
    app.run()


if __name__ == "__main__":
    main()
