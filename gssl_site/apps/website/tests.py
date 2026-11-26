"""
Smoke tests for the converted design build.

These check the conversion itself: every route renders, the shared chrome is
present on every page, nothing leaks an unrendered template tag, and no page
still points at the old ../assets/ paths.
"""

import codecs
import re

from django.conf import settings
from django.test import SimpleTestCase, override_settings
from django.urls import reverse

from .content import PROJECTS
from .pages import PAGES

ROUTED = [p for p in PAGES if p.name]


class PageRenderTests(SimpleTestCase):
    """Every page in the site map renders."""

    def test_every_page_returns_200(self):
        for page in ROUTED:
            with self.subTest(page=page.name):
                response = self.client.get(reverse(f"website:{page.name}"))
                self.assertEqual(response.status_code, 200)

    def test_pages_carry_the_shared_chrome(self):
        for page in ROUTED:
            with self.subTest(page=page.name):
                body = self.client.get(reverse(f"website:{page.name}")).content.decode()
                self.assertIn('<header class="site-header"', body)
                self.assertIn('<footer class="site-footer', body)
                self.assertIn('id="gs-mark"', body)          # svg sprite
                self.assertIn('<main id="main"', body)

    def test_no_unrendered_template_tags(self):
        # {# #} included: Django only treats it as a comment on ONE line, so a
        # multi-line one renders as visible text.
        leak = re.compile(r"\{%|\{\{|\{#")
        for page in ROUTED:
            with self.subTest(page=page.name):
                body = self.client.get(reverse(f"website:{page.name}")).content.decode()
                self.assertIsNone(leak.search(body), "unrendered template syntax in output")

    def test_no_design_build_asset_paths_remain(self):
        for page in ROUTED:
            with self.subTest(page=page.name):
                body = self.client.get(reverse(f"website:{page.name}")).content.decode()
                self.assertNotIn("../assets/", body)
                self.assertIn(settings.STATIC_URL, body)

    def test_no_links_to_raw_html_files(self):
        """Internal links must go through {% url %}, not foo.html."""
        for page in ROUTED:
            with self.subTest(page=page.name):
                body = self.client.get(reverse(f"website:{page.name}")).content.decode()
                stray = re.findall(r'href="(?!https?:)[^"]*?[a-z0-9-]+\.html[^"]*"', body)
                self.assertEqual(stray, [], f"{page.name} still links to .html files")


class MetadataTests(SimpleTestCase):
    def test_each_page_has_a_unique_title_and_description(self):
        titles, descriptions = {}, {}
        for page in ROUTED:
            body = self.client.get(reverse(f"website:{page.name}")).content.decode()
            title = re.search(r"<title>(.*?)</title>", body, re.S).group(1).strip()
            desc = re.search(r'<meta name="description" content="(.*?)">', body, re.S).group(1)
            self.assertTrue(title, f"{page.name} has an empty title")
            self.assertTrue(desc, f"{page.name} has an empty description")
            titles.setdefault(title, []).append(page.name)
            descriptions.setdefault(desc, []).append(page.name)
        dupes = {t: p for t, p in titles.items() if len(p) > 1}
        self.assertEqual(dupes, {}, f"duplicate <title>: {dupes}")
        dupes = {d: p for d, p in descriptions.items() if len(p) > 1}
        self.assertEqual(dupes, {}, f"duplicate meta description: {dupes}")

    def test_canonical_matches_the_page_url(self):
        for page in ROUTED:
            with self.subTest(page=page.name):
                url = reverse(f"website:{page.name}")
                body = self.client.get(url).content.decode()
                self.assertIn(f'<link rel="canonical" href="{settings.SITE_URL}{url}">', body)

    def test_canonical_has_no_hard_coded_domain(self):
        """The domain comes from SITE_URL, so overriding it moves every link."""
        with override_settings(SITE_URL="https://example.test"):
            body = self.client.get(reverse("website:home")).content.decode()
        self.assertIn('href="https://example.test/"', body)
        self.assertNotIn("gssl.thingbd.com", body)


class NavigationTests(SimpleTestCase):
    def test_nav_marks_the_current_section(self):
        expected = {
            "projects": "projects",
            "news": "news",
            "about": "about",
            "why_gssl": "why-gssl",
            "programme_rooftop_solar": "what-we-do",
        }
        for name, nav in expected.items():
            with self.subTest(page=name):
                body = self.client.get(reverse(f"website:{name}")).content.decode()
                self.assertTrue(
                    "is-current" in body or 'aria-current="page"' in body,
                    f"{name} does not mark {nav} as current",
                )

    def test_home_marks_nothing_as_current(self):
        body = self.client.get(reverse("website:home")).content.decode()
        self.assertNotIn("is-current", body)

    def test_internal_links_resolve(self):
        """Every in-site href on the home page is a real route."""
        body = self.client.get(reverse("website:home")).content.decode()
        hrefs = {h.split("#")[0] for h in re.findall(r'href="(/[^"]*)"', body)}
        known = ({reverse(f"website:{p.name}") for p in ROUTED}
                 | {reverse("website:project_detail", args=[pr.slug]) for pr in PROJECTS}
                 | {"/404", "/"})
        for href in hrefs:
            if href.startswith(settings.STATIC_URL) or href.startswith(settings.MEDIA_URL):
                continue
            with self.subTest(href=href):
                self.assertIn(href, known)


