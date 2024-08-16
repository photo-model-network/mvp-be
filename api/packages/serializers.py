from rest_framework import serializers
from api.packages.models import Package

class PackageCUDSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Package
        fields = '__all__'
    '''
    validated_data에서 tags필드를 분리하여 tags 리스트를 가져올 때 사용.(보류)
    '''
    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        package = Package.objects.create(**validated_data)
        package.tags.set(tags)
        return package

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        instance = super().update(instance, validated_data)
        instance.tags.set(tags)
        return instance

class PackageListSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Package
        fields = '__all__'


class PackageDetailSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Package
        fields = '__all__'
