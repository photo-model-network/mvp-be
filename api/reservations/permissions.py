from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from api.packages.models import Package
from api.reservations.models import Reservation


class IsReservationPackageProvider(BasePermission):
    """
    예약을 확정할 수 있는 권한이 있는지 확인하는 퍼미션.
    예약 패키지의 제공자가 현재 요청한 사용자와 동일한지 체크.
    """

    def has_object_permission(self, request, view, obj):

        if obj.package.provider == request.user:
            return True
        raise PermissionDenied("예약을 확정할 권한이 없습니다.")
