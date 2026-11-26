"""
RETIRED. The templates are now the source of truth: the site has diverged
from the design build by design (frontend changes requested after conversion).
Running this would overwrite those changes. Kept as the record of how the
conversion was done.

Convert the static design build into Django templates.

Reads  : green-spark-website/website/*.html   (never written to)
Writes : gssl_site/templates/{base.html,partials/*,pages/*}

The design build marks every repeated block with
``<!-- partial:start NAME --> … <!-- partial:end NAME -->`` and is otherwise
byte-identical across pages, so the conversion is mechanical and checkable:

  1. Pull each partial out of every page and prove the copies agree once
     active-state markers (aria-current / is-current) are removed.
  2. Work out, by offset, which marker belongs to which nav item, and emit the
     partial once with a ``{% if nav_active == … %}`` at each varying spot.
     A marker present on *every* page is static and is re-inserted as-is.
  3. Emit one page template per file, holding only that page's <main>.
  4. Rewrite ../assets/… to {% static %} and *.html links to {% url %}.

Re-runnable: it always regenerates from the design build, so the design build
stays the single source of truth until the CMS replaces it.

Usage:  python tools/convert_design_build.py
"""

from __future__ import annotations

import html
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE_ROOT = HERE.parent                      # gssl_site/
REPO_ROOT = SITE_ROOT.parent                 # repository root
DESIGN = REPO_ROOT / "green-spark-website"
SRC = DESIGN / "website"
TEMPLATES = SITE_ROOT / "templates"

# --- the site map -----------------------------------------------------------
# design-build filename -> (url name, template name, nav key)

PAGES: dict[str, tuple[str, str, str]] = {
    "index.html": ("home", "home.html", ""),
    "improved-cookstove.html": ("programme_improved_cookstove", "programme_improved_cookstove.html", "what-we-do"),
    "programme-rooftop-solar.html": ("programme_rooftop_solar", "programme_rooftop_solar.html", "what-we-do"),
    "programme.html": ("programme_safe_drinking_water", "programme_safe_drinking_water.html", "what-we-do"),
    "programme-solar-irrigation.html": ("programme_solar_irrigation", "programme_solar_irrigation.html", "what-we-do"),
    "programme-rural-productive-use-solar.html": ("programme_rural_productive_use_solar", "programme_rural_productive_use_solar.html", "what-we-do"),
    "programme-low-emission-rice.html": ("programme_low_emission_rice", "programme_low_emission_rice.html", "what-we-do"),
    "projects.html": ("projects", "projects.html", "projects"),
    "project-detail.html": ("project_detail", "project_detail.html", "projects"),
    "gallery.html": ("gallery", "gallery.html", "projects"),
    "gallery-album.html": ("gallery_album", "gallery_album.html", "projects"),
    "why-gssl.html": ("why_gssl", "why_gssl.html", "why-gssl"),
    "news.html": ("news", "news.html", "news"),
    "news-article.html": ("news_article", "news_article.html", "news"),
    "events.html": ("events", "events.html", "news"),
    "event-detail.html": ("event_detail", "event_detail.html", "news"),
    "event-feedback-round.html": ("event_feedback_round", "event_feedback_round.html", "news"),
    "feedback.html": ("feedback", "feedback.html", "news"),
    "about-us.html": ("about", "about.html", "about"),
    "team.html": ("team", "team.html", "about"),
    "faq.html": ("faq", "faq.html", "about"),
    "contact-us.html": ("enquire", "enquire.html", "enquire"),
    "privacy.html": ("privacy", "privacy.html", ""),
    # 404 has no route of its own; it is wired to handler404.
    "404.html": ("", "404.html", ""),
}

# Partials rendered by base.html for every page.
CHROME = ["svg-sprite", "preloader", "site-topbar", "site-header", "mobile-menu",
          "site-footer", "preview-ribbon"]
# Partials a page opts into.
OPTIONAL_PARTIALS = ["cta-band", "meet-gssl"]
# Partials nested inside another partial — emitted, but not stripped from pages.
NESTED = ["social-links", "contact-details"]
# Left inline in the page: every occurrence carries different event data.
INLINE = ["event-status-badge"]

PARTIAL_FILE = {
    "svg-sprite": "svg_sprite.html",
    "preloader": "preloader.html",
    "site-topbar": "site_topbar.html",
    "site-header": "site_header.html",
    "mobile-menu": "mobile_menu.html",
    "site-footer": "site_footer.html",
    "preview-ribbon": "preview_ribbon.html",
    "cta-band": "cta_band.html",
    "meet-gssl": "meet_gssl_modal.html",
    "social-links": "social_links.html",
    "contact-details": "contact_details.html",
}

