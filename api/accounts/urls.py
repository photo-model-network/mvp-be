from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import GoogleView, NaverView, KakaoView

urlpatterns = [
    path("accounts/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("accounts/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] + [
    path("accounts/google/login/", GoogleView.as_view(), name="google_login"),
    path("accounts/naver/login/", NaverView.as_view(), name="naver_login"),
    path("accounts/kakao/login/", KakaoView.as_view(), name="kakao_login"),
]
