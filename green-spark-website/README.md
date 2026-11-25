# Green Spark Solutions Australia — website design (v1.0)

Static design build for the new greensparksolutions.com, prepared by **ThingBD** to be converted into Django templates. Plain HTML5, CSS and vanilla JavaScript. Bootstrap 5.3.3 is used **for the grid only**; every visual style is our own.

- **Open it:** double-click `website/index.html` (relative paths, works from `file://`). The component library is `components/index.html`.
- **One-file preview:** `../green-spark-preview.html` holds every page in a single file (fonts and images inlined, page switching built in, "All pages" menu bottom-left). Use it for screenshots and comments. It is a review copy only: it uses inline CSS/JS and must never be deployed.
- **Motion reference:** structure, motion and rhythm follow climateimpact.com (full-bleed hero with a drawn line, logo-style marquee, collage with a drawn route, expanding cards that grow to full bleed, floating tiles, background-crossfade carousel, big CTA flush to the footer, black footer with a giant outlined wordmark). Content, artwork and code are original.

> **Update, 25 November 2026.** One company everywhere (the two office addresses appear only in the footer); one phone (+61 402 832 972) and one email (info@greensparksolutions.com); WhatsApp is the main contact channel (floating button on every page, top bar, menu, Enquire page with QR code); every "Contact us" is now **Enquire**; header order follows climateimpact.com: **What We Do ▾ · Projects ▾ · Why GSSL · Events · About Us · [Enquire]**; the Improved Cookstove Programme is one of six programmes, not the main one; new **Why GSSL** page and **Careers at GSSL** section on About; a new hand-drawn icon set in the logo green; photo cards have no icons below the photo, and their headings sit outlined until the card is hovered, focused or tapped, when they glow green.

> **Update 2, 25 November 2026.** Three **priority programmes** lead the site, in this order: **Clean Cooking** (improved cookstoves), **Rooftop Solar MRV** and **Safe Drinking Water**; Solar Irrigation, Rural Productive-Use Solar and Low-Emission Rice follow in sequence everywhere (menus, footer, pipeline). The supplied GIFs (night theme) are converted to looping MP4s (about 10× smaller than the GIFs, same 25 fps) and used in: the home collage cards (with floating, tilt, pulsing pins and a flowing route), a new **Priority programmes** showcase on the home page (auto-advancing tabs), and a "How it works" band on the three priority programme pages. A **Meet GSSL** button (home and About heroes) opens a 34-second intro film in a video modal. New **News & Insights** (menu, listing with filters, article template, latest posts on the home page). Header: What We Do ▾ · Projects ▾ · Why GSSL · News & Insights ▾ · About Us · [Enquire]; Events now sit under News & Insights.


