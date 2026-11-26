"""URL patterns, generated from the single site map in pages.py."""

from django.urls import path

from .pages import PAGES
from .views import ProjectDetailView, StaticPageView

app_name = "website"

urlpatterns = [
    path(page.route, StaticPageView.as_view(page=page), name=page.name)
    for page in PAGES
] + [
    # One page per project, driven by content.PROJECTS.
    path("projects/<slug:slug>/", ProjectDetailView.as_view(), name="project_detail"),
]
