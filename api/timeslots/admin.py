from django.contrib import admin
from .models import UnavailableTimeSlot


@admin.register(UnavailableTimeSlot)
class UnavailableTimeSlotAdmin(admin.ModelAdmin):
    pass
