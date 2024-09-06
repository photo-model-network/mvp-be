import requests
from datetime import timedelta, datetime
from django.conf import settings
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.packages.models import Package, PackageOption
from api.accounts.models import User
from api.timeslots.models import UnavailableTimeSlot
from .serializers import RequestReservationSerializer, PayReservationSerializer
from .models import Reservation, ReservationOption
from .permissions import IsReservationPackageProvider

import logging

logger = logging.getLogger(__name__)


class RequestReservationView(APIView):
    """구매자가 예약 신청"""

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=RequestReservationSerializer)
    def post(self, request):

        serializer = RequestReservationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        package_id = serializer.validated_data["packageId"]
        filming_date = serializer.validated_data["filmingDate"]
        filming_start_time = serializer.validated_data["filmingStartTime"]
        selected_option_id = serializer.validated_data["selectedOption"]

        # package_id = request.data.get("packageId")
        # customer_id = request.user.id

        # filming_date = request.data.get("filmingDate")
        # filming_start_time = request.data.get("filmingStartTime")
        # selected_option_id = request.data.get("selectedOption")

        try:

            package = get_object_or_404(Package, id=package_id)
            customer = get_object_or_404(User, id=request.user.id)
            selected_option = get_object_or_404(
                PackageOption, id=selected_option_id, package=package
            )

            # filming_date와 filming_start_time을 결합하여 datetime 객체로 변환
            start_datetime_naive = datetime.combine(filming_date, filming_start_time)

            # 타임존을 한국 표준시(KST)로 변환
            start_datetime = settings.KST.localize(start_datetime_naive)

            # 소요 시간 계산
            total_duration = timedelta(minutes=selected_option.duration_time)
            end_datetime = start_datetime + total_duration

            logger.debug(f"촬영 시작 시간: {start_datetime}")
            logger.debug(f"촬영 종료 시간: {end_datetime}")

            # 예약 가능한 시간대인지 확인
            unavailable_timeslots = UnavailableTimeSlot.objects.filter(
                package=package,
                start_datetime__lt=end_datetime,
                end_datetime__gt=start_datetime,
            )
            if unavailable_timeslots.exists():
                available_options = PackageOption.objects.filter(
                    package=package
                ).exclude(id=selected_option_id)
                valid_options = [
                    option
                    for option in available_options
                    if not unavailable_timeslots.filter(
                        start_datetime__lt=start_datetime
                        + timedelta(minutes=option.duration_time),
                        end_datetime__gt=start_datetime,
                    ).exists()
                ]

                if valid_options:
                    options_info = ", ".join(
                        [
                            f"{option.name} (소요 시간: {option.duration_time}분)"
                            for option in valid_options
                        ]
                    )
                    return Response(
                        {
                            "error": "해당 시간대는 예약 불가능한 시간대입니다.",
                            "availableOptions": options_info,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    return Response(
                        {"error": "해당 시간대에 가능한 옵션이 없습니다."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:

                reservation = Reservation.objects.create(
                    package=package,
                    customer=customer,
                    filming_date=filming_date,
                    filming_start_time=filming_start_time,
                )
                ReservationOption.objects.create(
                    reservation=reservation,
                    name=selected_option.name,
                    description=selected_option.description,
                    duration_time=selected_option.duration_time,
                    price=selected_option.price,
                    additional_person_price=selected_option.additional_person_price,
                )
                UnavailableTimeSlot.objects.create(
                    package=reservation.package,
                    start_datetime=start_datetime,
                    end_datetime=end_datetime,
                )
                return Response(
                    {"message": "예약 신청이 완료되었습니다."},
                    status=status.HTTP_200_OK,
                )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ConfirmReservationView(APIView):
    """(판매자가 들어온 예약을 확인하여) 예약 확정"""

    permission_classes = [IsAuthenticated, IsReservationPackageProvider]

    def post(self, request, reservation_id):
        reservation = get_object_or_404(Reservation, id=reservation_id)

        self.check_object_permissions(request, reservation)

        # if not request.user == reservation.package.provider:
        #     return Response(
        #         {"message": "예약을 확정할 권한이 없습니다."},
        #         status=status.HTTP_403_FORBIDDEN,
        #     )

        if reservation.status == reservation.ReservationStatus.PENDING:
            reservation.confirm()
            return Response(
                {"message": "예약 확정이 완료되었습니다."}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "요청된 예약이 '대기중' 상태가 아닙니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PayReservationView(APIView):
    """구매자가 확정된 예약을 결제(검증)"""

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=PayReservationSerializer)
    def post(self, request):
        try:

            serializer = PayReservationSerializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            payment_id = serializer.validated_data["paymentId"]
            # payment_id = request.data.get("paymentId")

            # if not payment_id:
            #     return Response(
            #         {"error": "paymentId는 필수 항목입니다."},
            #         status=status.HTTP_400_BAD_REQUEST,
            #     )

            reservation = get_object_or_404(
                Reservation, payment_id=payment_id, customer=request.user
            )

            if reservation.payment_status != Reservation.PaymentStatus.PENDING:
                return Response(
                    {"message": "결제가 이미 처리(결제 성공)되었습니다."},
                    status=status.HTTP_200_OK,
                )

            # 결제 정보 조회 시도
            try:
                response = requests.get(
                    f"https://api.portone.io/payments/{payment_id}",
                    headers={"Authorization": f"PortOne {settings.PORTONE_SECRET}"},
                )
            except requests.exceptions.RequestException:
                return Response(
                    {
                        "message": "네트워크 오류로 인해 결제 상태를 확인할 수 없습니다. 결제 완료 후 상태가 자동으로 업데이트됩니다.",
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            response_data = response.json()

            if reservation.status != reservation.ReservationStatus.CONFIRMED:
                return Response(
                    {"error": "예약이 확정되지 않았습니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if reservation.calculate_total_price() != response_data["amount"]["total"]:
                return Response(
                    {"error": "결제 금액이 일치하지 않습니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if reservation.payment_status == Reservation.PaymentStatus.PAID:
                return Response(
                    {"message": "이미 결제가 처리되었습니다."},
                    status=status.HTTP_200_OK,
                )

            reservation.payment_status = reservation.PaymentStatus.PAID
            reservation.save()

            return Response(
                {"message": "결제가 성공적으로 처리되었습니다."},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
