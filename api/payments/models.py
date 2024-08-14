from django.db import models
from api.common.models import CommonModel
from shortuuid.django_fields import ShortUUIDField

class Payment(CommonModel):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('operating', 'Operating'),
        ('done', 'Done'),
        ('complete', 'Complete'),
    ]
    id = ShortUUIDField(max_length=128, primary_key=True, editable=False)
    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    status = models.CharField(max_length=20, cboices=STATUS_CHOICES)
    payment_method = models.CharField(max_length=20)

class ReservationTimeSlot(CommonModel):
    id = ShortUUIDField(max_length=128, primary_key=True, editable=False)
    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)