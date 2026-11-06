# Test plan, TPT-2026-03078
# aiTransform and PK Hosting, accessibility, responsive and cross-browser audit.
# Standard: WCAG 2.1 AA. Date of automated run: 6 November 2026.
# Screen sizes: desktop 1440x900, mobile 390x844.
# LIVE RUN NOTE (6 Nov 2026): the live browser could not set a viewport size. Desktop checks ran at 1919x998, not 1440x900. Mobile 390x844 was not tested (no device emulation). Zoom 200 percent could not be verified (Ctrl+ showed no change).
# Browsers: Chromium (live checks run here), Firefox (not run), Safari (not run).

## Scope
Pages under test (all public, all HTTP 200 on 6 Nov 2026):
1. aiTransform home, https://aitransform.com/
2. aiTransform blog, https://aitransform.com/blog/
3. aiTransform terms, https://aitransform.com/terms
4. PK Hosting home, https://www.pkhosting.com/
5. PK Hosting pricing, https://www.pkhosting.com/pricing/
6. PK Hosting WordPress hosting, https://www.pkhosting.com/wordpress-hosting/

Out of scope: aiTransform tool pages (AI Writer, Image, Code, Chat) sit behind login and
were not tested, because the brief limits testing to public pages. aiTransform /pricing
returns 404 and was not used. No form was submitted on any live site. No load testing and
no security testing was done.

## Tools
- Automated static checks: hidden_files/auto_checks.py (Python, BeautifulSoup), results in
hidden_files/auto_results.json. Covers lang, title, viewport, alt text, input labels,
heading order, link and button names, duplicate ids, and inline-style contrast only.
- Live checks: Chromium browser session at 1440x900 and 390x844 (keyboard navigation,
zoom, tap targets, layout). Run separately by the parent agent; statuses below say
"pending live check" where the live run has not reported yet.
- Firefox and Safari: no Firefox or Safari is available in this environment, so their
columns say "not run". The test cases are written so they can be run there later.

## Test cases

### A. Accessibility (WCAG 2.1 AA)
| ID | Test case | Steps | Expected result | Status (automated) |
|---|---|---|---|---|
| A1 | html lang attribute present | Read the html tag on each page | lang is set (en, or en-PK) | Pass on all 6 pages |
| A2 | Page title present, non-empty, unique | Read the title element on each page | A non-empty title, different on each page | Pass on all 6 pages |
| A3 | All images have non-empty alt text | List every img and its alt | Every img has a non-empty alt | Pass on all 6 pages |
| A4 | Every visible form input has a label | List inputs, check label for, wrapping label, aria-label, or aria-labelledby | Every visible input is labelled | Pass on all 6 pages |
| A5 | Heading order has no skipped levels | List headings in order | Levels never jump by more than one | Fail on aiTransform home (12 jumps, starts with h6 before the h1). Pass on the other 5 pages |
| A6 | Exactly one h1 per page | Count h1 elements | One h1 | Pass on all 6 pages |
| A7 | Every link has an accessible name | List links, check text, aria-label, img alt, or title | Every link is named | Fail on aiTransform blog and terms (1 empty link each, the call-to-action link under Blog Posts). Pass on the other 4 pages |
| A8 | Every button has an accessible name | List buttons, check text, aria-label, or title | Every button is named | Fail on aiTransform home, blog, terms (mobile-nav-trigger button, 1 per page). Pass on all 3 PK Hosting pages |
| A9 | No duplicate id values | Count repeated id attributes | No id appears twice | Fail on aiTransform home (instagram x2, adwords x2, paint0_linear x3). Pass on the other 5 pages |
| A10 | Inline-style text contrast is at least 4.5:1 | Compute WCAG contrast where both foreground and background are inline styles | No element below 4.5:1 | Pass where checkable on all 6 pages (0 elements had a known inline background; stylesheet colours not verifiable statically) |
| A11 | Keyboard navigation reaches every interactive element, with a visible focus indicator | Tab through each page in Chromium at 1440x900, note every element that cannot be reached or has no visible focus | Every link and button is reachable, focus is visible | Pass on the 4 pages checked live at 1919x998 (aiTransform home, Image Generator tab, PK Hosting home, pricing): focus visible, order logical, no trap. No skip link on aiTransform (bug B6). PK Hosting skip link present. Blog, terms, WordPress page not live-checked |
| A12 | Zoom to 200 percent and text resize keep content readable | Zoom to 200 percent in Chromium at 1440x900, resize text to 200 percent, check for lost or overlapping content | No content lost, no overlap | NOT RUN. Ctrl+ presses showed no change in scale or layout, so reflow could not be verified. Needs a browser where zoom can be changed |

