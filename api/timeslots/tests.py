from django.test import TestCase
from datetime import time, date
from api.packages.models import Package, PackageProvider, PackagePolicy
from api.accounts.models import User
from .models import UnavailableTimeSlot
from .utils import get_available_times


class TimeSlotTestCase(TestCase):
    def setUp(self):
        # 테스트용 유저 생성
        self.user = User.objects.create(username="testuser", password="testpass")

        # 테스트용 패키지 제공자
        self.provider_info = PackageProvider.objects.create(
            inquiry_email="provider@example.com",
            inquiry_phone_number="010-1234-5678",
            kakao_id="kakao_provider",
            kakao_channel_url="http://example.com/kakao",
            homepage_url="http://example.com",
            facebook_url="http://facebook.com/provider",
            twitter_url="http://twitter.com/provider",
            instagram_url="http://instagram.com/provider",
        )

        # 테스트용 정책
        self.policy = PackagePolicy.objects.create()

        # 테스트용 패키지
        self.package = Package.objects.create(
            category=Package.CategoryChoices.PROFILE,
            provider=self.user,
            provider_info=self.provider_info,
            title="Test Package",
            thumbnail="http://example.com/thumbnail.jpg",
            location=Package.LocationChoices.SEOUL,
            summary="Test Summary",
            html_content="<p>Test Content</p>",
            policy=self.policy,
        )

        # 예약 불가 시간 설정
        UnavailableTimeSlot.objects.create(
            package=self.package,
            date=date(2023, 8, 14),
            start_time=time(15, 0),
            end_time=time(17, 12),
        )

    def test_time_available(self):
        # 예약 가능한 시간 조회
        print(get_available_times(self.package, date(2023, 8, 14)))