MARKER = re.compile(r'\s*aria-current="(?:page|true)"|\s+is-current\b')


class ConversionError(RuntimeError):
    pass


def fail(msg: str) -> None:
    raise ConversionError(msg)


# --- helpers ----------------------------------------------------------------

def find_blocks(text: str, name: str) -> list[tuple[int, int, str]]:
    """Every (start, end, inner) for partial `name`, outermost first."""
    out: list[tuple[int, int, str]] = []
    s, e = f"<!-- partial:start {name} -->", f"<!-- partial:end {name} -->"
    i = 0
    while (a := text.find(s, i)) >= 0:
        b = text.find(e, a)
        if b < 0:
            fail(f"unclosed partial {name}")
        out.append((a, b + len(e), text[a + len(s):b]))
        i = b + len(e)
    return out


def strip_markers(text: str) -> tuple[str, list[tuple[int, str]]]:
    """Remove active-state markers; return the clean text and (offset, marker)."""
    clean: list[str] = []
    found: list[tuple[int, str]] = []
    pos = 0
    length = 0
    for m in MARKER.finditer(text):
        chunk = text[pos:m.start()]
        clean.append(chunk)
        length += len(chunk)
        found.append((length, m.group(0)))
        pos = m.end()
    clean.append(text[pos:])
    return "".join(clean), found


def rewrite_assets(text: str) -> str:
    """../assets/foo.css -> {% static 'foo.css' %}"""
    return re.sub(r"\.\./assets/([^\"')\s]+)", lambda m: "{% static '" + m.group(1) + "' %}", text)


def rewrite_links(text: str, where: str) -> str:
    """page.html(#frag) -> {% url 'website:name' %}(#frag)"""
    def sub(m: re.Match) -> str:
        target, frag = m.group(1), m.group(2) or ""
        if target not in PAGES:
            fail(f"{where}: link to unknown page {target!r}")
        name = PAGES[target][0]
        if not name:  # 404 has no route
            return f'href="/404{frag}"'
        return "href=\"{% url 'website:" + name + "' %}" + frag + '"'

    return re.sub(r'href="([a-z0-9-]+\.html)(#[^"]*)?"', sub, text)


def clean_class(tag: str) -> str:
    """Tidy class="a  b " -> class="a b"; drop the attribute if it empties."""
    def sub(m: re.Match) -> str:
        value = " ".join(m.group(1).split())
        return f'class="{value}"' if value else ""
    return re.sub(r'class="([^"]*)"', sub, tag).replace("  ", " ").replace(" >", ">")


def body_classes(tag: str) -> list[str]:
    m = re.search(r'class="([^"]*)"', tag)
    return [c for c in (m.group(1).split() if m else []) if c != "is-preview"]


# --- load -------------------------------------------------------------------

def load() -> dict[str, str]:
    if not SRC.is_dir():
        fail(f"design build not found at {SRC}")
    pages = {}
    for name in PAGES:
        p = SRC / name
        if not p.is_file():
            fail(f"missing page {p}")
        pages[name] = p.read_text(encoding="utf-8")
    extra = {p.name for p in SRC.glob("*.html")} - set(PAGES)
    if extra:
        fail(f"design build has pages missing from the site map: {sorted(extra)}")
    return pages


# --- partials ---------------------------------------------------------------

def build_social_links(pages: dict[str, str]) -> str:
    """social-links appears three times a page and differs only by modifier."""
    bodies: set[str] = set()
    modifiers: set[str] = set()
    for text in pages.values():
        for _, _, inner in find_blocks(text, "social-links"):
            m = re.match(r'\s*<ul class="social-links\s*([^"]*)">', inner)
            if not m:
                fail("social-links: unexpected opening tag")
            modifiers.add(m.group(1).strip())
            bodies.add(inner[m.end():])
    if len(bodies) != 1:
        fail(f"social-links: {len(bodies)} bodies differ by more than the modifier")
    return ('<ul class="social-links{% if modifier %} {{ modifier }}{% endif %}">'
            + bodies.pop())


NESTED_INCLUDE = {
    "contact-details": '{% include "partials/contact_details.html" %}',
}


def nested_include(name: str, inner: str) -> str:
    if name == "social-links":
        m = re.match(r'\s*<ul class="social-links\s*([^"]*)">', inner)
        modifier = m.group(1).strip() if m else ""
        arg = f' with modifier="{modifier}"' if modifier else ""
        return '{% include "partials/social_links.html"' + arg + " %}"
    return NESTED_INCLUDE[name]


