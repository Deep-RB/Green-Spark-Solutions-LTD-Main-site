"""
The site map, in one place.

Every page of the design build is one row here: the URL route, the template
that renders it, and which top-level nav item should show as current.

The site is deliberately static for now — each row is a plain template with no
database behind it. When the admin panel lands, the rows that represent real
content (programmes, projects, events, posts, albums) become model-backed
detail views; the rows marked ``sample=True`` are the ones whose slug is
currently hard-coded sample data and will be replaced by a slug captured from
the URL. Nothing else about the templates has to change.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Page:
    name: str          # URL name, reachable as {% url 'website:<name>' %}
    route: str         # Django route, relative to the site root
    template: str      # template under templates/pages/
    nav: str = ""      # top-level nav key to mark current (see partials/site_header.html)
    sample: bool = False  # slug is sample data today; model-backed later


PAGES: tuple[Page, ...] = (
    Page("home", "", "home.html"),

    # What We Do — one page per programme. These six collapse into a single
    # slug-driven view once the Programme model exists.
    Page("programme_improved_cookstove", "what-we-do/improved-cookstove/",
         "programme_improved_cookstove.html", nav="what-we-do"),
    Page("programme_rooftop_solar", "what-we-do/rooftop-solar/",
         "programme_rooftop_solar.html", nav="what-we-do"),
    Page("programme_safe_drinking_water", "what-we-do/safe-drinking-water/",
         "programme_safe_drinking_water.html", nav="what-we-do"),
    Page("programme_solar_irrigation", "what-we-do/solar-irrigation/",
         "programme_solar_irrigation.html", nav="what-we-do"),
    Page("programme_rural_productive_use_solar", "what-we-do/rural-productive-use-solar/",
         "programme_rural_productive_use_solar.html", nav="what-we-do"),
    Page("programme_low_emission_rice", "what-we-do/low-emission-rice/",
         "programme_low_emission_rice.html", nav="what-we-do"),

    # Projects
    Page("projects", "projects/", "projects.html", nav="projects"),
    Page("project_detail", "projects/green-ics-phase-1/", "project_detail.html",
         nav="projects", sample=True),
    Page("gallery", "gallery/", "gallery.html", nav="projects"),
    Page("gallery_album", "gallery/green-ics-installations-manikganj/",
         "gallery_album.html", nav="projects", sample=True),

    # Why GSSL
    Page("why_gssl", "why-gssl/", "why_gssl.html", nav="why-gssl"),

    # News & Insights (events and feedback sit under this nav item)
    Page("news", "news-insights/", "news.html", nav="news"),
    Page("news_article", "news-insights/how-mrv-works-for-rooftop-solar/",
         "news_article.html", nav="news", sample=True),
    Page("events", "events/", "events.html", nav="news"),
    Page("event_detail", "events/lsc-manikganj-2027/", "event_detail.html",
         nav="news", sample=True),
    Page("event_feedback_round", "events/feedback-round-ics-2026/",
         "event_feedback_round.html", nav="news", sample=True),
    Page("feedback", "feedback/", "feedback.html", nav="news"),

    # About Us
    Page("about", "about-us/", "about.html", nav="about"),
    Page("team", "about-us/team/", "team.html", nav="about"),
    Page("faq", "faq/", "faq.html", nav="about"),

    # Utility
    Page("enquire", "contact-us/", "enquire.html", nav="enquire"),
    Page("privacy", "privacy/", "privacy.html"),
)

PAGES_BY_NAME = {page.name: page for page in PAGES}
