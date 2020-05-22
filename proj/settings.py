import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from proj import secrets

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = secrets.SECURITY_KEY


DEBUG = secrets.DEBUG


ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    secrets.SERVER_IP,
    secrets.SERVER_URL,
]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "encrypted_model_fields",
    "proj.apps.music",
    "proj.apps.users",
    "channels",
    "django_admin_listfilter_dropdown",
    "storages",
]


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "jukebox_radio_cache",
    }
}


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [(secrets.REDIS_HOST_URL, secrets.REDIS_HOST_PORT)],},
    },
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
]

ROOT_URLCONF = "proj.urls"

ASGI_APPLICATION = "proj.routing.application"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [f"{BASE_DIR}/proj/site/templates"],
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


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": secrets.DB_NAME,
        "USER": secrets.DB_USER,
        "PASSWORD": secrets.DB_PASSWORD,
        "HOST": secrets.DB_HOST_URL,
        "PORT": secrets.DB_HOST_PORT,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

DATA_UPLOAD_MAX_MEMORY_SIZE = 64000000  # 64 MB

AWS_S3_REGION_NAME = "sfo2"

AWS_ACCESS_KEY_ID = "V6ZQRTKVNKFIHCHZSPMF"
AWS_SECRET_ACCESS_KEY = "iH+3g1oRgK6MQFScbBYRfrTH4G2eHreR1Cu70gkeLw4"

if not secrets.DEBUG:
    # if True:
    AWS_STORAGE_BUCKET_NAME = "jukebox-radio-space"
    AWS_S3_ENDPOINT_URL = f"https://{AWS_S3_REGION_NAME}.digitaloceanspaces.com"
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
    }
    AWS_LOCATION = "jukebox-radio-space"

    STATIC_URL = "https://%s/%s/" % (AWS_S3_ENDPOINT_URL, AWS_LOCATION)
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

STATIC_URL = "/static/"


if not secrets.DEBUG:
    STATIC_ROOT = f"{BASE_DIR}/proj/site/static/"
else:
    STATIC_ROOT = f"{BASE_DIR}/proj/site/static/"
    # STATICFILES_DIRS = [f'{BASE_DIR}/proj/site/static/']

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


DATABASE_ENCRYPTION_KEY = secrets.DATABASE_ENCRYPTION_KEY.encode("utf-8")


# Error reporting
# https://sentry.io/for/django/



sentry_sdk.init(
    dsn=secrets.SENTRY_SECRET,
    integrations=[DjangoIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)
