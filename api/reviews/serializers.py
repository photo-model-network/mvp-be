from api.reviews.models import Review
from rest_framework.serializers import ModelSerializer

class ReviewCUDSerializer(ModelSerializer):

    class Meta:
        model = Review
        fields = ['package', 'customer', 'comment']