"""Local development settings. Never used in production."""

from .base import *  # noqa: F401,F403
from .base import env_bool, env_list

DEBUG = True

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,[::1]")

INTERNAL_IPS = ["127.0.0.1"]

# Serve static straight from STATICFILES_DIRS without a manifest, so no
# collectstatic is needed while working on the design.
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

# Show the design-build preview ribbon locally unless told otherwise.
SHOW_PREVIEW_RIBBON = env_bool("DJANGO_SHOW_PREVIEW_RIBBON", True)

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
