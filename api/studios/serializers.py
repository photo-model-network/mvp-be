from rest_framework.serializers import ModelSerializer
from .models import Studio


# 임시
class StudioCRUDSerializer(ModelSerializer):
    class Meta:
        model = Studio
        fields = "__all__"
