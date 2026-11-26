# Green Spark Solutions Australia — website: context prompt

Paste this whole file as the opening message to another AI assistant so it can
pick up the work. It describes the project, the decisions already made, the
traps that have already cost time, and what is still open.

---

## 1. What this is

The website for **Green Spark Solutions Australia Pty Ltd**, a carbon project
developer working in Bangladesh, Nepal and Cambodia. It positions itself as a
**carbon credit aggregator platform**. Priority order across the whole site:

1. **Rooftop Solar MRV** — first priority, lead with this everywhere
2. **Improved Cookstoves (Green ICS)** — the registered, revenue-earning work
3. **Safe Drinking Water** — next in the pipeline

It is going live on Green Spark's own server and domain, so treat everything as
production work, not a prototype.

- Repo: `https://github.com/Deep-RB/Green-Spark-Solutions-LTD-Main-site` (private)
- Branches: `django-conversion` (PR #1 against `main`) holds the conversion;
  `claude/loving-hopper-gc5fhq` continues from it with the production pass (§5)
- Old static site, still live: `https://gssl.thingbd.com`
- Real company site: `https://greensparksolutions.com` (a Next.js site; see §7)

## 2. Repository layout

```
green-spark-website/     ORIGINAL static design build. FROZEN — never edit.
                         Its README.md is excellent: colour tokens, CSP policy,
                         CMS field map, photo credits (§1b), sample-data list (§11).

gssl_site/               The Django project. This is the live codebase.
  manage.py              defaults to config.settings.dev
  config/settings/       base.py / dev.py / prod.py
  apps/website/
    pages.py             THE SITE MAP — one row per page, with LIVE/UNLISTED/OFFLINE
    content.py           the 7 projects as data; drives every project page
    views.py             StaticPageView, EnquireView, ProjectDetailView, robots, sitemap
    forms.py models.py   contact form -> Enquiry (the only model)
    mail.py admin.py     enquiry email; enquiries in the admin
    middleware.py        CSP + Permissions-Policy
    tests.py             58 tests — run these before claiming anything works
  templates/             base.html, partials/, pages/, sitemap.xml
  static/                CSS, JS, fonts, photos, video (no third-party loads)
  deploy/                gunicorn.conf.py, gssl.service, nginx.conf, release.sh
  tools/
    check_static_refs.py      ACTIVE. Proves every /static/ reference exists.
    self_host_photos.py       ACTIVE. Already run; re-run only to refresh stock photos.
    convert_design_build.py   RETIRED. Would overwrite the templates. Do not run.
    check_parity.py           RETIRED. The site has diverged deliberately.
.github/workflows/ci.yml      tests on 3.12 + 3.13; prod job runs check --deploy,
                              migrate and collectstatic
```

`gssl_site/README.md` has the deployment guide and go-live checklist.

## 3. Stack and conventions

- Django 5.2 LTS, Python 3.12+, SQLite (admin, sessions, enquiries — **no
  content models yet**, page content is deliberately static)
- WhiteNoise serves static files with hashed names; nginx serves them in production
- Plain HTML5 + CSS + vanilla JS. Bootstrap 5.3.3 **grid only**. No CDN, no
  third-party request of any kind at runtime.
- **CSP-enforced**: no inline `<script>`, no `on*=` handlers, no `style=""`.
  A test fails on any of them. JS hooks use `data-*` attributes.
- Design tokens live in `static/css/tokens.css`, all prefixed `--gs-`
- The live domain is never hard-coded; it comes from `DJANGO_SITE_URL`
- Removed content is wrapped in `{% comment %} HIDDEN: why … {% endcomment %}`
  rather than deleted. Whole pages are taken down with `status=OFFLINE` in
  `pages.py`. Follow both conventions.

### Commands

```
cd gssl_site
../.venv/bin/python manage.py migrate                    # once; the form needs it
../.venv/bin/python manage.py runserver                  # dev server on :8000
../.venv/bin/python manage.py test apps.website          # 58 tests
../.venv/bin/python tools/check_static_refs.py           # 24 pages, ~263 refs
```

(On Windows: `../.venv/Scripts/python.exe`.)

## 4. Traps that have already cost time — read before editing

1. **`website.js` calls `GS.boot()`**, which runs every module registered up to
   that point. A component script loaded *after* it never runs. Page scripts go
   in `{% block component_scripts %}`, above it. A test enforces the order.
2. **Django `{# ... #}` comments only work on a single line.** Use `{% comment %}`.
3. **`{% comment %}` does not nest.** The first `{% endcomment %}` closes it; the
   rest of the hidden block renders, or the stray tag 500s the page. When you
   wrap a block that already contains a hidden item, dissolve the inner wrapper.
   A test checks every template.
4. **`reveal.js` keys off `[data-text-reveal]`, not `class="text-reveal"`.**
   Several modules work this way — check the attribute the JS actually queries.
5. **`.site-chrome` is `position: fixed`** and carries the header state. It, the
   spacer and the skip link live in `base.html`. Removing them breaks the header.
6. **Static assets cache hard in dev.** Hard-refresh, or verify with `curl`.
7. **Never edit files through PowerShell `Set-Content -Encoding utf8`** — BOM.
8. **`TemplateView.as_view(foo=...)`** only accepts existing class attributes.
9. **Entities in Python data get escaped.** Put real characters in `content.py`.
10. **Browser-pane measurements are meaningless when the pane is hidden.**
11. **A test that checks "the string appears somewhere on the page" proves
    little.** The project pages passed one for weeks while every page was still
    headed "Green ICS — Phase 1". Assert on the specific element.
12. **The design build's sample data is everywhere.** Its README §11 lists it.
    Removing a "Sample data" badge does not make the figure behind it true.

## 5. What has been done

**The conversion** (branch `django-conversion`). All 24 design-build pages became
Django templates, 11 shared partials, `{% url %}` / `{% static %}` everywhere.

**Front-end changes since:** hero slogan and aggregator copy; marquee removed;
home collage MRV-first; expanding cards MRV → About → Approach; pipeline below
"Project activities"; district map and "Have your say" hidden; Gallery moved to
About Us; FAQ / Why GSSL / Give feedback hidden from menus; events page rebuilt
with the **three real events**; pipeline trimmed to Safe Drinking Water; project
sidebar call button removed; WhatsApp → Contact us; button animation smoothed;
every project its own URL; Gold Standard logo rebuilt; MRV video on the Rooftop
Solar MRV page.

**Production pass** (branch `claude/loving-hopper-gc5fhq`):

- *Sample banners*: the "Design preview · sample data" ribbon (on by default in
  dev) is retired and its setting removed. Build notes that leaked into visible
  copy are gone: "Optional · new field 'enquiry type'", "New field 'phone'",
  "Time zone to be confirmed", "districts to confirm", and the privacy page's
  "Draft for GSSL legal review…" notice.
- *Contact form*: it posted to `#` with `data-demo="success"` — visitors were
  thanked and nothing was sent. Now a Django form: CSRF, server validation,
  saved to the `Enquiry` model, emailed when SMTP is set, listed in the admin,
  honeypot, throttle, works without JavaScript.
- *Project pages*: the heading, lead, narrative, attributes and badge were still
  Phase 1's on all seven pages, so Rooftop Solar MRV and the unregistered Nepal
  scoping both said "Green ICS — Phase 1 … registered with Gold Standard".
  Everything now comes from `content.py`; Gold Standard claims render only with
  a `gs_id`; stove-only sections only for stove projects; the related strip
  never shows the page's own project.
- *Sample content offline*: News & Insights (GSSL asked for it to go; all posts
  were samples), the two invented events (a 2027 Manikganj LSC and a feedback
  round "open until 9 January 2027", which the home page advertised), and the
  feedback page. The nav's News dropdown is now one link, **Events &
  Consultations**. The five invented gallery albums are hidden; the real one is
  "Green ICS in the field · 9 photos". Fake pagination removed. The cookstove
  page's district map + sample counters (95,000 people, 10 districts, 38,400
  visits) hidden, matching the same section GSSL hid on the home page.
