"""
RETIRED. The site has intentionally diverged from the design build, so this
no longer passes and is no longer run in CI. Kept for reference.

Prove every Django page still renders the same content as the design build.

Compares each rendered page against ../green-spark-website/website/<page>.html
(byte-identical to what is live at gssl.thingbd.com) and reports anything the
Django version has lost: visible text, elements, classes, data-* hooks or ids.

Differences that are expected by design are normalised away first:
  ../assets/...   <-> /static/...
  foo.html        <-> the page's real URL
  data-now        <-> today's date
  partial markers <-> gone, they became {% include %}

Usage:  python tools/check_parity.py
"""

from __future__ import annotations

import os
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
DESIGN = SITE_ROOT.parent / "green-spark-website" / "website"
sys.path.insert(0, str(SITE_ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

import django  # noqa: E402

django.setup()

from django.conf import settings  # noqa: E402
from django.test import Client  # noqa: E402
from django.urls import reverse  # noqa: E402

from apps.website.pages import PAGES  # noqa: E402

if "testserver" not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append("testserver")

# Django template name -> the design build file it came from.
SOURCE = {
    "home": "index.html",
    "programme_improved_cookstove": "improved-cookstove.html",
    "programme_rooftop_solar": "programme-rooftop-solar.html",
    "programme_safe_drinking_water": "programme.html",
    "programme_solar_irrigation": "programme-solar-irrigation.html",
    "programme_rural_productive_use_solar": "programme-rural-productive-use-solar.html",
    "programme_low_emission_rice": "programme-low-emission-rice.html",
    "projects": "projects.html",
    "project_detail": "project-detail.html",
    "gallery": "gallery.html",
    "gallery_album": "gallery-album.html",
    "why_gssl": "why-gssl.html",
    "news": "news.html",
    "news_article": "news-article.html",
    "events": "events.html",
    "event_detail": "event-detail.html",
    "event_feedback_round": "event-feedback-round.html",
    "feedback": "feedback.html",
    "about": "about-us.html",
    "team": "team.html",
    "faq": "faq.html",
    "enquire": "contact-us.html",
    "privacy": "privacy.html",
}

# base.html adds these two on purpose: the design build leaves font preloads
# out so its pages also open from file:// (see its README section 5).
ALLOWED_EXTRA_TAGS = {"link": 2}


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.out.append(" ".join(data.split()))


class Inventory(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags: Counter[str] = Counter()
        self.classes: Counter[str] = Counter()
        self.data: Counter[str] = Counter()
        self.ids: set[str] = set()

    def handle_starttag(self, tag, attrs):
        self.tags[tag] += 1
        d = dict(attrs)
        if d.get("id"):
            self.ids.add(d["id"])
        for c in (d.get("class") or "").split():
            self.classes[c] += 1
        for key in d:
            if key.startswith("data-"):
                self.data[key] += 1


def url_map() -> list[tuple[str, str]]:
    pairs = [(reverse(f"website:{p.name}"), SOURCE[p.name]) for p in PAGES if p.name]
    return sorted(pairs, key=lambda t: -len(t[0]))


def normalise(markup: str, is_django: bool, urls: list[tuple[str, str]]) -> str:
    markup = re.sub(r"<!-- partial:(start|end) [a-z-]+ -->", "", markup)
    if is_django:
        markup = markup.replace("/static/", "../assets/")
        for url, filename in urls:
            markup = markup.replace(f'href="{url}"', f'href="{filename}"')
    return re.sub(r'data-now="[^"]*"', 'data-now="X"', markup)


def parse(markup: str, parser_cls):
    parser = parser_cls()
    parser.feed(markup)
    return parser


def dropped(a: Counter, b: Counter) -> dict[str, int]:
    return {k: a[k] - b.get(k, 0) for k in a if a[k] > b.get(k, 0)}


def main() -> int:
    if not DESIGN.is_dir():
        print(f"design build not found at {DESIGN}", file=sys.stderr)
        return 1

    client = Client()
    urls = url_map()
    failures = 0
    checked = 0

    for page in PAGES:
        if not page.name:
            continue
        source = DESIGN / SOURCE[page.name]
        original = normalise(source.read_text(encoding="utf-8"), False, urls)
        response = client.get(reverse(f"website:{page.name}"))
        if response.status_code != 200:
            print(f"FAIL {page.name}: HTTP {response.status_code}")
            failures += 1
            continue
        rendered = normalise(response.content.decode(), True, urls)
        checked += 1

        want_text = parse(original, VisibleText).out
        got_text = parse(rendered, VisibleText).out
        want = parse(original, Inventory)
        got = parse(rendered, Inventory)

        problems = []
        missing_text = [t for t in want_text if t not in got_text]
        extra_text = [t for t in got_text if t not in want_text]
        if missing_text:
            problems.append(f"{len(missing_text)} text fragment(s) missing: {missing_text[:3]}")
        if extra_text:
            problems.append(f"{len(extra_text)} text fragment(s) added: {extra_text[:3]}")
        for label, gap in (
            ("element", dropped(want.tags, got.tags)),
            ("class", dropped(want.classes, got.classes)),
            ("data-attribute", dropped(want.data, got.data)),
        ):
            if gap:
                problems.append(f"{label}(s) missing: {gap}")
        if want.ids - got.ids:
            problems.append(f"id(s) missing: {sorted(want.ids - got.ids)}")
        added = dropped(got.tags, want.tags)
        if added and added != ALLOWED_EXTRA_TAGS:
            problems.append(f"unexpected element(s) added: {added}")

        if problems:
            failures += 1
            print(f"FAIL {SOURCE[page.name]}")
            for p in problems:
                print(f"       {p}")

    if failures:
        print(f"\n{failures} page(s) differ from the design build")
        return 1
    print(f"{checked} pages match the design build "
          f"(text, elements, classes, data hooks and ids)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
