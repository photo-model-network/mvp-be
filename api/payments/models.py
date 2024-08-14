from django.db import models
from api.common.models import CommonModel
from shortuuid.django_fields import ShortUUIDField
from api.reservations.models import Reservation


class Payment(CommonModel):

    class StatusChoices(models.TextChoices):
        # 1 결제가 이루어졌지만 아직 승인되지 않은 상태
        PENDING = ("대기중", "대기중")
        # 2 결제 금액이 에스크로 계좌에 보류된 상태
        ESCROW_HOLD = ("에스크로 홀드", "에스크로 홀드")
        # 3 상품이나 서비스가 제공된 후 에스크로에서 판매자에게 결제가 승인된 상태
        ESCROW_RELEASED = ("에스크로 릴리스", "에스크로 릴리스")
        # 4 거래가 실패하거나 취소되어 에스크로에서 금액이 환불된 상태
        ESCROW_REFUNDED = ("에스크로 환불", "에스크로 환불")
        # 5 결제가 완료되고 모든 과정이 종료된 상태
        COMPLETED = ("결제완료", "결제완료")
        # 6 결제가 취소된 상태
        CANCELED = ("결제취소", "결제취소")

    id = ShortUUIDField(max_length=128, primary_key=True, editable=False)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    # 결제 금액
    amount = models.PositiveIntegerField()
    # 결제일
    payment_date = models.DateTimeField()
    # 결제상태 (6가지)
    status = models.CharField(
        max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )
    # 결제 방법
    payment_method = models.CharField(max_length=20)
