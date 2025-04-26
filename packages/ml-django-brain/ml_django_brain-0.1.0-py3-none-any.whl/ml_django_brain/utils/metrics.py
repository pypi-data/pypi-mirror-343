import logging
import numpy as np
from datetime import datetime

logger = logging.getLogger(__name__)

class ModelMetricsCalculator:
    """
    Utility class for calculating and tracking model performance metrics.
    """
    
    @staticmethod
    def calculate_classification_metrics(y_true, y_pred, y_prob=None):
        """
        Calculate common classification metrics.
        
        Args:
            y_true (array-like): True labels
            y_pred (array-like): Predicted labels
            y_prob (array-like, optional): Predicted probabilities
            
        Returns:
            dict: Dictionary of metrics
        """
        try:
            from sklearn.metrics import (
                accuracy_score, precision_score, recall_score, f1_score,
                roc_auc_score, confusion_matrix
            )
            
            metrics = {
                'accuracy': float(accuracy_score(y_true, y_pred)),
                'timestamp': datetime.now().isoformat()
            }
            
            # Try to calculate additional metrics that might fail for multi-class
            try:
                metrics['precision'] = float(precision_score(y_true, y_pred, average='weighted'))
                metrics['recall'] = float(recall_score(y_true, y_pred, average='weighted'))
                metrics['f1_score'] = float(f1_score(y_true, y_pred, average='weighted'))
            except Exception as e:
                logger.warning(f"Could not calculate precision/recall/f1: {str(e)}")
            
            # Calculate ROC AUC if probabilities are provided
            if y_prob is not None:
                try:
                    # For binary classification
                    if len(np.unique(y_true)) == 2:
                        if y_prob.ndim > 1 and y_prob.shape[1] > 1:
                            # Use the probability of the positive class
                            metrics['roc_auc'] = float(roc_auc_score(y_true, y_prob[:, 1]))
                        else:
                            metrics['roc_auc'] = float(roc_auc_score(y_true, y_prob))
                    # For multi-class classification
                    else:
                        metrics['roc_auc'] = float(roc_auc_score(y_true, y_prob, multi_class='ovr'))
                except Exception as e:
                    logger.warning(f"Could not calculate ROC AUC: {str(e)}")
            
            # Add confusion matrix
            try:
                cm = confusion_matrix(y_true, y_pred)
                metrics['confusion_matrix'] = cm.tolist()
            except Exception as e:
                logger.warning(f"Could not calculate confusion matrix: {str(e)}")
            
            return metrics
        
        except ImportError:
            logger.error("scikit-learn is not installed. Cannot calculate classification metrics.")
            raise ImportError("scikit-learn is required to calculate classification metrics")
    
    @staticmethod
    def calculate_regression_metrics(y_true, y_pred):
        """
        Calculate common regression metrics.
        
        Args:
            y_true (array-like): True values
            y_pred (array-like): Predicted values
            
        Returns:
            dict: Dictionary of metrics
        """
        try:
            from sklearn.metrics import (
                mean_squared_error, mean_absolute_error, r2_score,
                median_absolute_error, explained_variance_score
            )
            
            metrics = {
                'mse': float(mean_squared_error(y_true, y_pred)),
                'rmse': float(np.sqrt(mean_squared_error(y_true, y_pred))),
                'mae': float(mean_absolute_error(y_true, y_pred)),
                'r2': float(r2_score(y_true, y_pred)),
                'median_ae': float(median_absolute_error(y_true, y_pred)),
                'explained_variance': float(explained_variance_score(y_true, y_pred)),
                'timestamp': datetime.now().isoformat()
            }
            
            return metrics
        
        except ImportError:
            logger.error("scikit-learn is not installed. Cannot calculate regression metrics.")
            raise ImportError("scikit-learn is required to calculate regression metrics")
    
    @staticmethod
    def calculate_clustering_metrics(X, labels):
        """
        Calculate common clustering metrics.
        
        Args:
            X (array-like): Input features
            labels (array-like): Cluster labels
            
        Returns:
            dict: Dictionary of metrics
        """
        try:
            from sklearn.metrics import (
                silhouette_score, calinski_harabasz_score, davies_bouldin_score
            )
            
            metrics = {
                'timestamp': datetime.now().isoformat()
            }
            
            # Calculate silhouette score
            try:
                metrics['silhouette_score'] = float(silhouette_score(X, labels))
            except Exception as e:
                logger.warning(f"Could not calculate silhouette score: {str(e)}")
            
            # Calculate Calinski-Harabasz Index
            try:
                metrics['calinski_harabasz_score'] = float(calinski_harabasz_score(X, labels))
            except Exception as e:
                logger.warning(f"Could not calculate Calinski-Harabasz score: {str(e)}")
            
            # Calculate Davies-Bouldin Index
            try:
                metrics['davies_bouldin_score'] = float(davies_bouldin_score(X, labels))
            except Exception as e:
                logger.warning(f"Could not calculate Davies-Bouldin score: {str(e)}")
            
            return metrics
        
        except ImportError:
            logger.error("scikit-learn is not installed. Cannot calculate clustering metrics.")
            raise ImportError("scikit-learn is required to calculate clustering metrics")
    
    @staticmethod
    def record_metrics(model_version, metrics):
        """
        Record metrics for a model version.
        
        Args:
            model_version (ModelVersion): The model version
            metrics (dict): Dictionary of metrics
            
        Returns:
            list: List of created ModelMetric instances
        """
        from ml_django_brain.models import ModelMetric
        
        created_metrics = []
        
        for metric_name, metric_value in metrics.items():
            # Skip non-numeric metrics
            if not isinstance(metric_value, (int, float)) or metric_name == 'timestamp':
                continue
            
            # Create the metric record
            metric = ModelMetric.objects.create(
                model_version=model_version,
                metric_name=metric_name,
                metric_value=metric_value
            )
            
            created_metrics.append(metric)
        
        # Update the model version's metrics field
        model_version.metrics = metrics
        model_version.save(update_fields=['metrics'])
        
        return created_metrics
    
    @staticmethod
    def detect_drift(model_version, new_metrics, threshold=0.1):
        """
        Detect if there's significant drift in model performance.
        
        Args:
            model_version (ModelVersion): The model version
            new_metrics (dict): New metrics to compare
            threshold (float): Threshold for significant drift
            
        Returns:
            dict: Dictionary with drift information
        """
        from ml_django_brain.models import ModelMetric
        
        drift_info = {
            'detected': False,
            'metrics': {}
        }
        
        # Get historical metrics for this model version
        historical_metrics = {}
        for metric in ModelMetric.objects.filter(model_version=model_version):
            if metric.metric_name not in historical_metrics:
                historical_metrics[metric.metric_name] = []
            historical_metrics[metric.metric_name].append(metric.metric_value)
        
        # Compare new metrics with historical averages
        for metric_name, metric_value in new_metrics.items():
            if not isinstance(metric_value, (int, float)) or metric_name == 'timestamp':
                continue
            
            if metric_name in historical_metrics and len(historical_metrics[metric_name]) > 0:
                avg_value = np.mean(historical_metrics[metric_name])
                
                # Calculate relative change
                if avg_value != 0:
                    rel_change = abs(metric_value - avg_value) / abs(avg_value)
                    
                    # Check if change exceeds threshold
                    if rel_change > threshold:
                        drift_info['detected'] = True
                        drift_info['metrics'][metric_name] = {
                            'current': metric_value,
                            'historical_avg': avg_value,
                            'relative_change': rel_change
                        }
        
        return drift_info
