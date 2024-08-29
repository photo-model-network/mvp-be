from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            "일반",
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
            "아티스트",
            {
                "fields": (
                    "real_name",
                    "phone_number",
                    "is_identified",
                    "business_license_number",
                    "is_business",
                ),
            },
        ),
        (
            "은행 계좌",
            {
                "fields": (
                    "bank_account",
                    "bank_code",
                    "bank_verification_code",
                    "bank_verified",
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

    actions = ["make_business", "remove_business"]

    # 선택된 사용자들을 사업자로 변경하는 액션
    def make_business(self, request, queryset):
        queryset.update(is_business=True)

    make_business.short_description = "선택된 사용자들을 사업자로 설정"

    # 선택된 사용자들의 사업자 여부를 해제하는 액션
    def remove_business(self, request, queryset):
        queryset.update(is_business=False)

    remove_business.short_description = "선택된 사용자들의 사업자 여부 해제"
