import sys
import os
import unittest
import numpy as np
import pandas as pd

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the functions to test
from routes import (
    extract_location_features,
    create_user_location_matrix,
    calculate_user_similarity,
    create_location_feature_matrix,
    calculate_location_similarity,
    predict_stress_levels_hybrid
)

class TestMLUtils(unittest.TestCase):
    """Test ML utility functions"""
    
    def setUp(self):
        """Set up test data"""
        # Sample location data
        self.locations = [
            {
                "id": 1,
                "userId": 1,
                "latitude": 52.379189,  # Amsterdam Centraal
                "longitude": 4.899431,
                "stress_level": 3,
                "comment": "Busy area"
            },
            {
                "id": 2,
                "userId": 1,
                "latitude": 52.379289,  # Near Amsterdam Centraal
                "longitude": 4.899531,
                "stress_level": 4,
                "comment": "Traffic"
            },
            {
                "id": 3,
                "userId": 2,
                "latitude": 52.379189,  # Amsterdam Centraal
                "longitude": 4.899431,
                "stress_level": 2,
                "comment": "Nice day"
            }
        ]
    
    def test_extract_location_features(self):
        """Test feature extraction from locations"""
        df = extract_location_features(self.locations)
        
        # Check that the dataframe has the expected columns
        self.assertIn('dist_from_center', df.columns)
        self.assertIn('location_density', df.columns)
        
        # Check that the distance calculation works
        self.assertAlmostEqual(df.loc[0, 'dist_from_center'], 0, places=4)
    
    def test_create_user_location_matrix(self):
        """Test creation of user-location matrix"""
        user_loc_matrix = create_user_location_matrix(self.locations)
        
        # Check matrix shape
        self.assertEqual(user_loc_matrix.shape, (2, 2))
        
        # Check values
        self.assertEqual(user_loc_matrix.loc[1, '52.3792_4.8994'], 3)
        self.assertEqual(user_loc_matrix.loc[2, '52.3792_4.8994'], 2)
    
    def test_calculate_user_similarity(self):
        """Test calculation of user similarity"""
        user_loc_matrix = create_user_location_matrix(self.locations)
        similarity = calculate_user_similarity(user_loc_matrix)
        
        # Check matrix shape
        self.assertEqual(similarity.shape, (2, 2))
        
        # Check diagonal values (should be 1.0)
        self.assertEqual(similarity.loc[1, 1], 1.0)
        self.assertEqual(similarity.loc[2, 2], 1.0)
        
        # Check that similarity is between 0 and 1
        self.assertTrue(0 <= similarity.loc[1, 2] <= 1)
    
    def test_create_location_feature_matrix(self):
        """Test creation of location feature matrix"""
        df = extract_location_features(self.locations)
        feature_matrix, scaler, feature_cols = create_location_feature_matrix(df)
        
        # Check matrix shape
        self.assertEqual(feature_matrix.shape[0], 2)  # 2 unique locations
        
        # Check that scaler is returned
        self.assertIsNotNone(scaler)
        
        # Check that feature_cols is returned
        self.assertIsNotNone(feature_cols)
    
    def test_calculate_location_similarity(self):
        """Test calculation of location similarity"""
        df = extract_location_features(self.locations)
        feature_matrix, scaler, feature_cols = create_location_feature_matrix(df)
        similarity = calculate_location_similarity(feature_matrix)
        
        # Check matrix shape
        self.assertEqual(similarity.shape, (2, 2))
        
        # Check diagonal values (should be 1.0)
        self.assertAlmostEqual(similarity.iloc[0, 0], 1.0, places=10)
        self.assertAlmostEqual(similarity.iloc[1, 1], 1.0, places=10)
        
        # Check that similarity is reasonable (could be negative with standardized features)
        # Just check that it's a number
        self.assertTrue(isinstance(similarity.iloc[0, 1], float))
    
    def test_predict_stress_levels_hybrid(self):
        """Test hybrid prediction of stress levels"""
        # Prepare data
        df = extract_location_features(self.locations)
        user_loc_matrix = create_user_location_matrix(self.locations)
        user_similarity = calculate_user_similarity(user_loc_matrix)
        location_feature_matrix, scaler, feature_cols = create_location_feature_matrix(df)
        location_similarity = calculate_location_similarity(location_feature_matrix)
        
        # Test location to predict
        test_location = [
            {
                "id": 10,
                "userId": 1,
                "latitude": 52.379189,  # Amsterdam Centraal
                "longitude": 4.899431,
                "stress_level": 3,
                "comment": "Test location"
            }
        ]
        
        # Make prediction
        predictions = predict_stress_levels_hybrid(
            1,  # user_id
            test_location,
            user_similarity,
            location_similarity,
            user_loc_matrix,
            scaler,
            feature_cols
        )
        
        # Check that we got a prediction
        self.assertIn('predicted_stress_level', predictions[0])
        
        # Check that the prediction is between 1 and 4
        self.assertTrue(1 <= predictions[0]['predicted_stress_level'] <= 4) 