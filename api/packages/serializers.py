from api.packages.models import Package, PackagePicture
from rest_framework.serializers import ModelSerializer, ListField, URLField, ImageField
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
    tags = TagListSerializerField()


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
        package = super().create(validated_data)
        save_images(images, package)
        return package


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
            "html_content",
            "policy",
        ]



def save_images(images, package):
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