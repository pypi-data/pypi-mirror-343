from django.apps import AppConfig


class MLDjangoBrainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ml_django_brain'
    verbose_name = 'ML Django Brain'

    def ready(self):
        """
        Perform initialization tasks when the Django app is ready.
        This includes registering signals and initializing the model registry.
        """
        # Import signals
        import ml_django_brain.signals  # noqa

        # Initialize model registry
        from ml_django_brain.registry import ModelRegistry
        ModelRegistry()