- *Social icons*: Facebook / YouTube / LinkedIn pointed at the platforms' home
  pages (so does the current live site). Hidden until real URLs exist; WhatsApp kept.
- *Photos*: the six stock photos hot-linked Pexels/Unsplash, with a grey
  "Field photo" placeholder as fallback — which is what the Rooftop Solar MRV
  and Nepal project pages actually showed. Now self-hosted at 480/960/1600.
- *Security/ops*: strict CSP, Permissions-Policy, HSTS with env overrides
  (preload opt-in), admin path from env, prod refuses to start without secret
  key / hosts / https site URL, SQLite in WAL mode at a configurable path,
  robots.txt + sitemap.xml from the site map, `noindex` on unlisted pages,
  server errors emailed to `DJANGO_ADMINS`, deploy kit in `gssl_site/deploy/`.
- *Verified*: 58 tests; prod settings through gunicorn over HTTPS; every
  published page in Chromium at 1440px and iPhone 13 — no console errors, no
  CSP violations, no failed or third-party requests, no overflow; form tested
  end to end; video byte ranges (206) work.

## 6. Project pages — how they work

```
/projects/rooftop-solar-mrv/
/projects/green-ics-phase-1/                GS13141
/projects/green-ics-phase-2/                GS23304
/projects/green-ics-phase-3/
/projects/community-monitoring/
/projects/stove-design-and-manufacturing/
/projects/clean-cooking-scoping-nepal/
```

