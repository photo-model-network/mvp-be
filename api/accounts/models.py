from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField


class User(AbstractUser):

    class TypeChoices(models.TextChoices):
        INDIVIDUAL = ("개인", "개인")
        BUSINESS = ("개인사업자", "개인사업자")
        CORPORATE = ("법인사업자", "법인사업자")

    id = ShortUUIDField(max_length=128, primary_key=True, editable=False)
    name = models.CharField(max_length=100, default="익명의 사용자")
    avatar = models.URLField(
        default="https://cdn-icons-png.flaticon.com/512/149/149071.png", blank=True
    )
    # 한줄 소개
    bio = models.TextField(
        default="안녕하세요, 저의 프로필에 방문해주셔서 감사합니다.", blank=True
    )
    # 유저 타입
    type = models.CharField(
        max_length=10, choices=TypeChoices.choices, default=None, null=True, blank=False
    )

    # 아티스트 승인 여부
    is_approved = models.BooleanField(default=False)

    # 아티스트(기업)명
    artist_name = models.CharField(max_length=255, blank=True, null=True)
    # 관리자 명
    manager_name = models.CharField(max_length=255, blank=True, null=True)
    # 관리자 이메일
    manager_email = models.EmailField(blank=True, null=True)
    # 관리자 휴대폰 번호
    manager_phone_number = models.CharField(max_length=20, blank=True, null=True)

    def save(self, *args, **kwargs):
        # 아바타가 없을 경우 기본 이미지 저장
        if not self.avatar:
            self.avatar = "https://cdn-icons-png.flaticon.com/512/149/149071.png"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
