import sys
import os
import pytest
import json
from fastapi.testclient import TestClient
import joblib
import numpy as np
import pandas as pd
from unittest import mock

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import with error handling
try:
    from main import app
    from dependencies import MODEL_PATH
    from config import settings
except ImportError as e:
    print(f"Import error: {e}")
    # Create mock objects if imports fail
    app = mock.MagicMock()
    MODEL_PATH = os.path.join("model", "hybrid_model.pkl")
    settings = mock.MagicMock()

# Create test client
@pytest.fixture
def client():
    """Create a test client"""
    from main import app
    return TestClient(app)

# Sample data for tests
sample_locations = [
    {
        "id": 1,
        "userId": 1,
        "latitude": 40.7128,
        "longitude": -74.0060,
        "stress_level": 3,
        "comment": "Busy area",
        "geom": None
    },
    {
        "id": 2,
        "userId": 1,
        "latitude": 40.7129,
        "longitude": -74.0061,
        "stress_level": 4,
        "comment": "Traffic",
        "geom": None
    },
    {
        "id": 3,
        "userId": 2,
        "latitude": 40.7128,
        "longitude": -74.0060,
        "stress_level": 2,
        "comment": "Nice day",
        "geom": None
    }
]

# Mock the model loading
@pytest.fixture
def mock_model_loading():
    """Mock the model loading to return a test model"""
    # Create a simple model for testing
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    
    # Create sample dataframes
    user_ids = [1, 2]
    loc_ids = ["40.7128_-74.0060", "40.7129_-74.0061"]
    
    # User-location matrix
    data = np.array([[3, 4], [2, 0]])
    user_loc_matrix = pd.DataFrame(data, index=user_ids, columns=loc_ids)
    
    # User similarity
    user_sim_data = np.array([[1.0, 0.6], [0.6, 1.0]])
    user_similarity = pd.DataFrame(user_sim_data, index=user_ids, columns=user_ids)
    
    # Location similarity
    loc_sim_data = np.array([[1.0, 0.9], [0.9, 1.0]])
    location_similarity = pd.DataFrame(loc_sim_data, index=loc_ids, columns=loc_ids)
    
    # Create a simple StandardScaler
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    scaler.mean_ = np.array([40.7, -74.0, 0.5, 2.0])
    scaler.scale_ = np.array([0.1, 0.1, 0.2, 1.0])
    
    # Create model data
    model_data = {
        "user_loc_matrix": user_loc_matrix,
        "user_similarity": user_similarity,
        "location_similarity": location_similarity,
        "scaler": scaler,
        "feature_cols": ["latitude", "longitude", "dist_from_center", "location_density"]
    }
    
    # Save the model
    joblib.dump(model_data, MODEL_PATH)
    
    # Return the model data for use in tests
    return model_data

def create_test_model():
    """Create a test model file"""
    # Create a simple model for testing
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    
    # Create sample dataframes
    user_ids = [1, 2]
    loc_ids = ["40.7128_-74.0060", "40.7129_-74.0061"]
    
    # User-location matrix
    data = np.array([[3, 4], [2, 0]])
    user_loc_matrix = pd.DataFrame(data, index=user_ids, columns=loc_ids)
    
    # User similarity
    user_sim_data = np.array([[1.0, 0.6], [0.6, 1.0]])
    user_similarity = pd.DataFrame(user_sim_data, index=user_ids, columns=user_ids)
    
    # Location similarity
    loc_sim_data = np.array([[1.0, 0.9], [0.9, 1.0]])
    location_similarity = pd.DataFrame(loc_sim_data, index=loc_ids, columns=loc_ids)
    
    # Create a simple StandardScaler
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    scaler.mean_ = np.array([40.7, -74.0, 0.5, 2.0])
    scaler.scale_ = np.array([0.1, 0.1, 0.2, 1.0])
    
    # Create model data
    model_data = {
        "user_loc_matrix": user_loc_matrix,
        "user_similarity": user_similarity,
        "location_similarity": location_similarity,
        "scaler": scaler,
        "feature_cols": ["latitude", "longitude", "dist_from_center", "location_density"]
    }
    
    # Save the model
    joblib.dump(model_data, MODEL_PATH)

