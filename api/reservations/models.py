from django.db import models
from api.common.models import CommonModel
from shortuuid.django_fields import ShortUUIDField

class ReservationTimeSlot(CommonModel):
    id = ShortUUIDField(max_length=128, primary_key=True, editable=False)
    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE)
    # 예약 가능한 날짜
    date = models.DateField()
    # 예약 가능 시작시간
    start_time = models.TimeField()
    # 예약 가능 종료시간
    end_time = models.TimeField()
    # 예약 가능 여부
    is_available = models.BooleanField(default=True)