from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from ml_django_brain.models import MLModel, ModelVersion, PredictionLog, ModelMetric


class ModelVersionInline(admin.TabularInline):
    model = ModelVersion
    extra = 0
    readonly_fields = ('id', 'created_at')
    fields = ('version', 'is_active', 'file_path', 'created_at')


@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'model_type', 'version_count', 'latest_version_display', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'model_type')
    list_filter = ('model_type', 'created_at', 'updated_at')
    readonly_fields = ('id', 'created_at', 'updated_at')
    inlines = [ModelVersionInline]
    
    def version_count(self, obj):
        return obj.versions.count()
    version_count.short_description = 'Versions'
    
    def latest_version_display(self, obj):
        latest = obj.latest_version
        if latest:
            return latest.version
        return '-'
    latest_version_display.short_description = 'Latest Version'


@admin.register(ModelVersion)
class ModelVersionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_active', 'created_at', 'view_model_link')
    list_filter = ('is_active', 'created_at', 'model__name')
    search_fields = ('version', 'model__name')
    readonly_fields = ('id', 'created_at', 'file_path')
    
    def view_model_link(self, obj):
        url = reverse('admin:ml_django_brain_mlmodel_change', args=[obj.model.id])
        return format_html('<a href="{}">View Model</a>', url)
    view_model_link.short_description = 'Model'


@admin.register(PredictionLog)
class PredictionLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'model_version_display', 'prediction_time', 'created_at')
    list_filter = ('created_at', 'model_version__model__name')
    search_fields = ('model_version__model__name', 'model_version__version')
    readonly_fields = ('id', 'model_version', 'input_data', 'output_data', 'prediction_time', 'created_at')
    
    def model_version_display(self, obj):
        return str(obj.model_version)
    model_version_display.short_description = 'Model Version'


@admin.register(ModelMetric)
class ModelMetricAdmin(admin.ModelAdmin):
    list_display = ('id', 'model_version_display', 'metric_name', 'metric_value', 'created_at')
    list_filter = ('metric_name', 'created_at', 'model_version__model__name')
    search_fields = ('metric_name', 'model_version__model__name', 'model_version__version')
    readonly_fields = ('id', 'created_at')
    
    def model_version_display(self, obj):
        return str(obj.model_version)
    model_version_display.short_description = 'Model Version'
