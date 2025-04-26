import os
import joblib
import json
import logging
import uuid
from pathlib import Path
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone

logger = logging.getLogger(__name__)

class ModelRegistry:
    """
    Singleton class for registering, retrieving, and managing ML models.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelRegistry, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the model registry."""
        self.models_cache = {}
        self._setup_storage_directory()
    
    def _setup_storage_directory(self):
        """Set up the directory for storing model files."""
        # Check if ML_DJANGO_BRAIN_STORAGE_DIR is defined in settings
        try:
            self.storage_dir = getattr(settings, 'ML_DJANGO_BRAIN_STORAGE_DIR', None)
            if not self.storage_dir:
                # Default to a 'ml_models' directory in the MEDIA_ROOT
                if hasattr(settings, 'MEDIA_ROOT'):
                    self.storage_dir = os.path.join(settings.MEDIA_ROOT, 'ml_models')
                else:
                    # Fallback to a directory in the current project
                    self.storage_dir = os.path.join(os.getcwd(), 'ml_models')
            
            # Create the directory if it doesn't exist
            os.makedirs(self.storage_dir, exist_ok=True)
            logger.info(f"Model storage directory set to: {self.storage_dir}")
        except Exception as e:
            logger.error(f"Failed to set up storage directory: {str(e)}")
            raise ImproperlyConfigured("Failed to set up ML model storage directory")
    
    def register(self, name, model, version="1.0.0", description="", input_schema=None, output_schema=None, metrics=None):
        """
        Register a new ML model or a new version of an existing model.
        
        Args:
            name (str): Name of the model
            model (object): The trained ML model object
            version (str): Version string (default: "1.0.0")
            description (str): Description of the model
            input_schema (dict): JSON schema describing the expected input format
            output_schema (dict): JSON schema describing the expected output format
            metrics (dict): Performance metrics for this model version
            
        Returns:
            tuple: (MLModel instance, ModelVersion instance)
        """
        from ml_django_brain.models import MLModel, ModelVersion
        
        # Determine model type
        model_type = self._determine_model_type(model)
        
        # Get or create the model record
        ml_model, created = MLModel.objects.get_or_create(
            name=name,
            defaults={
                'description': description,
                'model_type': model_type
            }
        )
        
        if not created and ml_model.model_type != model_type:
            logger.warning(f"Model type changed from {ml_model.model_type} to {model_type}")
            ml_model.model_type = model_type
            ml_model.save()
        
        # Generate a unique filename for this model version
        filename = f"{name.lower().replace(' ', '_')}_{version}_{uuid.uuid4().hex}.joblib"
        file_path = os.path.join(self.storage_dir, filename)
        
        # Save the model to disk
        joblib.dump(model, file_path)
        
        # Create the model version record
        model_version = ModelVersion.objects.create(
            model=ml_model,
            version=version,
            file_path=file_path,
            input_schema=input_schema or {},
            output_schema=output_schema or {},
            metrics=metrics or {},
            is_active=True  # New versions are active by default
        )
        
        logger.info(f"Registered model {name} version {version}")
        return ml_model, model_version
    
    def load_model(self, name, version=None):
        """
        Load a model from the registry.
        
        Args:
            name (str): Name of the model
            version (str, optional): Specific version to load. If None, loads the active version.
            
        Returns:
            object: The loaded ML model
        """
        from ml_django_brain.models import MLModel, ModelVersion
        
        # Check if model is already in cache
        cache_key = f"{name}_{version}" if version else f"{name}_active"
        if cache_key in self.models_cache:
            logger.debug(f"Loading model {name} from cache")
            return self.models_cache[cache_key]
        
        try:
            # Get the model record
            ml_model = MLModel.objects.get(name=name)
            
            # Get the appropriate version
            if version:
                model_version = ml_model.versions.get(version=version)
            else:
                model_version = ml_model.versions.get(is_active=True)
            
            # Load the model from disk
            loaded_model = joblib.load(model_version.file_path)
            
            # Cache the model
            self.models_cache[cache_key] = loaded_model
            
            logger.debug(f"Loaded model {name} version {model_version.version}")
            return loaded_model
        
        except MLModel.DoesNotExist:
            logger.error(f"Model {name} not found in registry")
            raise ValueError(f"Model {name} not found in registry")
        
        except ModelVersion.DoesNotExist:
            if version:
                logger.error(f"Version {version} of model {name} not found")
                raise ValueError(f"Version {version} of model {name} not found")
            else:
                logger.error(f"No active version found for model {name}")
                raise ValueError(f"No active version found for model {name}")
        
        except Exception as e:
            logger.error(f"Error loading model {name}: {str(e)}")
            raise
    
    def get_model_info(self, name):
        """
        Get information about a model and its versions.
        
        Args:
            name (str): Name of the model
            
        Returns:
            dict: Information about the model and its versions
        """
        from ml_django_brain.models import MLModel
        
        try:
            ml_model = MLModel.objects.get(name=name)
            versions = ml_model.versions.all()
            
            return {
                'id': str(ml_model.id),
                'name': ml_model.name,
                'description': ml_model.description,
                'model_type': ml_model.model_type,
                'created_at': ml_model.created_at.isoformat(),
                'updated_at': ml_model.updated_at.isoformat(),
                'versions': [
                    {
                        'id': str(v.id),
                        'version': v.version,
                        'is_active': v.is_active,
                        'input_schema': v.input_schema,
                        'output_schema': v.output_schema,
                        'metrics': v.metrics,
                        'created_at': v.created_at.isoformat()
                    }
                    for v in versions
                ]
            }
        
        except MLModel.DoesNotExist:
            logger.error(f"Model {name} not found in registry")
            raise ValueError(f"Model {name} not found in registry")
    
    def list_models(self):
        """
        List all registered models.
        
        Returns:
            list: List of model information dictionaries
        """
        from ml_django_brain.models import MLModel
        
        models = MLModel.objects.all()
        return [
            {
                'id': str(model.id),
                'name': model.name,
                'description': model.description,
                'model_type': model.model_type,
                'created_at': model.created_at.isoformat(),
                'updated_at': model.updated_at.isoformat(),
                'latest_version': model.latest_version.version if model.latest_version else None,
                'is_active': model.is_active
            }
            for model in models
        ]
    
    def delete_model(self, name):
        """
        Delete a model and all its versions.
        
        Args:
            name (str): Name of the model
        """
        from ml_django_brain.models import MLModel
        
        try:
            ml_model = MLModel.objects.get(name=name)
            
            # Delete model files
            for version in ml_model.versions.all():
                try:
                    if os.path.exists(version.file_path):
                        os.remove(version.file_path)
                except Exception as e:
                    logger.warning(f"Error deleting model file {version.file_path}: {str(e)}")
            
            # Delete from cache
            for key in list(self.models_cache.keys()):
                if key.startswith(f"{name}_"):
                    del self.models_cache[key]
            
            # Delete the model record (will cascade to versions)
            ml_model.delete()
            
            logger.info(f"Deleted model {name} and all its versions")
        
        except MLModel.DoesNotExist:
            logger.error(f"Model {name} not found in registry")
            raise ValueError(f"Model {name} not found in registry")
    
    def _determine_model_type(self, model):
        """
        Determine the type of ML model.
        
        Args:
            model (object): The ML model object
            
        Returns:
            str: Type of the model (e.g., 'sklearn', 'tensorflow', 'pytorch')
        """
        module_name = model.__module__.split('.')[0].lower()
        
        if module_name in ('sklearn', 'scikit'):
            return 'sklearn'
        elif module_name in ('tensorflow', 'tf'):
            return 'tensorflow'
        elif module_name in ('torch', 'pytorch'):
            return 'pytorch'
        elif module_name in ('xgboost', 'lightgbm', 'catboost'):
            return module_name
        else:
            return 'unknown'
