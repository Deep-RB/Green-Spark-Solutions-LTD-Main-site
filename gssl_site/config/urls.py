"""Root URL configuration."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.website.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Error pages. The design build supplies 404; 500 reuses the same template
# without the site chrome's dynamic parts.
handler404 = "apps.website.views.page_not_found"
handler500 = "apps.website.views.server_error"
