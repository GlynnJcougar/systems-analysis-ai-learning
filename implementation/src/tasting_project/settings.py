import os
from urllib.parse import urlsplit

import dj_database_url
from django.core.exceptions import ImproperlyConfigured


def required_environment_variable(name):
    value = os.environ.get(name)
    if not value:
        raise ImproperlyConfigured(f"{name} must be set.")
    return value


SECRET_KEY = required_environment_variable("DJANGO_SECRET_KEY")

debug_value = os.environ.get("DJANGO_DEBUG", "false").lower()
if debug_value not in {"true", "false"}:
    raise ImproperlyConfigured("DJANGO_DEBUG must be true or false.")
DEBUG = debug_value == "true"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,[::1]"
    ).split(",")
    if host.strip()
]
if not ALLOWED_HOSTS:
    raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS must contain a host.")

database_url = required_environment_variable("DATABASE_URL")
database_parts = urlsplit(database_url)
if (
    database_parts.scheme not in {"postgres", "postgresql"}
    or not database_parts.hostname
    or not database_parts.username
    or not database_parts.path.strip("/")
):
    raise ImproperlyConfigured(
        "DATABASE_URL must specify a PostgreSQL host, user, and database."
    )
DATABASES = {"default": dj_database_url.parse(database_url)}

INSTALLED_APPS = [
    "django.contrib.contenttypes",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tasting_project.urls"
WSGI_APPLICATION = "tasting_project.wsgi.application"
ASGI_APPLICATION = "tasting_project.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    }
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
