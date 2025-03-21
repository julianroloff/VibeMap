from fastapi import APIRouter, HTTPException, Depends, status, Body
import numpy as np
import pandas as pd
import os
import joblib
import json
import logging
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any, List, Optional
from dependencies import get_model, set_current_model
from schemas import (
    PredictionRequest, 
    PredictionResponse, 
    TrainingRequest, 
    TrainingResponse,
    HealthResponse,
    ModelMetadataResponse
)
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create model directory if it doesn't exist
MODEL_PATH = os.path.join(settings.MODEL_DIR, "hybrid_model.pkl")
METADATA_PATH = os.path.join(settings.MODEL_DIR, "model_metadata.json")
os.makedirs(settings.MODEL_DIR, exist_ok=True)

router = APIRouter()

# In-memory storage for model metadata
model_metadata_list = []

# Helper functions
def extract_location_features(locations):
    """Extract features from locations for content-based filtering"""
    df = pd.DataFrame(locations)
    
    # Calculate distance from city center
    CITY_CENTER = (52.379189, 4.899431)  # Amsterdam Centraal
    df['dist_from_center'] = np.sqrt(
        (df['latitude'] - CITY_CENTER[0])**2 + 
        (df['longitude'] - CITY_CENTER[1])**2
    )
    
    # Create location density features
    def calculate_location_density(lat, lon, all_locs, radius=0.01):
        """Calculate how many locations are within a radius"""
        count = 0
        for _, loc in all_locs.iterrows():
            dist = np.sqrt((lat - loc['latitude'])**2 + (lon - loc['longitude'])**2)
            if dist < radius:
                count += 1
        return count
    
    # Apply density calculation (for small datasets only - would need optimization for large datasets)
    if len(df) < 1000:  # Only do this for reasonably sized datasets
        df['location_density'] = df.apply(
            lambda row: calculate_location_density(
                row['latitude'], row['longitude'], df
            ), 
            axis=1
        )
    
    return df

def create_user_location_matrix(locations):
    """Create a matrix of users and their average stress levels at different locations"""
    df = pd.DataFrame(locations)
    
    # Create a unique identifier for each location (simplified for demo)
    df['location_id'] = df.apply(
        lambda row: f"{round(row['latitude'], 4)}_{round(row['longitude'], 4)}", 
        axis=1
    )
    
    # Get average stress level per user per location
    user_loc_stress = df.groupby(['userId', 'location_id'])['stress_level'].mean().reset_index()
    
    # Pivot to create user-location matrix
    user_loc_matrix = user_loc_stress.pivot(
        index='userId', 
        columns='location_id', 
        values='stress_level'
    ).fillna(0)
    
    return user_loc_matrix

def calculate_user_similarity(user_loc_matrix):
    """Calculate similarity between users based on their stress patterns"""
    # Calculate cosine similarity between users
    similarity_matrix = cosine_similarity(user_loc_matrix)
    
    # Create a DataFrame with user IDs as index and columns
    similarity_df = pd.DataFrame(
        similarity_matrix,
        index=user_loc_matrix.index,
        columns=user_loc_matrix.index
    )
    
    return similarity_df

def create_location_feature_matrix(locations_df):
    """Create a matrix of location features for content-based filtering"""
    # Select numerical features
    feature_cols = ['latitude', 'longitude']
    
    # Add any additional features we extracted
    if 'dist_from_center' in locations_df.columns:
        feature_cols.append('dist_from_center')
    if 'location_density' in locations_df.columns:
        feature_cols.append('location_density')
    if 'hour' in locations_df.columns:
        feature_cols.append('hour')
    if 'day_of_week' in locations_df.columns:
        feature_cols.append('day_of_week')
    
    # Create location ID
    locations_df['location_id'] = locations_df.apply(
        lambda row: f"{round(row['latitude'], 4)}_{round(row['longitude'], 4)}", 
        axis=1
    )
    
    # Select unique locations
    unique_locations = locations_df.drop_duplicates('location_id')
    
    # Create feature matrix
    location_features = unique_locations[feature_cols].copy()
    
    # Normalize features
    scaler = StandardScaler()
    location_features_scaled = scaler.fit_transform(location_features)
    
    # Create DataFrame with location_id as index
    location_feature_matrix = pd.DataFrame(
        location_features_scaled,
        index=unique_locations['location_id'],
        columns=feature_cols
    )
    
    return location_feature_matrix, scaler, feature_cols

