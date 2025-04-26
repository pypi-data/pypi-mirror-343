from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ml_django_brain.views import (
    MLModelViewSet, ModelVersionViewSet, PredictionLogViewSet, ModelMetricViewSet
)

router = DefaultRouter()
router.register(r'models', MLModelViewSet)
router.register(r'versions', ModelVersionViewSet)
router.register(r'logs', PredictionLogViewSet)
router.register(r'metrics', ModelMetricViewSet)

app_name = 'ml_django_brain'

urlpatterns = [
    path('', include(router.urls)),
]
