from django.contrib import admin
from .models import Reservation, ReservationOption


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass


@admin.register(ReservationOption)
class ReservationOptionAdmin(admin.ModelAdmin):
    pass
