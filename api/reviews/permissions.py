from rest_framework.permissions import BasePermission


class IsReviewAuthor(BasePermission):
    """리뷰 작성자 여부"""

    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user
