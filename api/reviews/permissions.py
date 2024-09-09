from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from api.packages.models import Package
from api.reservations.models import Reservation


class IsReviewAuthor(BasePermission):
    """리뷰 작성자 여부"""

    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user


class HasPurchased(BasePermission):

    def has_permission(self, request, view):

        package_id = view.kwargs.get("package_id")

        try:
            package = Package.objects.only("id").get(id=package_id)
        except Package.DoesNotExist:
            raise PermissionDenied("존재하지 않는 패키지입니다.")

        has_purchased = Reservation.objects.filter(
            package=package,
            customer=request.user,
        ).exists()

        # 만약 패키지를 구매하지 않았다면 False 반환
        if not has_purchased:
            raise PermissionDenied("리뷰를 작성하려면 패키지를 신청하셔야 합니다.")

        return True
