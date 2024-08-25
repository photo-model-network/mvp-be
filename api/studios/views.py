from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import StudioCRUDSerializer
from .pagination import StudioPagination
from .models import Studio

# class NearbyStudioView(APIView):

#     permission_classes = [AllowAny]

#     def get(self, request):
#         user_latitude = float(request.query_params.get("lat"))
#         user_longitude = float(request.query_params.get("lng"))
#         radius_km = float(request.query_params.get("radius", 10))
#         region = request.query_params.get("region", None)

#         nearby_studios = Studio.get_nearby_studios(
#             user_latitude, user_longitude, radius_km, region
#         )

#         paginator = StudioPagination()
#         paginated_studios = paginator.paginate_queryset(nearby_studios, request)
#         serializer = StudioCRUDSerializer(paginated_studios, many=True)

#         return paginator.get_paginated_response(serializer.data)


class StudioListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudioCRUDSerializer
    pagination_class = StudioPagination

    def get_queryset(self):
        user_latitude = self.request.query_params.get("lat", None)
        user_longitude = self.request.query_params.get("lng", None)
        radius_km = self.request.query_params.get("radius", None)
        region = self.request.query_params.get("region", None)

        if user_latitude is None or user_longitude is None or radius_km is None:
            # 위치 정보가 제공되지 않은 경우, 모든 스튜디오 반환
            return Studio.objects.all()
        else:
            # 위치 정보가 제공된 경우, 근처 스튜디오 검색
            user_latitude = float(user_latitude)
            user_longitude = float(user_longitude)
            radius_km = float(radius_km)
            return Studio.get_nearby_studios(
                user_latitude, user_longitude, radius_km, region
            )
