from api.reviews.models import Review
from rest_framework.serializers import ModelSerializer
from api.core.utils import save_images

class ReviewCRUDSerializer(ModelSerializer):

    class Meta:
        model = Review
        fields = ['package', 'customer', 'comment', 'rating', 'images']
        read_only_fields = ['package', 'customer']
    
    def create(self, validated_data):
        images = validated_data.pop('images', None)
        review = super().create(validated_data)
        if images:
            save_images(images, review)
        return review