from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from .views import GoogleView, NaverView, KakaoView
from .views import (
    SendBankVerificationView,
    ConfirmBankVerificationView,
    BusinessVerificationView,
    IdentityVerificationView,
)
from .views import RegisterView, LoginView, DeleteAccountView, ChangePasswordView
from .views import FavoriteArtistManageView, ListFavoriteArtistsView, CheckNameDuplicationView

urlpatterns = (
    [
        path(
            "accounts/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
        ),
        path(
            "accounts/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
        ),
        path("accounts/logout/", TokenBlacklistView.as_view(), name="logout"),
    ]
    + [
        path("accounts/google/login/", GoogleView.as_view(), name="google_login"),
        path("accounts/naver/login/", NaverView.as_view(), name="naver_login"),
        path("accounts/kakao/login/", KakaoView.as_view(), name="kakao_login"),
    ]
    + [
        # 계좌로 1원 전송 및 인증 코드 저장
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
        # 국세청 사업자등록정보 유효성검증
        path(
            "accounts/business/verify/",
            BusinessVerificationView.as_view(),
            name="business_verification",
        ),
        # 본인인증
        path(
            "accounts/identity/verify/",
            IdentityVerificationView.as_view(),
            name="identity_verification",
        ),
    ]
    + [  # 관심 아티스트 관련
        path(
            "accounts/favorite-artists/<str:artist_id>/",
            FavoriteArtistManageView.as_view(),
            name="favorite-artists",
        ),
        path(
            "accounts/favorite-artists/",
            ListFavoriteArtistsView.as_view(),
            name="list-favorite-artists",
        ),
    ]
    + [
        # 자체 로그인 및 회원 탈퇴
        path('accounts/register/', RegisterView.as_view(), name='register'),
        path('accounts/login/', LoginView.as_view(), name='login'),
        path('accounts/delete-account/', DeleteAccountView.as_view(), name='delete_account'),
        path('accounts/change-password/', ChangePasswordView.as_view(), name='change_password'),
        path('accounts/check-name-duplication/', CheckNameDuplicationView.as_view(), name='name_duplicate_check'),    
    ]
)
