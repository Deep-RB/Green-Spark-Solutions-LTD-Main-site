"""
Values every template needs.

These are the slots the admin panel will fill later. Today they are read from
settings so that nothing is hard-coded in a template; when the CMS arrives,
this module reads the same keys from the database instead and no template
changes.
"""

from django.conf import settings


def site(request):
    return {
        "site_url": settings.SITE_URL,
        "site_name": settings.SITE_NAME,
    }
