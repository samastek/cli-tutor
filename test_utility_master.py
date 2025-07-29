#!/usr/bin/env python3
"""Simple test to verify Utility Master functionality."""

import sys
import os
from pathlib import Path

# Add the current directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from core.plugin_manager import PluginManager
from core.simple_ui import SimpleUI
from core.base_plugin import Task


def test_plugin_loading():
    """Test that plugins can be loaded."""
    print("Testing plugin loading...")
    manager = PluginManager()
    utilities = manager.get_available_utilities()
    
    if utilities:
        print(f"✅ Successfully loaded {len(utilities)} utilities: {', '.join(utilities)}")
        return True
    else:
        print("❌ No utilities loaded")
        return False


def test_ls_plugin():
    """Test the ls plugin functionality."""
    print("\nTesting ls plugin...")
    manager = PluginManager()
    ls_plugin = manager.get_plugin("ls")
    
    if not ls_plugin:
        print("❌ ls plugin not found")
        return False
    
    # Test getting tasks
    tasks = ls_plugin.get_tasks("beginner")
    if not tasks:
        print("❌ No beginner tasks found for ls plugin")
        return False
    
    print(f"✅ Found {len(tasks)} beginner tasks for ls")
    
    # Test task validation
    task = tasks[0]  # Basic ls task
    result = ls_plugin.validate_task(task, "ls")
    
    if result.success:
        print("✅ Task validation working correctly")
        return True
    else:
        print("❌ Task validation failed")
        return False


def test_ui():
    """Test the UI functionality."""
    print("\nTesting UI...")
    try:
        ui = SimpleUI()
        print("✅ Simple UI created successfully")
        return True
    except Exception as e:
        print(f"❌ UI creation failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 Running Utility Master tests...\n")
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    tests = [
        test_plugin_loading,
        test_ls_plugin,
        test_ui
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Utility Master is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
