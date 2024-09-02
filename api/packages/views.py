from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from api.packages.models import Package
from api.packages.serializers import (
    PackageCUDSerializer,
    PackageListSerializer,
    PackageDetailSerializer,
)
from .permissions import IsPackageProvider, IsApprovedArtist


class PackageCreateView(CreateAPIView):

    permission_classes = [IsAuthenticated, IsApprovedArtist]
    serializer_class = PackageCUDSerializer

    def perform_create(self, serializer):            
        serializer.save()


class PackageListView(ListAPIView):

    permission_classes = [AllowAny]
    """
    등록된 모든 packages 조회 / packages/?page=숫자로 페이지네이션 가능
    """
    queryset = Package.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = PackageListSerializer

    def get_queryset(self):
        """
        등록된 모든 packages 조회 후
        user 쿼리 파라미터가 있는 경우 해당 유저가 등록한 패키지들을 반환
        """
        user_id = self.request.query_params.get("user", None)
        category = self.request.query_params.get("category", None)
        filter_param = self.request.query_params.get("filter", None)

        queryset = Package.objects.select_related(
            "provider", "provider_info", "policy"
        ).prefetch_related("tags")

        # /packages/?user={유저아이디} 또는 {유저네임(이메일)}
        if user_id is not None:
            queryset = queryset.filter(
                Q(provider__id=user_id) | Q(provider__username=user_id)
            )

        # /packages/?category={카테고리명}
        if category is not None:
            queryset = queryset.filter(category=category)

        # /packages/?filter=recent
        if filter_param == "recent":
            queryset = queryset.order_by("-created_at")[:10]

        return queryset


class PackageDetailView(RetrieveAPIView):
    """
    package의 id 기준으로 package 조회
    """

    permission_classes = [AllowAny]

    queryset = Package.objects.all()
    serializer_class = PackageDetailSerializer


class PackageUpdateView(UpdateAPIView):
    """
    package의 id 기준으로 package 수정
    """

    permission_classes = [IsAuthenticated, IsPackageProvider]

    queryset = Package.objects.all()
    serializer_class = PackageCUDSerializer


class PackageDeleteView(DestroyAPIView):
    """
    package의 id 기준으로 package 삭제
    """

    permission_classes = [IsAuthenticated, IsPackageProvider]

    queryset = Package.objects.all()
    serializer_class = PackageCUDSerializer
