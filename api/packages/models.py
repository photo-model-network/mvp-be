from django.db import models
from shortuuid.django_fields import ShortUUIDField
from api.common.models import CommonModel


class PackageTag(CommonModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PackagePicture(CommonModel):
    package = models.ForeignKey("Package", on_delete=models.CASCADE)
    image = models.URLField()


class PackagePolicy(CommonModel):
    pass


class PackageOption(CommonModel):
    package = models.ForeignKey("Package", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    is_delivered = models.BooleanField(default=False)
    delivery_fee = models.PositiveIntegerField(default=0)


class Package(CommonModel):
    id = ShortUUIDField(max_length=128, primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    # 대표 이미지
    thumbnail = models.URLField()
    # 패키지 요약
    summary = models.TextField()
    # 패키지 내용
    content = models.TextField()
    # 검색용 태그; 역참조 시 tag.packages.all
    tags = models.ManyToManyField(PackageTag, related_name="packages")
