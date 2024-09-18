from storages.backends.s3 import S3Storage
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


class StaticFileStorage(S3Storage):
    """api.helpers.cloudflare.storages.StaticFileStorage"""

    location = "static"


class MediaFileStorage(S3Storage):
    """api.helpers.cloudflare.storages.MediaFileStorage"""

    location = "uploads"

    # 프론트에서 압축하여 전송하는것으로 대체
    # def _save(self, name, content):
    #     # 이미지 파일인 경우에만 처리
    #     if "image" in content.content_type:
    #         image = Image.open(content)

    #         # 파일 포맷 확인 (JPEG는 품질 조정, PNG는 최적화)
    #         image_format = image.format if image.format else "JPEG"

    #         # 새로운 이미지 파일을 바이트 버퍼에 저장 (JPEG 품질 85로 압축 또는 PNG 최적화)
    #         buffer = BytesIO()
    #         if image_format == "JPEG":
    #             # JPEG의 경우, 품질을 85로 설정해 압축
    #             image.save(buffer, format="JPEG", quality=85, optimize=True)
    #         elif image_format == "PNG":
    #             # PNG의 경우 최적화 적용
    #             image.save(buffer, format="PNG", optimize=True)
    #         else:
    #             # 다른 포맷일 경우 원본 포맷 유지
    #             image.save(buffer, format=image_format)

    #         # content를 압축된 이미지로 덮어씌우기
    #         content = ContentFile(buffer.getvalue(), name)

    #     # S3에 저장 (부모 클래스의 _save 호출)
    #     return super()._save(name, content)
