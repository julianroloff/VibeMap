import pytest
import os
import sys
from unittest import mock

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set testing environment variable
os.environ["TESTING"] = "True"

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup the test environment"""
    # Create test directories
    os.makedirs("model", exist_ok=True)
    
    # Yield to tests
    yield
    
    # Cleanup (optional)
    # You can add cleanup code here if needed 