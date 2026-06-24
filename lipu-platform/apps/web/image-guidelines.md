# Image Guidelines

Authoritative rules for every photograph used on the LIPU marketing site. All current assets in `public/images/` and all future selections must satisfy these criteria.

**Related files:** `config/gallery-inspiration-map.json` (100 inspiration photos), `config/city-style-map.json` (city-aware visuals), `lib/gallery-inspiration.ts`, `lib/city-style.ts`, `lib/images.ts`, `scripts/download-gallery-inspiration.ps1`, `scripts/download-images.ps1`, `DESIGN_REFERENCES.md`.

---

## Inspiration-first ratio (80 / 20)

The site is a **home design inspiration platform**, not a product catalogue. Homeowners think *"I need ideas for my balcony"* — not *"Show me a 2-track sliding window with 5mm glass."*

| Priority | Target | Use for |
|----------|--------|---------|
| **Real-home inspiration** | ~80% | Gallery, heroes, product cards, homepage sections |
| **Product / craft detail** | ~20% | Spec sheets, technical pages only — never as primary visuals |

Every image should answer: **"What will my home look like if I choose this style?"**

### Selection priorities

1. Real homes before isolated products
2. Complete rooms instead of window-only crops
3. Lifestyle and design inspiration (Pinterest / home-design tone)
4. Before-and-after transformations where possible
5. Natural light through large openings
6. Balconies, living rooms, bedrooms, kitchens, villas with UPVC installations
7. Modern Indian duplex homes and apartments
8. Combinations of windows, doors, glass, railings, and interiors

### Avoid as primary visuals

- Images that only show a window or door product
- Technical catalogue macros (profile cross-sections, hardware close-ups)
- Isolated glazing without room context

### Gallery categories (`public/images/inspiration/`)

Ten categories × ten photos each (100 total), defined in `config/gallery-inspiration-map.json`:

- Living Room Ideas · Balcony Ideas · Kitchen Ideas · Villa Ideas · Apartment Ideas
- French Door Ideas · Bedroom Ideas · Office & Commercial · Luxury Home Ideas · Small Space Ideas

---

## City-style system

Visual assets and copy adapt by selected city via `config/city-style-map.json`. When adding images:

1. Assign paths to the correct city and category (`hero`, `exterior`, `apartment`, `villa`, `duplex`, `coastal`, `commercial`, `interior`, etc.).
2. Follow the architecture type for each city cluster (Odisha, Kolkata, Delhi, Mumbai, Chennai, Bangalore).
3. Never assign foreign architecture to any city bucket.

---

Imagery must read as **Odisha, India**. Prefer scenes that could plausibly be set in or near:

- **Bhubaneswar** — planned city, institutional and residential architecture, warm tropical light
- **Cuttack** — older urban fabric, river-adjacent settings, mixed residential and commercial
- **Puri** — coastal context, sea breeze, pilgrimage-town adjacency, beach-side villas
- **Odisha (state-wide)** — tropical climate, laterite and concrete construction, monsoon-ready detailing

When writing alt text or case-study copy, anchor projects to these places where location is mentioned.

---

## Architecture

Subjects must reflect **Indian building types** and construction realities:

- **Indian duplex homes** — stacked floors, boundary walls, terrace use, local materials
- **Indian apartments** — mid- and high-rise towers, balcony glazing, urban density
- **Indian villas** — gated communities, courtyard or lawn adjacency, UPVC window/door focus
- **Commercial buildings in India** — office lobbies, retail facades, institutional entrances

Favour:

- Floor-to-ceiling or large-format glazing (core product story)
- Warm natural light, golden hour, monsoon-season greens
- Clean lines without importing foreign suburban or cottage aesthetics
- People optional; if shown, South Asian context only

---

## Avoid

Do **not** use imagery depicting:

| Category | Examples to reject |
|----------|-------------------|
| **American suburbs** | Detached ranch homes, picket fences, wide lawns, US street grids |
| **European cottages** | Thatched roofs, half-timber, stone village houses, Alpine chalets |
| **Foreign families** | Clearly Western-only casts in lifestyle shots |
| **Snow regions** | Winter scenes, snow-covered roofs, cold-climate landscaping |
| **Western architecture** | Cape Cod, Craftsman, Mediterranean villa (European), Scandinavian cabin |

When sourcing or commissioning photos, reject candidates at first glance if the setting or building type does not belong in Odisha.

---

## Asset workflow

1. **Select** — Apply the location, architecture, and avoid rules above before download or shoot.
2. **Store** — Save under `public/images/{category}/` using kebab-case filenames (see existing folders: `hero`, `projects`, `products`, `gallery`, `team`, etc.).
3. **Register** — Add an entry in `lib/images.ts` with descriptive alt text that reflects Indian/Odisha context.
4. **Review** — Confirm the image passes the checklist below before merge.

Local assets only. Do not link remote Unsplash, Pexels, or CDN URLs in application code.

---

## Pre-merge checklist

- [ ] Setting is plausible for Bhubaneswar, Cuttack, Puri, or wider Odisha
- [ ] Building type is an Indian duplex, apartment, villa, or commercial structure
- [ ] No American suburban, European cottage, or generic Western architecture
- [ ] No snow, cold-climate, or clearly foreign-only lifestyle context
- [ ] Alt text in `lib/images.ts` describes Indian architectural context accurately
- [ ] File lives under `public/images/` and is referenced via `lib/images.ts`

---

## Search terms (sourcing)

Use these when searching stock libraries or briefing photographers:

```
Indian villa architecture
Indian duplex house exterior
Indian apartment balcony glass
Bhubaneswar modern home
Odisha residential architecture
Indian commercial building facade
luxury UPVC windows India
Indian home floor to ceiling windows
tropical Indian villa natural light
```

Append **avoid** filters mentally: *suburb, cottage, snow, European, American home*.

---

*Last updated: project image migration — local assets under `public/images/`.*
