from pathlib import Path
import os

try:
    from .local_settings import *
except Exception as e:
    pass


class ENV:
    API_VERSION = os.getenv("API_VERSION")

    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

    SUPERUSER_USERNAME = os.getenv("SUPERUSER_USERNAME")
    SUPERUSER_PASSWORD = os.getenv("SUPERUSER_PASSWORD")

    SWAGGER = os.getenv("SWAGGER") == "on"
    REDOC = os.getenv("REDOC") == "on"
    DJANGO_ADMIN = os.getenv("DJANGO_ADMIN") == "on"
    DEBUG = os.getenv("DEBUG") == "on"
    IS_LOCAL = os.getenv("LOCAL") == "on"
    REDIS_HOST = os.getenv("REDIS_HOST", default="localhost")
    REDIS_PORT = os.getenv("REDIS_PORT", default="6379")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379")
    CELERY_RESULT_BACKEND = "django-db"
    OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")
    LLM_REQUESTS = os.getenv("LLM_REQUESTS") == "on"


BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
ALLOWED_HOSTS = ["*", "217.197.97.121"]

if not ENV.IS_LOCAL:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
else:
    DEBUG = True
    CORS_ALLOW_ALL_ORIGINS = True

AUTH_USER_MODEL = "authentication.User"
ROOT_URLCONF = "coreapi_django.urls"
WSGI_APPLICATION = "coreapi_django.wsgi.application"
APPEND_SLASH = True
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    # "django_celery_beat",
    # "django_celery_results",
    "drf_yasg",
    "rest_framework",
    "authentication",
    "assistants",
    "corsheaders",
    "goals",
    "files",
]
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "authentication.middleware.TokenAuthentication",
    ],
}
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "authentication.middleware.TokenMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
CORS_ORIGIN_ALLOW_ALL = True

if ENV.SWAGGER:
    SWAGGER_SETTINGS = {
        "SECURITY_DEFINITIONS": {
            "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"},
        },
        "USE_SESSION_AUTH": False,
    }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "USER": ENV.POSTGRES_USER,
        "PASSWORD": ENV.POSTGRES_PASSWORD,
        "NAME": ENV.POSTGRES_DATABASE,
        "HOST": ENV.POSTGRES_HOST,
        "PORT": ENV.POSTGRES_PORT,
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "propagate": True,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "myproject.custom": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379")
CELERY_RESULT_BACKEND = "django-db"
CELERY_TIMEZONE = "Asia/Tehran"
CELERY_TASK_TRACK_STARTED = True
CELERY_ACKS_LATE = True

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

REDIS_HOST = "localhost"
REDIS_PORT = "6379"

AUTH_PASSWORD_VALIDATORS = []

TIME_ZONE = "Asia/Tehran"
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

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
