from django.db.models import Q
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from api.packages.models import Package
from api.studios.models import Studio

class CoreSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # core/search/?q={검색어}
        query = request.GET.get('q', '')
        if not query:
            return Response({"results": "검색어를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        package_results = Package.objects.filter(
            Q(title__icontains=query) |
            Q(summary__icontains=query) |
            Q(provider__username__icontains=query)
        ).select_related('provider')[:10]

        studio_results = Studio.objects.filter(
            Q(name__icontains=query) |
            Q(juso__icontains=query) |
            Q(owner__username__icontains=query)
        ).select_related('owner')[:10]

        results = {
            "packages": list(package_results.values('title', 'summary', 'provider__username')),
            "studios": list(studio_results.values('name', 'juso', 'owner__username')),
        }

        return Response({"results": results}, status=status.HTTP_200_OK)