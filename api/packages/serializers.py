from api.packages.models import Package, PackagePicture
from rest_framework.serializers import ModelSerializer, ListField, URLField, ImageField
from rest_framework import serializers
from taggit.serializers import TagListSerializerField
from django.core.files.storage import default_storage
import os
import uuid


class PackageCUDSerializer(ModelSerializer):
    images = ListField(
        child=ImageField(),
        write_only=True,
    )
    thumbnail = ImageField(required=True)
    tags = TagListSerializerField(required=False)


    class Meta:
        model = Package
        fields = [
            "category",
            "provider",
            "provider_info",
            "title",
            "thumbnail",
            "html_content",
            "policy",
            "tags",
            "images",
        ]
       
    def create(self, validated_data):
        validated_data['provider'] = self.context.get('request').user
        images = validated_data.pop('images', None)
        thumbnail = validated_data.pop('thumbnail', None)
        tags = validated_data.pop('tags', [])
        tags_v = [t.strip() for t in tags[0].split(",") if t.strip()]
        
        package = super().create(validated_data)
        
        save_thumbnail(thumbnail, package)
        save_package_images(images, package)
        
        for tag in tags_v:
            package.tags.add(tag)
        return package


    """
    validated_data에서 tags필드를 분리하여 tags 리스트를 가져올 때 사용.(보류)
    """


class PackageListSerializer(ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Package
        fields = [
            "category",
            "provider",
            "provider_info",
            "title",
            "thumbnail",
            "summary",
            "average_rating",
        ]
        
    def get_average_rating(self, obj):
        return obj.average_rating()


class PackageDetailSerializer(ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Package
        fields = [
            "category",
            "provider",
            "provider_info",
            "title",
            "thumbnail",
            "html_content",
            "policy",
            "average_rating",
        ]

    def get_average_rating(self, obj):
        return obj.average_rating()
    

def save_package_images(images, package):
    if images:
        for image in images:
            original_filename = image.name
            ext = os.path.splitext(image.name)[1]  # 파일 확장자 추출
            unique_filename = f"{uuid.uuid4()}{ext}"  # 파일명 중복 방지를 위한 유니크한 파일명 생성
            default_storage.save(unique_filename, image)  # 파일 저장
            PackagePicture.objects.create(
                package = package,
                original_url = original_filename,
                store_url = unique_filename
            )
            
def save_thumbnail(thumbnail, package):
    if thumbnail:
        original_filename = thumbnail.name
        ext = os.path.splitext(thumbnail.name)[1]
        unique_filename = f"{uuid.uuid4()}{ext}"  # 파일명 중복 방지를 위한 유니크한 파일명 생성
        default_storage.save(unique_filename, thumbnail)  # 파일 저장
        package.thumbnail = original_filename
        package.thumbnail_store_url = unique_filename
        package.save()