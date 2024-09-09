import re
import json
import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from .throttles import SendBankVerificationThrottle
from .serializers import GoogleSerializer, KakaoSerializer, NaverSerializer, BusinessVerificationSerializer, LoginSerializer, RegisterSerializer
from .models import User

import logging

logger = logging.getLogger(__name__)

class RegisterView(APIView):
    """자체 회원가입"""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입에 성공했습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CustomLoginView(APIView):
    """자체 로그인"""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.context.get('user')
            login(request, user)
            return Response({
                "message": "로그인에 성공했습니다.",
                "user": serializer.get_user(user)
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteAccountView(APIView):
    """자체로그인 계정 삭제"""

    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        logout(request)
        return Response({"message": "회원 탈퇴가 완료되었습니다."}, status=status.HTTP_200_OK)
    

class GoogleView(APIView):
    """구글 소셜 연동 회원가입 및 로그인"""

    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=GoogleSerializer)
    def post(self, request):

        serializer = GoogleSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        code = serializer.validated_data["code"]

        logger.debug(f"구글 로그인 code: {code}")

        try:

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

            if not email:
                return Response(
                    {"error": "이메일은 필수 항목입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user, created = User.objects.get_or_create(
                username=email,
                defaults={
                    "email": email,
                    "name": email.split("@")[0],
                    "avatar": user_data.get("picture"),
                },
            )

            if created:
                user.set_unusable_password()
                user.save()

            refresh = RefreshToken.for_user(user)

            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)},
                status=status.HTTP_200_OK,
            )

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": "네트워크 오류가 발생했습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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

    @swagger_auto_schema(request_body=NaverSerializer)
    def post(self, request):

        serializer = NaverSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        code = serializer.validated_data["code"]
        state = serializer.validated_data["state"]

        logger.debug(f"네이버 로그인 code: {code}")
        logger.debug(f"네이버 로그인 state: {state}")

        try:

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

            if not email:
                return Response(
                    {"error": "이메일은 필수 항목입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user, created = User.objects.get_or_create(
                username=email,
                defaults={
                    "email": email,
                    "avatar": response.get("profile_image"),
                    "name": response.get("nickname") or response.get("name"),
                },
            )

            if created:
                user.set_unusable_password()
                user.save()

            refresh = RefreshToken.for_user(user)

            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)},
                status=status.HTTP_200_OK,
            )

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": "네트워크 오류가 발생했습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class RegisterView(APIView):
#     def post(self, request):

#         username = request.data.get("username")
#         password = request.data.get("password")
#         name = request.data.get("name")

#         if not username or not password or not name:
#             return Response(
#                 {"error": "모든 필드를 입력해야 합니다."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # 중복 사용자명 확인
#         if User.objects.filter(username=username).exists():
#             return Response(
#                 {"error": "이미 사용중인 아이디입니다."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         try:

#             user = User.objects.create(
#                 username=username,
#                 email=username,
#                 name=name,
#                 password=make_password(password),
#             )

#             user.save()

#             return Response(
#                 {"message": "회원가입이 성공적으로 완료되었습니다."},
#                 status=status.HTTP_201_CREATED,
#             )
#         except Exception as e:
#             return Response(
#                 {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )


