from django.contrib import admin
from .models import Studio


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    pass
