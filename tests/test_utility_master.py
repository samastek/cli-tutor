"""Tests for Utility Master."""

import pytest
from utility_master.core.plugin_manager import PluginManager
from utility_master.core.simple_ui import SimpleUI
from utility_master.plugins.ls_plugin import LsPlugin


def test_plugin_loading():
    """Test that plugins can be loaded."""
    manager = PluginManager("utility_master/plugins")
    utilities = manager.get_available_utilities()
    
    assert len(utilities) >= 2  # ls and grep
    assert "ls" in utilities
    assert "grep" in utilities


def test_ls_plugin():
    """Test the ls plugin functionality."""
    plugin = LsPlugin()
    
    # Test basic properties
    assert plugin.get_utility_name() == "ls"
    assert plugin.get_name() == "LS Command Learning Plugin"
    
    # Test getting tasks
    tasks = plugin.get_tasks("beginner")
    assert len(tasks) > 0
    
    # Test task validation
    task = tasks[0]  # Basic ls task
    result = plugin.validate_task(task, "ls")
    
    assert result.success is True
    assert result.score == 100


def test_ui():
    """Test the UI functionality."""
    ui = SimpleUI()
    
    # Test utilities display
    utilities = {
        "ls": "Learn the ls command",
        "grep": "Learn the grep command"
    }
    
    # This should not raise any exceptions
    ui.show_available_utilities(utilities)


def test_task_validation():
    """Test task validation with various inputs."""
    plugin = LsPlugin()
    tasks = plugin.get_tasks("beginner")
    
    # Find the basic ls task
    basic_task = next(task for task in tasks if task.expected_command == "ls")
    
    # Test correct answer
    result = plugin.validate_task(basic_task, "ls")
    assert result.success is True
    assert result.score == 100
    
    # Test incorrect answer
    result = plugin.validate_task(basic_task, "wrong")
    assert result.success is False
    assert result.score < 100
    
    # Test partial credit
    result = plugin.validate_task(basic_task, "ls -z")
    assert result.success is False
    assert result.score > 0  # Should get some points for starting with "ls"
