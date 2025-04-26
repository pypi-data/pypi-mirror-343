import time
import logging
import numpy as np
import pandas as pd
import json
from django.conf import settings
from jsonschema import validate, ValidationError

from ml_django_brain.registry import ModelRegistry
from ml_django_brain.models import PredictionLog, ModelVersion

logger = logging.getLogger(__name__)

class PredictionService:
    """
    Service for making predictions using registered ML models.
    """
    
    def __init__(self):
        self.registry = ModelRegistry()
    
    def predict(self, model_name, input_data, version=None, log_prediction=True):
        """
        Make a prediction using a registered model.
        
        Args:
            model_name (str): Name of the model to use
            input_data (dict or list): Input data for prediction
            version (str, optional): Specific version to use. If None, uses the active version.
            log_prediction (bool): Whether to log this prediction
            
        Returns:
            dict: Prediction results
        """
        start_time = time.time()
        
        try:
            # Get the model version
            model_version = self._get_model_version(model_name, version)
            
            # Validate input data against schema
            self._validate_input(input_data, model_version.input_schema)
            
            # Load the model
            model = self.registry.load_model(model_name, version)
            
            # Prepare input data for the model
            prepared_input = self._prepare_input_data(input_data, model_version.model.model_type)
            
            # Make prediction
            raw_prediction = self._make_prediction(model, prepared_input, model_version.model.model_type)
            
            # Format the prediction result
            prediction_result = self._format_prediction_result(raw_prediction, model_version.output_schema)
            
            # Calculate prediction time
            prediction_time = time.time() - start_time
            
            # Log the prediction if requested
            if log_prediction:
                self._log_prediction(model_version, input_data, prediction_result, prediction_time)
            
            return prediction_result
        
        except Exception as e:
            logger.error(f"Error making prediction with model {model_name}: {str(e)}")
            raise
    
    def batch_predict(self, model_name, input_data_list, version=None, log_predictions=True):
        """
        Make batch predictions using a registered model.
        
        Args:
            model_name (str): Name of the model to use
            input_data_list (list): List of input data dictionaries
            version (str, optional): Specific version to use. If None, uses the active version.
            log_predictions (bool): Whether to log these predictions
            
        Returns:
            list: List of prediction results
        """
        if not input_data_list:
            return []
        
        start_time = time.time()
        
        try:
            # Get the model version
            model_version = self._get_model_version(model_name, version)
            
            # Load the model
            model = self.registry.load_model(model_name, version)
            
            # Validate and prepare all inputs
            prepared_inputs = []
            for input_data in input_data_list:
                self._validate_input(input_data, model_version.input_schema)
                prepared_input = self._prepare_input_data(input_data, model_version.model.model_type)
                prepared_inputs.append(prepared_input)
            
            # Combine inputs for batch prediction if possible
            model_type = model_version.model.model_type
            if model_type == 'sklearn' and all(isinstance(x, (list, np.ndarray)) for x in prepared_inputs):
                combined_input = np.vstack(prepared_inputs)
                raw_predictions = self._make_prediction(model, combined_input, model_type)
                # Split the predictions back into individual results
                raw_prediction_list = [raw_predictions[i:i+1] for i in range(len(raw_predictions))]
            else:
                # Fall back to individual predictions
                raw_prediction_list = [self._make_prediction(model, input_data, model_type) 
                                      for input_data in prepared_inputs]
            
            # Format all prediction results
            prediction_results = [self._format_prediction_result(raw_pred, model_version.output_schema) 
                                 for raw_pred in raw_prediction_list]
            
            # Calculate total prediction time
            total_prediction_time = time.time() - start_time
            avg_prediction_time = total_prediction_time / len(input_data_list)
            
            # Log predictions if requested
            if log_predictions:
                for i, (input_data, prediction_result) in enumerate(zip(input_data_list, prediction_results)):
                    self._log_prediction(model_version, input_data, prediction_result, avg_prediction_time)
            
            return prediction_results
        
        except Exception as e:
            logger.error(f"Error making batch predictions with model {model_name}: {str(e)}")
            raise
    
    def _get_model_version(self, model_name, version=None):
        """
        Get the model version object.
        
        Args:
            model_name (str): Name of the model
            version (str, optional): Specific version to get. If None, gets the active version.
            
        Returns:
            ModelVersion: The model version object
        """
        try:
            if version:
                return ModelVersion.objects.get(model__name=model_name, version=version)
            else:
                return ModelVersion.objects.get(model__name=model_name, is_active=True)
        except ModelVersion.DoesNotExist:
            if version:
                raise ValueError(f"Version {version} of model {model_name} not found")
            else:
                raise ValueError(f"No active version found for model {model_name}")
    
    def _validate_input(self, input_data, input_schema):
        """
        Validate input data against the schema.
        
        Args:
            input_data (dict or list): Input data to validate
            input_schema (dict): JSON schema for validation
            
        Raises:
            ValidationError: If validation fails
        """
        if not input_schema:
            logger.warning("No input schema defined, skipping validation")
            return
        
        try:
            validate(instance=input_data, schema=input_schema)
        except ValidationError as e:
            logger.error(f"Input validation failed: {str(e)}")
            raise ValidationError(f"Input validation failed: {str(e)}")
    
    def _prepare_input_data(self, input_data, model_type):
        """
        Prepare input data for the specific model type.
        
        Args:
            input_data (dict or list): Input data to prepare
            model_type (str): Type of the model
            
        Returns:
            object: Prepared input data suitable for the model
        """
        if model_type == 'sklearn':
            # For sklearn, convert to numpy array
            if isinstance(input_data, dict):
                # Convert dict to array
                return np.array(list(input_data.values())).reshape(1, -1)
            elif isinstance(input_data, list):
                # Already a list, convert to 2D array
                return np.array(input_data).reshape(1, -1)
            else:
                return input_data
        
        elif model_type == 'tensorflow':
            # For tensorflow, convert to numpy array with appropriate shape
            return np.array(list(input_data.values()) if isinstance(input_data, dict) else input_data)
        
        elif model_type == 'pytorch':
            # For pytorch, return as is (will be converted to tensor in prediction method)
            return input_data
        
        else:
            # For other models, return as is
            return input_data
    
    def _make_prediction(self, model, input_data, model_type):
        """
        Make a prediction using the appropriate method for the model type.
        
        Args:
            model (object): The ML model
            input_data (object): Prepared input data
            model_type (str): Type of the model
            
        Returns:
            object: Raw prediction result
        """
        if model_type == 'sklearn':
            # For sklearn models
            if hasattr(model, 'predict_proba'):
                # For classifiers, return probabilities
                return model.predict_proba(input_data)
            else:
                # For regressors or other models
                return model.predict(input_data)
        
        elif model_type == 'tensorflow':
            # For tensorflow models
            return model.predict(input_data)
        
        elif model_type == 'pytorch':
            # For pytorch models
            import torch
            
            # Convert to tensor if not already
            if not isinstance(input_data, torch.Tensor):
                if isinstance(input_data, (list, np.ndarray)):
                    input_tensor = torch.tensor(input_data, dtype=torch.float32)
                elif isinstance(input_data, dict):
                    input_tensor = torch.tensor(list(input_data.values()), dtype=torch.float32)
                else:
                    input_tensor = input_data
            else:
                input_tensor = input_data
            
            # Set model to evaluation mode
            model.eval()
            
            # Make prediction
            with torch.no_grad():
                output = model(input_tensor)
            
            # Convert output tensor to numpy array
            return output.numpy()
        
        elif model_type in ('xgboost', 'lightgbm', 'catboost'):
            # For boosting libraries
            return model.predict(input_data)
        
        else:
            # For unknown model types, try a generic predict method
            return model.predict(input_data)
    
    def _format_prediction_result(self, raw_prediction, output_schema):
        """
        Format the raw prediction result according to the output schema.
        
        Args:
            raw_prediction (object): Raw prediction from the model
            output_schema (dict): Schema describing the expected output format
            
        Returns:
            dict: Formatted prediction result
        """
        # Convert numpy arrays to lists for JSON serialization
        if isinstance(raw_prediction, np.ndarray):
            prediction_data = raw_prediction.tolist()
        else:
            prediction_data = raw_prediction
        
        # If output schema defines properties, use them to format the result
        if output_schema and 'properties' in output_schema:
            properties = output_schema['properties']
            result = {}
            
            # Single prediction
            if len(np.array(prediction_data).shape) == 1 or np.array(prediction_data).shape[0] == 1:
                flat_pred = np.array(prediction_data).flatten()
                for i, (key, _) in enumerate(properties.items()):
                    if i < len(flat_pred):
                        result[key] = flat_pred[i]
            # Multiple predictions (e.g., class probabilities)
            else:
                for i, (key, _) in enumerate(properties.items()):
                    if i < len(prediction_data):
                        result[key] = prediction_data[i]
            
            return result
        
        # If no schema or schema doesn't define properties, return a simple format
        if isinstance(prediction_data, list) and len(prediction_data) == 1:
            return {"prediction": prediction_data[0]}
        else:
            return {"prediction": prediction_data}
    
    def _log_prediction(self, model_version, input_data, output_data, prediction_time):
        """
        Log a prediction to the database.
        
        Args:
            model_version (ModelVersion): The model version used
            input_data (dict or list): Input data for the prediction
            output_data (dict or list): Output data from the prediction
            prediction_time (float): Time taken for prediction in seconds
        """
        try:
            # Convert numpy arrays to lists for JSON serialization
            if isinstance(input_data, np.ndarray):
                input_data = input_data.tolist()
            if isinstance(output_data, np.ndarray):
                output_data = output_data.tolist()
            
            # Create the prediction log
            PredictionLog.objects.create(
                model_version=model_version,
                input_data=input_data,
                output_data=output_data,
                prediction_time=prediction_time
            )
        except Exception as e:
            logger.error(f"Error logging prediction: {str(e)}")
            # Don't raise the exception, just log it
            # We don't want prediction logging failures to affect the main prediction flow