def calculate_location_similarity(location_feature_matrix):
    """Calculate similarity between locations based on their features"""
    # Calculate cosine similarity between locations
    similarity_matrix = cosine_similarity(location_feature_matrix)
    
    # Create a DataFrame with location IDs as index and columns
    similarity_df = pd.DataFrame(
        similarity_matrix,
        index=location_feature_matrix.index,
        columns=location_feature_matrix.index
    )
    
    return similarity_df

def train_hybrid_model(locations):
    """Train a hybrid recommendation model for stress level prediction"""
    # Extract features from locations
    locations_df = extract_location_features(locations)
    
    # Create user-location matrix
    user_loc_matrix = create_user_location_matrix(locations)
    
    # Calculate user similarity
    user_similarity = calculate_user_similarity(user_loc_matrix)
    
    # Create location feature matrix
    location_feature_matrix, scaler, feature_cols = create_location_feature_matrix(locations_df)
    
    # Calculate location similarity
    location_similarity = calculate_location_similarity(location_feature_matrix)
    
    # Create model data
    model_data = {
        "user_loc_matrix": user_loc_matrix,
        "user_similarity": user_similarity,
        "location_similarity": location_similarity,
        "scaler": scaler,
        "feature_cols": feature_cols
    }
    
    return model_data

def predict_stress_levels_hybrid(user_id, locations, user_similarity, location_similarity, 
                                user_loc_matrix, scaler, feature_cols):
    """Predict stress levels using a hybrid approach"""
    # Weight for collaborative vs. content-based filtering
    collab_weight = 0.7
    content_weight = 0.3
    
    # Check if user exists in our data
    user_exists = user_id in user_similarity.index
    if not user_exists:
        logger.warning(f"User {user_id} not found in similarity matrix")
        # Fall back to content-based only with lower weight
        collab_weight = 0
        content_weight = 0.3  # Lower weight to preserve original values more
    
    # For each location, predict stress level
    for location in locations:
        lat, lon = location['latitude'], location['longitude']
        loc_id = f"{round(lat, 4)}_{round(lon, 4)}"
        
        # Get original stress level (will be used as a base)
        original_stress = location['stress_level']
        
        # Collaborative filtering component
        collab_prediction = original_stress  # Default to original
        if collab_weight > 0 and user_exists:
            # Get similar users
            similar_users = user_similarity.loc[user_id].sort_values(ascending=False)
            similar_users = similar_users[similar_users.index != user_id]
            
            # Get stress levels of similar users for this location
            stress_levels = []
            weights = []
            
            for sim_user, similarity in similar_users.items():
                if similarity <= 0:  # Skip users with no positive similarity
                    continue
                    
                if loc_id in user_loc_matrix.columns and not pd.isna(user_loc_matrix.loc[sim_user, loc_id]) and user_loc_matrix.loc[sim_user, loc_id] > 0:
                    stress_levels.append(user_loc_matrix.loc[sim_user, loc_id])
                    weights.append(similarity)
            
            # If we have data from similar users, calculate weighted average
            if stress_levels:
                weights = np.array(weights) / sum(weights)  # Normalize weights
                collab_prediction = sum(np.array(stress_levels) * weights)
        
        # Content-based filtering component
        content_prediction = original_stress  # Default to original
        if content_weight > 0:
            # Check if this location exists in our data
            if loc_id in location_similarity.index:
                # Get similar locations
                similar_locs = location_similarity.loc[loc_id].sort_values(ascending=False)
                similar_locs = similar_locs[similar_locs.index != loc_id]
                
                # Get stress levels for similar locations for this user
                stress_levels = []
                weights = []
                
                for sim_loc, similarity in similar_locs.items():
                    if similarity <= 0:  # Skip locations with no positive similarity
                        continue
                        
                    if sim_loc in user_loc_matrix.columns and user_id in user_loc_matrix.index:
                        if not pd.isna(user_loc_matrix.loc[user_id, sim_loc]) and user_loc_matrix.loc[user_id, sim_loc] > 0:
                            stress_levels.append(user_loc_matrix.loc[user_id, sim_loc])
                            weights.append(similarity)
                
                # If we have data from similar locations, calculate weighted average
                if stress_levels:
                    weights = np.array(weights) / sum(weights)  # Normalize weights
                    content_prediction = sum(np.array(stress_levels) * weights)
            else:
                # This is a new location, try to predict based on features
                # Extract features for this location
                loc_features = np.array([[
                    location['latitude'], 
                    location['longitude'],
                    # Add any additional features that were used in training
                    # These should match the feature_cols used in training
                ]])
                
                # Add any additional features that were used in training
                if 'dist_from_center' in feature_cols:
                    CITY_CENTER = (52.379189, 4.899431)  # Amsterdam Centraal
                    dist = np.sqrt(
                        (location['latitude'] - CITY_CENTER[0])**2 + 
                        (location['longitude'] - CITY_CENTER[1])**2
                    )
                    loc_features = np.append(loc_features, [[dist]], axis=1)
                
                # Scale features
                if scaler is not None:
                    # Make sure we have the right number of features
                    if loc_features.shape[1] == len(feature_cols):
                        loc_features_scaled = scaler.transform(loc_features)
                        
                        # Find most similar location in our data
                        all_features = location_similarity.index.tolist()
                        all_features_matrix = location_similarity.values
                        
                        # Calculate similarity to all known locations
                        sims = cosine_similarity(loc_features_scaled, all_features_matrix)[0]
                        
                        # Get top 3 similar locations
                        top_indices = np.argsort(sims)[-3:]
                        top_locs = [all_features[i] for i in top_indices]
                        top_sims = [sims[i] for i in top_indices]
                        
                        # Get stress levels for similar locations
                        stress_levels = []
                        weights = []
                        
                        for sim_loc, similarity in zip(top_locs, top_sims):
                            if similarity <= 0:
                                continue
                                
                            if sim_loc in user_loc_matrix.columns and user_id in user_loc_matrix.index:
                                if not pd.isna(user_loc_matrix.loc[user_id, sim_loc]) and user_loc_matrix.loc[user_id, sim_loc] > 0:
                                    stress_levels.append(user_loc_matrix.loc[user_id, sim_loc])
                                    weights.append(similarity)
                        
                        # If we have data, calculate weighted average
                        if stress_levels:
                            weights = np.array(weights) / sum(weights)
                            content_prediction = sum(np.array(stress_levels) * weights)
        
        # Combine predictions - for new users, use a smaller adjustment to preserve original values
        if not user_exists:
            # Apply a smaller adjustment (max ±1 level) to preserve the original stress level
            adjustment = (content_weight * (content_prediction - original_stress))
            # Limit adjustment to ±1
            adjustment = max(min(adjustment, 1), -1)
            final_prediction = original_stress + adjustment
        else:
            # For existing users, use the full hybrid approach
            final_prediction = (collab_weight * collab_prediction) + (content_weight * content_prediction)
        
        # Ensure the final prediction is between 1 and 4
        final_prediction = max(1, min(4, final_prediction))
        
        # Round to nearest integer
        location['predicted_stress_level'] = int(round(final_prediction))
    
    return locations

