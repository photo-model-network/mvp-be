from rest_framework.permissions import BasePermission


class IsPackageProvider(BasePermission):
    """패키지 제공자인지 여부 체크"""

    def has_object_permission(self, request, view, obj):
        return obj.provider == request.user
