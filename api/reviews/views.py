from api.reviews.models import Review
from api.reviews.serializers import ReviewCUDSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView

class ReviewCreateListView(CreateAPIView, ListAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewCUDSerializer

    def get_queryset(self):
        package_id = self.kwargs['packages_id']
        return Review.objects.filter(package=package_id)
    
    def perform_create(self, serializer):
        package_id = self.kwargs['packages_id']
        serializer.save(customer=self.request.user, package_id=package_id)


class ReviewUpdateDeleteView(UpdateAPIView, DestroyAPIView):
        
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewCUDSerializer
    lookup_field = 'id'