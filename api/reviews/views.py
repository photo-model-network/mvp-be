from api.reviews.models import Review
from api.packages.models import Package
from api.reviews.serializers import ReviewCRUDSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView


class ReviewCreateView(CreateAPIView):
    
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewCRUDSerializer

    def perform_create(self, serializer):
        package = Package.objects.get(id=self.kwargs['packages_id'])
        serializer.save(package=package, customer=self.request.user)


class ReviewListView(ListAPIView):
    
    permission_classes = [AllowAny]
    serializer_class = ReviewCRUDSerializer

    def get_queryset(self):
        package_id = self.kwargs['packages_id']
        return Review.objects.filter(package=package_id)


class ReviewUpdateView(UpdateAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewCRUDSerializer

    def get_queryset(self):
        return Review.objects.filter(customer=self.request.user)


class ReviewDeleteView(DestroyAPIView):
        
        permission_classes = [IsAuthenticated]
        serializer_class = ReviewCRUDSerializer

        def get_queryset(self):
            user = self.request.user
            if user.is_superuser:
                return Review.objects.all()
            return Review.objects.filter(customer=user)