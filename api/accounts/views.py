import requests
from django.conf import settings
from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

import logging

logger = logging.getLogger(__name__)


class GoogleView(APIView):
    """구글 소셜 연동 회원가입 및 로그인"""

    permission_classes = [AllowAny]

    def post(self, request):
        try:
            code = request.data.get("code")

            logger.debug(f"구글 로그인 code: {code}")

            token_response = requests.post(
                "https://oauth2.googleapis.com/token",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data={
                    "grant_type": "authorization_code",
                    "client_id": settings.GOOGLE_CLIENT,
                    "client_secret": settings.GOOGLE_SECRET,
                    "redirect_uri": settings.SOCIAL_CALLBACK_URI,
                    "code": code,
                },
            )

            token_json = token_response.json()
            access_token = token_json.get("access_token")

            logger.debug(f"구글 로그인 access_token: {access_token}")

            if not access_token:
                return Response(
                    {"error": "토큰 발급에 실패하였습니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user_data_response = requests.get(
                "https://www.googleapis.com/oauth2/v1/userinfo",
                headers={
                    "Authorization": f"Bearer {access_token}",
                },
            )
            user_data = user_data_response.json()
            email = user_data.get("email")

            logger.debug(f"구글 로그인 email: {email}")

            if not email:
                return Response(
                    {"error": "이메일은 필수 항목입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                user = User.objects.get(username=email)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=email,
                    email=email,
                    name=email.split("@")[0],
                    avatar=user_data.get("picture"),
                )
                user.set_unusable_password()
                user.save()

            refresh = RefreshToken.for_user(user)

            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class KakaoView(APIView):
    """카카오 소셜 연동 회원가입 및 로그인"""

    # 사업자번호를 등록해야 이메일 필드값을 받을 수 있어 추후 연동
    pass


class NaverView(APIView):
    """네이버 소셜 연동 회원가입 및 로그인"""

    permission_classes = [AllowAny]

    def post(self, request):
        try:

            code = request.data.get("code")
            state = request.data.get("state")

            logger.debug(f"네이버 로그인 code: {code}")
            logger.debug(f"네이버 로그인 state: {state}")

            token_response = requests.post(
                "https://nid.naver.com/oauth2.0/token",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data={
                    "grant_type": "authorization_code",
                    "client_id": settings.NAVER_CLIENT,
                    "client_secret": settings.NAVER_SECRET,
                    "redirect_uri": settings.SOCIAL_CALLBACK_URI,
                    "code": code,
                    "state": state,
                },
            )

            token_json = token_response.json()
            access_token = token_json.get("access_token")
            logger.debug(f"네이버 로그인 access_token: {access_token}")

            if not access_token:
                return Response(
                    {"error": "토큰 발급에 실패하였습니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user_data_response = requests.get(
                "https://openapi.naver.com/v1/nid/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                },
            )

            user_data = user_data_response.json()
            response = user_data.get("response", {"프로필 정보 조회에 실패하였습니다."})
            email = response.get("email")

            logger.debug(f"네이버 로그인 email: {email}")

            if not email:
                return Response(
                    {"error": "이메일은 필수 항목입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                user = User.objects.get(username=email)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=email,
                    email=email,
                    avatar=response.get("profile_image"),
                    name=(
                        response.get("nickname")
                        if response.get("nickname") is not None
                        else response.get("name")
                    ),
                )
                user.set_unusable_password()
                user.save()

            refresh = RefreshToken.for_user(user)

            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "로그아웃 성공!"}, status=status.HTTP_200_OK)
