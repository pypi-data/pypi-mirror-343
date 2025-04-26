from django.db import models
from django.utils import timezone
import uuid
import json


class MLModel(models.Model):
    """
    Model to store metadata about machine learning models.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text="Name of the model")
    description = models.TextField(blank=True, help_text="Description of the model")
    model_type = models.CharField(max_length=100, help_text="Type of ML model (e.g., sklearn, tensorflow, pytorch)")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "ML Model"
        verbose_name_plural = "ML Models"
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.name} ({self.model_type})"
    
    @property
    def latest_version(self):
        """Return the latest version of this model."""
        return self.versions.order_by('-created_at').first()
    
    @property
    def is_active(self):
        """Check if the model has any active versions."""
        return self.versions.filter(is_active=True).exists()


class ModelVersion(models.Model):
    """
    Model to store different versions of a machine learning model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model = models.ForeignKey(MLModel, on_delete=models.CASCADE, related_name='versions')
    version = models.CharField(max_length=50, help_text="Version identifier (e.g., '1.0.0')")
    file_path = models.CharField(max_length=500, help_text="Path to the stored model file")
    is_active = models.BooleanField(default=True, help_text="Whether this version is active")
    input_schema = models.JSONField(default=dict, help_text="JSON schema describing expected input format")
    output_schema = models.JSONField(default=dict, help_text="JSON schema describing expected output format")
    metrics = models.JSONField(default=dict, help_text="Performance metrics for this model version")
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "Model Version"
        verbose_name_plural = "Model Versions"
        ordering = ['-created_at']
        unique_together = [['model', 'version']]
    
    def __str__(self):
        return f"{self.model.name} v{self.version}"
    
    def save(self, *args, **kwargs):
        """Override save to ensure only one active version per model if needed."""
        if self.is_active:
            # Deactivate other versions if this one is active
            ModelVersion.objects.filter(
                model=self.model, 
                is_active=True
            ).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class PredictionLog(models.Model):
    """
    Model to log predictions made by ML models.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model_version = models.ForeignKey(ModelVersion, on_delete=models.CASCADE, related_name='predictions')
    input_data = models.JSONField(help_text="Input data for the prediction")
    output_data = models.JSONField(help_text="Output data from the prediction")
    prediction_time = models.FloatField(help_text="Time taken for prediction in seconds")
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "Prediction Log"
        verbose_name_plural = "Prediction Logs"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Prediction for {self.model_version} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class ModelMetric(models.Model):
    """
    Model to store performance metrics for model versions over time.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model_version = models.ForeignKey(ModelVersion, on_delete=models.CASCADE, related_name='performance_metrics')
    metric_name = models.CharField(max_length=100, help_text="Name of the metric (e.g., accuracy, f1_score)")
    metric_value = models.FloatField(help_text="Value of the metric")
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "Model Metric"
        verbose_name_plural = "Model Metrics"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.metric_name}: {self.metric_value} for {self.model_version}"
