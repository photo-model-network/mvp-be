from django.core.management.base import BaseCommand
from django.utils import timezone
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken


# 운영환경에서 등록하여 사용 (예시 : 오전 3시에 만료된 토큰 삭제)
# 0 3 * * * /project/path/env/bin/python /project/path/manage.py delete_expired
# python manage.py delete_expired 명령어로 실행
class Command(BaseCommand):
    help = "만료된 토큰 삭제"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_tokens = OutstandingToken.objects.filter(expires_at__lt=now)
        count, _ = expired_tokens.delete()
        self.stdout.write(
            self.style.SUCCESS(f"{count}개의 만료된 토큰이 삭제되었습니다.")
        )
