import os
import json
import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from ml_django_brain.registry import ModelRegistry
from ml_django_brain.utils.metrics import ModelMetricsCalculator
from ml_django_brain.models import ModelVersion


class Command(BaseCommand):
    help = 'Evaluate a registered model on a test dataset and record metrics'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Name of the model to evaluate')
        parser.add_argument('test_data_path', type=str, help='Path to test data file (CSV or JSON)')
        parser.add_argument('--version', type=str, help='Specific model version to evaluate (defaults to active version)')
        parser.add_argument('--target-column', type=str, required=True, help='Name of the target column in the test data')
        parser.add_argument('--task-type', type=str, choices=['classification', 'regression', 'clustering'], 
                           default='classification', help='Type of ML task')
        parser.add_argument('--output', type=str, help='Path to save evaluation results as JSON')
        parser.add_argument('--record-metrics', action='store_true', help='Record metrics in the database')

    def handle(self, *args, **options):
        model_name = options['model_name']
        test_data_path = options['test_data_path']
        version = options['version']
        target_column = options['target_column']
        task_type = options['task_type']
        
        # Check if test data file exists
        if not os.path.exists(test_data_path):
            raise CommandError(f"Test data file not found: {test_data_path}")
        
        # Load the test data
        try:
            self.stdout.write(f"Loading test data from {test_data_path}...")
            if test_data_path.endswith('.csv'):
                test_data = pd.read_csv(test_data_path)
            elif test_data_path.endswith('.json'):
                test_data = pd.read_json(test_data_path)
            else:
                raise CommandError("Test data file must be CSV or JSON")
            
            # Check if target column exists
            if target_column not in test_data.columns:
                raise CommandError(f"Target column '{target_column}' not found in test data")
            
            # Split features and target
            X_test = test_data.drop(columns=[target_column])
            y_test = test_data[target_column]
            
            self.stdout.write(f"Loaded test data with {len(test_data)} samples and {len(X_test.columns)} features")
        except Exception as e:
            raise CommandError(f"Failed to load test data: {str(e)}")
        
        # Load the model
        try:
            registry = ModelRegistry()
            model = registry.load_model(model_name, version)
            
            # Get the model version object
            if version:
                model_version = ModelVersion.objects.get(model__name=model_name, version=version)
            else:
                model_version = ModelVersion.objects.get(model__name=model_name, is_active=True)
            
            self.stdout.write(f"Loaded model '{model_name}' version '{model_version.version}'")
        except Exception as e:
            raise CommandError(f"Failed to load model: {str(e)}")
        
        # Make predictions
        try:
            self.stdout.write("Making predictions...")
            
            # Get predictions
            if hasattr(model, 'predict_proba') and task_type == 'classification':
                y_prob = model.predict_proba(X_test)
                y_pred = model.predict(X_test)
            else:
                y_prob = None
                y_pred = model.predict(X_test)
            
            self.stdout.write(f"Made predictions for {len(y_pred)} samples")
        except Exception as e:
            raise CommandError(f"Failed to make predictions: {str(e)}")
        
        # Calculate metrics
        try:
            self.stdout.write("Calculating metrics...")
            
            if task_type == 'classification':
                metrics = ModelMetricsCalculator.calculate_classification_metrics(y_test, y_pred, y_prob)
                
                # Print classification metrics
                self.stdout.write(f"Accuracy: {metrics.get('accuracy', 'N/A'):.4f}")
                if 'precision' in metrics:
                    self.stdout.write(f"Precision: {metrics['precision']:.4f}")
                if 'recall' in metrics:
                    self.stdout.write(f"Recall: {metrics['recall']:.4f}")
                if 'f1_score' in metrics:
                    self.stdout.write(f"F1 Score: {metrics['f1_score']:.4f}")
                if 'roc_auc' in metrics:
                    self.stdout.write(f"ROC AUC: {metrics['roc_auc']:.4f}")
            
            elif task_type == 'regression':
                metrics = ModelMetricsCalculator.calculate_regression_metrics(y_test, y_pred)
                
                # Print regression metrics
                self.stdout.write(f"MSE: {metrics.get('mse', 'N/A'):.4f}")
                self.stdout.write(f"RMSE: {metrics.get('rmse', 'N/A'):.4f}")
                self.stdout.write(f"MAE: {metrics.get('mae', 'N/A'):.4f}")
                self.stdout.write(f"R²: {metrics.get('r2', 'N/A'):.4f}")
            
            elif task_type == 'clustering':
                metrics = ModelMetricsCalculator.calculate_clustering_metrics(X_test, y_pred)
                
                # Print clustering metrics
                if 'silhouette_score' in metrics:
                    self.stdout.write(f"Silhouette Score: {metrics['silhouette_score']:.4f}")
                if 'calinski_harabasz_score' in metrics:
                    self.stdout.write(f"Calinski-Harabasz Score: {metrics['calinski_harabasz_score']:.4f}")
                if 'davies_bouldin_score' in metrics:
                    self.stdout.write(f"Davies-Bouldin Score: {metrics['davies_bouldin_score']:.4f}")
        except Exception as e:
            raise CommandError(f"Failed to calculate metrics: {str(e)}")
        
        # Record metrics if requested
        if options['record_metrics']:
            try:
                self.stdout.write("Recording metrics in database...")
                recorded_metrics = ModelMetricsCalculator.record_metrics(model_version, metrics)
                self.stdout.write(f"Recorded {len(recorded_metrics)} metrics")
                
                # Check for drift
                drift_info = ModelMetricsCalculator.detect_drift(model_version, metrics)
                if drift_info['detected']:
                    self.stdout.write(self.style.WARNING("Model drift detected!"))
                    for metric_name, drift_data in drift_info['metrics'].items():
                        self.stdout.write(
                            f"  - {metric_name}: current={drift_data['current']:.4f}, "
                            f"historical avg={drift_data['historical_avg']:.4f}, "
                            f"change={drift_data['relative_change']:.2%}"
                        )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to record metrics: {str(e)}"))
        
        # Save results to file if requested
        if options['output']:
            try:
                with open(options['output'], 'w') as f:
                    json.dump(metrics, f, indent=2)
                self.stdout.write(f"Saved evaluation results to {options['output']}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to save results: {str(e)}"))
        
        self.stdout.write(self.style.SUCCESS("Evaluation completed successfully"))
