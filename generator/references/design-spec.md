# Design spec — studio portfolio pattern

## Principles
- Photography carries the site. UI chrome stays thin, neutral and quiet.
- Generous white space; content max width 1200px; section padding 96px desktop / 56px mobile.
- Two type voices: **UPPERCASE letter-spaced labels** (nav, buttons, footer headings,
  tile labels) and **lowercase light display headings** (page titles, section titles).

## Tokens (CSS custom properties, set from `site.json`)
| Token            | Default    | Use                                   |
|------------------|------------|---------------------------------------|
| `--ink`          | `#1d1d1b`  | body text, headings                   |
| `--paper`        | `#ffffff`  | page background                       |
| `--muted`        | `#7a756f`  | secondary text, captions              |
| `--line`         | `#e4e1dc`  | hairlines, borders                    |
| `--accent`       | `#a4462f`  | links, buttons, tagline dots          |
| `--footer-bg`    | `#1d1d1b`  | footer background                     |
| `--footer-ink`   | `#d9d5cf`  | footer text                           |
| `--font-display` | Jost       | headings, labels                      |
| `--font-body`    | Source Serif 4 | paragraphs                         |

## Header
- Height 88px. Logo left (wordmark text if no logo image), nav right.
- Nav items: 13px, weight 500, letter-spacing .18em, uppercase.
- Dropdown: white panel, 1px `--line` border, items 12px uppercase, opens on hover
  and on focus-within; arrow keys not required.
- Home: header is transparent and white-text over the hero; turns solid white with
  shadow after 80px scroll (`.is-solid`).
- <900px: hamburger toggles a full-height panel; dropdown children shown indented.

## Tagline strip
Three short phrases separated by small accent dots, uppercase 12px, letter-spaced,
centered, 1px lines above and below. Appears under the hero and atop inner pages.

## Hero (home)
100svh, crossfading slides every 6s (1.2s fade), dark gradient at bottom,
wordmark/logo centered in white, optional caption bottom-left in small uppercase.

## Tiles
- Market tiles: 2×2 grid desktop (4 markets) or auto-fit `minmax(260px,1fr)`;
  aspect 4/3; label centered in white uppercase over a 35% dark overlay that
  lightens and image scales to 1.05 on hover/focus.
- Project cards: 3-column grid, image 3/2, title below in display font, location in
  muted uppercase 11px.
- Team cards: 4-column grid, portrait 4/5, grayscale → color on hover.

## Footer
Four columns: ABOUT, PROJECTS, SERVICES (lowercase links) and LOCATIONS (office
blocks), then social icons row and a copyright line. Column headings uppercase bold
12px.

## Motion
Only opacity/transform, 250–400ms ease. Disable under `prefers-reduced-motion`.
