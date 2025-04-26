from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from ml_django_brain.models import MLModel, ModelVersion, PredictionLog, ModelMetric
from ml_django_brain.serializers import (
    MLModelSerializer, ModelVersionSerializer, PredictionLogSerializer,
    ModelMetricSerializer, PredictionInputSerializer, BatchPredictionInputSerializer
)
from ml_django_brain.registry import ModelRegistry
from ml_django_brain.services import PredictionService


class MLModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ML models.
    """
    queryset = MLModel.objects.all()
    serializer_class = MLModelSerializer
    permission_classes = []
    
    def get_queryset(self):
        """
        Optionally filter by model type.
        """
        queryset = MLModel.objects.all()
        model_type = self.request.query_params.get('model_type', None)
        if model_type:
            queryset = queryset.filter(model_type=model_type)
        return queryset
    
    @action(detail=True, methods=['get'])
    def versions(self, request, pk=None):
        """
        Get all versions of a model.
        """
        model = self.get_object()
        versions = model.versions.all()
        serializer = ModelVersionSerializer(versions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def predict(self, request, pk=None):
        """
        Make a prediction using the model.
        """
        model = self.get_object()
        serializer = PredictionInputSerializer(data=request.data)
        
        if serializer.is_valid():
            input_data = serializer.validated_data['input_data']
            version = serializer.validated_data.get('version')
            
            service = PredictionService()
            try:
                result = service.predict(model.name, input_data, version)
                return Response(result)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def batch_predict(self, request, pk=None):
        """
        Make batch predictions using the model.
        """
        model = self.get_object()
        serializer = BatchPredictionInputSerializer(data=request.data)
        
        if serializer.is_valid():
            input_data_list = serializer.validated_data['input_data_list']
            version = serializer.validated_data.get('version')
            
            service = PredictionService()
            try:
                results = service.batch_predict(model.name, input_data_list, version)
                return Response(results)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'])
    def delete_from_registry(self, request, pk=None):
        """
        Delete a model from the registry.
        """
        model = self.get_object()
        registry = ModelRegistry()
        
        try:
            registry.delete_model(model.name)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ModelVersionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for model versions.
    """
    queryset = ModelVersion.objects.all()
    serializer_class = ModelVersionSerializer
    permission_classes = []
    
    def get_queryset(self):
        """
        Optionally filter by model.
        """
        queryset = ModelVersion.objects.all()
        model_id = self.request.query_params.get('model_id', None)
        if model_id:
            queryset = queryset.filter(model_id=model_id)
        return queryset
    
    @action(detail=True, methods=['post'])
    def set_active(self, request, pk=None):
        """
        Set a version as the active version.
        """
        version = self.get_object()
        
        # Deactivate all other versions of this model
        ModelVersion.objects.filter(model=version.model).update(is_active=False)
        
        # Activate this version
        version.is_active = True
        version.save()
        
        serializer = self.get_serializer(version)
        return Response(serializer.data)


class PredictionLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for prediction logs.
    """
    queryset = PredictionLog.objects.all()
    serializer_class = PredictionLogSerializer
    permission_classes = []
    
    def get_queryset(self):
        """
        Optionally filter by model version.
        """
        queryset = PredictionLog.objects.all()
        model_version_id = self.request.query_params.get('model_version_id', None)
        if model_version_id:
            queryset = queryset.filter(model_version_id=model_version_id)
        
        model_id = self.request.query_params.get('model_id', None)
        if model_id:
            queryset = queryset.filter(model_version__model_id=model_id)
        
        # Limit the number of logs returned
        limit = self.request.query_params.get('limit', 100)
        try:
            limit = int(limit)
        except ValueError:
            limit = 100
        
        return queryset.order_by('-created_at')[:limit]


class ModelMetricViewSet(viewsets.ModelViewSet):
    """
    API endpoint for model metrics.
    """
    queryset = ModelMetric.objects.all()
    serializer_class = ModelMetricSerializer
    permission_classes = []
    
    def get_queryset(self):
        """
        Optionally filter by model version or metric name.
        """
        queryset = ModelMetric.objects.all()
        model_version_id = self.request.query_params.get('model_version_id', None)
        if model_version_id:
            queryset = queryset.filter(model_version_id=model_version_id)
        
        metric_name = self.request.query_params.get('metric_name', None)
        if metric_name:
            queryset = queryset.filter(metric_name=metric_name)
        
        return queryset
