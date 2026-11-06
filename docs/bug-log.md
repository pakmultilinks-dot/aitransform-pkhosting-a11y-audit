# Bug log, TPT-2026-03078
# aiTransform and PK Hosting, WCAG 2.1 AA, checked 6 Nov 2026.
# Severity: High blocks use, Medium hard to use, Low cosmetic.
# Screenshots: docs/screenshots/ (live-check captures; automated bugs list the
# saved-page evidence instead where no live capture applies).

## B1, Medium, aiTransform home, heading order
- Steps to reproduce: open https://aitransform.com/ and read the heading outline
  (or run automation/auto_checks.py on docs/saved-pages/page-1-aitransform-home.html).
- Expected: headings in order (h1, then h2, then h3), one h1, outline matching the
  visual hierarchy.
- Actual: 12 skipped-level jumps. The page starts with an h6 before the h1. The six
  feature blocks jump h2 to h4. Feature eyebrow lines jump h3/h4 to h6. The h1 is one
  long concatenated string (Ultimate AITransformationTrainingBrandingVoiceoverProgrammer
  Image GeneratorSpeech To Text) that reads badly to a screen reader.
- Evidence: automated check, verified by hand against the saved page.
- Recommended fix: rebuild the heading outline to match the visual hierarchy (h1 page
  title, h2 section titles, h3 feature titles, h4 feature detail). Put the rotating
  words in the h1 as separate spans with spaces, or move the animation out of the h1.

## B2, Medium, aiTransform home, blog, terms, mobile menu button has no accessible name
- Steps to reproduce: open any aiTransform page on a mobile-width viewport (390x844)
  and inspect the menu button (class mobile-nav-trigger), or run the automated checker.
- Expected: the button has an accessible name (aria-label "Menu" or visible text).
- Actual: icon-only button with spans, no text, no aria-label, no title. A screen
  reader announces it as an unnamed button. It is the only unnamed button on each of
  the three pages.
- Evidence: automated check, verified by hand. Live check: pending browser task result.
- Recommended fix: add aria-label="Menu" and aria-expanded to the button in the shared
  header template. One fix clears all three pages.

## B3, Low, aiTransform home, duplicate id values
- Steps to reproduce: run automation/auto_checks.py on
  docs/saved-pages/page-1-aitransform-home.html and check the duplicate-id output.
- Expected: every id value used once per page.
- Actual: id instagram appears twice, id adwords twice, id paint0_linear three times,
  all on inline SVG elements.
- Evidence: automated check, verified by hand.
- Recommended fix: give each inline SVG a unique id (prefix by section), or drop the
  ids where they are not referenced.

