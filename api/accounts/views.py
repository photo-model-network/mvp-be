import re
import requests
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from PublicDataReader import Nts
from .models import User

import logging

logger = logging.getLogger(__name__)


class GoogleView(APIView):
    """구글 소셜 연동 회원가입 및 로그인"""

    permission_classes = [AllowAny]

    def post(self, request):
        code = request.data.get("code")

        if not code:
            return Response(
                {"error": "code는 필수 항목입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # 1. 구글 OAuth2.0 토큰 발급
            token_response = self.get_google_token(code)
            token_json = token_response.json()
            access_token = token_json.get("access_token")

            if not access_token:
                logger.debug("토큰 발급에 실패하였습니다.")
                return Response(
                    {"error": "토큰 발급에 실패하였습니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 2. 구글 사용자 정보 가져오기
            user_data = self.get_google_user_data(access_token)
            email = user_data.get("email")

            if not email:
                logger.debug("이메일은 필수 항목입니다.")
                return Response(
                    {"error": "이메일은 필수 항목입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 3. 사용자 생성 또는 가져오기
            user = self.get_or_create_user(email, user_data)
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

    def get_google_token(self, code):
        """구글 OAuth2.0 토큰을 가져오는 헬퍼 함수"""
        return requests.post(
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

    def get_google_user_data(self, access_token):
        """구글 사용자 정보를 가져오는 헬퍼 함수"""
        response = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )
        return response.json()

    def get_or_create_user(self, email, user_data):
        """사용자를 생성하거나 가져오는 함수"""
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
        return user


class KakaoView(APIView):
    """카카오 소셜 연동 회원가입 및 로그인"""

    # 사업자번호를 등록해야 이메일 필드값을 받을 수 있어 추후 연동
    pass


class NaverView(APIView):
    """네이버 소셜 연동 회원가입 및 로그인"""

    permission_classes = [AllowAny]
    
    def post(self, request):

        code = request.data.get("code")
        state = request.data.get("state")

        if not code or not state:
            return Response(
                {"error": "code와 state는 필수 항목입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            token_response = self.get_naver_token(code, state)
            token_json = token_response.json()
            access_token = token_json.get("access_token")

            if not access_token:
                logger.error("토큰 발급에 실패하였습니다.")
                return Response(
                    {"error": "토큰 발급에 실패하였습니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user_data = self.get_naver_user_data(access_token)
            response = user_data.json().get("response")

            if not response:
                logger.debug("프로필 정보 조회에 실패하였습니다.")
                return Response(
                    {"error": "프로필 정보 조회에 실패하였습니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            email = response.get("email")

            if not email:
                logger.debug("이메일은 필수 항목입니다.")
                return Response(
                    {"error": "이메일은 필수 항목입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = self.get_or_create_user(email, response)
            refresh = RefreshToken.for_user(user)

            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)},
                status=status.HTTP_200_OK,
            )
        except requests.exceptions.RequestException as e:
            logger.debug("네트워크 오류가 발생했습니다.")
            return Response(
                {"error": "네트워크 오류가 발생했습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_naver_token(self, code, state):
        """네이버 토큰을 가져오는 헬퍼 함수"""
        return requests.post(
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

    def get_naver_user_data(self, access_token):
        """유저 프로필을 가져오는 함수"""
        return requests.get(
            "https://openapi.naver.com/v1/nid/me",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )

    def get_or_create_user(self, email, response):
        """유저를 생성하거나 가져오는 함수"""
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
        return user


# class LogoutView(APIView):

#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         logout(request)
#         return Response({"message": "로그아웃 성공!"}, status=status.HTTP_200_OK)


class SendBankVerificationView(APIView):

    permission_classes = [IsAuthenticated]
    # 하루 5번 호출가능
    throttle_classes = [UserRateThrottle]

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
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ConfirmBankVerificationView(APIView):

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


class BusinessStatusView(APIView): 

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        b_no = request.data.get('b_no')
        start_dt = request.data.get('start_dt')
        p_nm = request.data.get('p_nm')

        if not b_no or not start_dt or not p_nm:
            return Response({"error": "사업자등록번호, 설립일자, 대표자 이름 모두 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        nts = Nts(settings.NTS_API_KEY)
        try:
            # 상태조회 API 호출
            business = [{'b_no': f"{b_no}",     # 사업자등록번호
                         'start_dt': start_dt,  # 설립일자
                         'p_nm': p_nm}]         # 대표자명
            logger.debug(business)
            df = nts.validate(business)
            df_dict = df.to_dict(orient='records')
            logger.debug(df_dict)

            if not df_dict:
                return Response({"error": "NTS API로부터 유효한 응답을 받지 못했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            status_data = df_dict[0]
            if status_data['status.b_stt_cd'] == '01':  # 정상 사업자라 >> User 모델에 사업자번호 저장, is_business=True로 변경
                user = request.user
                user.business_license_number = b_no
                user.is_business = True
                user.save()
                return Response({"status": "사업자번호가 유효합니다.", "data": status_data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "사업자 번호가 유효하지 않습니다.", "data": status_data}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)