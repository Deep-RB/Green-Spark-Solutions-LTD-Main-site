"""URL patterns, generated from the single site map in pages.py."""

from django.urls import path

from .pages import PAGES
from .views import StaticPageView

app_name = "website"

urlpatterns = [
    path(page.route, StaticPageView.as_view(page=page), name=page.name)
    for page in PAGES
]
