from rest_framework import serializers
from ml_django_brain.models import MLModel, ModelVersion, PredictionLog, ModelMetric


class ModelVersionSerializer(serializers.ModelSerializer):
    """Serializer for model versions."""
    
    class Meta:
        model = ModelVersion
        fields = ['id', 'version', 'is_active', 'input_schema', 'output_schema', 
                  'metrics', 'created_at']
        read_only_fields = ['id', 'created_at']


class MLModelSerializer(serializers.ModelSerializer):
    """Serializer for ML models."""
    
    versions = ModelVersionSerializer(many=True, read_only=True)
    latest_version = serializers.SerializerMethodField()
    
    class Meta:
        model = MLModel
        fields = ['id', 'name', 'description', 'model_type', 'created_at', 
                  'updated_at', 'versions', 'latest_version']
        read_only_fields = ['id', 'model_type', 'created_at', 'updated_at']
    
    def get_latest_version(self, obj):
        """Get the latest version of the model."""
        latest = obj.latest_version
        if latest:
            return ModelVersionSerializer(latest).data
        return None


class PredictionLogSerializer(serializers.ModelSerializer):
    """Serializer for prediction logs."""
    
    model_name = serializers.SerializerMethodField()
    model_version = serializers.SerializerMethodField()
    
    class Meta:
        model = PredictionLog
        fields = ['id', 'model_name', 'model_version', 'input_data', 'output_data', 
                  'prediction_time', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_model_name(self, obj):
        """Get the name of the model."""
        return obj.model_version.model.name
    
    def get_model_version(self, obj):
        """Get the version string of the model."""
        return obj.model_version.version


class ModelMetricSerializer(serializers.ModelSerializer):
    """Serializer for model metrics."""
    
    model_name = serializers.SerializerMethodField()
    model_version = serializers.SerializerMethodField()
    
    class Meta:
        model = ModelMetric
        fields = ['id', 'model_name', 'model_version', 'metric_name', 'metric_value', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_model_name(self, obj):
        """Get the name of the model."""
        return obj.model_version.model.name
    
    def get_model_version(self, obj):
        """Get the version string of the model."""
        return obj.model_version.version


class PredictionInputSerializer(serializers.Serializer):
    """Serializer for prediction input data."""
    
    input_data = serializers.JSONField(help_text="Input data for prediction")
    version = serializers.CharField(required=False, allow_null=True, 
                                   help_text="Model version to use (defaults to active version)")


class BatchPredictionInputSerializer(serializers.Serializer):
    """Serializer for batch prediction input data."""
    
    input_data_list = serializers.ListField(
        child=serializers.JSONField(),
        help_text="List of input data objects for batch prediction"
    )
    version = serializers.CharField(required=False, allow_null=True,
                                   help_text="Model version to use (defaults to active version)")
