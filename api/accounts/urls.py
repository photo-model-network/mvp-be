from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import GoogleView, NaverView, KakaoView
from .views import BankVerificationView, BusinessStatusView

urlpatterns = (
    [
        path(
            "accounts/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
        ),
        path(
            "accounts/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
        ),
    ]
    + [
        path("accounts/google/login/", GoogleView.as_view(), name="google_login"),
        path("accounts/naver/login/", NaverView.as_view(), name="naver_login"),
        path("accounts/kakao/login/", KakaoView.as_view(), name="kakao_login"),
    ]
    + [
        # 1원 계좌인증 (본인 계좌 등록)
        path(
            "accounts/bank/verify/", BankVerificationView.as_view(), name="bank_verify"
        ),
        # 국세청_사업자등록정보 상태조회
        path(
            "accounts/business/verify/", BusinessStatusView.as_view(), name="tax_verify"
        ),
    ]
)
