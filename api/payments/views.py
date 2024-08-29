import uuid
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.reservations.models import Reservation
from standardwebhooks.webhooks import Webhook


WEBHOOK_TOLERANCE_IN_SECONDS = 10 * 60  # 허용 오차 범위 10분


class PortOneWebhookView(APIView):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):

        try:

            headers = {
                "webhook-id": request.headers.get("Webhook-Id"),
                "webhook-signature": request.headers.get("Webhook-Signature"),
                "webhook-timestamp": request.headers.get("Webhook-Timestamp"),
            }

            webhook = Webhook(settings.PORTONE_WEBHOOK)

            try:
                payload = webhook.verify(data=request.body, headers=headers)
            except Exception as e:
                return Response(
                    {"error": f"시그니처 검증에 실패하였습니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            event_type = payload.get("type")
            data = payload.get("data", {})

            payment_id = data.get("paymentId")
            reservation = Reservation.objects.filter(payment_id=payment_id).first()

            if not reservation:
                return Response(
                    {"error": "해당 paymentId와 일치하는 예약이 없습니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if event_type == "Transaction.Paid":
                if (
                    reservation.status == reservation.ReservationStatus.CONFIRMED
                    and reservation.payment_status == Reservation.PaymentStatus.PENDING
                ):
                    reservation.payment_status = (
                        Reservation.PaymentStatus.SHIPPING_REGISTERED
                    )
                    reservation.save()
                else:
                    return Response(
                        {"message": "예약상태 혹은 결제상태를 확인해주세요."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            return Response(
                {"message": "성공적으로 결제 상태가 업데이트 되었습니다."},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PreparePaymentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            reservation_id = request.data.get("reservationId")
            reservation = get_object_or_404(
                Reservation, id=reservation_id, customer=request.user
            )

            if reservation.payment_status != reservation.PaymentStatus.PENDING:
                return Response(
                    {"message": "이미 결제 처리된 예약입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # paymentId 생성
            payment_id = str(uuid.uuid4())

            # 예약에 paymentId 저장
            reservation.payment_id = payment_id
            reservation.save()

            return Response({"paymentId": payment_id}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
