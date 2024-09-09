from rest_framework.permissions import BasePermission


class IsPackageProvider(BasePermission):
    """패키지 제공자인지 여부 체크"""

    def has_object_permission(self, request, view, obj):
        return obj.provider == request.user


class IsApprovedArtist(BasePermission):
    """요청을 보낸 사용자가 승인된 아티스트인지 여부 체크"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_approved
