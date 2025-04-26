# ML Django Brain

A Django plugin for AI/ML integration that provides model registry, API integration, performance optimization, and monitoring capabilities for machine learning models in Django applications.

## Features

- **Model Registry and Management**: Register, version, and manage ML models with support for different formats (scikit-learn, TensorFlow, PyTorch)
- **Simplified API Integration**: Automatic REST API generation for ML models with standardized input/output serialization
- **Performance Optimization**: Model caching mechanisms and batch prediction capabilities
- **Monitoring and Logging**: Track model performance metrics and prediction logging

## Table of Contents

- [Author](#author)
- [Example Project](#example-project)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Components](#components)
- [API Reference](#api-reference)
- [Supported ML Frameworks](#supported-ml-frameworks)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Author

**Saeed Ghanbari** - [GitHub](https://github.com/sgh370)

## Example Project

The plugin includes an example project that demonstrates its usage. Here's a preview of what it looks like:

![Home Page](docs/images/01.png)

![Details](docs/images/02.png)

![View Metrics](docs/images/03.png)

![Make Prediction](docs/images/04.png)

![Admin Interface Login](docs/images/05.png)

![Admin Interface](docs/images/06.png)

To run the example:

1. Clone the repository:

```bash
git clone https://github.com/sgh370/ml-django-brain.git
cd ml-django-brain
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
cd example_project
pip install -r requirements.txt
```

3. Run migrations:

```bash
python manage.py migrate
```

4. Create a superuser:

```bash
python manage.py createsuperuser
```

5. Train and register the example model:

```bash
python manage.py train_iris_model
```

6. Run the development server:

```bash
python manage.py runserver
```

7. Access the example project at http://localhost:8000/

### Admin Access

You can access the admin interface at http://localhost:8000/admin/ with:

- **Username**: admin
- **Password**: admin123

### Example API Endpoints

- List all models: `/api/models/`
- Get model details: `/api/models/<id>/`
- Make a prediction: `/api/models/<id>/predict/`
- Make batch predictions: `/api/models/<id>/batch_predict/`

## Installation

```bash
pip install ml-django-brain
```

## Quick Start

1. Add `ml_django_brain` to your `INSTALLED_APPS` in settings.py:

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',  # Required dependency
    'ml_django_brain',
    # ...
]

# ML Django Brain settings
ML_DJANGO_BRAIN = {
    'STORAGE_DIR': os.path.join(MEDIA_ROOT, 'ml_models'),
    'CACHE_ENABLED': True,
    'LOG_PREDICTIONS': True,
}
```

2. Add the URLs to your project's urls.py:

```python
from django.urls import path, include

urlpatterns = [
    # ...
    path('api/', include('ml_django_brain.urls', namespace='ml_django_brain')),
    # ...
]
```

3. Run migrations:

```bash
python manage.py migrate
```

4. Register your first model:

```python
from ml_django_brain.registry import ModelRegistry
import sklearn.ensemble

# Train your model
model = sklearn.ensemble.RandomForestClassifier()
model.fit(X_train, y_train)

# Register the model
registry = ModelRegistry()
registry.register(
    name="my_classifier",
    model=model,
    version="1.0.0",
    input_schema={
        "title": "Input Schema",
        "type": "object",
        "properties": {
            "feature1": {"type": "number"},
            "feature2": {"type": "number"}
        }
    },
    output_schema={
        "title": "Output Schema",
        "type": "object",
        "properties": {
            "prediction": {"type": "string"}
        }
    }
)
```

5. Use the model in your views:

```python
from ml_django_brain.services import PredictionService
from django.http import JsonResponse

def predict_view(request):
    service = PredictionService()
    prediction = service.predict("my_classifier", {"feature1": 0.5, "feature2": 0.7})
    return JsonResponse(prediction)
```

## Architecture

ML Django Brain follows a modular architecture with the following key components:

1. **Model Registry**: Central system for registering, versioning, and retrieving ML models
2. **Prediction Service**: Handles model inference with input validation and output formatting
3. **API Layer**: REST API endpoints for model management and predictions
4. **Monitoring System**: Tracks model performance and logs predictions

## Components

### Core Models

- **MLModel**: Stores metadata about machine learning models
- **ModelVersion**: Manages different versions of a model
- **PredictionLog**: Logs predictions made by models
- **ModelMetric**: Tracks performance metrics for model versions

### Services

- **ModelRegistry**: Singleton class for model management
- **PredictionService**: Handles model inference
- **ModelMetricsCalculator**: Calculates and records model performance metrics

### Utilities

- **ModelLoader**: Loads models from different formats
- **ModelSerializer**: Serializes models to different formats
- **InputOutputSerializer**: Handles serialization of inputs and outputs

### Management Commands

- **register_model**: Register a model from a file
- **list_models**: List all registered models
- **evaluate_model**: Evaluate a model on a test dataset

## API Reference

### REST API Endpoints

- **GET /api/models/**: List all registered models
- **GET /api/models/{id}/**: Get details of a specific model
- **POST /api/models/{id}/predict/**: Make a prediction using a model
- **POST /api/models/{id}/batch_predict/**: Make batch predictions
- **GET /api/versions/**: List all model versions
- **GET /api/logs/**: List prediction logs
- **GET /api/metrics/**: List model metrics

### Python API

```python
# Registry API
from ml_django_brain.registry import ModelRegistry
registry = ModelRegistry()
registry.register(name, model, version, description, input_schema, output_schema, metrics)
registry.load_model(name, version=None)
registry.get_model_info(name)
registry.list_models()
registry.delete_model(name)

# Prediction API
from ml_django_brain.services import PredictionService
service = PredictionService()
result = service.predict(model_name, input_data, version=None, log_prediction=True)
results = service.batch_predict(model_name, input_data_list, version=None, log_predictions=True)

# Metrics API
from ml_django_brain.utils.metrics import ModelMetricsCalculator
metrics = ModelMetricsCalculator.calculate_classification_metrics(y_true, y_pred, y_prob)
metrics = ModelMetricsCalculator.calculate_regression_metrics(y_true, y_pred)
MetricsCalculator.record_metrics(model_version, metrics)
```

## Supported ML Frameworks

ML Django Brain supports the following machine learning frameworks:

- **scikit-learn**: Full support for all model types
- **TensorFlow/Keras**: Support for saved models and h5 files
- **PyTorch**: Support for saved models (.pt/.pth files)
- **XGBoost**: Support for all model types
- **LightGBM**: Support for all model types
- **CatBoost**: Support for all model types
- **ONNX**: Support for ONNX format models

## Configuration

ML Django Brain can be configured through the `ML_DJANGO_BRAIN` dictionary in your Django settings:

```python
ML_DJANGO_BRAIN = {
    # Storage directory for ML models
    'STORAGE_DIR': os.path.join(MEDIA_ROOT, 'ml_models'),
    
    # Cache settings
    'CACHE_ENABLED': True,
    'CACHE_TIMEOUT': 3600,  # 1 hour in seconds
    
    # Logging settings
    'LOGGING_ENABLED': True,
    'LOG_PREDICTIONS': True,
    'LOG_LEVEL': 'INFO',
    
    # Performance settings
    'BATCH_SIZE': 32,
    'ASYNC_PREDICTION': False,
    
    # Monitoring settings
    'DRIFT_DETECTION_ENABLED': True,
    'DRIFT_THRESHOLD': 0.1,  # 10% change
    
    # API settings
    'API_AUTHENTICATION_REQUIRED': True,
    'API_THROTTLE_RATE': '100/hour',
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT
