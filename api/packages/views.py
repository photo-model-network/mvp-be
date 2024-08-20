from api.packages.models import Package
from api.packages.serializers import PackageCUDSerializer, PackageListSerializer, PackageDetailSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView

class PackageCreateView(generics.CreateAPIView):
    
    permission_classes = [IsAuthenticated]

    queryset = Package.objects.all()
    serializer_class = PackageCUDSerializer



class PackageListView(generics.ListAPIView):
    
    permission_classes = [AllowAny]
    """
    등록된 모든 packages 조회
    """
    queryset = Package.objects.all()
    serializer_class = PackageListSerializer


class PackageDetailView(generics.RetrieveAPIView):
    
    permission_classes = [AllowAny]
    """
    package의 id 기준으로 package 조회
    """
    queryset = Package.objects.all()
    serializer_class = PackageDetailSerializer

    

class PackageUpdateView(generics.UpdateAPIView):
    
    permission_classes = [IsAuthenticated]
    """
    package의 id 기준으로 package 수정
    """
    queryset = Package.objects.all()
    serializer_class = PackageCUDSerializer

    

class PackageDeleteView(generics.DestroyAPIView):
    
    permission_classes = [IsAuthenticated]
    """
    package의 id 기준으로 package 삭제
    """
    queryset = Package.objects.all()
    serializer_class = PackageCUDSerializer


    