from django.core.management.base import BaseCommand
from ml_django_brain.registry import ModelRegistry
from ml_django_brain.models import MLModel, ModelVersion
from django.utils import timezone
import json


class Command(BaseCommand):
    help = 'List all registered machine learning models in the ML Django Brain registry'

    def add_arguments(self, parser):
        parser.add_argument('--name', type=str, help='Filter by model name')
        parser.add_argument('--type', type=str, help='Filter by model type')
        parser.add_argument('--json', action='store_true', help='Output in JSON format')
        parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed information')

    def handle(self, *args, **options):
        # Get the registry
        registry = ModelRegistry()
        
        # Get all models
        queryset = MLModel.objects.all()
        
        # Apply filters
        if options['name']:
            queryset = queryset.filter(name__icontains=options['name'])
        
        if options['type']:
            queryset = queryset.filter(model_type__icontains=options['type'])
        
        # Check if any models exist
        if not queryset.exists():
            if options['json']:
                self.stdout.write(json.dumps([]))
            else:
                self.stdout.write(self.style.WARNING("No models found in registry"))
            return
        
        # Output in JSON format if requested
        if options['json']:
            models_data = []
            for model in queryset:
                model_data = {
                    'id': str(model.id),
                    'name': model.name,
                    'type': model.model_type,
                    'description': model.description,
                    'created_at': model.created_at.isoformat(),
                    'updated_at': model.updated_at.isoformat(),
                    'versions': []
                }
                
                for version in model.versions.all():
                    version_data = {
                        'id': str(version.id),
                        'version': version.version,
                        'is_active': version.is_active,
                        'created_at': version.created_at.isoformat()
                    }
                    
                    if options['verbose']:
                        version_data.update({
                            'file_path': version.file_path,
                            'input_schema': version.input_schema,
                            'output_schema': version.output_schema,
                            'metrics': version.metrics
                        })
                    
                    model_data['versions'].append(version_data)
                
                models_data.append(model_data)
            
            self.stdout.write(json.dumps(models_data, indent=2))
        
        # Output in human-readable format
        else:
            self.stdout.write(self.style.SUCCESS(f"Found {queryset.count()} models in registry:"))
            
            for model in queryset:
                self.stdout.write("\n" + "="*50)
                self.stdout.write(f"Model: {model.name} (ID: {model.id})")
                self.stdout.write(f"Type: {model.model_type}")
                self.stdout.write(f"Description: {model.description}")
                self.stdout.write(f"Created: {model.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                self.stdout.write(f"Updated: {model.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Show versions
                versions = model.versions.all()
                self.stdout.write(f"\nVersions ({versions.count()}):")
                
                for version in versions:
                    active_marker = " (ACTIVE)" if version.is_active else ""
                    self.stdout.write(f"  - {version.version}{active_marker} (ID: {version.id})")
                    self.stdout.write(f"    Created: {version.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    if options['verbose']:
                        self.stdout.write(f"    File path: {version.file_path}")
                        
                        # Show input schema
                        if version.input_schema:
                            self.stdout.write(f"    Input schema: {json.dumps(version.input_schema, indent=6)}")
                        
                        # Show output schema
                        if version.output_schema:
                            self.stdout.write(f"    Output schema: {json.dumps(version.output_schema, indent=6)}")
                        
                        # Show metrics
                        if version.metrics:
                            self.stdout.write(f"    Metrics: {json.dumps(version.metrics, indent=6)}")
            
            self.stdout.write("\n" + "="*50)
