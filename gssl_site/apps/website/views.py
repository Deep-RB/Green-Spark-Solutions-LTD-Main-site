"""
Views for the static website.

Every page is the same shape: render a template, tell the chrome which nav
item is current. One generic view covers all of them, driven by pages.PAGES.
When content models arrive, individual pages graduate out of this table into
their own views without touching the templates.
"""

from django.shortcuts import render
from django.views.generic import TemplateView

from .pages import Page


class StaticPageView(TemplateView):
    """Render one row of pages.PAGES."""

    # Set per URL by as_view(page=…); must exist on the class for Django to
    # accept it as a keyword there.
    page: Page | None = None

    def get_template_names(self) -> list[str]:
        return [f"pages/{self.page.template}"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_active"] = self.page.nav
        context["page_name"] = self.page.name
        return context


def page_not_found(request, exception=None, template_name="pages/404.html"):
    return render(request, template_name, {"nav_active": ""}, status=404)


def server_error(request, template_name="pages/500.html"):
    return render(request, template_name, {"nav_active": ""}, status=500)
