from django.contrib import admin
from .models import UnavailableTimeSlot


@admin.register(UnavailableTimeSlot)
class UnavailableTimeSlotAdmin(admin.ModelAdmin):
    list_display = ["package", "start_datetime", "end_datetime"]
