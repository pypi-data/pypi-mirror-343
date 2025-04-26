import os
import joblib
import pickle
import json
import logging
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)

class ModelSerializer:
    """
    Utility class for serializing and deserializing ML models.
    """
    
    @staticmethod
    def serialize_model(model, file_path, format='joblib'):
        """
        Serialize a model to a file.
        
        Args:
            model (object): The ML model to serialize
            file_path (str): Path to save the serialized model
            format (str): Format to use for serialization ('joblib', 'pickle', 'keras', 'pytorch', 'onnx')
            
        Returns:
            str: Path to the serialized model file
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        
        try:
            if format == 'joblib':
                return ModelSerializer.serialize_joblib(model, file_path)
            elif format == 'pickle':
                return ModelSerializer.serialize_pickle(model, file_path)
            elif format == 'keras':
                return ModelSerializer.serialize_keras(model, file_path)
            elif format == 'pytorch':
                return ModelSerializer.serialize_pytorch(model, file_path)
            elif format == 'onnx':
                return ModelSerializer.serialize_onnx(model, file_path)
            else:
                logger.warning(f"Unknown format: {format}, using joblib")
                return ModelSerializer.serialize_joblib(model, file_path)
        except Exception as e:
            logger.error(f"Error serializing model to {file_path}: {str(e)}")
            raise
    
    @staticmethod
    def serialize_joblib(model, file_path):
        """Serialize a model using joblib."""
        joblib.dump(model, file_path)
        return file_path
    
    @staticmethod
    def serialize_pickle(model, file_path):
        """Serialize a model using pickle."""
        with open(file_path, 'wb') as f:
            pickle.dump(model, f)
        return file_path
    
    @staticmethod
    def serialize_keras(model, file_path):
        """Serialize a Keras model."""
        try:
            # Ensure the file has .h5 extension
            if not file_path.endswith('.h5'):
                file_path = f"{file_path}.h5"
            
            model.save(file_path)
            return file_path
        except Exception as e:
            logger.error(f"Error serializing Keras model: {str(e)}")
            raise
    
    @staticmethod
    def serialize_pytorch(model, file_path):
        """Serialize a PyTorch model."""
        try:
            import torch
            
            # Ensure the file has .pt extension
            if not file_path.endswith('.pt') and not file_path.endswith('.pth'):
                file_path = f"{file_path}.pt"
            
            torch.save(model, file_path)
            return file_path
        except ImportError:
            logger.error("PyTorch is not installed. Cannot serialize PyTorch model.")
            raise ImportError("PyTorch is required to serialize PyTorch models")
    
    @staticmethod
    def serialize_onnx(model, file_path, input_shape=None):
        """Serialize a model to ONNX format."""
        try:
            import onnx
            
            # Ensure the file has .onnx extension
            if not file_path.endswith('.onnx'):
                file_path = f"{file_path}.onnx"
            
            # This is a simplified example, actual conversion depends on the model type
            if hasattr(model, 'to_onnx'):
                # Some models have built-in ONNX conversion
                onnx_model = model.to_onnx(file_path)
            else:
                raise NotImplementedError(
                    "Direct ONNX serialization not implemented for this model type. "
                    "Please convert to ONNX format before serializing."
                )
            
            return file_path
        except ImportError:
            logger.error("ONNX is not installed. Cannot serialize to ONNX format.")
            raise ImportError("ONNX is required to serialize to ONNX format")


class InputOutputSerializer:
    """
    Utility class for serializing and deserializing model inputs and outputs.
    """
    
    @staticmethod
    def infer_schema_from_data(data, name="input"):
        """
        Infer a JSON schema from sample data.
        
        Args:
            data: Sample data to infer schema from
            name (str): Name for the schema
            
        Returns:
            dict: JSON schema
        """
        schema = {
            "title": f"{name.capitalize()} Schema",
            "type": "object",
            "properties": {}
        }
        
        if isinstance(data, dict):
            for key, value in data.items():
                schema["properties"][key] = InputOutputSerializer._infer_type(value)
        elif isinstance(data, (list, np.ndarray)):
            # For array-like data, create a schema with indexed properties
            if len(data) > 0:
                if isinstance(data[0], (dict, list, np.ndarray)):
                    # Nested structure, use a more generic schema
                    schema = {
                        "title": f"{name.capitalize()} Schema",
                        "type": "array",
                        "items": InputOutputSerializer._infer_type(data[0])
                    }
                else:
                    # Flat array, create properties for each index
                    for i, value in enumerate(data):
                        schema["properties"][f"feature_{i}"] = InputOutputSerializer._infer_type(value)
        
        return schema
    
    @staticmethod
    def _infer_type(value):
        """
        Infer the JSON schema type for a value.
        
        Args:
            value: Value to infer type from
            
        Returns:
            dict: JSON schema type definition
        """
        if isinstance(value, (int, np.integer)):
            return {"type": "integer"}
        elif isinstance(value, (float, np.floating)):
            return {"type": "number"}
        elif isinstance(value, (str, np.character)):
            return {"type": "string"}
        elif isinstance(value, (bool, np.bool_)):
            return {"type": "boolean"}
        elif isinstance(value, (list, np.ndarray)):
            if len(value) > 0:
                # Infer type from the first element
                item_type = InputOutputSerializer._infer_type(value[0])
                return {
                    "type": "array",
                    "items": item_type
                }
            else:
                return {"type": "array", "items": {}}
        elif isinstance(value, dict):
            properties = {}
            for k, v in value.items():
                properties[k] = InputOutputSerializer._infer_type(v)
            return {
                "type": "object",
                "properties": properties
            }
        elif value is None:
            return {"type": "null"}
        else:
            # Default to string for unknown types
            return {"type": "string"}
    
    @staticmethod
    def validate_data_against_schema(data, schema):
        """
        Validate data against a JSON schema.
        
        Args:
            data: Data to validate
            schema (dict): JSON schema to validate against
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            from jsonschema import validate, ValidationError
            
            validate(instance=data, schema=schema)
            return True
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error validating data: {str(e)}")
            return False
    
    @staticmethod
    def serialize_numpy(obj):
        """
        Custom JSON serializer for handling NumPy types.
        
        Args:
            obj: Object to serialize
            
        Returns:
            JSON serializable object
        """
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        else:
            return obj
    
    @staticmethod
    def serialize_to_json(data, file_path=None):
        """
        Serialize data to JSON, handling NumPy types.
        
        Args:
            data: Data to serialize
            file_path (str, optional): Path to save the JSON file
            
        Returns:
            str: JSON string or file path if file_path is provided
        """
        try:
            json_str = json.dumps(data, default=InputOutputSerializer.serialize_numpy)
            
            if file_path:
                with open(file_path, 'w') as f:
                    f.write(json_str)
                return file_path
            else:
                return json_str
        except Exception as e:
            logger.error(f"Error serializing to JSON: {str(e)}")
            raise
    
    @staticmethod
    def deserialize_from_json(json_str=None, file_path=None):
        """
        Deserialize data from JSON.
        
        Args:
            json_str (str, optional): JSON string to deserialize
            file_path (str, optional): Path to JSON file to deserialize
            
        Returns:
            object: Deserialized data
        """
        try:
            if file_path:
                with open(file_path, 'r') as f:
                    return json.load(f)
            elif json_str:
                return json.loads(json_str)
            else:
                raise ValueError("Either json_str or file_path must be provided")
        except Exception as e:
            logger.error(f"Error deserializing from JSON: {str(e)}")
            raise
