from rest_framework import generics
from api.packages.models import Package
from api.packages.serializers import PackageSerializer

class PackageCreateView(generics.CreateAPIView):
    """
    new package 생성
    """
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

class PackageListView(generics.ListAPIView):
    """
    all packages 조회
    """
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

class PackageDetailView(generics.RetrieveAPIView):
    """
    package의 id 기준으로 package 조회
    """
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    

class PackageUpdateView(generics.UpdateAPIView):
    """
    package의 id 기준으로 package 수정
    """
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    

class PackageDeleteView(generics.DestroyAPIView):
    """
    package의 id 기준으로 package 삭제
    """
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    