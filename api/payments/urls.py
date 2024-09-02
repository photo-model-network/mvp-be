from django.urls import path
from .views import PortOneWebhookView
from .views import PreparePaymentView

urlpatterns = [
    path("payments/webhook/", PortOneWebhookView.as_view(), name="portone_webhook"),
    path("payments/prepare/", PreparePaymentView.as_view(), name="payment_prepare"),
]