## B4, Medium, aiTransform blog, empty call-to-action link
- Steps to reproduce: open https://aitransform.com/blog/ and inspect the call-to-action
  link under the "Blog Posts" heading (class lqd-btn, href #), or run the automated
  checker on docs/saved-pages/page-2-aitransform-blog.html.
- Expected: the link has accessible text in the HTML.
- Actual: no inner text in the static HTML. Its label appears to be injected by
  JavaScript from the link and text attributes on the tag. If JavaScript fails or is
  slow, the link is nameless.
- Evidence: automated check. Live check: pending browser task result (does it render
  with text?).
- Recommended fix: put the label text inside the link in the HTML, and keep the
  JavaScript enhancement as an enhancement, not the only source of the label.

## B5, Medium, aiTransform terms, empty call-to-action link
- Steps to reproduce: open https://aitransform.com/terms and inspect the same
  call-to-action link (class lqd-btn, href #), or run the automated checker on
  docs/saved-pages/page-3-aitransform-terms.html.
- Expected: the link has accessible text in the HTML.
- Actual: same as B4, no inner text in the static HTML, label injected by JavaScript.
- Evidence: automated check. Live check: pending browser task result.
- Recommended fix: same as B4. One template fix clears B4 and B5 together.

## Live-check bugs (Chromium desktop, 1919x998, 6 Nov 2026)
- Live pages checked: aiTransform home, aiTransform Image Generator tab (in-page, no
  separate public tool page exists), PK Hosting home, PK Hosting pricing. Blog, terms, and
  WordPress hosting were not live-checked. Desktop size was 1919x998, not the requested
  1440x900 (the browser cannot set a viewport size). Mobile 390x844 was not tested (no
  device emulation). Zoom 200 percent was not verified (Ctrl+ showed no change).

## B6, Medium, aiTransform home, no skip-to-content link
- Steps to reproduce: open https://aitransform.com/ and press Tab from the top of the page.
- Expected: the first Tab lands on a "Skip to content" link.
- Actual: the first Tab lands on the logo link. A keyboard user must tab through the whole
  navigation (logo, Home, Features, How it Works, Testimonials, Pricing, Resources, Login,
  Sign Up) to reach the content.
- Evidence: live check, screenshot docs/screenshots/Live-A-aiTransform-Home-Desktop.pdf.
- Recommended fix: add a "Skip to main content" link as the first focusable element, visible
  on focus, pointing at the main content region.

## B7, Medium, aiTransform home and Image Generator tab, low contrast in the hero
- Steps to reproduce: open https://aitransform.com/ at desktop size and read the hero.
- Expected: body and navigation text meets WCAG 2.1 AA contrast (4.5:1 for normal text).
- Actual: navigation links and the hero lines "Discover aiTransform" and "Do something
  extraordinary" are pale lavender/white on the light-purple gradient. Audience labels are
  faint: "Digital Agencies" gold on cream, "Enterpreneurs" teal on pale mint, "Businesses"
  pale purple on pale lavender. Unselected tool buttons ("AI Text Generator", "AI Code
  Generator", and others) are grey on white. No contrast ratio was measured for these
  colours; this is a visual observation, so the fix should be checked with a contrast tool.
- Evidence: live check, screenshots Live-A and Live-D. The faint text is visible in the
  first page of Live-A.
- Recommended fix: darken the hero text and the unselected tool-button text until each
  passes 4.5:1 on its background, and re-check with a contrast meter.

## B8, Low, aiTransform home, floating chat avatar button has no visible text label
- Steps to reproduce: open https://aitransform.com/ and look at the bottom-right corner.
- Expected: the chat button shows a label or an accessible name.
- Actual: a circular avatar image button with no visible text label.
- Evidence: live check, screenshot Live-A (bottom-right corner).
- Recommended fix: add an aria-label such as "Chat with support" to the button.

## B9, Medium, aiTransform Image Generator tab, composite image alt does not describe content
- Steps to reproduce: open https://aitransform.com/, switch to the "AI Image Generator"
  tab, and read the alt text of the large example image.
- Expected: the alt text describes the image content.
- Actual: the alt text is "Imagine, Genearate, Publish." (spelling as on the site), but the
  image shows six generated example images, including a robot, a cat, and a house, which the
  alt text does not describe. Meaningful image content has no text equivalent.
- Evidence: live check, screenshot Live-D.
- Recommended fix: rewrite the alt text to describe the six examples, or mark the image
  decorative (empty alt) and describe the examples in the surrounding text.

## B10, Low, PK Hosting home, top-bar text low contrast
- Steps to reproduce: open https://www.pkhosting.com/ and read the black top bar.
- Expected: small text meets 4.5:1.
- Actual: "support@pkhosting.com" and "(042) 35692952" are small light-grey text on black.
  The contact details are still readable, but the contrast is weak for small text.
- Evidence: live check, screenshot Live-B.
- Recommended fix: lighten the top-bar text colour until it passes 4.5:1 on black.

## B11, Low, PK Hosting home, billing toggle and struck-through prices low contrast
- Steps to reproduce: open https://www.pkhosting.com/ and read the billing toggle and the
  plan prices.
- Expected: prices and savings text meet 4.5:1.
- Actual: "Save up to 16%" is small dark-red text on a pale-pink pill, and struck-through
  original prices such as "was Rs 3,762" are small grey-green. Readable, but weak.
- Evidence: live check, screenshot Live-B.
- Recommended fix: darken the savings and struck-through price text until each passes
  4.5:1.

## B12, Medium, PK Hosting pricing, billing-term toggle repeated six times
- Steps to reproduce: open https://www.pkhosting.com/pricing/ and press Tab through the
  page.
- Expected: a keyboard user can pass each plan section without repeating the same control.
- Actual: the same four-button "Billing term" toggle (Monthly / Annually / 2 years /
  3 years) is repeated six times, once per plan section, so a keyboard user must tab
  through it repeatedly with no way past it.
- Evidence: live check, screenshot Live-C.
- Recommended fix: keep one billing-term toggle at the top of the page that applies to all
  plan sections, or add a skip link before each repeated toggle.

## B13, Low, PK Hosting pricing, small grey text on plan and domain cards
- Steps to reproduce: open https://www.pkhosting.com/pricing/ and read the plan cards and
  domain cards.
- Expected: renewal and offer text meets 4.5:1.
- Actual: the renewal line "First year Rs 4,490. Renews at Rs 6,990 for the same term.
  Add-ons and taxes extra." is small grey text, as are "Save up to 16% / 36%" and
  "Supplier offer ends 31 Dec 2026" on domain cards (.shop, .xyz, .me, .asia, .digital,
  .agency, .business, .company, .blog, .email).
- Evidence: live check, screenshot Live-C.
- Recommended fix: darken the renewal, savings, and offer-end text until each passes 4.5:1.

## Not verified (still open, needs a different environment)
- Mobile 390x844 layout, navigation, tap targets, and overflow on all 6 pages: not tested.
- Zoom to 200 percent and text resize on all 6 pages: not verified.
- Firefox and Safari rendering on all 6 pages: not run.
- B4 and B5 (empty call-to-action link on aiTransform blog and terms): live check still
  open, the live run did not open those pages, so whether JavaScript fills the label is
  still unknown.
- Console errors on all 6 pages: not read.
