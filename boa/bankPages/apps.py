from django.apps import AppConfig


class bankPagesConfig(AppConfig):  # Replace with your actual app name
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bankPages'  # Replace with your actual app name

    def ready(self):
        import bankPages.signals  # Import signals when the app is ready