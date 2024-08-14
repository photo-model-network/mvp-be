from django.contrib import admin
from .models import Reservation, ReservationOption, ReservationTimeSlot


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass


@admin.register(ReservationOption)
class ReservationOptionAdmin(admin.ModelAdmin):
    pass


@admin.register(ReservationTimeSlot)
class ReservationTimeSlotAdmin(admin.ModelAdmin):
    pass
