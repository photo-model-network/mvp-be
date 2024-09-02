from django.test import TestCase
from api.accounts.models import User
from api.packages.models import Package, PackageProvider, PackagePolicy
from api.reservations.models import Reservation, ReservationOption
import datetime


class ReservationTestCase(TestCase):

    def setUp(self):
        # 테스트용 사용자와 패키지 생성

        self.customer = User.objects.create(username="customer", password="testpass")

        self.provider = User.objects.create(username="provider", password="testpass")

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
            provider=self.provider,
            provider_info=self.provider_info,
            title="Test Package",
            thumbnail="http://example.com/thumbnail.jpg",
            summary="Test Summary",
            html_content="<p>Test Content</p>",
            policy=self.policy,
        )

        # 예약 생성
        self.reservation = Reservation.objects.create(
            package=self.package,
            customer=self.customer,
            filming_date=datetime.date.today(),
            filming_start_time=datetime.time(10, 0),
            additional_people=2,
        )

        # 옵션 생성
        self.option1 = ReservationOption.objects.create(
            reservation=self.reservation,
            name="Option 1",
            description="This is the first option",
            duration_time=60,
            price=200,
            additional_person_price=50,
        )

    def test_reservation_total_price(self):
        # 옵션과 추가 인원을 고려한 총 가격 계산
        total_price = self.reservation.calculate_total_price()
        self.assertEqual(total_price, 300)
