from datetime import datetime, timedelta, time
from .models import UnavailableTimeSlot


def get_available_times(package, check_date):
    """특정 날짜에 예약 가능한 시간대를 동적으로 계산하는 함수"""
    start_time = time(10, 0)  # 오전 8시
    end_time = time(20, 0)  # 오후 7시 30분 (오후 8시)
    available_times = []

    current_time = start_time
    while current_time < end_time:
        # 해당 시간대가 예약 불가 시간에 포함되지 않는지 확인
        if not UnavailableTimeSlot.objects.filter(
            package=package,
            date=check_date,
            start_time__lte=current_time,
            end_time__gt=current_time,
        ).exists():
            available_times.append(current_time)

        current_time = (
            datetime.combine(datetime.today(), current_time) + timedelta(minutes=30)
        ).time()

    return available_times
