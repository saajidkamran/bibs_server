from django.apps import AppConfig


class BibsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bibs"

    def ready(self):
        import bibs.signal  # Import your signals module
