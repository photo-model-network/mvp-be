import os, uuid, shortuuid
import requests
from django.db import models
from django.core.files.base import ContentFile
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField



def save_user_avatar(instance, filename):
    ext = filename.split(".")[-1]
    new_filename = f"{shortuuid.uuid()}.{ext}"
    return os.path.join(f"users/{instance.id}/avatar", new_filename)


class User(AbstractUser):

    class TypeChoices(models.TextChoices):
        INDIVIDUAL = ("개인", "개인")
        BUSINESS = ("개인사업자", "개인사업자")
        CORPORATE = ("법인사업자", "법인사업자")

    id = ShortUUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=100, unique=True)
    avatar = models.ImageField(upload_to=save_user_avatar, blank=True)
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

    # 실명(기업명)
    real_name = models.CharField(max_length=255, blank=True, null=True)
    # 본인 휴대폰 번호
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    # 본인 인증 여부 (로그인 여부 X)
    is_identified = models.BooleanField(default=False)

    # 은행 계좌번호
    bank_account = models.CharField(max_length=20, blank=True, null=True)
    # 은행 코드
    bank_code = models.CharField(max_length=3, blank=True, null=True)
    # 1원 인증 코드
    bank_verification_code = models.CharField(max_length=4, blank=True, null=True)
    # 은행 계좌 인증 여부
    bank_verified = models.BooleanField(default=False)

    # 사업자 등록 번호
    business_license_number = models.CharField(max_length=30, blank=True, null=True)
    # 사업자 여부
    is_business = models.BooleanField(default=False)

    # 스튜디오 보유 여부
    has_studio = models.BooleanField(default=False)

    # 관심 아티스트
    favorite_artists = models.ManyToManyField(
        "self", symmetrical=False, related_name="favorited_by", blank=True
    )

    def save(self, *args, **kwargs):
        # 아바타가 없을 경우 기본 이미지 저장
        if not self.avatar:
            response = requests.get(
                "https://cdn-icons-png.flaticon.com/512/149/149071.png"
            )
            if response.status_code == 200:
                # ContentFile에 다운로드한 이미지를 저장한 뒤, 아바타 필드에 저장
                self.avatar.save(
                    "default_avatar.png", ContentFile(response.content), save=False
                )
        # 유니크한 이름 생성
        if not self.name:
            if '@' in self.username:
                local_part, domain_part = self.username.split('@')
                domain_part = domain_part.split('.')[0]
                base_name = f"{local_part}-{domain_part}"
            else:
                base_name = "익명의 사용자"
            
            unique_name = base_name
            while User.objects.filter(name=unique_name).exists():
                unique_name = f"{base_name}_{uuid.uuid4().hex[:8]}"
            self.name = unique_name
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username