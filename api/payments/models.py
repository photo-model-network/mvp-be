from django.db import models
from api.common.models import CommonModel
from shortuuid.django_fields import ShortUUIDField

class Payment(CommonModel):

    class StatusChoices(models.TextChoices):
        CONFIRMED = ("confirmed", "Confirmed")
        CANCELLED = ("cancelled", "Cancelled")
        OPERATING = ("operating", "Operating")
        DONE = ("done", "Done")
        COMPLETE = ("complete", "Complete")

    id = ShortUUIDField(max_length=128, primary_key=True, editable=False)
    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE)
    # 결제 금액
    amount = models.PositiveIntegerField()
    # 결제일
    payment_date = models.DateTimeField()
    # 결제상태 (5가지로 구분)
    status = models.CharField(max_length=20, choices=StatusChoices)
    # 결제 방법 
    payment_method = models.CharField(max_length=20)