def replace_nested(text: str) -> str:
    """Swap any nested partial block for its {% include %}."""
    for name in NESTED:
        for a, b, inner in reversed(find_blocks(text, name)):
            text = text[:a] + nested_include(name, inner) + text[b:]
    return text


def build_partial(name: str, pages: dict[str, str]) -> str:
    """Emit one partial, with a conditional where pages disagree."""
    clean_forms: set[str] = set()
    markers_by_page: dict[str, list[tuple[int, str]]] = {}

    for fn, text in pages.items():
        blocks = find_blocks(text, name)
        if not blocks:
            continue
        if len(blocks) > 1:
            fail(f"{name}: expected one block per page, {fn} has {len(blocks)}")
        clean, markers = strip_markers(replace_nested(blocks[0][2]))
        clean_forms.add(clean)
        markers_by_page[fn] = markers

    if len(clean_forms) != 1:
        fail(f"{name}: {len(clean_forms)} distinct forms after normalising — cannot share one partial")
    body = clean_forms.pop()

    carriers: dict[tuple[int, str], set[str]] = defaultdict(set)
    for fn, markers in markers_by_page.items():
        for item in markers:
            carriers[item].add(fn)

    everywhere = set(markers_by_page)
    inserts: list[tuple[int, str]] = []
    for (offset, marker), pages_with in sorted(carriers.items(), reverse=True):
        if pages_with == everywhere:
            inserts.append((offset, marker))          # static, always present
            continue

        # A marker shared by every page of one nav group highlights that group
        # (the desktop header). A marker on a single page highlights that page
        # (the mobile menu, which marks the sub-item). Anything else means the
        # design build is inconsistent and must be looked at by hand.
        navs = {PAGES[fn][2] for fn in pages_with}
        condition = ""
        if len(navs) == 1 and (nav := navs.pop()):
            if pages_with == {fn for fn in everywhere if PAGES[fn][2] == nav}:
                condition = 'nav_active == "' + nav + '"'
        if not condition and len(pages_with) == 1:
            only = next(iter(pages_with))
            url_name = PAGES[only][0]
            if not url_name:
                fail(f"{name}: marker at {offset} is only on {only}, which has no URL name")
            condition = 'page_name == "' + url_name + '"'
        if not condition:
            fail(f"{name}: marker at {offset} matches neither one nav group nor one "
                 f"page (pages: {sorted(pages_with)})")
        inserts.append((offset, "{% if " + condition + " %}" + marker + "{% endif %}"))

    for offset, snippet in inserts:                   # descending, so offsets hold
        body = body[:offset] + snippet + body[offset:]

    return body


def write_partials(pages: dict[str, str]) -> dict[str, str]:
    out = TEMPLATES / "partials"
    out.mkdir(parents=True, exist_ok=True)
    written = {}
    for name in CHROME + OPTIONAL_PARTIALS + NESTED:
        if name == "social-links":
            body = build_social_links(pages)
        else:
            body = build_partial(name, pages)
        body = rewrite_links(rewrite_assets(body), f"partial {name}")
        header = "{% load static %}\n" if "{% static" in body else ""
        text = header + body.strip("\n") + "\n"
        (out / PARTIAL_FILE[name]).write_text(text, encoding="utf-8")
        written[name] = text
    return written


# --- body skeleton ----------------------------------------------------------
# Everything inside <body> that is NOT a partial and NOT inside <main>.
# base.html supplies this, so the converter verifies it: markup living between
# partials is invisible to the partial extractor and was silently dropped once
# already (the skip link, the .site-chrome wrapper and its spacer).

PLACEHOLDER = re.compile(r"^\[\[[A-Za-z-]+\]\]$")

SKELETON = [
    "[[svg-sprite]]",
    "[[preloader]]",
    '<a class="skip-link" href="#main">Skip to content</a>',
    '<div class="site-chrome" data-site-chrome>',
    "[[site-topbar]]",
    "[[site-header]]",
    "</div>",
    '<div class="site-chrome__spacer" aria-hidden="true"></div>',
    "[[mobile-menu]]",
    "[[MAIN]]",
    "[[cta-band]]",      # optional
    "[[site-footer]]",
    "[[meet-gssl]]",     # optional
    "[[BODY-END]]",      # optional raw markup, e.g. the lightbox dialog
    "[[preview-ribbon]]",
]
OPTIONAL = {"[[cta-band]]", "[[meet-gssl]]", "[[BODY-END]]"}


