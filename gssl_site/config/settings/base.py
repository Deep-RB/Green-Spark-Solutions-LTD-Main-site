"""
Shared Django settings for the Green Spark Solutions Australia website.

Environment-specific values live in dev.py / prod.py. Nothing secret is
stored here; secrets come from the environment (see .env.example).
"""

from pathlib import Path
import os

# gssl_site/config/settings/base.py -> gssl_site/
BASE_DIR = Path(__file__).resolve().parents[2]

# Load gssl_site/.env if it exists, so local work needs no shell setup.
# Real environment variables always win; in production there is no .env file
# and the server's own environment supplies everything.
try:
    from dotenv import load_dotenv
except ImportError:  # dotenv is optional
    pass
else:
    load_dotenv(BASE_DIR / ".env", override=False)


def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)


def env_bool(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def env_list(name: str, default: str = "") -> list[str]:
    return [item.strip() for item in env(name, default).split(",") if item.strip()]


# --- Core -------------------------------------------------------------------

SECRET_KEY = env("DJANGO_SECRET_KEY", "insecure-key-for-local-development-only")
DEBUG = False
ALLOWED_HOSTS: list[str] = env_list("DJANGO_ALLOWED_HOSTS")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.website",
]

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

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.website.context_processors.site",
            ],
        },
    },
]

# --- Database ---------------------------------------------------------------
# The site is entirely static for now. SQLite is here only so the admin and
# sessions work; the content models arrive with the admin panel.

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Internationalisation ---------------------------------------------------
# Bangla is planned (see README §4, --gs-font-bn); English only for now.

LANGUAGE_CODE = "en-au"
TIME_ZONE = "Australia/Sydney"
USE_I18N = True
USE_TZ = True

# --- Static files -----------------------------------------------------------

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# --- Site identity ----------------------------------------------------------
# Canonical, Open Graph and share URLs are built from SITE_URL. Change it here
# (or via the environment) when the final domain is confirmed — the templates
# never hard-code a domain.

SITE_URL = env("DJANGO_SITE_URL", "https://gssl.thingbd.com").rstrip("/")
SITE_NAME = "Green Spark Solutions Australia"

# The design build ships with a "preview" ribbon and body class. Off unless
# explicitly enabled, so production never shows it.
SHOW_PREVIEW_RIBBON = env_bool("DJANGO_SHOW_PREVIEW_RIBBON", False)
