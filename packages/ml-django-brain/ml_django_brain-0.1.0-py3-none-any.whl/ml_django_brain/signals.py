from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import logging

from ml_django_brain.models import MLModel, ModelVersion, PredictionLog, ModelMetric

logger = logging.getLogger(__name__)

@receiver(post_save, sender=ModelVersion)
def handle_model_version_save(sender, instance, created, **kwargs):
    """
    Signal handler for when a model version is saved.
    Updates the parent model's updated_at timestamp.
    """
    if created:
        logger.info(f"New model version created: {instance.model.name} v{instance.version}")
    else:
        logger.info(f"Model version updated: {instance.model.name} v{instance.version}")
    
    # Update the parent model's updated_at timestamp
    instance.model.save(update_fields=['updated_at'])

@receiver(post_delete, sender=ModelVersion)
def handle_model_version_delete(sender, instance, **kwargs):
    """
    Signal handler for when a model version is deleted.
    Updates the parent model's updated_at timestamp.
    """
    logger.info(f"Model version deleted: {instance.model.name} v{instance.version}")
    
    # Update the parent model's updated_at timestamp
    instance.model.save(update_fields=['updated_at'])

@receiver(post_save, sender=PredictionLog)
def handle_prediction_log_save(sender, instance, created, **kwargs):
    """
    Signal handler for when a prediction log is saved.
    Could be used for real-time monitoring or alerting.
    """
    if created:
        # This could be extended to implement real-time monitoring
        # For example, sending notifications if prediction time exceeds a threshold
        if instance.prediction_time > 1.0:  # More than 1 second
            logger.warning(
                f"Slow prediction detected for {instance.model_version}: "
                f"{instance.prediction_time:.2f} seconds"
            )

@receiver(post_save, sender=ModelMetric)
def handle_model_metric_save(sender, instance, created, **kwargs):
    """
    Signal handler for when a model metric is saved.
    Could be used for performance monitoring or drift detection.
    """
    if created:
        # This could be extended to implement performance monitoring
        # For example, sending alerts if a metric falls below a threshold
        logger.info(
            f"New metric recorded for {instance.model_version}: "
            f"{instance.metric_name} = {instance.metric_value}"
        )
