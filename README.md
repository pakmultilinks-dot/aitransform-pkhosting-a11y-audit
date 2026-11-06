# aiTransform and PK Hosting: Accessibility, Responsive and Cross-Browser Audit

Task TPT-2026-03078, 4 pts, due 11 November 2026. Standard: WCAG 2.1 AA.
Public pages only. No forms submitted, no logins, no load testing, no security testing.

## Pages audited (all HTTP 200, fetched 6 Nov 2026)
| # | Page | URL |
|---|---|---|
| 1 | aiTransform home | https://aitransform.com/ |
| 2 | aiTransform blog | https://aitransform.com/blog/ |
| 3 | aiTransform terms | https://aitransform.com/terms |
| 4 | PK Hosting home | https://www.pkhosting.com/ |
| 5 | PK Hosting pricing | https://www.pkhosting.com/pricing/ |
| 6 | PK Hosting WordPress hosting | https://www.pkhosting.com/wordpress-hosting/ |

aiTransform tool pages (AI Writer, Image, Code, Chat) sit behind login, so they were not
audited. aiTransform /pricing returns 404 and was not used.

## What is in this repo
- `docs/test-plan.md`: test plan with 28 numbered test cases (A1-A12 accessibility,
  R1-R8 responsive, C1-C8 cross-browser), pages, devices, browsers, standard.
- `docs/automated-findings.md`: automated check failures, passes, and what could not
  be verified, with severity and reasoning.
- `docs/bug-log.md`: the bug log. Every bug has steps to reproduce, expected and actual
  result, severity, a screenshot reference, and a recommended fix.
- `docs/saved-pages/`: the exact HTML copies the automated checks ran against.
- `automation/auto_checks.py`: the automated checker (static HTML analysis).
- `automation/auto_results.json`: the checker's raw results for all 6 pages.
- `docs/report.html`: the published test report (also live on GitHub Pages).

## Method
1. Automated static checks on saved HTML copies (lang, title, viewport, alt text, labels,
   heading order, link and button names, duplicate ids, inline-style contrast only).
2. Live Chromium checks at desktop 1440x900 and mobile 390x844: keyboard navigation,
   visible focus, 200 percent zoom, text resize, contrast spot checks, menu and overflow.
3. Firefox and Safari were NOT run: no Firefox or Safari is available in this environment.
   Their test cases are written in the test plan so they can be run later.

## Headline results (6 Nov 2026)
- 5 distinct bugs, all on aiTransform. PK Hosting passed every automated check on all
  3 pages, and no live-check bug was found on PK Hosting.
- B1 (Medium): aiTransform home heading order, 12 skipped-level jumps, h6 before h1.
- B2 (Medium): aiTransform mobile menu button has no accessible name, on all 3 pages.
- B3 (Low): aiTransform home duplicate ids on inline SVGs.
- B4 (Medium): aiTransform blog empty call-to-action link (label injected by JavaScript).
- B5 (Medium): aiTransform terms, same empty call-to-action link.
- B2, B4, B5 come from shared header/footer/template components, so one template fix
  clears them on all three pages.

## How to re-run the automated checks
```
python3 automation/auto_checks.py
```
It reads the saved pages in `docs/saved-pages/` and writes `automation/auto_results.json`.
Re-fetch pages first if you want fresh input; the saved copies are the audited snapshot.
