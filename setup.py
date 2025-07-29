#!/usr/bin/env python3
"""Setup script for Utility Master."""

import sys
import subprocess
from pathlib import Path


def install_requirements():
    """Install required packages."""
    print("Installing required packages...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements. Please install manually:")
        print("pip install -r requirements.txt")
        return False
    return True


def setup_directories():
    """Create necessary directories."""
    directories = [
        "data/test_files",
        "plugins",
        "core"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directories created successfully!")


def main():
    """Main setup function."""
    print("🚀 Setting up Utility Master...")
    
    # Change to script directory
    script_dir = Path(__file__).parent
    import os
    os.chdir(script_dir)
    
    # Setup directories
    setup_directories()
    
    # Install requirements
    if install_requirements():
        print("\n🎉 Setup completed successfully!")
        print("\nTo run Utility Master:")
        print("python utility_master.py")
    else:
        print("\n⚠️  Setup completed with warnings.")
        print("Please install requirements manually and try running:")
        print("python utility_master.py")


if __name__ == "__main__":
    main()
