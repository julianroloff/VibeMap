import os
import joblib
from fastapi import HTTPException, status
from config import settings
from typing import Dict, Any, Optional

# Model path
MODEL_PATH = os.path.join(settings.MODEL_DIR, "hybrid_model.pkl")
os.makedirs(settings.MODEL_DIR, exist_ok=True)

# In-memory model storage
_CURRENT_MODEL: Optional[Dict[str, Any]] = None

async def get_model():
    """Dependency to get the trained model"""
    global _CURRENT_MODEL
    
    # First check if we have the model in memory
    if _CURRENT_MODEL is not None:
        return _CURRENT_MODEL
    
    # If not in memory, try to load from disk
    if not os.path.exists(MODEL_PATH):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not trained yet. Please trigger training first."
        )
    
    try:
        _CURRENT_MODEL = joblib.load(MODEL_PATH)
        return _CURRENT_MODEL
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading model: {str(e)}"
        )

def set_current_model(model_data: Dict[str, Any]):
    """Set the current model in memory"""
    global _CURRENT_MODEL
    _CURRENT_MODEL = model_data
    
    # Also save to disk for persistence
    try:
        joblib.dump(model_data, MODEL_PATH)
    except Exception as e:
        # Log the error but don't fail - we still have the model in memory
        print(f"Error saving model to disk: {str(e)}") 