# Issue #1 — visual review

The website now uses a shared midnight-blue palette, cyan interaction states, and violet, mint, and blue capability groups. Layered SVG nodes preserve their aspect ratio. Mobile layouts separate the illustration from the six capability buttons to keep long English labels readable.

## Before and after

| Area | Before | After |
| --- | --- | --- |
| Desktop hero | [Before](before-desktop-hero.png) | [After](after-desktop-hero.png) |
| Desktop capability map | [Before](before-desktop-map.png) | [After](after-desktop-map.png) |
| Mobile hero | [Before](before-mobile-hero.png) | [After](after-mobile-hero.png) |
| Mobile capability map | [Before](before-mobile-map.png) | [After](after-mobile-map.png) |

Additional narrow-screen check: [English hero at 320px](after-mobile-en-320.png).

Desktop captures use a 1440px viewport; mobile comparisons use 390px. The sticky header is hidden only while capturing individual sections so it does not obscure the comparison. Reduced motion is enabled for stable captures.

## Validation

- `python3 scripts/build.py`
- `python3 scripts/check.py`
- `node --check docs/assets/site.js`
- `git diff --check`
- Chromium browser checks for English and Chinese at 320, 390, 768, 1024, and 1440px: no horizontal overflow; all three ecosystem modes, six nodes, eight capability panels, and three guided journeys work.
- Checked journey first/last boundaries, backward navigation, reset, related capabilities, mobile menu and Escape behavior, keyboard node highlighting, and play/pause.
- Reduced motion disables autoplay and animated effects. Navigation and fallback content remain available without JavaScript.
- No JavaScript page errors during the interaction checks. English labels and the downloadable English SVG were also inspected visually.

No new runtime dependencies or external assets are required. Browser verification was performed with an existing local Chromium installation; Safari and Firefox have not been tested.