> **Update 3, 25 November 2026 (live at https://gssl.thingbd.com).**
> - **Domain:** canonical, Open Graph and share links now use `https://gssl.thingbd.com`. Change it in one search-and-replace when the final domain is chosen.
> - **Home hero:** a “WELCOME | TO GREEN SPARK SOLUTIONS” badge (logo-green tag, Open Sauce Sans) sits above the headline; the small per-slide eyebrows were removed.
> - **Gold Standard:** registered projects show the Gold Standard “certified SDG impacts” mark (transparent PNG/WebP in `img/logo/`, plus an `-on-dark` version) and a separate registry button. **Phase 1 → GS13141, Phase 2 → GS23304** — please confirm this mapping. Links: `https://registry.goldstandard.org/projects?q=GS13141&page=1&countries=BD` and `…q=GS23304…`. Shown on the home projects carousel, Projects, Project detail, the Improved Cookstove phases and the FAQ.
> - **No document fields:** all document lists and “Download …” buttons were removed (project detail, event detail, feedback round). The project page links to the public Gold Standard record instead.
> - **Animations:** removed from the home priority showcase, the home collage and the news article. Each priority programme page (clean cooking, rooftop solar MRV, safe drinking water) and the project page now has one small “In three steps” section: three cards, each with a short white-line loop (`video/small/<programme>-1|2|3.mp4`, 426×300, 30–70 KB), a title and one sentence.
> - **Solid text only:** no outlined, faded or see-through text anywhere (photo-card titles, Why Green Spark list, project carousel, footer links, letter-by-letter intro reveal and the giant footer wordmark were changed or removed). Muted text uses solid colours.
> - **Photo cards:** programme chips/icons removed from every photo card. Cards now show real (stock) photos from Unsplash and Pexels instead of illustrations — see section 1b for credits, self-hosting and swapping in GSSL's own photos.
> - **About Us** is now a dropdown (desktop mega menu and mobile submenu): About GSSL, **Our team** (new `team.html`), **Careers** (`about-us.html#careers`) and **FAQ**. The footer Company column lists the same pages.
> - **New pages:** `team.html` (leadership + teams; names, roles and photos to confirm), `faq.html` (20 questions in five topics, accordion) and `privacy.html` (full policy, draft for legal review).
> - **WhatsApp:** the floating “WhatsApp us” button is gone from every page, and the mobile menu now offers Enquire + Call. WhatsApp stays as a contact channel (top bar, contact details, contact and feedback pages).
> - **Footer logo** reads “SOLUTIONS AUSTRALIA PTY LTD” (`img/logo/gssl-logo-pty-ltd.svg` and `-light.svg`).


> **Update 4, 25 November 2026.**
> - **GSSL's own photos** now fill the photo cards, project carousel backgrounds, "Why Green Spark" backgrounds, news cards, gallery album, project gallery and About pages. Field photos were cropped to remove the GPS Map Camera stamps (no village names or coordinates), clipboards/ID cards are blurred, and all location metadata (EXIF) is stripped. Files: `img/photos/` (`clean-cooking`, `ics-phase-1|2|3`, `monitoring`, `field-visit`, `team`, `kitchen-portrait`, `gallery-1…9`).
> - **Green ICS product photos** replace the illustrated stove: the single-burner / double-burner tabs switch between the two real product photos (`green-ics-single`, `green-ics-double`).
> - **Rooftop Solar MRV** added after Green ICS Phase 2 in the home projects carousel and on the Projects page.
> - **Animations:** the white (daylight) versions now run in the "In three steps" sections (`video/day/<programme>-1|2|3.mp4`, cut from the supplied daylight GIFs).
> - **Preloader:** the GSSL spark shows on a linen screen while a page loads, then fades (like climateimpact.com). Partial `preloader`; hidden by `website.js`, with a CSS fail-safe after 4 s.
> - **Removed:** the notice bar above the header, the priority-programmes showcase on the home page, and one employee card on the Team page. The large "Green Spark" wordmark is back at the foot of the footer, in solid low-contrast type.


> **Update 5, 25 November 2026.**
> - **Video hero:** the home page hero now plays GSSL's 21.7-second footage loop (`video/hero/`, wide and tall cuts, WebM + MP4, poster first). It pauses off screen, respects reduced motion and Save-Data, and has a pause/play button. Script: `js/components/video-hero.js` (CSP-safe, no inline code). The illustrated slideshow is retired.
> - **Hero copy:** the WELCOME | TO GREEN SPARK SOLUTIONS badge stays; the headline is now "Cleaner kitchens. Clearer skies." ("Partner in building a clean planet." remains in the green band above the footer).
> - **Meet GSSL:** the "Meet GSSL" button opens GSSL's own film (`video/meet-gssl.mp4`, re-encoded to 720p, about 10 MB, with sound).

---

## 1. Folder structure

```
green-spark-website/
  README.md
  components/index.html            component library + every state
  website/
    index.html  about-us.html  why-gssl.html  news.html  news-article.html  projects.html  project-detail.html
    improved-cookstove.html        → /what-we-do/improved-cookstove
    events.html  event-detail.html  event-feedback-round.html  feedback.html
    gallery.html  gallery-album.html  contact-us.html (Enquire)  privacy.html  404.html
    programme.html                 → /what-we-do/<slug>  (template, sample: Safe Drinking Water)
    programme-solar-irrigation.html, programme-rooftop-solar.html,
    programme-rural-productive-use-solar.html, programme-low-emission-rice.html
                                   (same template, other sample data — one Django template)
  assets/
    css/tokens.css  base.css  website.css
    css/components/  buttons header slider sections cards badges stats flow forms lightbox tabs accordion map misc footer (.css)
    js/components/   core nav notice-bar slider hero-canvas reveal scroll-scenes counters map lightbox modal tabs accordion forms events glow media showcase (.js)
    js/website.js
    fonts/           Open Sauce Sans 300/400/500/600 (Latin subset, WOFF2) + OFL licence
    img/logo/        gssl-mark.svg (the ORIGINAL GSSL spark, traced to vector from the supplied PNG, #00AC36), gssl-mark-white.svg,
                     gssl-logo.svg / -light / -mono-ink (spark + wordmark lock-ups), gssl-logo-original.png (supplied file)
    img/icons/       62 SVG icons: 56 hand-drawn in the logo green (marker stroke + lighter retrace, like the spark) + 6 brand/social marks
    video/           meet-gssl.mp4 (+ -poster.jpg): GSSL's Meet GSSL film, 1 min 55 s, 1280×720, voice-over + burned-in captions
    video/hero/      gs-hero(.webm|.mp4) 1920×1080 + gs-hero-mobile 720×1280: 21.7 s silent home-hero loop, with posters
    video/day/       cooking|mrv|water-1|2|3.mp4 (+ .jpg posters): daylight step-card loops cut from the supplied daylight GIFs;
                     decorative, muted, play only while on screen
    img/qr/          whatsapp-qr.svg (opens a WhatsApp chat with +61 402 832 972; verified by scanning)
    img/illustrations/  10 illustrated scenes × 6 sizes (WebP + JPEG) + grain.webp
    img/photos/      photo slots: photos.json (stock photo list + credits) and <slot>-480|960.jpg/.webp local files (fallback placeholders)
    img/logo/        + gold-standard-certified-sdg-impacts.png/.webp (+ -on-dark), gssl-logo-pty-ltd(-light).svg
    img/map/         bangladesh-districts.svg
    img/favicon/     favicon.ico/.svg, 32px, apple-touch-icon, 192/512, site.webmanifest
    vendor/bootstrap-5.3.3/  bootstrap-grid.min.css + LICENSE
  tools/self-host-photos.py        downloads the stock photos into the slots and points pages at the local files
  tools/make-photo-sizes.py        turns one real photo into a slot's four files
```

## 1b. Photo cards: stock photos and photo slots

Photo cards use **GSSL's own field and product photos** wherever one fits (cookstove projects, monitoring, team, gallery, Green ICS product viewer). Topics with no GSSL photo yet (rooftop solar, water, irrigation, rural solar, rice, Nepal) use **free-licence stock photos** from Unsplash and Pexels until GSSL has its own. Both licences allow free commercial use without attribution; we credit the photographers here anyway. Do not use them in a way that suggests the people shown endorse GSSL or take part in its programmes.

| Slot | Photo | Photographer | Source |
|---|---|---|---|
| `rooftop-solar` | Solar panels on the roof of a commercial building | Kindel Media | [Pexels](https://www.pexels.com/photo/9799994/) |
| `safe-water` | A clear glass of drinking water on a wooden table | Stephan Müller | [Pexels](https://www.pexels.com/photo/928854/) |
| `solar-irrigation` | A farmer working on an irrigation pump in green farmland | Ravinder Ravi | [Pexels](https://www.pexels.com/photo/29519027/) |
| `rural-solar` | Solar panels in a green countryside field | K (Kelly) | [Pexels](https://www.pexels.com/photo/4320475/) |
| `low-emission-rice` | Sunset over rice fields, Sonagazi, Bangladesh | Tamim Arafat | [Unsplash](https://unsplash.com/photos/OEJjBmy48Wg) |
| `nepal-scoping` | Green hills and villages in Nepal | BiZay Sunuwar | [Pexels](https://www.pexels.com/photo/34766893/) |

**How they load.** Each card loads its photo from the Unsplash or Pexels image server (`<picture data-photo="slot">`). If that fails (offline, or a Content-Security-Policy `img-src 'self'`), `website.js` swaps in the local file `assets/img/photos/<slot>-960.jpg`, which is a neutral "Field photo" placeholder.

**Before launch, self-host them** (one command on any computer with internet; removes third-party requests and works with a strict CSP):

```
pip install Pillow
python3 tools/self-host-photos.py
```

**Use GSSL's own photo for a slot:**

```
python3 tools/make-photo-sizes.py ~/Pictures/stove-kitchen.jpg clean-cooking
```

If the pages still point at the stock photo for that slot, run `tools/self-host-photos.py` first (it switches every page to the local files), then replace the slot. Use GSSL's own photos with consent; never show household names, phone numbers or village-level locations in captions.

## 2. Colour palette — and why

| Role | Token | Hex | Use |
|---|---|---|---|
| Canopy ink | `--gs-ink-900` | `#0B1D17` | Text, dark sections, buttons on light |
| Canopy deep | `--gs-ink-950` | `#06130F` | Hero base, footer, notice bar |
| Leaf (logo green) | `--gs-leaf-500` | `#00AC36` | Exact green of the GSSL logo: the spark mark, icons, map highlight |
| Leaf text | `--gs-leaf-700` | `#157A3F` | Green text and links on light (4.9:1 on linen) |
| **Spark** (action) | `--gs-spark-400` | `#C4EE5A` | Primary buttons, accents on dark — always with ink text (14:1) |
| Linen | `--gs-linen-100` | `#F6F3EC` | Page background |
| Stone | `--gs-stone-500` | `#5B635E` | Secondary text (5.4:1 on linen) |

**Rationale.** Climate-finance audiences expect calm, credible surfaces; communities and field partners need contrast that holds up outdoors on a phone. A near-black canopy green and warm linen give the formal, editorial tone of the reference site, and every text pair passes WCAG AA (most pass AAA). The original logo and its exact green (`#00AC36`) stay as the brand mark, while the action colour moves to a lime **spark**: it reads as "Green Spark" next to the logo, is not a stock green, and black-on-lime is the most legible pairing in bright sunlight. The old site green `#52B864` is not used.

**Programme colours** (each always shown with its name and icon, never colour alone):

| Programme | Token | Hex | Icon |
|---|---|---|---|
| Improved cookstoves | `--gs-prog-cookstove` | `#E46A2E` ember | flame |
| Safe drinking water | `--gs-prog-water` | `#2C9AC7` river | droplet |
| Solar irrigation | `--gs-prog-irrigation` | `#EDB21F` sun | pump |
| Rooftop solar | `--gs-prog-rooftop` | `#5568E0` volt | home-solar |
| Rural productive-use solar | `--gs-prog-rural` | `#13A08F` field | snowflake |
| Low-emission rice | `--gs-prog-rice` | `#94A834` paddy | sprout |

Each has an `-ink` (text) and `-tint` (background) variant. Use `data-programme="water"` on any element to get `--prog`, `--prog-ink`, `--prog-tint`.

### Logo

The site uses the **original GSSL spark**. It was traced from the supplied PNG into an SVG path (same shape, same green `#00AC36`, on light and dark backgrounds) so it stays sharp at any size; nothing was redrawn. The header and footer pair it with a "Green Spark / Solutions Australia" wordmark in Open Sauce Sans. Pages include the spark once in a hidden SVG sprite (`partial: svg-sprite`, `<symbol id="gs-mark">`) and reference it with `<use href="#gs-mark">`, because the traced path is ~30 KB.

## 3. Tokens (adopted by the MRV platform)

All tokens are in `assets/css/tokens.css` with the `--gs-` prefix. Components only use tokens.

- **Colour:** `ink-950…600`, `leaf-100/500/600/700`, `spark-100/300/400/500`, `linen-0…400`, `stone-500/600`, `prog-*` (+ `-ink`, `-tint`), `success/warning/danger/info-100/700`.
- **Semantic roles:** `--gs-color-bg, -surface, -surface-alt, -text, -text-muted, -border, -border-strong, -primary, -primary-hover, -primary-active, -on-primary, -brand, -link, -focus, -inverse-*, -overlay`. `.theme-dark` re-maps the roles for dark sections (the MRV dark mode can reuse this).
- **Type:** `--gs-font-sans`, `--gs-font-bn` (future Bangla), weights `300/400/500/600`, sizes `fs-display, h1–h4, lead, body, small, xs, stat` (fluid `clamp()`), line-heights `tight/snug/body`, letter-spacing `tight/stat/caps`.
- **Space:** `--gs-space-1…32` (4px base), `--gs-section-y`, `--gs-gutter`.
- **Layout:** `--gs-container` 1440px, `--gs-container-text` 46rem, `--gs-header-h` 80px.
- **Radius:** `xs 3 · sm 5 · md 8 · lg 14 · xl 22 · pill`.
- **Elevation:** `--gs-shadow-sm/md/lg`.
- **Motion:** `--gs-ease`, `--gs-ease-out`, `--gs-ease-in`, `--gs-dur-fast .2s / dur .4s / dur-slow .8s`, `--gs-dur-slide 7s`. All set to 0 under `prefers-reduced-motion`.
- **Layers:** `--gs-z-header 100 · menu 110 · modal 200 · toast 300 · ribbon 400`.

## 4. Fonts, licences and libraries

| Item | Version | Licence | Notes |
|---|---|---|---|
| Open Sauce Sans (Light, Regular, Medium, SemiBold) | 1.478 | SIL OFL 1.1 (`assets/fonts/OFL-open-sauce-sans.txt`) | Latin subset, ~11 KB per weight, `font-display: swap`, tabular figures (`tnum`) for data. The MRV platform uses the same family. For Bangla later: Hind Siliguri or Noto Sans Bengali via `--gs-font-bn`. |
| Bootstrap grid | 5.3.3 | MIT | `bootstrap-grid.min.css` only (grid, flex, spacing, display). No Bootstrap JS. |
| Logo | supplied by GSSL | © GSSL | Original spark traced to SVG (potrace); colour unchanged. |
| Icons | own | © GSSL / ThingBD | Hand-drawn for this project in the logo green `#00AC36` (Nov 2026 set). Inline icons use `.icon` + `.icon__echo` (the lighter retrace stroke). Social marks are simplified brand glyphs, used as plain links. |
| Illustrations | own | © GSSL / ThingBD | Procedural placeholders; real field photos come from the CMS. |
| District boundaries | geoBoundaries gbOpen BGD ADM2 (2023 build) | CC BY 3.0 IGO | Source: Bangladesh Bureau of Statistics / OCHA ROAP via HDX. Simplified for web. Attribution kept in the SVG file. |

No CDN at runtime, no Google Maps iframes, map tiles, YouTube embeds or social widgets. "Open in Google Maps" is a plain link.

## 5. Security (CSP)

No inline `<script>`, no `on*=` handlers, no `style=""` attributes (checked by the build). JS hooks use `data-*` attributes; dynamic values are set through the CSSOM, which CSP allows. Suggested policy:

```
default-src 'self'; script-src 'self' 'nonce-{{ request.csp_nonce }}'; style-src 'self'; img-src 'self' data:;
font-src 'self'; connect-src 'self'; frame-ancestors 'none'; form-action 'self'; base-uri 'self'
```
(`nonce` only for the JSON-LD block; `data:` only needed if the CMS stores small inline images.)
Fonts: when served over HTTP(S), add `<link rel="preload" as="font" type="font/woff2" crossorigin>` for Regular and Light. They are left out so the files also open from `file://`.

## 6. Partials → Django `{% include %}`

Every repeated block is wrapped in `<!-- partial:start NAME --> … <!-- partial:end NAME -->` and is byte-identical on every page (only `aria-current` differs).

| Partial | Django include | Notes |
|---|---|---|
| `notice-bar` | `partials/notice_bar.html` | Render only when an event's feedback window is open (see §12). |
| `site-topbar` | `partials/site_topbar.html` | WhatsApp +61 402 832 972 (first, highlighted), email, hours, `social-links`, language switch. |
| `site-header` | `partials/site_header.html` | Pass `active` = url name; adds `aria-current="page"` or `.is-current` on the dropdown. |
| `mobile-menu` | `partials/mobile_menu.html` | Same nav data as the header. |
| `social-links` | `partials/social_links.html` | `{% if social.facebook %}` per item — empty URL hides the icon. |
| `contact-details` | `partials/contact_details.html` | **Footer only.** The two office addresses (Head office · Australia, Operations · Bangladesh) with map links, then WhatsApp, Call, email and hours. No company names: the site presents one company. |
| `cta-band` | `partials/cta_band.html` | "Partner in building a clean planet." with a single **Enquire us** button. Optional per page (`{% block cta %}`); off on Enquire, feedback, privacy, 404. |
| `meet-gssl` | `partials/meet_gssl_modal.html` | Video modal for the Meet GSSL button (home, About). Video file and poster from site settings. |
| `site-footer` | `partials/site_footer.html` | |
| `event-status-badge` | `partials/event_status_badge.html` | Server renders the label; JS re-checks dates for cached pages. |
| `svg-sprite` | `partials/svg_sprite.html` | First thing in `<body>`: the logo symbol used by header, footer, marquee and ribbon. |
| `preview-ribbon` | `partials/preview_ribbon.html` | Shown only with `body.is-preview`. Remove the class in production. |

## 7. Loops → `{% for %}`

| Loop marker | Page(s) | Django |
|---|---|---|
| `slides`, `slides-headline`, `slides-text` | Home hero | `{% for slide in slides %}` (Web › Slider, `active=True`). Three loops over the same queryset: media, headline, text/buttons. |
| `impact-counters` | Home, cookstove page | `{% for c in counters %}` (from Dashboard; approved figures only) |
| `areas` | Map list fallback | `{% for d in districts %}` (Area › District with active ICS installations) |
| `approach-attributes`, `approach-highlights` | Home, About | `approach.attributes` |
| `vision-attributes` | About | `vision.attributes` |
| `projects`, `related-projects` | Home carousel, Projects, detail | `{% for p in projects %}` |
| `project-description`, `project-attributes`, `project-gallery` | Project detail | `project.description`, `project.attributes`, `project.images` (+ `project.gs_id` for the registry button) |
| `programmes`, `other-programmes`, `programme-attributes` | Projects, programme page | `Programme.objects.filter(show_on_website=True).order_by("sort_order")` |
| `events`, `related-events`, `agenda`, `participation`, `feedback-steps` | Events pages | `Event` + `EventAgendaItem` |
| `audiences`, `benefits`, `process-steps`, `faq` | About, cookstove page | Static or a small FAQ model |
| `albums`, `gallery-images` | Gallery | `Album`, `AlbumImage` |
| `priority-programmes` | Home showcase | `Programme.objects.filter(priority=True).order_by("sort_order")` (three) |
| `posts`, `latest-posts`, `related-posts` | News & Insights, home, article | `Post.objects.filter(published=True).order_by("-published_at")`; filter chips by `category` |
| `career-areas`, `job-openings` | About › Careers at GSSL | static areas; `JobOpening.objects.filter(published=True)`; the empty-state text shows when there are none |
| `why-reasons`, `why-audiences`, `why-steps` | Why GSSL | static, or a small "Why GSSL" CMS block |

## 8. CMS field map

| Slot | Admin module › field | Status |
|---|---|---|
| Hero image | Web › Slider › image, active | existing |
| Hero headline, short text, button label, button link, alt text, optional video (MP4/WebM) | Web › Slider | **ThingBD to add** |
| Top bar / footer / Enquire page details | Web › Contact › Australia Address, Bangladesh Address, Mobile 1 (+61 402 832 972, also the WhatsApp number), Email, Details | existing. Company names and Mobile 2 are **no longer shown** (one company, one phone). Addresses appear in the footer only. |
| Working hours (per office, with time zone) | Web › Contact | **add** (`[to confirm]`) |
| Social icons | Web › Social Link › Facebook, YouTube, LinkedIn, WhatsApp, Twitter (shown as X) | existing — values are placeholders; empty = hidden |
| Our approach | Web › Approach › image, title, description, attributes[] (title, description) | existing — add `icon` to attributes |
| Our vision | Web › Vision › image, title, description, attributes[] | existing — add `icon` |
| Project | Web › Project › image, title, description[], attributes[] (icon, title, details) | existing — **add** `programme` FK, `status`, `location`, `stage`, `gs_id` (Gold Standard ID, e.g. GS13141), `gallery[]` |
| Programme | **new model**: title, slug, stage (In development / Active / Paused), summary, description (rich text), icon, image, sort order, show on website | **add**; also `stage_step` (Concept, Feasibility, Pilot, Active) for the tracker |
| Event | Web › Event — **add structured fields**: type, title, slug, start/end datetime, venue, district, language, organiser, feedback_start/end, summary, body, agenda items (time, title, text), gallery | **add** |
| Contact form (Enquire page) | `name`, `email`, `subject`, `message` | existing — **add** `enquiry_type`, `phone` |
| Programme (additions) | `priority` (bool), `sort_order` (cookstove 1, rooftop 2, water 3, irrigation 4, rural 5, rice 6), `animation_strip` and `animation_card` (MP4 + poster), `steps[]` (title, text) for "How it works" | **add** |
| News & Insights | **new model** `Post`: title, slug, category (News, Insights, Programme updates, Field stories), excerpt, cover image, body (rich text), author, published_at, reading time, featured, published | **add** |
| Site settings | intro video (MP4) + poster for Meet GSSL | **add** |
| Careers | **new model** `JobOpening`: title, location, type, summary, closing date, apply link or email, published | **add** (optional; About shows an empty state until a role is published) |
| Contact inbox | email to info@ and/or new admin module "Enquiries" | **to confirm** |
| Feedback form | **new model**: event (FK, nullable), stakeholder_type, name, organisation, email, phone, message, attachment, consent, created_at, reference, status, reply | **add** |
| Impact counters | Dashboard (clients, cookstove sales, monitoring visits, stock) + Area | read-only; approved figure + "as of" date stored per counter |
| District map | Area › Division › District (district level only) | read-only |

## 9. Page titles and meta descriptions

| File | URL | `<title>` | Meta description |
|---|---|---|---|
| `index.html` | `/` | Green Spark Solutions Australia | Carbon projects & clean energy in Bangladesh | Green Spark Solutions Australia develops carbon projects and clean-energy programmes with communities in Bangladesh, Nepal and Cambodia, including cookstove projects registered with Gold Standard. |
| `news.html` | `/news-insights` | News &amp; Insights | Green Spark Solutions Australia | News, insights and field stories from Green Spark Solutions Australia: programme updates, notes from the field and plain-language insights on carbon projects. |
| `news-article.html` | `/news-insights/<slug>` (sample: how-mrv-works-for-rooftop-solar) | How MRV works for rooftop solar | News &amp; Insights | Green Spark Solutions Australia | Measure, report, verify: how generation from many rooftops can become one carbon programme that buyers can check. |
| `why-gssl.html` | `/why-gssl` | Why GSSL | Green Spark Solutions Australia | Why partners, carbon buyers and communities work with Green Spark Solutions Australia: built with communities, held to recognised standards, monitoring you can check. |
| `about-us.html` | `/about-us` | About Us | Green Spark Solutions Australia | Who we are: carbon project developers in Bangladesh, Nepal and Cambodia. Our vision, our approach, and the partners we work with. |
| `projects.html` | `/projects` | Projects | Green Spark Solutions Australia | Our cookstove projects registered with Gold Standard, ongoing project activities, and the clean-energy and water programmes in our pipeline. |
| `project-detail.html` | `/projects/green-ics-phase-1` | Green ICS — Phase 1 | Projects | Green Spark Solutions Australia | Green ICS Phase 1: improved cookstoves installed with households in Manikganj, Bangladesh. Registered with Gold Standard and monitored by our field team. |
| `improved-cookstove.html` | `/what-we-do/improved-cookstove` | Improved Cookstove Programme (Green ICS) | Green Spark Solutions Australia | The Green ICS improved cookstove for Bangladeshi households who cook with firewood and biomass. Gold Standard registered phases, how it works, benefits and FAQ. |
| `events.html` | `/events` | Events and consultations | Green Spark Solutions Australia | Upcoming local stakeholder consultations, open feedback rounds and past events for the Green Spark Improved Cookstove Programme in Bangladesh. |
| `event-detail.html` | `/events/lsc-manikganj-2027` | Local Stakeholder Consultation — Improved Cookstove Programme, Manikganj | Events | Green Spark Solutions Australia | Local stakeholder consultation for the Green Spark Improved Cookstove Programme in Manikganj: date, venue, agenda, documents and how to give feedback. |
| `event-feedback-round.html` | `/events/feedback-round-ics-2026` | Stakeholder feedback round — open now | Green Spark Solutions Australia | Share your views on the Green Spark Improved Cookstove Programme. The stakeholder feedback round is open until 9 January 2027. |
| `feedback.html` | `/feedback` | Give feedback | Green Spark Solutions Australia | Share feedback, questions or concerns about Green Spark projects and consultations, in Bangla or English. Every comment is recorded and answered. |
| `gallery.html` | `/gallery` | Gallery | Green Spark Solutions Australia | Photo albums from Green ICS installations, community demonstrations, consultations and monitoring visits in Bangladesh. |
| `gallery-album.html` | `/gallery/green-ics-installations-manikganj` | Green ICS installations, Manikganj | Gallery | Green Spark Solutions Australia | Photos of Green ICS improved cookstove installations with households in Manikganj district, Bangladesh. |
| `contact-us.html` | `/contact-us` (label: Enquire) | Enquire | Green Spark Solutions Australia | Enquire with Green Spark Solutions Australia. WhatsApp +61 402 832 972 is the quickest way to reach us, or call, email or use the enquiry form. |
| `privacy.html` | `/privacy` | Privacy policy | Green Spark Solutions Australia | How Green Spark Solutions Australia collects, uses and protects the personal information you share through our website and feedback channels. |
| `404.html` | `/404` | Page not found | Green Spark Solutions Australia | The page you are looking for could not be found. |
| `programme.html` | `/what-we-do/safe-drinking-water` | Safe Drinking Water | Programmes in development | Green Spark Solutions Australia | Small residential water filters with high filtering capacity, backed by nature's own filtration, for safe drinking water at home. A Green Spark Solutions programme in development. |
| `programme-solar-irrigation.html` | `/what-we-do/solar-irrigation` | Solar Irrigation | Programmes in development | Green Spark Solutions Australia | Replacing diesel irrigation pumps with solar pumping, so farmers can water their fields without diesel. A Green Spark Solutions programme in development. |
| `programme-rooftop-solar.html` | `/what-we-do/rooftop-solar` | Rooftop Solar | Programmes in development | Green Spark Solutions Australia | Bringing rooftop solar systems together into one carbon programme, so more owners can take part. A Green Spark Solutions programme in development. |
| `programme-rural-productive-use-solar.html` | `/what-we-do/rural-productive-use-solar` | Rural Productive-Use Solar | Programmes in development | Green Spark Solutions Australia | Solar power for cold storage, crop processing, water pumping and rural businesses. A Green Spark Solutions programme in development. |
| `programme-low-emission-rice.html` | `/what-we-do/low-emission-rice` | Low-Emission Rice | Programmes in development | Green Spark Solutions Australia | Helping rice farmers move from continuous flooding to alternate wetting and drying (AWD). A Green Spark Solutions programme in development. |
| `components/index.html` | `/components` | Component library | Green Spark design system | Green Spark website component library: tokens, typography, buttons, navigation, cards, forms and every state. |

All pages also carry canonical, Open Graph, Twitter card, favicons and a `<!-- seo:jsonld -->` marker (Organization everywhere, Event on event pages).

## 10. Statistics used

| Figure | Where | Source |
|---|---|---|
| 2.1 billion people cook using open fires or inefficient stoves | Cookstove page | WHO, *Household air pollution* fact sheet, 16 Dec 2025 — https://www.who.int/news-room/fact-sheets/detail/household-air-pollution-and-health |
| 2.9 million deaths a year attributed to household air pollution (2021) | Cookstove page | Same WHO fact sheet |
| Fewer than 30% of households in Bangladesh cook with gas, electricity or improved stoves | Cookstove page | Our World in Data, Oct 2025 (WHO data) — https://ourworldindata.org/data-insights/access-to-clean-cooking-fuels-in-bangladesh-is-far-lower-than-in-its-asian-neighbors |
| ~20,000 stoves installed in Phase 1; 50,000 planned in Phase 2 | Home, cookstove, projects | Supplied by GSSL in the brief — **GSSL to approve before publishing** |

## 11. Sample data to replace before launch

- Impact counters: 8+ years, 20,000+ installed, 95,000 people (estimated), 10 districts, 38,400 monitoring visits; "as of 30 September 2026". Firewood saved is shown as "Published once measured".
- Highlighted districts on the map: Manikganj (base), Dhaka, Tangail, Gazipur, Munshiganj, Narayanganj, Faridpur, Rajbari, Sirajganj, Pabna.
- All six events, their dates, venues and agendas; the notice bar text and window (10 Nov 2026 – 9 Jan 2027).
- Projects: Phase 2 location ("Dhaka and Rajshahi divisions"), Nepal scoping project, Gold Standard IDs per phase (GS13141 / GS23304).
- Programme stages (Water: Concept · Irrigation: Feasibility · Rooftop: Feasibility · Rural: Concept · Rice: Concept) and programme attribute copy.
- Country chips: Nepal and Cambodia "Scoping".
- Gallery albums and photo counts; all illustrations (replace with field photos).
- Office time zones and hours; FAQ answer on stove pricing; feedback reference number GS-FB-1042; privacy-policy retention periods and ABN.

## 12. Component behaviour to keep in Django

- **Hero slider:** 7 s autoplay; pauses on hover, keyboard focus, hidden tab and the pause button; **no autoplay with `prefers-reduced-motion`** (Ken Burns, canvas and word animation also off). Image-only slides show `.hero__fallback`. A slide video loads only on desktop, not on Save-Data, not with reduced motion.
- **Spark canvas** (`data-spark-canvas`): decorative, `aria-hidden`, stops off-screen.
- **Scroll scenes** (expanding cards, floating tiles): sticky only ≥ 992px with motion allowed; otherwise a tap-to-open list and a swipe row.
- **Focus trapping:** mobile menu, lightbox and modal trap focus, close on Escape, restore focus, lock scroll.
- **Dropdowns:** hover with intent delay, click/tap toggle, ↓ to enter, ↑/↓ to move, Escape to close.
- **Notice bar:** render server-side only when `now` is inside an event's feedback window; JS also hides it outside `data-window-start/-end` (cached pages) and remembers dismissal per notice id.
- **Event status:** compute in the view from dates (Upcoming → Open for feedback → Closed, plus "Happening today"); JS re-computes from `data-start/end/feedback-start/feedback-end`.
- **Feedback form pre-fill:** use the URL path `/events/<slug>/feedback/` and set the initial value server-side. The static build uses `#event=slug` (the hash never reaches the server).
- **Forms:** POST only, `{% csrf_token %}` where `<!-- csrf_token -->` sits, honeypot field `website` (reject silently), client validation mirrored by Django form validation. `data-ajax` expects JSON `{ok:true}` or `{ok:false, errors:{field:"msg"}}`; remove `data-demo` in production. States: sending (button spinner), success, server error, error summary.
- **Counters:** the final number is in the HTML (SEO/no-JS); JS only animates.
- **Map:** district-level only. Never show household names, phone numbers or village locations.
- **Programme animations** (`media.js`): `video[data-loop-video]` is muted, looping and decorative (`aria-hidden`); it plays only while on screen, and never with reduced motion or Save-Data (the poster frame shows instead). Collage cards (`data-tilt`) lean towards the pointer on desktop; cards float, pins pulse and the dotted route flows only when motion is allowed.
- **Priority showcase** (`showcase.js`): ARIA tabs, auto-advance every 9 s with a progress bar; pauses on hover, focus, hidden tab or off screen; stops after the visitor picks a tab; no autoplay with reduced motion. On phones the three-panel animation scrolls with snap points.
- **Meet GSSL** (`media.js` + `modal.js`): the video plays when the modal opens and pauses when it closes (Escape, backdrop, close button).
- **Photo-card glow** (`glow.js`): cards with `data-glow` (project, programme and album cards; photo + attribute splits with `data-glow-trigger` on the photo). Headings with `.glow-text` sit outlined (transparent fill) and glow in the logo green while the card is hovered, focused or tapped; `.glow-body` text darkens. Solid text without JS, with `prefers-contrast: more` and in forced colours. No icons below a photo.

## 13. Programmes in development — visibility and confidentiality

- Each programme is a `Programme` record; `show_on_website=False` by default, so new records stay hidden until GSSL approves them. Templates loop over visible records only, so programmes can be added or hidden without redesign.
- Pages for programmes in development show **name, icon, colour, one-line summary, generic description and stage only** (no developer company: the site presents one company). They never show volumes (tonnes, hectares, installations), prices, revenue shares, buyers, funding applications, or any organisation not confirmed in writing as a partner. They have no counters.
- ICS Phase 3 is shown as "In pipeline" with no numbers.

## 14. Open questions for GSSL `[to confirm]`

1. Approval of every public figure (Phase 1 and 2 numbers, counters, districts) and the "as of" date.
2. Time zone for the published hours (one phone number now).
3. Revised short blurb (7.1) and benefit wording (7.3) under the claims rules.
4. Where contact-form submissions go (email to info@, admin inbox, or both).
5. Nepal and Cambodia: what is public, and at what stage.
6. Programme stages for each programme in development.
7. Gold Standard registry links for Phase 1 and Phase 2.
8. Real social media URLs (current values are placeholders).
9. Stove pricing language for the FAQ.
10. Privacy policy: ABN, retention periods, legal review.
11. Bangla version timeline (the language switch is in place, disabled).
12. Whether to keep the lime "spark" as the MRV action colour (recommended).
13. Confirm that +61 402 832 972 is on WhatsApp (every WhatsApp link and the QR code use it). Calls to it from Bangladesh are international, so WhatsApp is the better route for communities there.
14. Careers: whether to publish openings on the site, and who receives CVs (currently info@).
15. A dedicated Impact page for the header (the climateimpact.com order has one; the slot is empty for now).
16. Replace the generated Meet GSSL film (34 s, silent) with GSSL's own intro video, if there is one.
17. Real News & Insights posts (the six posts are samples) and who publishes them.

## 15. Performance

Home page, first mobile visit: ~790 KB uncompressed (≈450 KB with gzip/brotli on HTML/CSS/JS): HTML 180 KB (includes the inline district map), CSS 180 KB (16 files incl. Bootstrap grid), JS 56 KB, fonts 32 KB (3 weights used above the fold), images ~285 KB WebP. All images use `<picture>` with WebP + JPEG fallback, `srcset`, explicit `width`/`height`, `loading="lazy"` below the fold and `fetchpriority="high"` for the first hero. Mobile gets a portrait hero crop. For production, bundle and minify CSS/JS (e.g. django-compressor) and serve with long cache headers.
