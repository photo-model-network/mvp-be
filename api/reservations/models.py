from django.db import models
from shortuuid.django_fields import ShortUUIDField
from api.common.models import CommonModel
from api.packages.models import Package
from api.accounts.models import User


class Reservation(CommonModel):
    class ReservationStatus(models.TextChoices):
        PENDING = ("대기중", "Pending")
        CONFIRMED = ("확정", "Confirmed")
        CANCELED = ("취소", "Canceled")
        OPERATING = ("운행중", "Operating")
        DONE = ("서비스 완료", "Done")
        COMPLETE = ("결제 완료", "Complete")

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
    package_name = models.CharField(max_length=150, default="")
    package_price = models.PositiveIntegerField(default=0)
    reservation_date = models.DateField(null=True, blank=True)


class ReservationOption(CommonModel):
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="options"
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)


class ReservationTimeSlot(CommonModel):
    id = ShortUUIDField(max_length=128, primary_key=True, editable=False)
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)
    # 예약 가능한 날짜
    date = models.DateField()
    # 예약 가능 시작시간
    start_time = models.TimeField()
    # 예약 가능 종료시간
    end_time = models.TimeField()
    # 예약 가능 여부
    is_available = models.BooleanField(default=True)
