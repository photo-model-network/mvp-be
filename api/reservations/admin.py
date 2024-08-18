from django.contrib import admin
from .models import Reservation, ReservationOption


class ReservationOptionInline(admin.TabularInline):
    model = ReservationOption
    extra = 0


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "customer",
        "status",
        "filming_date",
        "filming_start_time",
        "created_at",
    ]

    # 예약 상태, 결제 상태로 필터링 가능
    list_filter = ["status", "payment_status"]
    # 고유아이디, 고객 이메일, 패키지 이름으로 필터링 검색 가능
    search_fields = ["id", "customer__username", "package__title"]
    inlines = [ReservationOptionInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # 성능 최적화를 위해 prefetch_related 사용
        queryset = queryset.prefetch_related("options")
        return queryset


@admin.register(ReservationOption)
class ReservationOptionAdmin(admin.ModelAdmin):
    list_display = ["reservation", "name", "created_at"]
