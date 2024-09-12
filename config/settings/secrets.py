from decouple import config

NAVER_CLIENT = config("NAVER_CLIENT", cast=str)
NAVER_SECRET = config("NAVER_SECRET", cast=str)

GOOGLE_CLIENT = config("GOOGLE_CLIENT", cast=str)
GOOGLE_SECRET = config("GOOGLE_SECRET", cast=str)
SOCIAL_CALLBACK_URI = config("SOCIAL_CALLBACK_URI", cast=str)

PORTONE_SECRET = config("PORTONE_SECRET", cast=str)
PORTONE_WEBHOOK = config("PORTONE_WEBHOOK", cast=str)

APICK_SECRET = config("APICK_SECRET", cast=str)

NTS_SECRET = config("NTS_SECRET", cast=str)
