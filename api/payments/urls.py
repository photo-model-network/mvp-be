from django.urls import path
from .views import PortOneWebhookView

urlpatterns = [
    path("payments/webhook/", PortOneWebhookView.as_view(), name="portone_webhook"),
]
