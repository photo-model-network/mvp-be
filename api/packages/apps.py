from django.apps import AppConfig


class PackagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.packages"

    def ready(self):
        import api.packages.signals
