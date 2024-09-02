from api.reviews.models import Review
from api.packages.models import Package
from api.reviews.serializers import ReviewCRUDSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.exceptions import PermissionDenied
from api.reservations.models import Reservation
from .permissions import IsReviewAuthor


class ReviewCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewCRUDSerializer

    def perform_create(self, serializer):
        package = Package.objects.only("id").get(id=self.kwargs["package_id"])

        has_purchased = Reservation.objects.filter(
            package=package,
            customer=self.request.user,
        ).exists()

        if not has_purchased:
            raise PermissionDenied("리뷰를 달기 위해서는 패키지를 신청하셔야 합니다.")

        serializer.save(package=package, customer=self.request.user)


class ReviewListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReviewCRUDSerializer

    def get_queryset(self):
        package_id = self.kwargs["package_id"]
        return Review.objects.filter(package__id=package_id)


class ReviewUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsReviewAuthor]
    serializer_class = ReviewCRUDSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Review.objects.none()

        return Review.objects.filter(
            package__id=self.kwargs["package_id"], customer=self.request.user
        )


class ReviewDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsReviewAuthor]
    serializer_class = ReviewCRUDSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Review.objects.none()

        return Review.objects.filter(
            package__id=self.kwargs["package_id"],
            customer=self.request.user,
            id=self.request.user,
        )
