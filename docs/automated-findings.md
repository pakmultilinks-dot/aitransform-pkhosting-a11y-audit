# Automated findings, TPT-2026-03078
# aiTransform and PK Hosting, WCAG 2.1 AA, static HTML analysis of pages saved 6 Nov 2026.
# Method: hidden_files/auto_checks.py on saved copies in hidden_files/pages/.
# Contrast covers inline styles only. Tap-target sizes cannot be verified from static HTML.

## Pages audited (all HTTP 200, fetched 6 Nov 2026)
| # | Page | URL |
|---|---|---|
| 1 | aiTransform home | https://aitransform.com/ |
| 2 | aiTransform blog | https://aitransform.com/blog/ |
| 3 | aiTransform terms | https://aitransform.com/terms |
| 4 | PK Hosting home | https://www.pkhosting.com/ |
| 5 | PK Hosting pricing | https://www.pkhosting.com/pricing/ |
| 6 | PK Hosting WordPress hosting | https://www.pkhosting.com/wordpress-hosting/ |

Note on page choice: aiTransform tool pages (AI Writer, Image, Code, Chat) sit behind login,
so they were not audited. The brief limits testing to public pages, and no login was used.
Blog and terms were substituted as the two extra public aiTransform pages. aiTransform
/pricing was not used: it returns 404.

## Failures (7 automated check failures across 3 pages)

| Bug | Page | Check | Count | Severity | Why this severity |
|---|---|---|---|---|---|
| B1 | aiTransform home | Heading order, skipped levels | 12 jumps | Medium | Screen reader users navigate by headings. The page starts with an h6 before the h1, jumps h2 to h4 for the six feature blocks (AI Generator, Advanced Dashboard, Payment Gateways, Multi-Lingual, Custom Templates, Support Platform), and jumps h3/h4 to h6 for the feature eyebrow lines. The outline does not match the visual hierarchy. The h1 itself is one long concatenated string (Ultimate AITransformationTrainingBrandingVoiceoverProgrammerImage GeneratorSpeech To Text), which reads badly to a screen reader. |
| B2 | aiTransform home, blog, terms | Button without an accessible name | 1 per page | Medium | The mobile menu button (class mobile-nav-trigger) is an icon-only button with spans and no text, no aria-label, and no title. A screen reader announces it as an unnamed button, and the mobile menu cannot be identified by assistive technology. It is the only unnamed button on each of the three pages (home has 38 buttons, blog and terms have 2 each). |
| B3 | aiTransform home | Duplicate id values | 3 ids | Low | id instagram appears twice, id adwords twice, id paint0_linear three times, all on inline SVG elements. Duplicate ids break getElementById lookups and can break SVG gradient references. Low because no visible break was observed in the static markup. |
| B4 | aiTransform blog | Link without an accessible name | 1 of 18 links | Medium | A call-to-action link under the Blog Posts heading (class lqd-btn, href #) has no inner text at all in the static HTML. Its label appears to be injected by JavaScript from the link and text attributes on the tag. If JavaScript fails or is slow, the link is nameless. Needs a live check to confirm whether it renders with text. |
| B5 | aiTransform terms | Link without an accessible name | 1 of 20 links | Medium | Same as B4: the same empty call-to-action link (class lqd-btn, href #) with no inner text in the static HTML. Needs a live check to confirm whether JavaScript fills it. |

Note: B2, B4 and B5 are the same shared header, footer, and template components repeated
across the three aiTransform pages, so one template fix clears them on all three pages.

## What passed (automated checks)

| Check | Result |
|---|---|
| html lang attribute | Pass on all 6 pages (aiTransform en, PK Hosting en-PK) |
| Title present, non-empty, unique | Pass on all 6 pages, all 6 titles different |
| Viewport meta | Pass on all 6 pages |
| Images with non-empty alt | Pass on all 6 pages (aiTransform home 22 images, blog 2, terms 2; PK Hosting 5 per page, 0 missing alt) |
| Form inputs with labels | Pass on all 6 pages (aiTransform pages have 0 visible inputs in the static HTML; PK Hosting home and pricing have 1 labelled input each) |
| Exactly one h1 | Pass on all 6 pages |
| Heading order | Pass on aiTransform blog, aiTransform terms, and all 3 PK Hosting pages |
| Links with accessible names | Pass on aiTransform home and all 3 PK Hosting pages (home 27 links, PK Hosting 115 to 145 links per page, 0 bad) |
| Buttons with accessible names | Pass on all 3 PK Hosting pages |
| Duplicate ids | Pass on aiTransform blog, aiTransform terms, and all 3 PK Hosting pages |
| Inline-style contrast | Pass where checkable on all 6 pages: no inline-styled text element with a known inline background fell below 4.5:1 |

## Not verified by the automated run (needs a live check)

| Item | Reason |
|---|---|
| Colour contrast of stylesheet colours | All text colours on both sites come from external CSS, not inline styles. The script could score 0 elements with a known background. No contrast ratio is claimed for any stylesheet colour. The PK Hosting footer logo link (white inline text on a dark footer set by CSS) was wrongly flagged in an early run that assumed a white background; that flag was removed after hand verification. |
| Tap-target size (24x24 CSS px minimum) | Rendered size cannot be verified from static HTML. 27 links and 38 buttons on aiTransform home, 115 to 145 links per PK Hosting page, all need a live measurement at 1440x900 and 390x844. |
| Keyboard navigation, focus visibility | Needs a live browser session. |
| Zoom to 200 percent and text resize | Needs a live browser session. |
| Firefox and Safari rendering | No Firefox or Safari is available in this environment. Chromium only. |
| aiTransform tool pages (Writer, Image, Code, Chat) | Behind login; public-pages-only rule, so not audited. |

## Corrections made during the run (false positives removed)
1. Logo links on aiTransform (2 per page) were first flagged as empty links. Hand check showed
each contains an img with alt "aiTransform logo", which is its accessible name. The script
was fixed to count img alt text as a link name, and the flags were removed.
2. The PK Hosting footer logo link was first flagged for white text on an assumed white
background (ratio 1.00:1). Hand check showed it sits in the dark footer set by CSS, so the
background was unknown, not white. The script was fixed to score contrast only when both
foreground and background are known from inline styles, and the flag was removed.

## Files
- Script: hidden_files/auto_checks.py
- Results: hidden_files/auto_results.json
- Saved pages: hidden_files/pages/page-1 to page-6
- This file: hidden_files/automated-findings.md