def save_model_metadata(metadata):
    """Save model metadata to file"""
    global model_metadata_list
    
    # Add to in-memory list
    model_metadata_list.append(metadata)
    
    # Save to file
    try:
        with open(METADATA_PATH, 'w') as f:
            json.dump([m.model_dump() for m in model_metadata_list], f)
    except Exception as e:
        logger.error(f"Error saving model metadata: {str(e)}")

def load_model_metadata():
    """Load model metadata from file"""
    global model_metadata_list
    
    try:
        if os.path.exists(METADATA_PATH):
            with open(METADATA_PATH, 'r') as f:
                metadata_list = json.load(f)
                model_metadata_list = [ModelMetadataResponse(**m) for m in metadata_list]
    except Exception as e:
        logger.error(f"Error loading model metadata: {str(e)}")
        model_metadata_list = []

# Load metadata on startup
load_model_metadata()

# API endpoints
@router.post("/train", response_model=TrainingResponse)
async def train_model(
    request: TrainingRequest = Body(...)
):
    """Train the ML model using location data provided in the request"""
    try:
        # Check if model already exists and if we should retrain
        if os.path.exists(MODEL_PATH) and not request.force_retrain:
            return {
                "success": True,
                "message": "Model already trained. Use force_retrain=true to retrain.",
                "num_locations": len(request.locations)
            }
        
        # Get locations from request
        locations = request.locations
        
        # Convert Pydantic models to dicts if needed
        locations_dicts = []
        for location in locations:
            if hasattr(location, "model_dump"):
                locations_dicts.append(location.model_dump())
            else:
                locations_dicts.append(location)
        
        # Check if we have enough data
        if not locations_dicts:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No location data provided for training"
            )
        
        # Train the model
        model_data = train_hybrid_model(locations_dicts)
        
        # Save the model in memory and to disk
        set_current_model(model_data)
        
        # Save model metadata
        metadata = ModelMetadataResponse(
            id=len(model_metadata_list) + 1,
            model_name="hybrid_model",
            version="1.0",
            accuracy=0.85,  # Placeholder - in a real app, calculate this
            num_samples=len(locations),
            created_at=datetime.now().isoformat()
        )
        save_model_metadata(metadata)
        
        return {
            "success": True,
            "message": "Model trained successfully",
            "num_locations": len(locations)
        }
    except Exception as e:
        # Log the error
        logger.error(f"Error training model: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error training model: {str(e)}"
        )

