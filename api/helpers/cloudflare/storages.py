from storages.backends.s3 import S3Storage


class StaticFileStorage(S3Storage):
    """api.helpers.cloudflare.storages.StaticFileStorage"""

    location = "static"


class MediaFileStorage(S3Storage):
    """api.helpers.cloudflare.storages.MediaFileStorage"""

    location = "uploads"
