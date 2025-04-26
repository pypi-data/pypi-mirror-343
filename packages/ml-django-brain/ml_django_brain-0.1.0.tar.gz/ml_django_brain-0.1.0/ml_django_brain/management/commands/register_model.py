import os
import sys
import joblib
import pickle
from django.core.management.base import BaseCommand, CommandError
from ml_django_brain.registry import ModelRegistry
from ml_django_brain.utils.serialization import InputOutputSerializer
import json


class Command(BaseCommand):
    help = 'Register a machine learning model with the ML Django Brain registry'

    def add_arguments(self, parser):
        parser.add_argument('model_path', type=str, help='Path to the model file')
        parser.add_argument('--name', type=str, required=True, help='Name for the model')
        parser.add_argument('--version', type=str, default='1.0.0', help='Version string (default: 1.0.0)')
        parser.add_argument('--description', type=str, default='', help='Description of the model')
        parser.add_argument('--input-schema', type=str, help='Path to JSON file with input schema')
        parser.add_argument('--output-schema', type=str, help='Path to JSON file with output schema')
        parser.add_argument('--metrics', type=str, help='Path to JSON file with model metrics')
        parser.add_argument('--sample-input', type=str, help='Path to JSON file with sample input data (for schema inference)')
        parser.add_argument('--sample-output', type=str, help='Path to JSON file with sample output data (for schema inference)')

    def handle(self, *args, **options):
        model_path = options['model_path']
        name = options['name']
        version = options['version']
        description = options['description']
        
        # Check if model file exists
        if not os.path.exists(model_path):
            raise CommandError(f"Model file not found: {model_path}")
        
        # Load the model
        try:
            self.stdout.write(f"Loading model from {model_path}...")
            if model_path.endswith('.joblib'):
                model = joblib.load(model_path)
            elif model_path.endswith('.pkl') or model_path.endswith('.pickle'):
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)
            else:
                self.stdout.write(self.style.WARNING(f"Unknown model format, trying joblib..."))
                model = joblib.load(model_path)
        except Exception as e:
            raise CommandError(f"Failed to load model: {str(e)}")
        
        # Load or infer input schema
        input_schema = {}
        if options['input_schema']:
            try:
                with open(options['input_schema'], 'r') as f:
                    input_schema = json.load(f)
            except Exception as e:
                raise CommandError(f"Failed to load input schema: {str(e)}")
        elif options['sample_input']:
            try:
                with open(options['sample_input'], 'r') as f:
                    sample_input = json.load(f)
                input_schema = InputOutputSerializer.infer_schema_from_data(sample_input, "input")
                self.stdout.write(f"Inferred input schema from sample data")
            except Exception as e:
                raise CommandError(f"Failed to infer input schema: {str(e)}")
        
        # Load or infer output schema
        output_schema = {}
        if options['output_schema']:
            try:
                with open(options['output_schema'], 'r') as f:
                    output_schema = json.load(f)
            except Exception as e:
                raise CommandError(f"Failed to load output schema: {str(e)}")
        elif options['sample_output']:
            try:
                with open(options['sample_output'], 'r') as f:
                    sample_output = json.load(f)
                output_schema = InputOutputSerializer.infer_schema_from_data(sample_output, "output")
                self.stdout.write(f"Inferred output schema from sample data")
            except Exception as e:
                raise CommandError(f"Failed to infer output schema: {str(e)}")
        
        # Load metrics
        metrics = {}
        if options['metrics']:
            try:
                with open(options['metrics'], 'r') as f:
                    metrics = json.load(f)
            except Exception as e:
                raise CommandError(f"Failed to load metrics: {str(e)}")
        
        # Register the model
        try:
            registry = ModelRegistry()
            ml_model, model_version = registry.register(
                name=name,
                model=model,
                version=version,
                description=description,
                input_schema=input_schema,
                output_schema=output_schema,
                metrics=metrics
            )
            
            self.stdout.write(self.style.SUCCESS(
                f"Successfully registered model '{name}' version '{version}'\n"
                f"Model ID: {ml_model.id}\n"
                f"Version ID: {model_version.id}\n"
                f"Model type: {ml_model.model_type}"
            ))
        except Exception as e:
            raise CommandError(f"Failed to register model: {str(e)}")
