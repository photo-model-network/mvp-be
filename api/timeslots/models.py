from django.db import models
from api.packages.models import Package


class UnavailableTimeSlot(models.Model):
    """패키지의 촬영 불가능한 시간대를 정의하는 모델"""

    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, related_name="unavaliable_timeslots"
    )

    # 예약 불가 시작 날짜/시간
    start_datetime = models.DateTimeField()
    # 예약 불가 종료 날짜/시간
    end_datetime = models.DateTimeField()

    def __str__(self):
        return f"{self.start_datetime} - {self.end_datetime} 예약 불가"

    class Meta:
        verbose_name = "예약 불가 날짜/시간 설정"
        verbose_name_plural = "예약 불가 날짜/시간 설정"

        unique_together = ("package", "start_datetime", "end_datetime")
