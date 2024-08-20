from api.packages.models import Package
from api.packages.serializers import PackageCUDSerializer, PackageListSerializer, PackageDetailSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from api.packages.models import Package
from api.accounts.models import User

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


class ProviderPackagesListView(APIView):

    permission_classes = [IsAuthenticated]
    """
    /packages?user={userId} 요청을 받아서 해당 유저가 등록한 패키지들을 반환
    """
    def get(self, request, *args, **kwargs):
        provider_id = request.query_params.get('provider')
        if not provider_id:
            return Response({"error": "user parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            provider = User.objects.get(id=provider_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if not provider.is_approved:
            return Response({"error": "User is not approved"}, status=status.HTTP_403_FORBIDDEN)

        packages = Package.objects.filter(provider_id=provider_id)
        serializer = PackageListSerializer(packages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)