### B. Responsive layout
| ID | Test case | Steps | Expected result | Status |
|---|---|---|---|---|
| R1 | Viewport meta present | Read the meta viewport tag on each page | Viewport meta is set | Pass on all 6 pages (automated) |
| R2 | No horizontal scroll at 390px width | Open each page in Chromium at 390x844, scroll and check for horizontal overflow | No horizontal scrollbar, no content cut off at the right edge | NOT RUN. No device emulation in this browser, mobile 390x844 could not be tested. |
| R3 | Navigation works at 390px | Open each page at 390x844, open the mobile menu, follow one link | Menu opens, links work, menu closes | NOT RUN. No device emulation in this browser, mobile 390x844 could not be tested. |
| R4 | Pricing tables and cards stack without overlap at 390px | Open PK Hosting pricing and WordPress pages at 390x844 | Cards stack in one column, prices and buttons fully visible, no overlap | NOT RUN. No device emulation in this browser, mobile 390x844 could not be tested. |
| R5 | Tap targets are at least 24x24 CSS px at 390px | Measure links and buttons on each page at 390x844 | Every target is at least 24x24 px | NOT RUN. No device emulation in this browser, mobile 390x844 could not be tested. |
| R6 | Images scale without overflow at 390px | Open each page at 390x844, check every image | Images fit the viewport width, none overflow | NOT RUN. No device emulation in this browser, mobile 390x844 could not be tested. |
| R7 | Forms are usable at 390px | Open the visible forms on PK Hosting home and pricing at 390x844 | Labels, inputs, and buttons are fully visible and usable (no submission) | NOT RUN. No device emulation in this browser, mobile 390x844 could not be tested. |
| R8 | Desktop layout is intact at 1440px | Open each page in Chromium at 1440x900 | No overlap, no cut-off text, no broken layout | Pass at 1919x998 on the 4 pages checked live (no overlap or cut-off text observed). NOT RUN at the requested 1440x900, viewport could not be set |

### C. Cross-browser
| ID | Test case | Steps | Expected result | Status |
|---|---|---|---|---|
| C1 | aiTransform home renders in Chromium, Firefox, Safari | Open the home page in each browser at 1440x900 | Same layout and content in all three, no missing sections | Chromium pass at 1919x998 (page rendered, same content, no missing sections observed); Firefox not run; Safari not run |
| C2 | PK Hosting home renders in Chromium, Firefox, Safari | Open the home page in each browser at 1440x900 | Same layout and content in all three | Chromium pass at 1919x998 (page rendered, same content, no missing sections observed); Firefox not run; Safari not run |
| C3 | PK Hosting pricing renders in Chromium, Firefox, Safari | Open the pricing page in each browser at 1440x900 | Prices, plan cards, and buttons identical in all three | Chromium pass at 1919x998 (page rendered, same content, no missing sections observed); Firefox not run; Safari not run |
| C4 | PK Hosting WordPress page renders in Chromium, Firefox, Safari | Open the WordPress page in each browser at 1440x900 | Same layout and content in all three | Chromium pass at 1919x998 (page rendered, same content, no missing sections observed); Firefox not run; Safari not run |
| C5 | aiTransform blog and terms render in Chromium, Firefox, Safari | Open both pages in each browser at 1440x900 | Same layout and content in all three | Chromium pass at 1919x998 (page rendered, same content, no missing sections observed); Firefox not run; Safari not run |
| C6 | Fonts load in Chromium, Firefox, Safari | Open all 6 pages in each browser, check for fallback-font flashes or missing glyphs | Same fonts in all three, no missing glyphs | Chromium pass on the 4 pages checked live (no missing glyphs observed); Firefox not run; Safari not run |
| C7 | No console errors in Chromium, Firefox, Safari | Open all 6 pages in each browser, read the console | No errors that break layout or interaction | NOT RUN. Console was not read during the live run |
| C8 | Layout at 390px matches across Chromium, Firefox, Safari | Open all 6 pages in each browser at 390x844 | Same stacked layout in all three, no browser-only overflow | NOT RUN. No device emulation in this browser |

## Bug log summary (automated run)
B1: aiTransform home heading order, 12 skipped-level jumps, Medium.
B2: aiTransform mobile menu button has no accessible name (all 3 aiTransform pages), Medium.
B3: aiTransform home duplicate ids (instagram x2, adwords x2, paint0_linear x3), Low.
B4: aiTransform blog empty call-to-action link, Medium, needs a live check for JavaScript-injected label.
B5: aiTransform terms empty call-to-action link, Medium, needs a live check for JavaScript-injected label.
Full detail with steps to reproduce and recommended fixes: hidden_files/automated-findings.md.
Live-check bugs (added 6 Nov 2026, desktop 1919x998):
B6: aiTransform no skip-to-content link, Medium.
B7: aiTransform hero low contrast (nav links, hero text, audience labels, unselected tool buttons), Medium. Ratio not measured, visual observation only.
B8: aiTransform floating chat avatar button has no visible text label, Low.
B9: aiTransform Image Generator composite image alt does not describe its six example images, Medium.
B10: PK Hosting home top-bar text small light-grey on black, Low.
B11: PK Hosting home "Save up to 16%" and struck-through prices low contrast, Low.
B12: PK Hosting pricing billing-term toggle repeated 6 times, Medium.
B13: PK Hosting pricing small grey renewal text and domain-card grey text, Low.
B4 and B5 (empty call-to-action link on aiTransform blog and terms) are still unverified live: the live run did not open the blog or terms pages, so whether JavaScript fills the label is still unknown.
Full detail with steps to reproduce and recommended fixes: docs/bug-log.md.
