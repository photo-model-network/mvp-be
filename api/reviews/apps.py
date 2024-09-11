from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.reviews"

    def ready(self):
        import api.reviews.signals
