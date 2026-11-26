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
- Working branch: `django-conversion`, open as PR #1 against `main`
- Old static site, still live: `https://gssl.thingbd.com`
- Real company site: `https://greensparksolutions.com`

## 2. Repository layout

```
green-spark-website/     ORIGINAL static design build. FROZEN — never edit.
                         Byte-identical to what is live at gssl.thingbd.com.
                         Its README.md is excellent: colour tokens, CSP policy,
                         CMS field map, loop markers, pre-launch checklist.

gssl_site/               The Django project. This is the live codebase.
  manage.py              defaults to config.settings.dev
  config/settings/       base.py / dev.py / prod.py
  apps/website/
    pages.py             THE SITE MAP — one row per static page, drives URLs + nav
    content.py           Project data (7 projects), drives per-project pages
    views.py             StaticPageView + ProjectDetailView
    urls.py              generated from pages.py, plus the project slug route
    context_processors.py    site_url, site_name, show_preview_ribbon
    tests.py             25 tests — run these before claiming anything works
  templates/
    base.html            the whole document shell
    partials/            12 shared partials
    pages/               one template per page
  static/                copied from the design build's assets
  tools/
    convert_design_build.py   RETIRED. Would overwrite the templates. Do not run.
    check_parity.py           RETIRED. The site has diverged deliberately.
    check_static_refs.py      ACTIVE. Proves every /static/ reference exists.
.github/workflows/ci.yml      tests on Python 3.12 + 3.13, plus a prod build job
```

**Critical:** `templates/` is now the source of truth. The converter that
generated it is retired because the site has intentionally diverged from the
design build. Running it would destroy the front-end work.

## 3. Stack and conventions

- Django 5.2 LTS, Python 3.12+, SQLite (only for admin/sessions — **no content
  models yet**, the site is deliberately static)
- WhiteNoise serves static files with hashed names in production
- Plain HTML5 + CSS + vanilla JS. Bootstrap 5.3.3 **grid only**. No CDN at runtime.
- **CSP-safe by design**: no inline `<script>`, no `on*=` handlers, no `style=""`.
  Keep it that way. JS hooks use `data-*` attributes.
- Design tokens live in `static/css/tokens.css`, all prefixed `--gs-`
- The live domain is never hard-coded; it comes from `SITE_URL` in settings
- Removed content is wrapped in `{% comment %}` rather than deleted, so it can be
  restored by deleting one wrapper. Follow this convention.

### Commands

```
cd gssl_site
../.venv/Scripts/python.exe manage.py runserver          # dev server on :8000
../.venv/Scripts/python.exe manage.py test apps.website  # 25 tests
../.venv/Scripts/python.exe tools/check_static_refs.py   # 29 pages, 241 refs
```

## 4. Traps that have already cost time — read before editing

1. **`website.js` calls `GS.boot()`**, which runs every module registered up to
   that point. A component script loaded *after* it registers too late and
   silently never runs. This broke the hero video. `base.html` has a
   `{% block component_scripts %}` **above** `website.js` for page-specific
   scripts, and a test enforces the ordering.
2. **Django `{# ... #}` comments only work on a single line.** A multi-line one
   renders as visible text on the page. Use `{% comment %}`.
3. **`reveal.js` keys off `[data-text-reveal]`, not `class="text-reveal"`.** The
   scroll-fill effect was dead site-wide because the markup only had the class.
   Several modules work this way — check the attribute the JS actually queries.
4. **`.site-chrome` is `position: fixed`** and carries the header state
   (`.is-scrolled`, `.is-hidden`, `.menu-open`) plus the transparent-over-dark-
   hero treatment. It, `.site-chrome__spacer` and the skip link live in
   `base.html`. Removing them breaks the sticky header on every page.
5. **Static assets cache hard in dev.** After editing CSS or images, hard-refresh
   or you will be looking at the old file and chasing a ghost. Verify with
   `curl localhost:8000/static/...` rather than trusting the browser.
6. **Never edit files through PowerShell `Set-Content -Encoding utf8`** — it adds
   a BOM and mangles em dashes. Use Python or an editor tool. A test now fails on
   any template containing a BOM.
7. **`TemplateView.as_view(foo=...)`** only accepts kwargs that already exist as
   class attributes with a value. An annotation alone is not enough.
8. **Entities in Python data get escaped.** Put real characters in `content.py`,
   not `&mdash;`.
9. **Browser-pane measurements are meaningless when the pane is hidden** —
   viewport reads 0x0 and IntersectionObserver never fires, so reveals, counters
   and the hero video all look broken when they are fine.

## 5. What has been done

**The conversion.** All 24 design-build pages became Django templates. The design
build marked every repeated block with `<!-- partial:start NAME -->`, so the
conversion was mechanical and verified: 11 shared partials, active nav state as
`{% if %}` conditionals, `{% url %}` for all 1,886 internal links, `{% static %}`
for all assets.

**Front-end changes since:**

- Hero: "Why GSSL" button removed; slogan is now "Climate impact, measured and
  verified." with aggregator-platform copy
