import shortuuid
from django.db import models
from taggit.models import GenericTaggedItemBase, TagBase
from taggit.managers import TaggableManager
from api.common.models import CommonModel
from api.accounts.models import User


class PackagePicture(CommonModel):
    """촬영 패키지 소개 이미지 (여러장)"""

    package = models.ForeignKey("Package", on_delete=models.CASCADE)
    original_url = models.ImageField()
    store_url = models.ImageField()

    class Meta:
        verbose_name = "패키지 소개 이미지"
        verbose_name_plural = "패키지 소개 이미지"


class PackagePolicy(CommonModel):
    """촬영 패키지 환불 및 A/S 정책"""

    class Meta:
        verbose_name = "패키지 정책"
        verbose_name_plural = "패키지 정책"


class PackageOption(CommonModel):
    """촬영 패키지 세부 옵션"""

    package = models.ForeignKey("Package", on_delete=models.CASCADE)
    # 옵션명
    name = models.CharField(max_length=200)
    # 옵션 구성 설명
    description = models.TextField()
    # 소요시간 (분)
    duration_time = models.PositiveIntegerField(default=0)
    # 금액
    price = models.PositiveIntegerField(default=0)
    # 인원 추가시 추가요금 (1인당 금액)
    additional_person_price = models.PositiveIntegerField(default=0)

    # 배송 여부
    # is_delivered = models.BooleanField(default=False)
    # 배송비
    # delivery_fee = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "패키지 옵션"
        verbose_name_plural = "패키지 옵션"


class PackageProvider(CommonModel):
    """촬영 패키지 제공자 정보"""

    # 문의 받을 이메일 (*필수)
    inquiry_email = models.EmailField(blank=False)
    # 문의 받을 전화번호 (*필수)
    inquiry_phone_number = models.CharField(max_length=20, blank=False)
    # 카카오톡 채널 (검색용 아이디)
    kakao_id = models.CharField(max_length=100, blank=True, null=True)
    # 카카오톡 채널 (홈페이지 URL)
    kakao_channel_url = models.URLField(blank=True, null=True)
    # 홈페이지 주소
    homepage_url = models.URLField(blank=True, null=True)
    # 페이스북 URL
    facebook_url = models.URLField(blank=True, null=True)
    # 트위터 URL
    twitter_url = models.URLField(blank=True, null=True)
    # 인스타그램 URL
    instagram_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "패키지 제공자 정보"
        verbose_name_plural = "패키지 제공자 정보"


class PackageTag(TagBase):

    class Meta:
        verbose_name = "패키지 검색용 태그"
        verbose_name_plural = "패키지 검색용 태그"


class PackageTaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(
        PackageTag,
        related_name="%(app_label)s_%(class)s_items",
        on_delete=models.CASCADE,
    )
    object_id = models.CharField(max_length=22, default=shortuuid.uuid, editable=False)

    def __str__(self):
        return f"{self.object_id} : [{self.tag}]"

    class Meta:
        verbose_name = "패키지 + 태그"
        verbose_name_plural = "패키지 + 태그"


class Package(CommonModel):
    """촬영 패키지"""

    class CategoryChoices(models.TextChoices):
        SEASON_PACKAGE = ("시즌패키지", "시즌패키지")
        OUTDOOR_SNAP = ("야외스냅", "야외스냅")
        WEDDING = ("웨딩", "웨딩")
        PROFILE = ("프로필", "프로필")
        BODY_PROFILE = ("바디프로필", "바디프로필")
        PET = ("반려동물", "반려동물")
        BASIC_SHOOTING = ("기본촬영대행", "기본촬영대행")

    id = models.CharField(
        max_length=22, default=shortuuid.uuid, primary_key=True, editable=False
    )
    # 패키지 카테고리
    category = models.CharField(
        max_length=20, choices=CategoryChoices.choices, default=CategoryChoices.PROFILE
    )
    # 패키지 제공자
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    # 패키지 제공자 정보 (SNS, 문의 이메일 등)
    provider_info = models.ForeignKey(PackageProvider, on_delete=models.CASCADE)
    # 패키지 제목
    title = models.CharField(max_length=255)
    # 대표 이미지
    thumbnail = models.ImageField()
    thumbnail_store_url = models.ImageField(blank=True, null=True)
    # 패키지 요약 (카드로 표시될 경우 간단히 보이는 글)
    summary = models.TextField()
    # 패키지 내용 (에디터로 작성한 글과 이미지)
    html_content = models.TextField()
    # 검색용 태그
    tags = TaggableManager(through=PackageTaggedItem)
    # 기본 정책 및 사용자 추가 정책
    policy = models.ForeignKey(PackagePolicy, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} : {self.provider}"

    class Meta:
        verbose_name = "패키지"
        verbose_name_plural = "패키지"

        ordering = ["-created_at"]
