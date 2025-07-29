#!/usr/bin/env python3
"""
Demo script for Utility Master - shows basic functionality
"""

import sys
import os
from pathlib import Path

# Add the current directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from core.plugin_manager import PluginManager
from core.simple_ui import SimpleUI
from plugins.ls_plugin import LsPlugin


def demo_plugin_system():
    """Demonstrate the plugin system."""
    print("=" * 60)
    print("🔌 PLUGIN SYSTEM DEMO")
    print("=" * 60)
    
    # Load plugins
    manager = PluginManager()
    utilities = manager.get_available_utilities()
    
    print(f"📦 Loaded {len(utilities)} plugins:")
    for utility in utilities:
        plugin = manager.get_plugin(utility)
        print(f"  • {plugin.name}")
        print(f"    Command: {plugin.utility_name}")
        print(f"    Description: {plugin.description}")
        print()


def demo_ls_plugin():
    """Demonstrate the ls plugin."""
    print("=" * 60)
    print("📁 LS PLUGIN DEMO")
    print("=" * 60)
    
    plugin = LsPlugin()
    
    # Show introduction
    print("Introduction:")
    print(plugin.get_introduction())
    
    # Get beginner tasks
    tasks = plugin.get_tasks("beginner")
    print(f"📚 Found {len(tasks)} beginner tasks:")
    
    for i, task in enumerate(tasks, 1):
        print(f"\n  Task {i}: {task.description}")
        print(f"  Expected: {task.expected_command}")
        
        # Test validation with correct answer
        result = plugin.validate_task(task, task.expected_command)
        print(f"  ✅ Validation: {'PASS' if result.success else 'FAIL'} (Score: {result.score}/100)")
        
        # Test validation with incorrect answer
        result = plugin.validate_task(task, "wrong command")
        print(f"  ❌ Wrong input: {'PASS' if result.success else 'FAIL'} (Score: {result.score}/100)")
        if result.feedback:
            print(f"     Feedback: {result.feedback}")


def demo_task_examples():
    """Show examples of different task types."""
    print("=" * 60)
    print("📝 TASK EXAMPLES")
    print("=" * 60)
    
    manager = PluginManager()
    
    # Show ls tasks
    ls_plugin = manager.get_plugin("ls")
    if ls_plugin:
        print("🔍 LS Command Tasks:")
        tasks = ls_plugin.get_tasks("all")
        for task in tasks[:3]:  # Show first 3 tasks
            print(f"  • [{task.difficulty.upper()}] {task.description}")
            print(f"    Command: {task.expected_command}")
            if task.hints:
                print(f"    Hint: {task.hints[0]}")
            print()
    
    # Show grep tasks
    grep_plugin = manager.get_plugin("grep")
    if grep_plugin:
        print("🔍 GREP Command Tasks:")
        tasks = grep_plugin.get_tasks("all")
        for task in tasks[:3]:  # Show first 3 tasks
            print(f"  • [{task.difficulty.upper()}] {task.description}")
            print(f"    Command: {task.expected_command}")
            if task.hints:
                print(f"    Hint: {task.hints[0]}")
            print()


def demo_ui():
    """Demonstrate the UI system."""
    print("=" * 60)
    print("🖥️  UI SYSTEM DEMO")
    print("=" * 60)
    
    ui = SimpleUI()
    
    # Demo utilities display
    utilities = {
        "ls": "Learn the ls command for listing directory contents",
        "grep": "Learn the grep command for searching text patterns"
    }
    
    print("Utilities display:")
    ui.show_available_utilities(utilities)
    
    # Demo task display
    from core.base_plugin import Task
    demo_task = Task(
        id="demo",
        description="This is a demonstration task",
        expected_command="demo command",
        difficulty="beginner",
        hints=["This is just a demo", "No real execution needed"]
    )
    
    print("\nTask display:")
    ui.show_task(demo_task, 1, 3)


def main():
    """Run the demo."""
    print("🚀 Utility Master Demo")
    print("Demonstrating the educational CLI learning tool\n")
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    try:
        demo_plugin_system()
        demo_ls_plugin()
        demo_task_examples()
        demo_ui()
        
        print("=" * 60)
        print("✅ Demo completed successfully!")
        print("=" * 60)
        print("\nTo start learning, run: python utility_master.py")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