- The "what we do" marquee band removed
- Home collage reordered — **MRV first**, then clean cooking, then safe water —
  and all three link through to their programme page
- The three expanding cards are now Rooftop Solar MRV → About Green Spark →
  Our approach
- "Next in our pipeline" moved below "Project activities on the ground"
- District map and the events / "Have your say" section hidden via `{% comment %}`
- Gallery moved from the Projects menu into About Us
- **FAQ, Why GSSL and Give feedback hidden** from header, mobile menu, footer and
  footer legal row. Routes still exist; only the links are hidden.
- Events page rebuilt with the **three real events** from greensparksolutions.com
  (Khagrachhari LSC 18 Jun 2025, Bagerhat LSC 25 Jun 2025, Khagrachhari feedback
  round 25 Jun – 24 Jul 2025), with venues, dates and links to each notice
- Pipeline trimmed to **Safe Drinking Water only**
- Project sidebar: Call button removed; "Stoves installed 20,000+" is now
  "Stove installation: Ongoing — temporarily paused"
- Enquire page: "WhatsApp us" became "Contact us" (mailto)
- Button animations smoothed — the `btn-roll` label flip cut between keyframes;
  replaced with an eased lift
- **Every project now has its own page** (see section 6)
- 21 "Sample data" badges removed with the figures kept; four build notes that
  were leaking into visible copy removed
- Gold Standard logo rebuilt at 902x214 transparent (was 451x90 and soft), one
  PNG/WebP pair used everywhere, the `-on-dark` variant retired
- MRV platform video embedded on the Rooftop Solar MRV page below the hero

## 6. Project pages — how they work

The design build shipped **one** project-detail page holding Phase 1's content,
and all seven cards pointed at it, so Phase 2 and Phase 3 opened Phase 1. Fixed:

```
/projects/rooftop-solar-mrv/
/projects/green-ics-phase-1/                GS13141
/projects/green-ics-phase-2/                GS23304
/projects/green-ics-phase-3/
/projects/community-monitoring/
/projects/stove-design-and-manufacturing/
/projects/clean-cooking-scoping-nepal/
```

`apps/website/content.py` holds one `Project` row each — title, summary,
location, stage, photo, Gold Standard id, standard. `project_detail.html` is
driven by it: metadata, hero photo, accent colour, key-details sidebar. The
registry button and the "Registered with Gold Standard" card render **only** when
`project.gs_id` is set — previously every project claimed GS13141, including
Nepal scoping, which is not registered at all.

This is the pattern to follow for Programme, Event, Post and Album when the admin
panel arrives: static dataclasses now, swap the source later, templates unchanged.

## 7. Still open

| Item | Notes |
|---|---|
| **Hero video re-order** | Client wants MRV straight after the forest shots. Current order: Forest (0–4.4s) → Hill (4.4–6.6s) → Stove (6.27–12.47s) → **Solar/MRV (12.47–16.27s)** → Water (16.27–21.67s). Re-cutting the finished file breaks two things: the stove section opens mid-crossfade (starts 10 frames early) and the final shot dissolves into the forest opening to hide the loop point. A clean fix needs a re-render from source via the supplied `render.py`, but the source clips (3 Pexels downloads + GSSL stills) were not supplied. ffmpeg is not installed. |
| **Enquiry form to email** | Paused by the client. Needs SMTP settings via env vars to info@greensparksolutions.com, and ideally a model so enquiries are not lost if mail fails. |
| **News & Insights dropdown** | Client said "remove these three", meaning News & insights / Events & consultations / Give feedback. Only Give feedback is hidden so far. Client wants **only Events and Consultation rounds — no Feedback**. |
| **MRV prioritisation** | Done on the home page. Remaining pages still need MRV-first ordering and "carbon credit aggregator platform" wording. |
| **Home project summary list** | Client wants each project listed with a short summary below "Project activities on the ground", each clicking through. Now unblocked, since the project pages exist. |
| **Safe Drinking Water pipeline card** | Needs a new image. Do not invent a stock URL; verify it loads first. |
| **Gold Standard logo on dark** | The `-on-dark` variant was retired per instruction, so the home project carousel now shows a dark-grey wordmark over a dark photo. Check the contrast. |
| **Events PDFs** | Client asked for "all the pdf and date". The dates are in. **There are no PDFs** — all three source pages say documents "are enclosed" but link none: no PDF links, no iframes, no mention in the markup. The files must come from the client. |
| **Pre-launch** | Section 11 of `green-spark-website/README.md` lists sample data still needing GSSL sign-off. `tools/self-host-photos.py` should be run so no photo loads from a third-party server. |

## 8. How to work on this

1. Run the tests before and after. 25 should pass.
2. Run `tools/check_static_refs.py` after touching any asset path.
3. Verify in a browser with the preview pane **visible**, and hard-refresh.
4. Do not fabricate project facts, figures, dates or Gold Standard IDs. This is a
   carbon-credit business and wrong numbers on a live site are a real problem. If
   content is missing, say so and ask.
5. Add a regression test when you fix something that was silently broken —
   several bugs here were invisible until a test pinned them.