def test_health_endpoint(client):
    """Test the health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_train_endpoint(client):
    """Test the train endpoint"""
    # Remove existing model if it exists
    if os.path.exists(MODEL_PATH):
        os.remove(MODEL_PATH)
    
    # Test data
    test_data = {
        "force_retrain": True,
        "locations": sample_locations
    }
    
    # Call the train endpoint
    response = client.post("/ml/train", json=test_data)
    
    # Check response
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert response.json()["num_locations"] == len(sample_locations)

def test_train_endpoint_with_existing_model(client):
    """Test the train endpoint when a model already exists"""
    # Create a test model
    create_test_model()
    
    # Test data
    test_data = {
        "force_retrain": False,
        "locations": sample_locations
    }
    
    # Call the train endpoint
    response = client.post("/ml/train", json=test_data)
    
    # Check response
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert response.json()["message"] == "Model already trained. Use force_retrain=true to retrain."

def test_predict_endpoint(client, mock_model_loading):
    """Test the predict endpoint"""
    # Test data
    test_data = {
        "user_id": 1,
        "locations": [
            {
                "id": 10,
                "userId": 1,
                "latitude": 40.7128,
                "longitude": -74.0060,
                "stress_level": 3,
                "comment": "Test location",
                "geom": None
            }
        ]
    }
    
    # Call the predict endpoint
    response = client.post("/ml/predict", json=test_data)
    
    # Check response
    assert response.status_code == 200
    predictions = response.json()["predictions"]
    assert len(predictions) == 1
    assert "predicted_stress_level" in predictions[0]

def test_predict_endpoint_no_user(client, mock_model_loading):
    """Test the predict endpoint with no user ID"""
    # Test data
    test_data = {
        "locations": [
            {
                "id": 10,
                "userId": 1,
                "latitude": 40.7128,
                "longitude": -74.0060,
                "stress_level": 3,
                "comment": "Test location",
                "geom": None
            }
        ]
    }
    
    # Call the predict endpoint
    response = client.post("/ml/predict", json=test_data)
    
    # Check response
    assert response.status_code == 200
    predictions = response.json()["predictions"]
    assert len(predictions) == 1
    assert predictions[0]["predicted_stress_level"] == 3  # Should match original stress level

def test_predict_endpoint_new_user(client, mock_model_loading):
    """Test the predict endpoint with a new user"""
    # Set a new user ID
    new_user_id = 99
    
    # Test data for new user
    test_data = {
        "user_id": new_user_id,
        "locations": [
            {
                "id": 10,
                "userId": new_user_id,
                "latitude": 40.7128,
                "longitude": -74.0060,
                "stress_level": 3,
                "comment": "Test location",
                "geom": None
            }
        ]
    }
    
    # Call the predict endpoint
    response = client.post("/ml/predict", json=test_data)
    
    # Check response
    assert response.status_code == 200
    predictions = response.json()["predictions"]
    assert len(predictions) == 1
    assert "predicted_stress_level" in predictions[0]

def test_predict_endpoint_new_location(client, mock_model_loading):
    """Test the predict endpoint with a new location"""
    # Test data with new location
    test_data = {
        "user_id": 1,
        "locations": [
            {
                "id": 10,
                "userId": 1,
                "latitude": 41.0,  # New location not in the model
                "longitude": -75.0,
                "stress_level": 3,
                "comment": "New location",
                "geom": None
            }
        ]
    }
    
    # Call the predict endpoint
    response = client.post("/ml/predict", json=test_data)
    
    # Check response
    assert response.status_code == 200
    predictions = response.json()["predictions"]
    assert len(predictions) == 1
    assert "predicted_stress_level" in predictions[0]

def test_models_endpoint(client):
    """Test the models endpoint"""
    # Call the endpoint
    response = client.get("/ml/models")
    
    # Check response
    assert response.status_code == 200
    assert isinstance(response.json(), list) 