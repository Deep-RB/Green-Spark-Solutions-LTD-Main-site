"""
Views for the website.

Every static page is the same shape: render a template, tell the chrome which
nav item is current. One generic view covers all of them, driven by
pages.PAGES. The contact page adds a POST handler; projects are slug-driven
from content.PROJECTS. robots.txt and sitemap.xml are built from the same
two tables, so a page taken offline drops out of both automatically.
"""

import hashlib

from django.conf import settings
from django.core.cache import cache
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView

from .content import PROJECTS, PROJECTS_BY_SLUG, related_projects
from .forms import EnquiryForm
from .mail import notify_enquiry
from .models import ENQUIRY_SUBJECTS, ENQUIRY_TYPES
from .pages import PAGES, Page


class StaticPageView(TemplateView):
    """Render one row of pages.PAGES."""

    # Set per URL by as_view(page=…); must exist on the class for Django to
    # accept it as a keyword there.
    page: Page | None = None

    def dispatch(self, request, *args, **kwargs):
        if not self.page.is_published:
            raise Http404("This page is not published.")
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self) -> list[str]:
        return [f"pages/{self.page.template}"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_active"] = self.page.nav
        context["page_name"] = self.page.name
        context["noindex"] = not self.page.in_sitemap
        return context


# --- Contact form -----------------------------------------------------------

def _client_key(request) -> str:
    """A hashed per-visitor key for throttling. The raw IP is never stored."""
    ip = request.META.get("REMOTE_ADDR", "")
    if settings.BEHIND_PROXY:
        # The reverse proxy appends the address it saw; the last entry is the
        # one a visitor cannot forge.
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if forwarded:
            ip = forwarded.split(",")[-1].strip()
    return "enquiry-throttle:" + hashlib.sha256(ip.encode()).hexdigest()[:32]


def _throttled(request) -> bool:
    key = _client_key(request)
    window = settings.ENQUIRY_THROTTLE_SECONDS
    if cache.add(key, 1, timeout=window):
        return False
    try:
        count = cache.incr(key)
    except ValueError:  # expired between add() and incr()
        cache.add(key, 1, timeout=window)
        return False
    return count > settings.ENQUIRY_THROTTLE_COUNT


class EnquireView(StaticPageView):
    """The contact page. GET shows the form; POST stores and emails it."""

    http_method_names = ["get", "post", "head", "options"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("form", EnquiryForm())
        context["subject_choices"] = ENQUIRY_SUBJECTS
        context["enquiry_type_choices"] = ENQUIRY_TYPES
        context["sent"] = self.request.GET.get("sent") == "1"
        return context

    def post(self, request, *args, **kwargs):
        wants_json = (
            request.headers.get("x-requested-with") == "XMLHttpRequest"
            or "application/json" in request.headers.get("accept", "")
        )
        form = EnquiryForm(request.POST)

        if form.is_bot():
            # Pretend it worked; store and send nothing.
            return JsonResponse({"ok": True}) if wants_json else self._sent()

        if _throttled(request):
            message = (
                "You have sent several messages in a short time. Please wait a few "
                "minutes, or email info@greensparksolutions.com."
            )
            if wants_json:
                return JsonResponse({"ok": False, "errors": {}, "message": message}, status=429)
            context = self.get_context_data(form=form, throttle_message=message)
            return self.render_to_response(context, status=429)

        if not form.is_valid():
            if wants_json:
                errors = {field: msgs[0] for field, msgs in form.errors.items()}
                return JsonResponse({"ok": False, "errors": errors}, status=400)
            return self.render_to_response(self.get_context_data(form=form), status=400)

        enquiry = form.save()
        notify_enquiry(enquiry)
        return JsonResponse({"ok": True}) if wants_json else self._sent()

    def _sent(self):
        # Post/Redirect/Get, so a refresh never resubmits.
        return redirect(f"{reverse('website:enquire')}?sent=1#contact-form")


# --- Projects ---------------------------------------------------------------

class ProjectDetailView(TemplateView):
    """One page per project, from content.PROJECTS."""

    template_name = "pages/project_detail.html"

    def get_context_data(self, **kwargs):
        project = PROJECTS_BY_SLUG.get(kwargs.get("slug"))
        if project is None:
            raise Http404("No such project")
        context = super().get_context_data(**kwargs)
        context["project"] = project
        context["related"] = related_projects(project)
        context["nav_active"] = "projects"
        context["page_name"] = "project_detail"
        return context


# --- robots.txt and sitemap.xml ---------------------------------------------

@require_GET
@cache_control(max_age=60 * 60 * 24, public=True)
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow:",
        "",
        f"Sitemap: {settings.SITE_URL}{reverse('website:sitemap')}",
        "",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


@require_GET
@cache_control(max_age=60 * 60, public=True)
def sitemap_xml(request):
    urls = [reverse(f"website:{page.name}") for page in PAGES if page.in_sitemap]
    urls += [reverse("website:project_detail", args=[p.slug]) for p in PROJECTS]
    body = render_to_string("sitemap.xml", {"urls": urls, "site_url": settings.SITE_URL})
    return HttpResponse(body, content_type="application/xml; charset=utf-8")


# --- Errors -----------------------------------------------------------------

def page_not_found(request, exception=None, template_name="pages/404.html"):
    return render(request, template_name, {"nav_active": "", "noindex": True}, status=404)


def server_error(request, template_name="pages/500.html"):
    return render(request, template_name, {"nav_active": "", "noindex": True}, status=500)
