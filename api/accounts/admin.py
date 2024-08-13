from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            "일반 유저 필드",
            {
                "fields": (
                    "username",
                    "name",
                    "avatar",
                    "bio",
                    "type",
                    "is_approved",
                ),
            },
        ),
        (
            "아티스트 필드",
            {
                "fields": (
                    "real_name",
                    "phone_number",
                    "is_authenticated",
                    "business_license_number",
                    "is_business",
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Important Dates",
            {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
            },
        ),
    )

    list_display = ["username", "is_approved", "type", "real_name"]
