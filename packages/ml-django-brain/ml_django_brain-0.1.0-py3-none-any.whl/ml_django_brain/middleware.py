import time
import logging
import json
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from ml_django_brain.views import MLModelViewSet

logger = logging.getLogger(__name__)

class MLMonitoringMiddleware(MiddlewareMixin):
    """
    Middleware for monitoring ML model API usage and performance.
    """
    
    def process_request(self, request):
        """
        Process the request before it reaches the view.
        Add a timestamp to track request processing time.
        """
        request.ml_request_start_time = time.time()
        return None
    
    def process_response(self, request, response):
        """
        Process the response after the view is called.
        Log information about ML model API usage.
        """
        # Check if this is a request to the ML model API
        try:
            resolver_match = resolve(request.path)
            view_class = resolver_match.func.cls if hasattr(resolver_match.func, 'cls') else None
            
            # Only process ML model API requests
            if view_class and issubclass(view_class, MLModelViewSet):
                # Calculate request processing time
                if hasattr(request, 'ml_request_start_time'):
                    processing_time = time.time() - request.ml_request_start_time
                else:
                    processing_time = None
                
                # Get the action and model name
                action = resolver_match.kwargs.get('action', 'unknown')
                model_id = resolver_match.kwargs.get('pk', 'unknown')
                
                # Log the request
                log_data = {
                    'timestamp': time.time(),
                    'method': request.method,
                    'path': request.path,
                    'action': action,
                    'model_id': model_id,
                    'status_code': response.status_code,
                    'processing_time': processing_time
                }
                
                # Add request data for prediction requests
                if action in ['predict', 'batch_predict'] and request.method == 'POST':
                    try:
                        # Don't log the actual data, just the shape or size
                        if hasattr(request, 'data'):
                            if action == 'predict' and 'input_data' in request.data:
                                if isinstance(request.data['input_data'], dict):
                                    log_data['input_size'] = len(request.data['input_data'])
                                elif isinstance(request.data['input_data'], list):
                                    log_data['input_size'] = len(request.data['input_data'])
                            elif action == 'batch_predict' and 'input_data_list' in request.data:
                                log_data['batch_size'] = len(request.data['input_data_list'])
                    except Exception as e:
                        logger.warning(f"Error logging request data: {str(e)}")
                
                # Log successful predictions
                if action in ['predict', 'batch_predict'] and response.status_code == 200:
                    logger.info(f"ML API Request: {json.dumps(log_data)}")
                
                # Log failed predictions with warning level
                elif action in ['predict', 'batch_predict'] and response.status_code != 200:
                    logger.warning(f"Failed ML API Request: {json.dumps(log_data)}")
                
                # Log other API requests with debug level
                else:
                    logger.debug(f"ML API Request: {json.dumps(log_data)}")
        
        except Exception as e:
            logger.error(f"Error in MLMonitoringMiddleware: {str(e)}")
        
        return response