`content.py` holds one `Project` row each: title, summary, location, stage,
photo, programme, `gs_id`, standard, badge, status label and note, description
paragraphs, and `stove_detail` (show the Green ICS attributes, how-it-works and
field photos). Every description sentence is copy that already existed on the
site; replace with GSSL's per-project copy when it arrives. Cards elsewhere use
`partials/project_card.html`.

This is the pattern for Programme, Event, Post and Album when the admin panel
arrives: static dataclasses now, swap the source later, templates unchanged.

## 7. Still open

### GSSL must confirm before launch

None of these can be checked from public sources. The current
greensparksolutions.com (fetched 26 Nov 2026) shows **no** headline figures, no
Gold Standard IDs, no news and no team page, and the Gold Standard registry
blocks automated lookups.

| Item | Where | What we know |
|---|---|---|
| **GS13141 / GS23304, and "registered"** | home, cookstove page, projects, Phase 1/2 pages | Not verifiable here. The current site's June 2025 notices describe GREEN ICS BANGLADESH PART 2 and PART 3 as going through Gold Standard stakeholder consultation. Open each registry link by hand. |
| **Phase 2 location** | `content.py`, projects page | Site says "Dhaka and Rajshahi divisions". The current site's notices put **PART 2 in Khagrachhari (Chittagong)** and **PART 3 in Bagerhat (Khulna)**. The design README already flagged this location as sample data. If Phase 2/3 = Part 2/3, correct it. |
| **20,000+ installed (Phase 1), 50,000 planned (Phase 2)** | home collage + carousel, cookstove phases, projects | From GSSL's brief; design README: "GSSL to approve before publishing". The "Figures as of 30 September 2026" date is the designer's. |
| **CEO name and title** | team page | Site: "Pankaj Rajbangshi, Director and CEO". Current site's notices: "Pankaj Kumar Rajbangshi, Managing Director". |
| **Opening hours** | top bar, footer, contact page | "Every day, 9 AM – 5 PM", no time zone; the current site shows none. |
| **Privacy policy** | `/privacy/` | Its own note said: have it legally reviewed before going public. ABN and retention periods also unconfirmed. |
| **Social profile URLs** | `partials/social_links.html` | Three icons hidden until supplied. |
| **Programme stages** | the five pipeline programme pages | Concept / Feasibility labels are design-build samples. |
| **Bangladesh phone** | contact details | The current site also lists +8801741587494; this site only the Australian number. |

### Decisions

| Item | Notes |
|---|---|
| **Domain switch and the three Gold Standard notices** | The events page links to the notices on `greensparksolutions.com/events/…`. If this site takes over that domain, those links 404 — and they are public consultation records. Either keep the old site on a subdomain and repoint the links, or rebuild the notices here at the same paths (`/events/green-ics-bangladesh` etc.). That needs the original text, agenda and photos from GSSL; only summaries were retrievable, and they mention enclosed documents that are not linked anywhere. |
| **HSTS and subdomains** | Production sends `includeSubDomains`. The current site uses `admin.` and `ics.greensparksolutions.com`; all must serve HTTPS, or set `DJANGO_HSTS_INCLUDE_SUBDOMAINS=0`. |
| **SMTP** | Client paused email. Enquiries are saved and visible in the admin regardless; set `DJANGO_EMAIL_*` to have them emailed. |
| **Feedback page** | Offline at GSSL's request. Its form was never wired; reuse `EnquireView`'s pattern before bringing it back. Gold Standard projects need a grievance channel — the contact form and WhatsApp currently serve. |

### Features still to build

| Item | Notes |
|---|---|
| **Hero video re-order** | MRV straight after the forest shots. Needs a re-render from source via `render.py`; source clips not supplied. |
| **MRV prioritisation** | Done on home. Other pages still need MRV-first ordering and "carbon credit aggregator platform" wording. |
| **Home project summary list** | Each project with a short summary below "Project activities on the ground", clicking through. `partials/project_card.html` + `content.PROJECTS` make this small. |
| **Safe Drinking Water pipeline card** | Needs a GSSL image. Do not invent a stock URL. |
| **Gold Standard logo on dark** | The home carousel shows the dark wordmark over a dark photo. Check contrast. |
| **Events PDFs** | None exist online; must come from GSSL. |

## 8. How to work on this

1. Run the tests before and after. 58 should pass.
2. Run `tools/check_static_refs.py` after touching any asset path.
3. Verify in a browser with the preview pane **visible**, and hard-refresh.
4. Do not fabricate project facts, figures, dates or Gold Standard IDs. This is a
   carbon-credit business and wrong numbers on a live site are a real problem —
   Australian regulators actively pursue misleading environmental claims. If
   content is missing, say so and ask.
5. Add a regression test when you fix something that was silently broken.