class SendBankVerificationView(APIView):
    """계좌로 1원 전송 및 인증 코드 저장"""

    permission_classes = [IsAuthenticated]
    throttle_classes = [SendBankVerificationThrottle]

    def post(self, request):

        # 은행 계좌번호
        bank_account = request.data.get("bankAccount")
        # 은행 코드
        bank_code = request.data.get("bankCode")

        if not bank_account or not bank_code:
            return Response(
                {"message": "은행 계좌번호와 인증 코드를 필수 항목입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            response = requests.post(
                "https://apick.app/rest/transfer_1won",
                headers={
                    "CL_AUTH_KEY": settings.APICK_SECRET,
                },
                data={
                    "account_num": bank_account,
                    "bank_code": bank_code,
                },
            )

            if response.status_code == 200:

                response_data = response.json()

                bank_verification_code = re.search(
                    r"\d+", response_data["data"]["입금통장메모"]
                ).group()

                logger.debug(
                    f"은행 계좌 인증 추출 코드 bank_verification_code: {bank_verification_code}"
                )

                user = request.user

                user.bank_verification_code = bank_verification_code
                user.bank_account = response_data["data"]["계좌번호"]
                user.bank_code = response_data["data"]["은행코드"]
                user.save(
                    update_fields=[
                        "bank_verification_code",
                        "bank_account",
                        "bank_code",
                    ]
                )

                return Response(
                    {"message": "1원이 전송되었습니다. 인증 코드를 입력해 주세요."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "계좌 인증 요청이 실패했습니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": "네트워크 오류가 발생했습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ConfirmBankVerificationView(APIView):
    """계좌로 전송된 인증 코드 일치 여부 확인"""

    permission_classes = [IsAuthenticated]

    def post(self, request):

        bank_account = request.data.get("bankAccount")
        bank_verification_code = request.data.get("bankVerificationCode")

        if not bank_account or not bank_verification_code:
            return Response(
                {"message": "은행 계좌번호와 인증 코드를 필수 항목입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            user = User.objects.get(
                id=request.user.id, bank_account=bank_account, bank_verified=False
            )

            if user.bank_verification_code == bank_verification_code:
                user.bank_verified = True
                user.save(update_fields=["bank_verified"])

                return Response(
                    {"message": "계좌 등록이 성공적으로 완료되었습니다."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "인증 코드가 일치하지 않습니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except User.DoesNotExist:
            return Response(
                {"message": "해당 계좌 인증 정보를 찾을 수 없습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )


class BusinessVerificationView(APIView):
    """국세청 사업자등록정보 유효성검증"""
    
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=BusinessVerificationSerializer)
    def post(self, request):
        
        serializer = BusinessVerificationSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        business_num = serializer.validated_data["businessNum"]

        try:
            response = requests.post(
                f"https://api.odcloud.kr/api/nts-businessman/v1/status?serviceKey={settings.NTS_SECRET}",
                headers={
                    "Content-Type": "application/json",
                },
                data=json.dumps(
                    {
                        "b_no": [business_num],
                    }
                ),
            )
            response_data = response.json()

            if response.status_code == 200 and response_data.get("status_code") == "OK":
                business_info = response_data.get("data", [])[0]
                logger.debug(f"사업자등록정보: {business_info}")
                
                if business_info.get("b_stt_cd") == "01":
                    user = request.user
                    user.business_license_number = business_num
                    user.save()
                    return Response({"message": "사업자 인증이 성공적으로 완료되었습니다."}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "유효하지 않은 사업자등록번호입니다."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "사업자 인증에 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)

        except requests.exceptions.RequestException:
            return Response(
                {"error": "네트워크 오류가 발생했습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class IdentityVerificationView(APIView):
    """본인인증"""

    def post(self, request):

        # 본인인증 api 구현

        return Response(
            {"message": "본인인증이 성공적으로 완료되었습니다."},
            status=status.HTTP_200_OK,
        )



class FavoriteArtistManageView(APIView):
    """관심 아티스트 등록 및 해제"""
    permission_classes = [IsAuthenticated]

    def post(self, request, artist_id):
        user = request.user
        artist = get_object_or_404(User, id=artist_id, is_approved=True)

        if artist == user:
            return Response({"detail": "자신을 관심 아티스트로 등록할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        if artist in user.favorite_artists.all():
            user.favorite_artists.remove(artist)
            return Response({"detail": "관심 아티스트에서 해제되었습니다."}, status=status.HTTP_200_OK)
        else:
            user.favorite_artists.add(artist)
            return Response({"detail": "관심 아티스트로 등록되었습니다."}, status=status.HTTP_200_OK)

class ListFavoriteArtistsView(APIView):
    """관심 아티스트 리스트 조회"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        favorite_artists = user.favorite_artists.all()
        data = [{"id": artist.id, "name": artist.name, "email": artist.email} for artist in favorite_artists]
        return Response(data, status=status.HTTP_200_OK)