def body_skeleton(text: str, fn: str) -> tuple[list[str], str]:
    """
    Walk the body against SKELETON in order.

    Order matters: raw body-end markup contains its own closing tags, so a
    line-by-line match against the skeleton's literals would cut it in half.
    """
    body = text[text.index("<body"):text.index("</body>")]
    body = body[body.index(">") + 1:]
    for name in CHROME + OPTIONAL_PARTIALS:
        for a, b, _ in reversed(find_blocks(body, name)):
            body = body[:a] + "[[" + name + "]]" + body[b:]
    a, b = body.index("<main"), body.index("</main>")
    body = body[:a] + "[[MAIN]]" + body[b + len("</main>"):]

    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    present: list[str] = []
    raw: list[str] = []
    i = 0
    for token in SKELETON:
        if token == "[[BODY-END]]":
            while i < len(lines) and lines[i] != "[[preview-ribbon]]":
                raw.append(lines[i])
                i += 1
            if raw:
                present.append(token)
        elif i < len(lines) and lines[i] == token:
            present.append(token)
            i += 1
        elif token not in OPTIONAL:
            got = lines[i] if i < len(lines) else "<end of body>"
            fail(f"{fn}: body structure differs at line {i + 1}.\n"
                 f"      expected {token}\n"
                 f"      got      {got[:120]}\n"
                 "      base.html renders this skeleton; markup outside a "
                 "partial must be added there or carried by a block.")
    if i != len(lines):
        fail(f"{fn}: {len(lines) - i} line(s) of body markup left over, "
             f"starting with {lines[i][:120]!r}")
    return present, "\n".join(raw)


# --- pages ------------------------------------------------------------------

META = {
    "title": re.compile(r"<title>(.*?)</title>", re.S),
    "description": re.compile(r'<meta name="description" content="(.*?)">', re.S),
    "og_image": re.compile(r'<meta property="og:image" content="(.*?)">', re.S),
}


def page_meta(text: str, fn: str) -> dict[str, str]:
    meta = {}
    for key, rx in META.items():
        m = rx.search(text)
        if not m:
            fail(f"{fn}: no {key} in <head>")
        meta[key] = m.group(1).strip()
    # og:image is an absolute URL into /static/ — keep only the static path.
    m = re.search(r"/static/(.+)$", meta["og_image"])
    meta["og_image"] = m.group(1) if m else meta["og_image"]
    return meta


def head_extras(text: str) -> tuple[list[str], list[str]]:
    """Preload links and scripts a page has beyond the shared set."""
    head = text[: text.index("</head>")]
    preloads = re.findall(r'^\s*(<link rel="preload"[^>]*>)\s*$', head, re.M)
    scripts = re.findall(r'^\s*(<script src="\.\./assets/js/components/video-hero\.js"[^>]*></script>)\s*$',
                         head, re.M)
    return preloads, scripts


def page_main(text: str, fn: str) -> str:
    a = text.find("<main")
    b = text.find("</main>")
    if a < 0 or b < 0:
        fail(f"{fn}: no <main> element")
    open_tag_end = text.index(">", a)
    open_tag = text[a:open_tag_end + 1]
    if open_tag != '<main id="main" tabindex="-1">':
        fail(f"{fn}: unexpected <main> tag {open_tag!r}")
    return text[open_tag_end + 1:b]


