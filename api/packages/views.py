from api.packages.models import Package
from api.packages.serializers import PackageCUDSerializer, PackageListSerializer, PackageDetailSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

class PackageCreateView(CreateAPIView):
    
    permission_classes = [IsAuthenticated]

    queryset = Package.objects.all()
    serializer_class = PackageCUDSerializer



class PackageListView(ListAPIView):
    
    permission_classes = [AllowAny]
    """
    등록된 모든 packages 조회
    """
    queryset = Package.objects.all()
    serializer_class = PackageListSerializer


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