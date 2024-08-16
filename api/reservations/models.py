import datetime
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from api.common.models import CommonModel
from api.packages.models import Package
from api.accounts.models import User


class Reservation(CommonModel):
    class ReservationStatus(models.TextChoices):
        PENDING = ("대기중", "대기중")
        CONFIRMED = ("예약확정", "예약확정")
        CANCELED = ("예약취소", "예약취소")
        OPERATING = ("작업중", "작업중")
        DONE = ("작업완료", "작업완료")
        COMPLETE = ("구매확정", "구매확정")

    id = ShortUUIDField(max_length=128, primary_key=True, editable=False)
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, related_name="reservations"
    )
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reservations"
    )
    status = models.CharField(
        max_length=15,
        default=ReservationStatus.PENDING,
        choices=ReservationStatus.choices,
    )

    # 요청사항
    request = models.TextField(blank=True, null=True)

    # 예약 당시 패키지 제목
    package_title = models.CharField(max_length=150, blank=True, null=True)

    # 촬영 날짜
    filming_date = models.DateField()
    # 촬영 시작 시간
    filming_start_time = models.TimeField()

    def save(self, *args, **kwargs):
        if not self.package_title:
            self.package_title = self.package.title

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "예약"
        verbose_name_plural = "예약"


class ReservationOption(CommonModel):
    """예약 당시 옵션 정보"""

    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="options"
    )
    # 예약 당시 옵션명
    name = models.CharField(max_length=200)
    # 예약 당시 구성 설명
    description = models.TextField()
    # 예약 당시 가격
    price = models.PositiveIntegerField(default=0)
    # 예약 당시 배송 여부
    is_delivered = models.BooleanField(default=False)
    # 예약 당시 배송비
    delivery_fee = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "예약 당시 옵션"
        verbose_name_plural = "예약 당시 옵션"