def write_pages(pages: dict[str, str]) -> list[str]:
    out = TEMPLATES / "pages"
    out.mkdir(parents=True, exist_ok=True)
    notes = []
    body_end_markup: dict[str, list[str]] = {}

    for fn, text in pages.items():
        url_name, template, nav = PAGES[fn]
        meta = page_meta(text, fn)
        preloads, scripts = head_extras(text)

        body_tag = re.search(r"<body[^>]*>", text).group(0)
        classes = body_classes(body_tag)

        main = page_main(text, fn)
        # Drop the partials base.html already renders; keep inline ones.
        for name in OPTIONAL_PARTIALS:
            for a, b, _ in reversed(find_blocks(main, name)):
                main = main[:a] + main[b:]
        for name in INLINE:
            main = main.replace(f"<!-- partial:start {name} -->", "") \
                       .replace(f"<!-- partial:end {name} -->", "")
        for name in NESTED:
            main = main.replace(f"<!-- partial:start {name} -->", "") \
                       .replace(f"<!-- partial:end {name} -->", "")

        has = {name: bool(find_blocks(text, name)) for name in OPTIONAL_PARTIALS}

        # Verify nothing outside the partials is being dropped, and pick up
        # any raw tail markup (the lightbox dialog on the two gallery pages).
        _, body_end = body_skeleton(text, fn)
        if body_end:
            body_end = rewrite_links(rewrite_assets(body_end), fn)
            body_end_markup.setdefault(body_end, []).append(fn)

        main = rewrite_links(rewrite_assets(main), fn)
        preloads = [rewrite_assets(p) for p in preloads]
        scripts = [rewrite_assets(s) for s in scripts]

        canonical = "/" if url_name == "home" else None
        parts = ['{% extends "base.html" %}', "{% load static %}", ""]
        parts.append("{% block head_meta %}{% include \"partials/page_meta.html\" with "
                     f"title=\"{html.unescape(meta['title'])}\" "
                     f"description=\"{html.unescape(meta['description'])}\" "
                     f"og_image=\"{meta['og_image']}\" %}}{{% endblock %}}")
        if classes:
            parts.append("{% block body_class %}" + " ".join(classes) + "{% endblock %}")
        if preloads:
            parts.append("{% block head_preload %}\n  " + "\n  ".join(preloads) + "\n{% endblock %}")
        if scripts:
            # Goes in component_scripts, which base.html places above
            # website.js — the file that boots every registered module.
            parts.append("{% block component_scripts %}\n  " + "\n  ".join(scripts) + "\n{% endblock %}")
        if not has["cta-band"]:
            parts.append("{% block cta %}{% endblock %}")
        if has["meet-gssl"]:
            parts.append('{% block modals %}{% include "partials/meet_gssl_modal.html" %}{% endblock %}')
        if body_end:
            parts.append('{% block body_end %}{% include "partials/lightbox.html" %}{% endblock %}')
        parts.append("")
        parts.append("{% block content %}" + main.rstrip() + "\n{% endblock %}")

        (out / template).write_text("\n".join(parts) + "\n", encoding="utf-8")
        notes.append(f"  pages/{template:44} <- {fn}")

    if body_end_markup:
        if len(body_end_markup) != 1:
            fail(f"body-end markup differs between pages: "
                 f"{[v for v in body_end_markup.values()]}")
        markup, where = next(iter(body_end_markup.items()))
        (TEMPLATES / "partials" / "lightbox.html").write_text(markup + chr(10), encoding="utf-8")
        notes.append(f"  partials/lightbox.html{'':24} <- {', '.join(where)}")
    return notes


# --- static assets ----------------------------------------------------------

SOURCE_MAP = re.compile(rb"\s*/\*#\s*sourceMappingURL=([^\s*]+)\s*\*/\s*$")


def drop_dangling_source_maps(root: Path) -> list[str]:
    """
    Remove sourceMappingURL comments whose .map file was never shipped.

    ManifestStaticFilesStorage resolves every reference a stylesheet makes and
    refuses to build when one is missing, and a browser would request a 404 for
    it anyway. Only the copy under static/ is touched; the design build keeps
    its vendored files byte for byte.
    """
    dropped = []
    for path in list(root.rglob("*.css")) + list(root.rglob("*.js")):
        data = path.read_bytes()
        m = SOURCE_MAP.search(data)
        if not m:
            continue
        target = (path.parent / m.group(1).decode()).resolve()
        if target.is_file():
            continue
        path.write_bytes(SOURCE_MAP.sub(b"", data) + b"\n")
        dropped.append(f"{path.relative_to(root).as_posix()} -> {m.group(1).decode()}")
    return dropped


def copy_assets() -> str:
    src, dst = DESIGN / "assets", SITE_ROOT / "static"
    if not src.is_dir():
        fail(f"no assets at {src}")
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    files = sum(1 for _ in dst.rglob("*") if _.is_file())
    mb = sum(f.stat().st_size for f in dst.rglob("*") if f.is_file()) / 1024 / 1024
    lines = [f"  static/: {files} files, {mb:.1f} MB (copied from green-spark-website/assets)"]
    for note in drop_dangling_source_maps(dst):
        lines.append(f"  dropped dangling source map: {note}")
    return "\n".join(lines)


# --- main -------------------------------------------------------------------

def main() -> int:
    try:
        pages = load()
        print(f"read {len(pages)} pages from {SRC}\n")

        written = write_partials(pages)
        print("partials:")
        for name, text in sorted(written.items()):
            cond = text.count("{% if nav_active")
            extra = f"  ({cond} active-state conditionals)" if cond else ""
            print(f"  partials/{PARTIAL_FILE[name]:26} {len(text):>7,} bytes{extra}")

        print("\npages:")
        for line in write_pages(pages):
            print(line)

        print("\nassets:")
        print(copy_assets())
    except ConversionError as exc:
        print(f"\nCONVERSION FAILED: {exc}", file=sys.stderr)
        return 1
    print("\nok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
