# ML Service

This service provides personalized stress level recommendations using a hybrid collaborative filtering approach.

## Features

- Collaborative filtering based on user similarities
- Content-based filtering using location features
- Hybrid approach combining both methods
- API endpoints for training and prediction
- Database storage for model metadata

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the service:
   ```
   uvicorn main:app --host 0.0.0.0 --port 8005 --reload
   ```

## API Endpoints

- `POST /ml/train`: Train the recommendation model
- `POST /ml/predict`: Get personalized stress level predictions
- `GET /ml/models`: List all trained models
- `GET /ml/health`: Health check endpoint

## Testing

To run the tests:

```
python run_tests.py
```

Or using pytest directly:

```
pytest -v tests/
```

### Troubleshooting Tests

If you encounter errors related to Pydantic:

1. Make sure you have the correct version of pydantic and pydantic-settings:
   ```
   pip install pydantic>=2.0.0 pydantic-settings>=2.0.0
   ```

2. If you're using an older version of Pydantic (v1), update the config.py file:
   ```python
   # For Pydantic v1
   from pydantic import BaseSettings
   
   # For Pydantic v2
   from pydantic_settings import BaseSettings
   ```

### Testing in Isolation

The tests are designed to run in isolation without requiring other services to be running. They use mocks to simulate the behavior of external dependencies.

## How It Works

The hybrid recommendation system combines:

1. **Collaborative Filtering**: Recommends stress levels based on similar users' experiences
2. **Content-Based Filtering**: Recommends stress levels based on location features

This approach provides more robust recommendations, especially for new users or locations. 