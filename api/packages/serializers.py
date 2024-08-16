from rest_framework import serializers
from api.packages.models import Package

class PackageCUDSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Package
        fields = ['category', 'provider', 'provider_info', 'title', 'thumbnail', 'location', 'summary', 'html_content', 'tags', 'policy']

class PackageListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Package
        fields = ['category', 'provider', 'provider_info', 'title', 'thumbnail', 'location', 'summary', 'tags']

class PackageDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Package
        fields = ['category', 'provider', 'provider_info', 'title', 'thumbnail', 'location', 'summary', 'html_content', 'policy']



