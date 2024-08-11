from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("accounts/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("accounts/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
