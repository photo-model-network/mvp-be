from rest_framework import serializers
from api.packages.models import Package

class PackageCUDSerializer(serializers.ModelSerializer):

    class Meta:
        model = Package
        fields = ['category', 'provider', 'provider_info', 'title', 'thumbnail', 'location', 'html_content', 'policy', 'tags']
    '''
    validated_data에서 tags필드를 분리하여 tags 리스트를 가져올 때 사용.(보류)
    '''

class PackageListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Package
        fields = ['category', 'provider', 'provider_info', 'title', 'thumbnail', 'location', 'summary']


class PackageDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Package
        fields = ['category', 'provider', 'provider_info', 'title', 'thumbnail', 'location', 'html_content', 'policy']
