# Green Spark Solutions Australia — Django site

The website for Green Spark Solutions Australia Pty Ltd. Page content is
static (templates plus a little data in `apps/website/content.py`); the
database holds only the admin login, sessions and the enquiries visitors send
through the contact form.

The original static design build lives in
[`../green-spark-website/`](../green-spark-website/). It is **frozen**: the
templates here are now the source of truth, and the converter that first
generated them is retired.

---

## Quick start

```bash
python -m venv ../.venv
../.venv/bin/pip install -r requirements.txt        # Windows: ..\.venv\Scripts\...
../.venv/bin/python manage.py migrate                # the contact form stores enquiries
../.venv/bin/python manage.py runserver
```

Open <http://localhost:8000>. Enquiries sent locally are printed in the
runserver console and listed at <http://localhost:8000/admin/> (create a login
with `manage.py createsuperuser`).

Run the checks before and after every change:

```bash
../.venv/bin/python manage.py test apps.website     # 58 tests
../.venv/bin/python tools/check_static_refs.py      # every /static/ reference exists
```

---

## Layout

```
gssl_site/
  manage.py                     defaults to config.settings.dev
  requirements.txt
  .env.example                  every setting, with production values

  config/
    settings/base.py            shared settings, CSP, email, logging
    settings/dev.py             DEBUG, console email, report-only CSP
    settings/prod.py            refuses to start without its required values
    urls.py                     admin (at ADMIN_URL) + website
    wsgi.py  asgi.py            entry points (default to prod settings)

  apps/website/
    pages.py                    THE SITE MAP — one row per page, with its status
    content.py                  the seven projects, as data
    views.py                    static pages, contact form, projects, robots, sitemap
    forms.py  models.py         the contact form and the Enquiry it saves
    mail.py                     emails an enquiry; never loses one
    admin.py                    enquiries in the Django admin
    middleware.py               Content-Security-Policy, Permissions-Policy
    tests.py                    58 tests

  templates/
    base.html                   the whole document shell
    partials/                   header, footer, menus, project card, ...
    pages/                      one template per page
    sitemap.xml

  static/                       CSS, JS, fonts, images, video
  deploy/                       gunicorn, systemd, nginx, release script

  tools/
    check_static_refs.py        ACTIVE  every /static/ reference exists
    self_host_photos.py         ACTIVE  re-download the stock photos (already done)
    convert_design_build.py     RETIRED would overwrite the templates. Do not run.
    check_parity.py             RETIRED the site has diverged from the design build
```

### Where to change things

| To change | Edit |
|---|---|
| Page text, markup | `templates/pages/<page>.html` |
| Header, footer, menus | `templates/partials/` |
| A project's text, location, stage, Gold Standard ID | `apps/website/content.py` |
| Take a page offline, or hide it from search | `status=` on its row in `apps/website/pages.py` |
| Adding or moving a URL | `apps/website/pages.py` |
| Where enquiries are emailed | `DJANGO_ENQUIRY_RECIPIENTS` |
| The live domain | `DJANGO_SITE_URL` — never a template |
| Colours, spacing, type | `static/css/tokens.css` (see the design build README) |

To **hide** a block of markup, wrap it in `{% comment %} HIDDEN: why … {% endcomment %}`
so it can come back by deleting the wrapper. Comments do not nest: dissolve any
inner wrapper first (a test checks).

---

## Pages and their status

Each row in `pages.py` has a status:

| Status | Routed | In menus | In sitemap | Used for |
|---|---|---|---|---|
| `LIVE` | yes | yes | yes | the site |
| `UNLISTED` | yes, `noindex` | no | no | pages GSSL hid from the menus (FAQ, Why GSSL) |
| `OFFLINE` | 404 | no | no | pages holding only design-build sample content |

| URL | Name | Status |
|---|---|---|
| `/` | `home` | live |
| `/what-we-do/<programme>/` (six) | `programme_*` | live |
| `/projects/` | `projects` | live |
| `/projects/<slug>/` (seven, from `content.py`) | `project_detail` | live |
| `/gallery/` | `gallery` | live |
| `/gallery/green-ics-in-the-field/` | `gallery_album` | live |
| `/events/` | `events` | live |
| `/about-us/`, `/about-us/team/` | `about`, `team` | live |
| `/contact-us/` | `enquire` | live (GET and POST) |
| `/privacy/` | `privacy` | live |
| `/faq/`, `/why-gssl/` | `faq`, `why_gssl` | unlisted |
| `/news-insights/…` (two) | `news`, `news_article` | offline — removed at GSSL's request; sample posts |
| `/events/lsc-manikganj-2027/`, `/events/feedback-round-ics-2026/` | `event_detail`, `event_feedback_round` | offline — invented sample events |
| `/feedback/` | `feedback` | offline — removed at GSSL's request |
| `/robots.txt`, `/sitemap.xml` | | generated from `pages.py` and `content.py` |

URLs end in a slash; the slash-less form (as on the current
greensparksolutions.com, e.g. `/about-us`) answers with a 301 to it.

---

## Contact form

`/contact-us/` posts to Django. With JavaScript, `forms.js` sends it with
`fetch()` and shows the success state from the JSON reply; without, the page
posts normally and redirects to `?sent=1`.

