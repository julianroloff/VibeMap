#!/usr/bin/env python3
import os
import sys
import pytest
import subprocess

def run_tests():
    """Run all tests for the ML service"""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add the parent directory to the path
    sys.path.append(script_dir)
    
    # Set testing environment variable
    os.environ["TESTING"] = "True"
    
    # Check and install required packages
    required_packages = [
        "pydantic-settings>=2.0.0",
        "pytest-asyncio>=0.18.0",
        "pytest-mock>=3.6.1",
        "aiosqlite>=0.17.0"
    ]
    
    for package in required_packages:
        try:
            package_name = package.split(">=")[0]
            __import__(package_name.replace("-", "_"))
            print(f"{package_name} is installed.")
        except ImportError:
            print(f"{package_name} is not installed. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"{package_name} installed successfully.")
    
    # Run pytest with verbose output
    pytest.main(["-v", os.path.join(script_dir, "tests")])

if __name__ == "__main__":
    run_tests() 