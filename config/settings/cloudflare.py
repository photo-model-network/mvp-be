"""
Cloudflare R2 스토리지 설정
"""

from decouple import config

AWS_S3_REGION_NAME = "auto"
CLOUDFLARE_R2_BUCKET_NAME = config("CLOUDFLARE_R2_BUCKET_NAME", cast=str)
CLOUDFLARE_R2_ACCESS = config("CLOUDFLARE_R2_ACCESS", cast=str)
CLOUDFLARE_R2_SECRET = config("CLOUDFLARE_R2_SECRET", cast=str)
CLOUDFLARE_R2_ENDPOINT = config("CLOUDFLARE_R2_ENDPOINT", cast=str)


CLOUDFLARE_R2_CONFIG_OPTIONS = {
    "bucket_name": CLOUDFLARE_R2_BUCKET_NAME,
    "access_key": CLOUDFLARE_R2_ACCESS,
    "secret_key": CLOUDFLARE_R2_SECRET,
    "endpoint_url": CLOUDFLARE_R2_ENDPOINT,
    "default_acl": "public-read",
    "signature_version": "s3v4",
}

STORAGES = {
    "default": {
        "BACKEND": "api.helpers.cloudflare.storages.MediaFileStorage",
        "OPTIONS": CLOUDFLARE_R2_CONFIG_OPTIONS,
    },
    "staticfiles": {
        "BACKEND": "api.helpers.cloudflare.storages.StaticFileStorage",
        "OPTIONS": CLOUDFLARE_R2_CONFIG_OPTIONS,
    },
}
