from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MLModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Name of the model', max_length=255)),
                ('description', models.TextField(blank=True, help_text='Description of the model')),
                ('model_type', models.CharField(help_text='Type of ML model (e.g., sklearn, tensorflow, pytorch)', max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'ML Model',
                'verbose_name_plural': 'ML Models',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='ModelVersion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('version', models.CharField(help_text="Version identifier (e.g., '1.0.0')", max_length=50)),
                ('file_path', models.CharField(help_text='Path to the stored model file', max_length=500)),
                ('is_active', models.BooleanField(default=True, help_text='Whether this version is active')),
                ('input_schema', models.JSONField(default=dict, help_text='JSON schema describing expected input format')),
                ('output_schema', models.JSONField(default=dict, help_text='JSON schema describing expected output format')),
                ('metrics', models.JSONField(default=dict, help_text='Performance metrics for this model version')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='ml_django_brain.mlmodel')),
            ],
            options={
                'verbose_name': 'Model Version',
                'verbose_name_plural': 'Model Versions',
                'ordering': ['-created_at'],
                'unique_together': {('model', 'version')},
            },
        ),
        migrations.CreateModel(
            name='PredictionLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('input_data', models.JSONField(help_text='Input data for the prediction')),
                ('output_data', models.JSONField(help_text='Output data from the prediction')),
                ('prediction_time', models.FloatField(help_text='Time taken for prediction in seconds')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('model_version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='predictions', to='ml_django_brain.modelversion')),
            ],
            options={
                'verbose_name': 'Prediction Log',
                'verbose_name_plural': 'Prediction Logs',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ModelMetric',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('metric_name', models.CharField(help_text='Name of the metric (e.g., accuracy, f1_score)', max_length=100)),
                ('metric_value', models.FloatField(help_text='Value of the metric')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('model_version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performance_metrics', to='ml_django_brain.modelversion')),
            ],
            options={
                'verbose_name': 'Model Metric',
                'verbose_name_plural': 'Model Metrics',
                'ordering': ['-created_at'],
            },
        ),
    ]
