from api.reviews.models import Review, ReviewPicture
from rest_framework.serializers import ModelSerializer
from api.core.utils import save_review_images

class ReviewPictureSerializer(ModelSerializer):

    class Meta:
        model = ReviewPicture
        fields = ['id', 'review', 'image']
        read_only_fields = ['review']

class ReviewCRUDSerializer(ModelSerializer):
    images = ReviewPictureSerializer(many=True, required=False)

    class Meta:
        model = Review
        fields = ['package', 'customer', 'comment', 'rating', 'images']
        read_only_fields = ['package', 'customer']
    
    def create(self, validated_data):
        images = validated_data.pop('images', None)
        review = super().create(validated_data)
        if images:
            save_review_images(images, review)
        return review