@router.post("/predict", response_model=PredictionResponse)
async def predict(
    request: PredictionRequest,
    model_data: Dict[str, Any] = Depends(get_model)
):
    """Predict personalized stress levels for a user using hybrid approach"""
    try:
        user_id = request.user_id
        locations = request.locations
        
        # If no user_id is provided, just return the original stress levels
        if user_id is None:
            # Copy the original stress levels to predicted_stress_level
            for location in locations:
                # Convert Pydantic model to dict if needed
                if hasattr(location, "model_dump"):
                    location_dict = location.model_dump()
                    location_dict["predicted_stress_level"] = location.stress_level
                    locations_with_predictions = [location_dict for location in locations]
                else:
                    location["predicted_stress_level"] = location["stress_level"]
                    locations_with_predictions = locations
            return PredictionResponse(predictions=locations_with_predictions)
        
        # Convert Pydantic models to dicts if needed
        locations_dicts = []
        for location in locations:
            if hasattr(location, "model_dump"):
                locations_dicts.append(location.model_dump())
            else:
                locations_dicts.append(location)
        
        # Extract model components
        user_loc_matrix = model_data["user_loc_matrix"]
        user_similarity = model_data["user_similarity"]
        location_similarity = model_data["location_similarity"]
        scaler = model_data["scaler"]
        feature_cols = model_data["feature_cols"]
        
        # Predict stress levels using hybrid approach
        locations_with_predictions = predict_stress_levels_hybrid(
            user_id, 
            locations_dicts,  # Use the dict version
            user_similarity,
            location_similarity,
            user_loc_matrix,
            scaler,
            feature_cols
        )
        
        return PredictionResponse(predictions=locations_with_predictions)
    
    except Exception as e:
        logger.error(f"Error making predictions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error making predictions: {str(e)}")

@router.get("/models", response_model=List[ModelMetadataResponse])
async def get_models():
    """Get all trained model metadata"""
    return model_metadata_list

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(status="healthy") 