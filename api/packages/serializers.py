from api.packages.models import Package
from rest_framework.serializers import ModelSerializer


class PackageCUDSerializer(ModelSerializer):

    class Meta:
        model = Package
        fields = [
            "category",
            "provider",
            "provider_info",
            "title",
            "thumbnail",
            "region",
            "html_content",
            "policy",
            "tags",
        ]

    """
    validated_data에서 tags필드를 분리하여 tags 리스트를 가져올 때 사용.(보류)
    """


class PackageListSerializer(ModelSerializer):

    class Meta:
        model = Package
        fields = [
            "category",
            "provider",
            "provider_info",
            "title",
            "thumbnail",
            # "region",
            "summary",
        ]


class PackageDetailSerializer(ModelSerializer):

    class Meta:
        model = Package
        fields = [
            "category",
            "provider",
            "provider_info",
            "title",
            "thumbnail",
            # "region",
            "html_content",
            "policy",
        ]