Every enquiry is **saved first**, then emailed to `DJANGO_ENQUIRY_RECIPIENTS`
if `DJANGO_EMAIL_HOST` is set. If email is not configured, or the mail server
fails, the enquiry is still in the admin (*Website › Enquiries*), with the
reason recorded on it. A hidden honeypot field drops bots silently, and more
than five messages in ten minutes from one visitor get a polite 429.

---

## Security

- **Content-Security-Policy**: `default-src 'self'`, no inline script or style.
  The templates have no inline `<script>`, no `on*=` handlers and no `style=""`
  (tests enforce it). Enforced in production, report-only in development.
- No third-party requests: fonts, scripts, photos and video are all served
  from the site itself. The six stock photos were self-hosted with
  `tools/self_host_photos.py`; credits are in the design build README §1b.
- HSTS (one year, subdomains), secure cookies, `X-Frame-Options: DENY`,
  `nosniff`, `Referrer-Policy`, `Cross-Origin-Opener-Policy`, `Permissions-Policy`.
- The admin path is set by `DJANGO_ADMIN_URL`; choose something other than `admin/`.
- `config.settings.prod` refuses to start without a secret key, allowed hosts
  and an `https://` site URL.

---

## Deployment

The example files in `deploy/` assume a Linux server with nginx and systemd.
Any host that runs a WSGI app can serve `config.wsgi:application` instead.

### Layout on the server

```
/srv/gssl/app        this repository (git clone)
/srv/gssl/venv       Python 3.12+ virtualenv
/srv/gssl/data       SQLite database — enquiries live here: back it up
/srv/gssl/static     collectstatic output, served by nginx
/etc/gssl/gssl.env   settings, from .env.example (root:gssl, mode 640)
```

### First deploy

```bash
sudo useradd --system --home /srv/gssl --shell /usr/sbin/nologin gssl
sudo mkdir -p /srv/gssl/{data,static} /etc/gssl
sudo git clone https://github.com/Deep-RB/Green-Spark-Solutions-LTD-Main-site.git /srv/gssl/app
sudo python3 -m venv /srv/gssl/venv
sudo chown -R gssl:gssl /srv/gssl

sudo cp /srv/gssl/app/gssl_site/.env.example /etc/gssl/gssl.env
sudoedit /etc/gssl/gssl.env               # secret key, domain, email, admin path
sudo chown root:gssl /etc/gssl/gssl.env && sudo chmod 640 /etc/gssl/gssl.env

sudo -u gssl /srv/gssl/app/gssl_site/deploy/release.sh
sudo -u gssl env DJANGO_ENV_FILE=/etc/gssl/gssl.env DJANGO_SETTINGS_MODULE=config.settings.prod \
    /srv/gssl/venv/bin/python /srv/gssl/app/gssl_site/manage.py createsuperuser

sudo cp /srv/gssl/app/gssl_site/deploy/gssl.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now gssl

sudo cp /srv/gssl/app/gssl_site/deploy/nginx.conf /etc/nginx/sites-available/gssl
sudo ln -s /etc/nginx/sites-available/gssl /etc/nginx/sites-enabled/gssl
sudo certbot --nginx -d greensparksolutions.com -d www.greensparksolutions.com
sudo nginx -t && sudo systemctl reload nginx
```

### Every release after that

```bash
cd /srv/gssl/app && sudo -u gssl git pull
sudo -u gssl gssl_site/deploy/release.sh   # pip, check --deploy, migrate, collectstatic
sudo systemctl reload gssl
```

`release.sh` stops at the first failure, so a broken release never reaches the reload.

### Environment

Required: `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_SITE_URL`.
Everything else is optional and documented in [`.env.example`](.env.example):
database and static paths, admin path, SMTP, enquiry recipients, HSTS.

**HSTS warning.** Production sends HSTS with `includeSubDomains` for a year.
Browsers will then refuse plain HTTP on *every* subdomain of the domain. The
current site uses `admin.greensparksolutions.com` and
`ics.greensparksolutions.com`; make sure every subdomain has HTTPS, or set
`DJANGO_HSTS_INCLUDE_SUBDOMAINS=0`, **before** the first deploy.

### Backups

`/srv/gssl/data/db.sqlite3` holds every enquiry. Back it up daily, for example:

```bash
sqlite3 /srv/gssl/data/db.sqlite3 ".backup '/var/backups/gssl/db-$(date +%F).sqlite3'"
```

---

## Go-live checklist

The full list of open content questions, with what was checked and how, is
in [`../AI-HANDOFF.md`](../AI-HANDOFF.md) §7. In short:

**GSSL must confirm** (the current greensparksolutions.com shows none of these):
Gold Standard IDs and registration status, Phase 2's location, the 20,000+ /
50,000 stove figures and their "as of" date, the CEO's name and title, opening
hours, social profile URLs, and a legal review of the privacy policy.

**Technical:**

- [ ] Server set up as above; `release.sh` runs clean
- [ ] `DJANGO_ADMIN_URL` changed from `admin/`; superuser created
- [ ] SMTP set; send a test enquiry and confirm it arrives at info@
- [ ] Every subdomain on HTTPS (or HSTS subdomains switched off)
- [ ] Decide what happens to the three Gold Standard notices the events page
      links to on the current site (see AI-HANDOFF.md §7)
- [ ] Daily backup of the database
- [ ] Sitemap submitted in Google Search Console
