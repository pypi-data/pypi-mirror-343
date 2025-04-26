"""
Default settings for ML Django Brain.
This module provides default settings that can be imported and used in your Django project.
"""

from pathlib import Path
import os

# Default settings for ML Django Brain
ML_DJANGO_BRAIN = {
    # Storage directory for ML models
    # If not specified, defaults to MEDIA_ROOT/ml_models
    'STORAGE_DIR': None,
    
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

def get_setting(name, default=None):
    """
    Get a setting from Django settings or use the default.
    
    Args:
        name (str): Name of the setting
        default: Default value if setting is not found
        
    Returns:
        The setting value
    """
    from django.conf import settings
    
    # Check if ML_DJANGO_BRAIN is defined in settings
    if hasattr(settings, 'ML_DJANGO_BRAIN'):
        # Get the setting from ML_DJANGO_BRAIN
        if name in settings.ML_DJANGO_BRAIN:
            return settings.ML_DJANGO_BRAIN[name]
    
    # Check if setting is defined directly in settings
    full_name = f'ML_DJANGO_BRAIN_{name}'
    if hasattr(settings, full_name):
        return getattr(settings, full_name)
    
    # Use default from this module
    if name in ML_DJANGO_BRAIN:
        return ML_DJANGO_BRAIN[name]
    
    # Use provided default
    return default
