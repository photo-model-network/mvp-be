import base64, hashlib, hmac, json
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.reservations.models import Reservation

WEBHOOK_TOLERANCE_IN_SECONDS = 10 * 60  # 허용 오차 범위 10분


# class WebhookVerificationError(Exception):
#     pass


# class PortOneWebhookView(APIView):
#     @csrf_exempt
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def post(self, request):
#         try:

#             # 헤더 검증
#             msg_id = self.get_header(request, "Webhook-Id")
#             msg_signature = self.get_header(request, "Webhook-Signature")
#             msg_timestamp = self.get_header(request, "Webhook-Timestamp")

#             print(msg_id, msg_signature, msg_timestamp)

#             # 타임스탬프 검증
#             self.verify_timestamp(msg_timestamp)

#             print("타임스탬프 이후")

#             # 시그니처 생성 및 검증
#             expected_signature = self.sign(msg_id, msg_timestamp, request.data)
#             print("생성된 사인", expected_signature)

#             print("사인 이후")

#             if not self.verify_signature(msg_signature, expected_signature):
#                 raise WebhookVerificationError("일치하는 시그니처가 없습니다.")

#             print("시그니처 검증")

#             payload = request.data
#             event_type = payload.get("type")
#             data = payload.get("data", {})

#             payment_id = data.get("paymentId")

#             reservation = Reservation.objects.filter(payment_id=payment_id).first()
#             if not reservation:
#                 return Response(
#                     {"error": "해당 paymentId와 일치하는 예약이 없습니다."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             if event_type == "Transaction.Paid":
#                 """결제(예약 결제 포함)가 승인되었을 때 (모든 결제 수단)"""
#                 reservation.payment_status = (
#                     Reservation.PaymentStatus.SHIPPING_REGISTERED
#                 )
#                 reservation.save()
#             elif event_type == "Transaction.Cancelled":
#                 """결제가 완전 취소되었을 때"""
#                 reservation.payment_status = Reservation.PaymentStatus.CANCELLED
#                 reservation.save()

#             return Response(
#                 {"message": "성공적으로 결제 상태가 업데이트 되었습니다."},
#                 status=status.HTTP_200_OK,
#             )

#         except WebhookVerificationError as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#     def get_header(self, request, header_name):
#         value = request.headers.get(header_name)
#         if not value:
#             raise WebhookVerificationError("필수 헤더가 누락되었습니다.")
#         return value

#     def verify_timestamp(self, timestamp) -> None:
#         print("verify 타임스탬프")
#         now = timezone.now()
#         now_timestamp = now.timestamp()

#         # Unix 타임스탬프를 float으로 변환
#         webhook_timestamp = float(timestamp)

#         # 타임스탬프 검증
#         if now_timestamp - webhook_timestamp > WEBHOOK_TOLERANCE_IN_SECONDS:
#             raise WebhookVerificationError("TIMESTAMP_TOO_OLD")
#         if webhook_timestamp > now_timestamp + WEBHOOK_TOLERANCE_IN_SECONDS:
#             raise WebhookVerificationError("TIMESTAMP_TOO_NEW")

#     def sign(self, msg_id, msg_timestamp, payload):

#         message = f"{msg_id}.{msg_timestamp}.{json.dumps(payload, separators=(',', ':'), ensure_ascii=False)}"

#         print(message)
#         signature = hmac.new(
#             settings.PORTONE_WEBHOOK.encode("utf-8"),
#             message.encode("utf-8"),
#             hashlib.sha256,
#         ).digest()
#         signature_encoded = base64.b64encode(signature).decode()

#         return signature_encoded

#     def verify_signature(self, received_signature, expected_signature):
#         print("사인 검증 함수 내부")
#         for versioned_signature in received_signature.split(" "):
#             parts = versioned_signature.split(",", 1)
#             if len(parts) == 2 and parts[0] == "v1":
#                 received_signature_decoded = base64.b64decode(parts[1])
#                 expected_signature_decoded = base64.b64decode(expected_signature)
#                 if hmac.compare_digest(
#                     received_signature_decoded, expected_signature_decoded
#                 ):
#                     return True
#         return False


class WebhookVerificationError(Exception):
    pass


class PortOneWebhookView(APIView):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        try:
            # 헤더 검증

            print(f"{settings.PORTONE_WEBHOOK}")

            msg_id = self.get_header(request, "Webhook-Id")
            msg_signature = self.get_header(request, "Webhook-Signature")
            msg_timestamp = self.get_header(request, "Webhook-Timestamp")

            print(msg_id, msg_signature, msg_timestamp)

            print("원래 키", msg_signature)
            # 타임스탬프 검증
            self.verify_timestamp(msg_timestamp)
            print("타임스탬프 이후")

            # 시그니처 생성 및 검증
            expected_signature = self.sign(msg_id, msg_timestamp, request.data)
            print("생성된 사인", expected_signature)
            print("사인 이후")

            # if not self.verify_signature(msg_signature, expected_signature):
            #     raise WebhookVerificationError("일치하는 시그니처가 없습니다.")

            print("시그니처 검증")

            payload = request.data

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
                print("결제가 완료되었습니다.")
                reservation.payment_status = (
                    Reservation.PaymentStatus.SHIPPING_REGISTERED
                )
                reservation.save()
            elif event_type == "Transaction.Cancelled":
                print("결제가 취소되었습니다.")
                reservation.payment_status = Reservation.PaymentStatus.CANCELLED
                reservation.save()

            return Response(
                {"message": "성공적으로 결제 상태가 업데이트 되었습니다."},
                status=status.HTTP_200_OK,
            )

        except WebhookVerificationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_header(self, request, header_name):
        value = request.headers.get(header_name)
        if not value:
            raise WebhookVerificationError("필수 헤더가 누락되었습니다.")
        return value

    def verify_timestamp(self, timestamp) -> None:
        print("verify 타임스탬프")
        now = timezone.now()
        now_timestamp = now.timestamp()

        webhook_timestamp = float(timestamp)

        if now_timestamp - webhook_timestamp > WEBHOOK_TOLERANCE_IN_SECONDS:
            raise WebhookVerificationError("TIMESTAMP_TOO_OLD")
        if webhook_timestamp > now_timestamp + WEBHOOK_TOLERANCE_IN_SECONDS:
            raise WebhookVerificationError("TIMESTAMP_TOO_NEW")

    def sign(self, msg_id, msg_timestamp, payload):
        message = f"{msg_id}.{msg_timestamp}.{json.dumps(payload, separators=(',', ':'), ensure_ascii=False)}"
        print(f"Message to sign: {message}")

        signature = hmac.new(
            settings.PORTONE_WEBHOOK.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256,
        ).digest()
        signature_encoded = base64.b64encode(signature).decode()

        return signature_encoded

    def verify_signature(self, received_signature, expected_signature):
        print("사인 검증 함수 내부")
        print()
