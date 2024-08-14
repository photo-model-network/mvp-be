from django.db import models
from api.common.models import CommonModel
from api.accounts.models import User
from api.packages.models import Package
from shortuuid.django_fields import ShortUUIDField
class Reservation(CommonModel):
    class ReservationStatus(models.TextChoices):
        PENDING = ("대기중", "Pending")
        CONFIRMED = ("확정", "Confirmed")
        CANCELED = ("취소", "Canceled")
    id = ShortUUIDField(max_length=128, primary_key=True, editable=False)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="reservations")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations")
    status = models.CharField(max_length=15, default="대기중", choices=ReservationStatus.choices)
    package_name = models.CharField(max_length=150, default="")
    package_price = models.PositiveIntegerField(default=0)
    reservation_date = models.DateField(null=True, blank=True)


class ReservationOption(CommonModel):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name="options")
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)

