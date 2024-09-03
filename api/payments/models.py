import uuid
from django.db import models
from api.common.models import CommonModel


class AbstractPayment(CommonModel):

    class PaymentStatus(models.TextChoices):

        # 입금이 안된 상태
        PENDING = ("대기중", "대기중")

        PAID = ("입금완료", "입금완료")

        # 2 배송등록 단계: 상품이 발송되고 배송이 등록된 상태
        SHIPPING_REGISTERED = ("배송등록", "배송등록")

        # 3 구매결정 단계: 구매자가 상품을 수령하고 구매를 확정한 상태
        PURCHASE_DECIDED = ("구매결정", "구매결정")

        # 4 대금지급 단계: 구매결정 후 에스크로에서 판매자에게 결제가 승인된 상태
        ESCROW_RELEASED = ("에스크로 릴리스", "에스크로 릴리스")

        # 5 결제가 완료되고 모든 과정이 종료된 상태
        COMPLETED = ("결제완료", "결제완료")

        # 6 거래가 실패하거나 취소되어 에스크로에서 금액이 환불된 상태
        ESCROW_REFUNDED = ("에스크로 환불", "에스크로 환불")

        # 7 결제가 취소된 상태
        CANCELED = ("결제취소", "결제취소")

    # 고유 결제 ID
    payment_id = models.UUIDField(
        max_length=128, default=uuid.uuid4, editable=False, unique=True
    )
    # 결제 금액
    payment_amount = models.PositiveIntegerField(default=0)
    # 결제일
    payment_date = models.DateTimeField(blank=True, null=True)
    # 결제상태 (6가지)
    payment_status = models.CharField(
        max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )

    class Meta:
        abstract = True
