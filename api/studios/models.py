from django.db import models
from haversine import haversine, Unit
from shortuuid.django_fields import ShortUUIDField
from api.common.models import CommonModel
from api.accounts.models import User


class Studio(CommonModel):

    class RegionChoices(models.TextChoices):
        GYEONGGI = ("경기", "경기")
        BUSAN = ("부산", "부산")
        SEOUL = ("서울", "서울")
        INCHEON = ("인천", "인천")
        DAEGU = ("대구", "대구")
        GWANGJU = ("광주", "광주")
        DAEJEON = ("대전", "대전")
        ULSAN = ("울산", "울산")
        SEJONG = ("세종", "세종")
        GANGWON = ("강원", "강원")
        CHUNGBUK = ("충북", "충북")
        CHUNGNAM = ("충남", "충남")
        JEONBUK = ("전북", "전북")
        JEONNAM = ("전남", "전남")
        GYEONGBUK = ("경북", "경북")
        GYEONGNAM = ("경남", "경남")
        JEJU = ("제주", "제주")

    id = ShortUUIDField(primary_key=True, editable=False)
    # 관리자
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # 스튜디오 이름
    name = models.CharField(max_length=100)
    # 스튜디오 지역
    region = models.CharField(
        max_length=2, choices=RegionChoices.choices, default=RegionChoices.SEOUL
    )
    # 도로명 주소
    juso = models.TextField()
    # 우편번호
    postal_code = models.CharField(max_length=5)
    # 스튜디오 위치 위도
    latitude = models.FloatField(blank=True, null=True, default=None)
    # 스튜디오 위치 경도
    longitude = models.FloatField(blank=True, null=True, default=None)

    # 유저와 스튜디오와의 거리 계산
    def distance_to(self, user_latitude, user_longitude):
        if self.latitude is not None and self.longitude is not None:
            studio_coordinate = (self.latitude, self.longitude)
            user_coordinate = (user_latitude, user_longitude)
            return haversine(studio_coordinate, user_coordinate, unit=Unit.KILOMETERS)
        return None

    @staticmethod
    def get_nearby_studios(user_latitude, user_longitude, radius_km, region=None):
        studios = Studio.objects.all()

        if region:
            studios = studios.filter(region=region)

        nearby_studios = [
            studio
            for studio in studios
            if studio.distance_to(user_latitude, user_longitude) is not None
            and studio.distance_to(user_latitude, user_longitude) <= radius_km
        ]

        return nearby_studios

    class Meta:
        verbose_name = "스튜디오"
        verbose_name_plural = "스튜디오"
