import os, uuid
from django.core.files.storage import default_storage
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ListField, URLField, ImageField
from taggit.serializers import TagListSerializerField
from api.packages.models import Package, PackagePicture


def save_images(images, package):
    image_objects = []
    for image in images:
        ext = os.path.splitext(image.name)[1]
        new_filename = os.path.join(
            f"packages/{package.id}/images", f"{uuid.uuid4()}{ext}"
        )
        default_storage.save(new_filename, image)
        image_objects.append(PackagePicture(package=package, image=new_filename))
    PackagePicture.objects.bulk_create(image_objects)


def save_thumbnail(thumbnail, package):
    ext = os.path.splitext(thumbnail.name)[1]
    new_filename = os.path.join(
        f"packages/{package.id}/thumbnail", f"{uuid.uuid4()}{ext}"
    )
    default_storage.save(new_filename, thumbnail)
    package.thumbnail = new_filename
    package.save()


class PackageCUDSerializer(ModelSerializer):
    images = ListField(child=ImageField(), write_only=True, required=True)
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
            "images",
            "html_content",
            "policy",
            "tags",
        ]

    def create(self, validated_data):

        images = validated_data.pop("images", None)
        thumbnail = validated_data.pop("thumbnail", None)
        tags = validated_data.pop("tags", [])

        # 나머지 데이터를 이용해 패키지 생성
        package = super().create(validated_data)

        # 태그 처리
        if tags:
            tag_list = [tag.strip() for tag in tags[0].split(",") if tag.strip()]
            package.tags.add(*tag_list)

        # 썸네일 저장 처리 (필요하다면 별도의 함수로 처리)
        if thumbnail:
            save_thumbnail(thumbnail, package)

        # 이미지 저장 처리 (필요하다면 별도의 함수로 처리)
        if images:
            save_images(images, package)

        return package


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
            "average_rating",
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
            "average_rating",
        ]