class ScriptOrderTests(SimpleTestCase):
    """
    website.js calls GS.boot(), which runs every module registered up to that
    point. A component script loaded after it registers too late and never
    boots — which silently cost the home page its hero video once already.
    """

    def test_component_scripts_load_before_the_bootstrap(self):
        for page in ROUTED:
            with self.subTest(page=page.name):
                body = self.client.get(reverse(f"website:{page.name}")).content.decode()
                boot = body.find("js/website.js")
                self.assertNotEqual(boot, -1, "website.js is missing")
                after = [
                    src for src in re.findall(r'<script src="([^"]*js/components/[^"]*)"', body)
                    if body.find(src) > boot
                ]
                self.assertEqual(after, [], "component script loaded after website.js")

    def test_home_loads_the_video_hero_module(self):
        body = self.client.get(reverse("website:home")).content.decode()
        self.assertIn("js/components/video-hero.js", body)
        self.assertIn("data-vhero", body)
        for attr in ("data-wide-webm", "data-wide-mp4", "data-tall-webm", "data-tall-mp4"):
            self.assertIn(attr, body, f"hero video is missing {attr}")


class ErrorPageTests(SimpleTestCase):
    def test_unknown_url_renders_the_404_page(self):
        response = self.client.get("/no-such-page/")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Page not found", response.content.decode())


class PreviewRibbonTests(SimpleTestCase):
    def test_ribbon_is_absent_when_disabled(self):
        with override_settings(SHOW_PREVIEW_RIBBON=False):
            body = self.client.get(reverse("website:home")).content.decode()
        self.assertNotIn("is-preview", body)

    def test_ribbon_is_present_when_enabled(self):
        with override_settings(SHOW_PREVIEW_RIBBON=True):
            body = self.client.get(reverse("website:home")).content.decode()
        self.assertIn("is-preview", body)

class SiteChromeTests(SimpleTestCase):
    """
    Markup that lives between partials in the design build, so the partial
    extractor never saw it. All of this went missing in the first conversion.
    """

    def test_every_page_has_the_skip_link(self):
        for page in ROUTED:
            with self.subTest(page=page.name):
                body = self.client.get(reverse(f"website:{page.name}")).content.decode()
                self.assertIn('<a class="skip-link" href="#main">Skip to content</a>', body)

    def test_every_page_wraps_the_header_in_site_chrome(self):
        """nav.js queries [data-site-chrome]; the CSS makes it position:fixed."""
        for page in ROUTED:
            with self.subTest(page=page.name):
                body = self.client.get(reverse(f"website:{page.name}")).content.decode()
                self.assertIn('<div class="site-chrome" data-site-chrome>', body)
                self.assertIn('<div class="site-chrome__spacer" aria-hidden="true"></div>', body)
                chrome = body.index("data-site-chrome")
                self.assertLess(chrome, body.index('class="site-topbar'))
                self.assertLess(body.index("<header"), body.index("site-chrome__spacer"))

    def test_lightbox_is_on_the_two_gallery_pages_only(self):
        for page in ROUTED:
            with self.subTest(page=page.name):
                body = self.client.get(reverse(f"website:{page.name}")).content.decode()
                expected = page.name in {"gallery_album", "project_detail"}
                self.assertEqual("data-lightbox-root" in body, expected)


class TemplateFileTests(SimpleTestCase):
    def test_no_template_has_a_byte_order_mark(self):
        """A BOM renders as a stray character at the top of the page."""
        root = settings.BASE_DIR / "templates"
        culprits = [
            str(f.relative_to(root)) for f in root.rglob("*.html")
            if f.read_bytes()[:3] == codecs.BOM_UTF8
        ]
        self.assertEqual(culprits, [], "template(s) saved with a UTF-8 BOM")


class ProjectPageTests(SimpleTestCase):
    """
    Every project has its own page. The design build shipped one detail page
    holding Phase 1's content, and all seven cards pointed at it, so Phase 2
    and Phase 3 opened Phase 1.
    """

    def test_every_project_has_its_own_page(self):
        for project in PROJECTS:
            with self.subTest(project=project.slug):
                url = reverse("website:project_detail", args=[project.slug])
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_each_page_shows_its_own_details(self):
        for project in PROJECTS:
            with self.subTest(project=project.slug):
                body = self.client.get(
                    reverse("website:project_detail", args=[project.slug])
                ).content.decode()
                self.assertIn(project.location, body)
                self.assertIn(project.stage, body)

    def test_phase_2_and_3_are_not_phase_1(self):
        bodies = {}
        for slug in ("green-ics-phase-1", "green-ics-phase-2", "green-ics-phase-3"):
            bodies[slug] = self.client.get(
                reverse("website:project_detail", args=[slug])
            ).content.decode()
        def key_details(body):
            start = body.find("key-details")
            return body[start:body.find("</aside>", start)]

        self.assertIn("Dhaka and Rajshahi", key_details(bodies["green-ics-phase-2"]))
        self.assertNotIn("Dhaka and Rajshahi", key_details(bodies["green-ics-phase-1"]))
        self.assertIn("Manikganj", key_details(bodies["green-ics-phase-1"]))
        self.assertIn("districts to confirm", key_details(bodies["green-ics-phase-3"]))

    def test_registry_link_only_where_there_is_a_gold_standard_id(self):
        for project in PROJECTS:
            with self.subTest(project=project.slug):
                body = self.client.get(
                    reverse("website:project_detail", args=[project.slug])
                ).content.decode()
                self.assertEqual("registry.goldstandard.org" in body, bool(project.gs_id))

    def test_unknown_project_is_404(self):
        self.assertEqual(self.client.get("/projects/not-a-project/").status_code, 404)
