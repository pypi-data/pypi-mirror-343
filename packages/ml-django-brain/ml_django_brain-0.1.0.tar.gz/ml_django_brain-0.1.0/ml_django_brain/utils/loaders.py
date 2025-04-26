import os
import joblib
import pickle
import logging
from pathlib import Path
import importlib.util

logger = logging.getLogger(__name__)

class ModelLoader:
    """
    Utility class for loading ML models from different formats.
    """
    
    @staticmethod
    def load_model(file_path):
        """
        Load a model from a file path, automatically detecting the format.
        
        Args:
            file_path (str): Path to the model file
            
        Returns:
            object: The loaded model
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Model file not found: {file_path}")
        
        file_ext = Path(file_path).suffix.lower()
        
        try:
            if file_ext == '.joblib':
                return ModelLoader.load_joblib(file_path)
            elif file_ext in ['.pkl', '.pickle']:
                return ModelLoader.load_pickle(file_path)
            elif file_ext == '.h5':
                return ModelLoader.load_keras(file_path)
            elif file_ext == '.pt' or file_ext == '.pth':
                return ModelLoader.load_pytorch(file_path)
            elif file_ext == '.onnx':
                return ModelLoader.load_onnx(file_path)
            else:
                # Default to joblib for unknown extensions
                logger.warning(f"Unknown model format: {file_ext}, trying joblib")
                return ModelLoader.load_joblib(file_path)
        except Exception as e:
            logger.error(f"Error loading model from {file_path}: {str(e)}")
            raise
    
    @staticmethod
    def load_joblib(file_path):
        """Load a model using joblib."""
        return joblib.load(file_path)
    
    @staticmethod
    def load_pickle(file_path):
        """Load a model using pickle."""
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    
    @staticmethod
    def load_keras(file_path):
        """Load a Keras model."""
        try:
            # Lazy import to avoid requiring tensorflow for non-keras models
            import tensorflow as tf
            return tf.keras.models.load_model(file_path)
        except ImportError:
            logger.error("TensorFlow is not installed. Cannot load Keras model.")
            raise ImportError("TensorFlow is required to load Keras models")
    
    @staticmethod
    def load_pytorch(file_path):
        """Load a PyTorch model."""
        try:
            # Lazy import to avoid requiring torch for non-pytorch models
            import torch
            return torch.load(file_path)
        except ImportError:
            logger.error("PyTorch is not installed. Cannot load PyTorch model.")
            raise ImportError("PyTorch is required to load PyTorch models")
    
    @staticmethod
    def load_onnx(file_path):
        """Load an ONNX model."""
        try:
            # Lazy import to avoid requiring onnx for non-onnx models
            import onnx
            return onnx.load(file_path)
        except ImportError:
            logger.error("ONNX is not installed. Cannot load ONNX model.")
            raise ImportError("ONNX is required to load ONNX models")
    
    @staticmethod
    def load_from_module(module_path, model_attribute='model'):
        """
        Load a model from a Python module.
        
        Args:
            module_path (str): Path to the Python module
            model_attribute (str): Attribute name of the model in the module
            
        Returns:
            object: The loaded model
        """
        try:
            spec = importlib.util.spec_from_file_location("model_module", module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, model_attribute):
                return getattr(module, model_attribute)
            else:
                raise AttributeError(f"Module does not have attribute '{model_attribute}'")
        except Exception as e:
            logger.error(f"Error loading model from module {module_path}: {str(e)}")
            raise
