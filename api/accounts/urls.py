from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import GoogleView, NaverView, KakaoView
from .views import SendBankVerificationView, ConfirmBankVerificationView, BusinessStatusView

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
        # 1원 전송 및 인증 코드 저장
        path(
            "accounts/bank/verification/send/",
            SendBankVerificationView.as_view(),
            name="bank_verification_send",
        ),
        # 인증 코드 일치 여부 확인
        path(
            "accounts/bank/verification/confirm/",
            ConfirmBankVerificationView.as_view(),
            name="bank_verification_confirm",
        ),
        # 국세청_사업자등록정보 상태조회
        path(
            "accounts/business/verify/", BusinessStatusView.as_view(), name="tax_verify"
        ),
    ]
)
