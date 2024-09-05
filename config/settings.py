"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from decouple import config
from pytz import timezone


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

ENV = config("ENV", default="development")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("DJANGO_SECRET", cast=str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = ["*"]
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "https://*",
]

site_domain = config("RAILWAY_PUBLIC_DOMAIN", default="")

CSRF_TRUSTED_ORIGINS = [
    f"https://{site_domain}",
]

X_FRAME_OPTIONS = "DENY"

APPEND_SLASH = True
# Application definition

INSTALLED_APPS = [
    "daphne",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "drf_yasg",
    "taggit",
]

CUSTOM_APPS = [
    "api.common",
    "api.core",
    "api.accounts",
    "api.studios",
    "api.payments",
    "api.reservations",
    "api.packages",
    "api.reviews",
    "api.timeslots",
    "api.chats",
    "api",
]

INSTALLED_APPS += CUSTOM_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
# if ENV == "production":
#     import dj_database_url

#     DATABASES["default"] = dj_database_url.parse(config("DATABASE_URL", cast=str))

#     CHANNEL_LAYERS = {
#         "default": {
#             "BACKEND": "channels_redis.core.RedisChannelLayer",
#             "CONFIG": {"hosts": config("REDIS_URL", cast=str)},
#         },
#     }

#     CELERY_BROKER_URL = config("REDIS_URL", cast=str)
# CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True

KST = timezone(TIME_ZONE)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
# STATICFILES_DIRS = [BASE_DIR / "static"]
# STATIC_ROOT = BASE_DIR / "staticfiles"

# if not DEBUG:
#     STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# MEDIA_ROOT = BASE_DIR / "uploads"
# MEDIA_URL = "/uploads/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTH_USER_MODEL = "accounts.User"

# 소셜 연동 설정
NAVER_CLIENT = config("NAVER_CLIENT", cast=str)
NAVER_SECRET = config("NAVER_SECRET", cast=str)

GOOGLE_CLIENT = config("GOOGLE_CLIENT", cast=str)
GOOGLE_SECRET = config("GOOGLE_SECRET", cast=str)
SOCIAL_CALLBACK_URI = config("SOCIAL_CALLBACK_URI", cast=str)

PORTONE_SECRET = config("PORTONE_SECRET", cast=str)
PORTONE_WEBHOOK = config("PORTONE_WEBHOOK", cast=str)

APICK_SECRET = config("APICK_SECRET", cast=str)

NTS_SECRET = config("NTS_SECRET", cast=str)


# AWS_S3_REGION_NAME = "auto"
# CLOUDFLARE_R2_BUCKET_NAME = config("CLOUDFLARE_R2_BUCKET_NAME", cast=str)
# CLOUDFLARE_R2_ACCESS = config("CLOUDFLARE_R2_ACCESS", cast=str)
# CLOUDFLARE_R2_SECRET = config("CLOUDFLARE_R2_SECRET", cast=str)
# CLOUDFLARE_R2_ENDPOINT = config("CLOUDFLARE_R2_ENDPOINT", cast=str)


# CLOUDFLARE_R2_CONFIG_OPTIONS = {
#     "bucket_name": CLOUDFLARE_R2_BUCKET_NAME,
#     "access_key": CLOUDFLARE_R2_ACCESS,
#     "secret_key": CLOUDFLARE_R2_SECRET,
#     "endpoint_url": CLOUDFLARE_R2_ENDPOINT,
#     "default_acl": "public-read",
#     "signature_version": "s3v4",
# }

# STORAGES = {
#     "default": {
#         "BACKEND": "api.helpers.cloudflare.storages.MediaFileStorage",
#         "OPTIONS": CLOUDFLARE_R2_CONFIG_OPTIONS,
#     },
#     "staticfiles": {
#         "BACKEND": "api.helpers.cloudflare.storages.StaticFileStorage",
#         "OPTIONS": CLOUDFLARE_R2_CONFIG_OPTIONS,
#     },
# }

# REST Simple JWT 설정

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "PAGINATION": {
        "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
        "PAGE_SIZE": 10,
    },
}

from datetime import timedelta

SIMPLE_JWT = {
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# 로거 설정
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG" if DEBUG else "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "verbose",  # 로깅 포맷터 설정
        },
    },
    "loggers": {
        # api 아래의 모든 앱에 적용
        "api": {
            "handlers": ["console"],
            "level": "DEBUG" if DEBUG else "WARNING",
            "propagate": False,
        },
    },
}
