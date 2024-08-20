from api.reviews.models import Review
from api.reviews.serializers import ReviewCUDSerializer, ReviewListSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

class ReviewCreateView(CreateAPIView):
    
    permission_classes = [IsAuthenticated]

    queryset = Review.objects.all()
    serializer_class = ReviewCUDSerializer


class ReviewListView(ListAPIView):
    
    permission_classes = [AllowAny]
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer


class ReviewDetailView(RetrieveAPIView):
    
    permission_classes = [AllowAny]
    queryset = Review.objects.all()
    serializer_class = ReviewCUDSerializer


class ReviewUpdateView(UpdateAPIView):
        
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewCUDSerializer
    lookup_field = 'id'


class ReviewDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewCUDSerializer
    lookup_field = 'id'