from django.db import models
from api.packages.models import Package


class UnavailableTimeSlot(models.Model):
    """패키지의 예약 불가능한 시간대를 정의하는 모델"""

    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, related_name="unavaliable_timeslots"
    )
    # 예약 불가 날짜
    date = models.DateField()
    # 예약 불가 시작 시각
    start_time = models.TimeField()
    # 예약 불가 종료 시각
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.date} {self.start_time} - {self.end_time} 예약 불가"

    class Meta:
        verbose_name = "예약 불가 날짜/시간 설정"
        verbose_name_plural = "예약 불가 날짜/시간 설정"

        unique_together = ("package", "date", "start_time", "end_time")
