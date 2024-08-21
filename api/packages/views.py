from api.packages.models import Package
from api.packages.serializers import PackageCUDSerializer, PackageListSerializer, PackageDetailSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from api.packages.models import Package


class PackageCreateView(CreateAPIView):
    
    permission_classes = [IsAuthenticated]

    queryset = Package.objects.all()
    serializer_class = PackageCUDSerializer



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
        filter_param = self.request.query_params.get("filter", None)

        if user_id is not None:
            return Package.objects.filter(provider__id=user_id)
        
        if filter_param == "recent":
            return Package.objects.order_by('-created_at')[:10]
        
        return Package.objects.all()
    


class PackageDetailView(RetrieveAPIView):
    
    permission_classes = [AllowAny]
    """
    package의 id 기준으로 package 조회
    """
    queryset = Package.objects.all()
    serializer_class = PackageDetailSerializer

    

class PackageUpdateView(UpdateAPIView):
    
    permission_classes = [IsAuthenticated]
    """
    package의 id 기준으로 package 수정
    """
    queryset = Package.objects.all()
    serializer_class = PackageCUDSerializer

    

class PackageDeleteView(DestroyAPIView):
    
    permission_classes = [IsAuthenticated]
    """
    package의 id 기준으로 package 삭제
    """
    queryset = Package.objects.all()
    serializer_class = PackageCUDSerializer
