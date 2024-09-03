from api.reviews.models import Review
from rest_framework.serializers import ModelSerializer

class ReviewCRUDSerializer(ModelSerializer):

    class Meta:
        model = Review
        fields = ['package', 'customer', 'comment', 'rating']
        read_only_fields = ['package', 'customer']