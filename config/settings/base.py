from pathlib import Path
from decouple import config
from pytz import timezone

"""
프로젝트 기본 설정
"""
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("DJANGO_SECRET", cast=str)

DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = ["*"]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "https://*",
]

CSRF_TRUSTED_ORIGINS = [
    "https://*",
]

X_FRAME_OPTIONS = "DENY"

APPEND_SLASH = True


"""
설치된 앱
"""
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

"""
미들웨어 설정
"""
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

"""
URL 설정
"""

ROOT_URLCONF = "config.urls"


"""
템플릿 설정
"""
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


"""
WSGI/ASGI 설정
"""
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


"""
인증 관련 설정
"""
AUTH_USER_MODEL = "accounts.User"
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


"""
국제화 설정(언어, 시간대)
"""
LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True

KST = timezone(TIME_ZONE)


"""
정적 파일 및 미디어 파일 설정
"""
STATIC_URL = "/static/"


"""
로깅 설정
"""
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
