from django.urls import path
from .views import RequestReservationView, ConfirmReservationView, PayReservationView


urlpatterns = [
    # 구매자가 예약 요청
    path("reservations/", RequestReservationView.as_view(), name="reservation_request"),
    path("reservations/pay/", PayReservationView.as_view(), name="reservation_pay"),
    # (판매자가 들어온 예약을 확인하여) 예약 확정
    path(
        "reservations/<str:reservation_id>/confirm/",
        ConfirmReservationView.as_view(),
        name="reservation_confirm",
    ),
]
