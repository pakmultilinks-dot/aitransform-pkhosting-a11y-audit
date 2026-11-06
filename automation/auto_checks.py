# Automated accessibility checks (WCAG 2.1 AA) for TPT-2026-03078.
# Static HTML analysis only. Contrast covers inline styles only, not external CSS.
# Tap-target sizes cannot be verified from static HTML and are reported as needing a live check.
# No em dash or en dash anywhere in this file or its output.
import json
import os
import re
from collections import Counter

from bs4 import BeautifulSoup

BASE = os.path.expanduser("~/workspace/goals/aitransform-pkhosting-accessibility-cross-browser-audit-4-pts-due-11-nov")
PAGES_DIR = os.path.join(BASE, "hidden_files", "pages")
OUT = os.path.join(BASE, "hidden_files", "auto_results.json")

PAGES = [
    ("page-1-aitransform-home.html", "https://aitransform.com/", "aiTransform home"),
    ("page-2-aitransform-blog.html", "https://aitransform.com/blog/", "aiTransform blog"),
    ("page-3-aitransform-terms.html", "https://aitransform.com/terms", "aiTransform terms"),
    ("page-4-pkhosting-home.html", "https://www.pkhosting.com/", "PK Hosting home"),
    ("page-5-pkhosting-pricing.html", "https://www.pkhosting.com/pricing/", "PK Hosting pricing"),
    ("page-6-pkhosting-wordpress.html", "https://www.pkhosting.com/wordpress-hosting/", "PK Hosting WordPress hosting"),
]

GENERIC_LINK_TEXT = {"click here", "click", "here", "read more", "more", "link", "go", ">"}


def parse_style(style):
    out = {}
    for part in (style or "").split(";"):
        if ":" in part:
            k, v = part.split(":", 1)
            out[k.strip().lower()] = v.strip()
    return out


def parse_color(val):
    if not val:
        return None
    val = val.strip().lower()
    m = re.match(r"#([0-9a-f]{3}|[0-9a-f]{6})$", val)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    m = re.match(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", val)
    if m:
        return tuple(int(x) for x in m.groups())
    m = re.match(r"rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*\)", val)
    if m:
        if float(m.group(4)) < 1:
            return None  # translucent, cannot compute from static HTML
        return tuple(int(x) for x in m.groups()[:3])
    named = {
        "black": (0, 0, 0), "white": (255, 255, 255), "red": (255, 0, 0),
        "green": (0, 128, 0), "blue": (0, 0, 255), "gray": (128, 128, 128),
        "grey": (128, 128, 128), "yellow": (255, 255, 0),
    }
    return named.get(val)


def luminance(rgb):
    def ch(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg, bg):
    l1, l2 = luminance(fg), luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def check_page(fname, url, label):
    path = os.path.join(PAGES_DIR, fname)
    html = open(path, encoding="utf-8", errors="ignore").read()
    soup = BeautifulSoup(html, "html.parser")
    res = {"file": fname, "url": url, "label": label, "bytes": len(html), "checks": {}}
    c = res["checks"]

    # lang
    html_tag = soup.find("html")
    lang = (html_tag.get("lang") or "").strip() if html_tag else ""
    c["lang"] = {"status": "pass" if lang else "fail",
                 "value": lang or None,
                 "detail": "html lang attribute present: '%s'" % lang if lang else "html lang attribute missing"}

    # title
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    c["title"] = {"status": "pass" if title else "fail",
                  "value": title or None,
                  "detail": "title present and non-empty" if title else "title missing or empty"}

    # viewport
    vp = soup.find("meta", attrs={"name": "viewport"})
    c["viewport"] = {"status": "pass" if vp else "fail",
                     "value": vp.get("content") if vp else None,
                     "detail": "viewport meta present" if vp else "viewport meta missing"}

    # images and alt
    imgs = soup.find_all("img")
    missing_alt = []
    for img in imgs:
        alt = img.get("alt")
        if alt is None or alt.strip() == "":
            missing_alt.append(img.get("src", "")[:120] or "[no src]")
    c["img_alt"] = {"status": "pass" if not missing_alt else "fail",
                    "total_images": len(imgs), "missing_or_empty_alt": len(missing_alt),
                    "examples": missing_alt[:5],
                    "detail": "%d of %d images missing a non-empty alt" % (len(missing_alt), len(imgs))}

    # form inputs and labels
    inputs = soup.find_all(["input", "select", "textarea"])
    labelled_ids = set()
    for lab in soup.find_all("label"):
        if lab.get("for"):
            labelled_ids.add(lab["for"])
    unlabeled = []
    for inp in inputs:
        itype = (inp.get("type") or "").lower()
        if inp.name == "input" and itype in ("hidden", "submit", "button", "image", "reset"):
            continue
        ok = False
        if inp.get("id") and inp["id"] in labelled_ids:
            ok = True
        if inp.get("aria-label") or inp.get("aria-labelledby"):
            ok = True
        if inp.find_parent("label"):
            ok = True
        if not ok:
            unlabeled.append("%s name=%s id=%s" % (inp.name, inp.get("name", ""), inp.get("id", "")))
    c["input_labels"] = {"status": "pass" if not unlabeled else "fail",
                         "total_inputs": len(inputs), "unlabeled": len(unlabeled),
                         "examples": unlabeled[:5],
                         "detail": "%d of %d visible inputs without a label" % (len(unlabeled), len(inputs))}

    # headings
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    h1s = [h for h in headings if h.name == "h1"]
    levels = [int(h.name[1]) for h in headings]
    skipped = []
    prev = 0
    for i, lv in enumerate(levels):
        if prev and lv > prev + 1:
            skipped.append("heading %d (%s): level jumps from h%d to h%d" % (
                i + 1, headings[i].get_text(strip=True)[:60], prev, lv))
        prev = lv
    h1_fail = len(h1s) != 1
    c["headings"] = {"status": "pass" if (not h1_fail and not skipped) else "fail",
                     "total_headings": len(headings), "h1_count": len(h1s),
                     "h1_text": [h.get_text(strip=True)[:100] for h in h1s],
                     "skipped_levels": len(skipped), "examples": skipped[:5],
                     "detail": "h1 count %d; skipped-level jumps %d" % (len(h1s), len(skipped))}

    # links
    links = soup.find_all("a")
    bad_links = []
    for a in links:
        text = a.get_text(strip=True)
        aria = (a.get("aria-label") or "").strip()
        img_alts = " ".join((i.get("alt") or "").strip() for i in a.find_all("img")).strip()
        title = (a.get("title") or "").strip()
        if not text and not aria and not img_alts and not title:
            bad_links.append("empty link href=%s" % (a.get("href", "")[:100]))
        elif text.lower() in GENERIC_LINK_TEXT and not aria and not img_alts:
            bad_links.append("generic text '%s' href=%s" % (text, (a.get("href", "")[:80])))
    c["link_text"] = {"status": "pass" if not bad_links else "fail",
                      "total_links": len(links), "bad_links": len(bad_links),
                      "examples": bad_links[:5],
                      "detail": "%d of %d links with empty or generic text" % (len(bad_links), len(links))}

    # buttons
    buttons = soup.find_all("button")
    bad_btns = []
    for b in buttons:
        name = b.get_text(strip=True) or (b.get("aria-label") or "").strip() or (b.get("title") or "").strip()
        if not name:
            bad_btns.append("button type=%s class=%s" % (b.get("type", ""), (b.get("class") or [""])[0]))
    c["button_names"] = {"status": "pass" if not bad_btns else "fail",
                         "total_buttons": len(buttons), "unnamed_buttons": len(bad_btns),
                         "examples": bad_btns[:5],
                         "detail": "%d of %d buttons without an accessible name" % (len(bad_btns), len(buttons))}

    # duplicate ids
    ids = [t.get("id") for t in soup.find_all(True) if t.get("id")]
    dup = {k: v for k, v in Counter(ids).items() if v > 1}
    c["duplicate_ids"] = {"status": "pass" if not dup else "fail",
                          "total_ids": len(ids), "duplicated_ids": len(dup),
                          "examples": ["%s x%d" % (k, v) for k, v in list(dup.items())[:5]],
                          "detail": "%d duplicated id values" % len(dup)}

    # inline-style contrast. Only elements where BOTH foreground and background are known
    # from inline styles are scored. Where the background comes from a stylesheet it is
    # not verifiable from static HTML, so those elements are counted separately and never
    # assumed to sit on white. (An earlier run assumed white and wrongly flagged the
    # PK Hosting footer logo link, which sits on a dark footer set by CSS.)
    low = []
    checked = 0
    bg_unknown = 0
    for el in soup.find_all(True):
        st = parse_style(el.get("style", ""))
        fg = parse_color(st.get("color", ""))
        if fg is None:
            continue
        bg = None
        bgv = st.get("background-color") or st.get("background", "")
        bg = parse_color(bgv) if bgv else None
        if bg is None:
            node = el.parent
            depth = 0
            while node is not None and depth < 6:
                pst = parse_style(node.get("style", "") if hasattr(node, "get") else "")
                pb = parse_color(pst.get("background-color", "") or pst.get("background", ""))
                if pb is not None:
                    bg = pb
                    break
                node = node.parent
                depth += 1
        if bg is None:
            bg_unknown += 1
            continue
        ratio = contrast(fg, bg)
        checked += 1
        if ratio < 4.5:
            low.append("<%s> text='%s' fg=%s ratio=%.2f:1" % (
                el.name, el.get_text(strip=True)[:50], st.get("color", ""), ratio))
    c["inline_contrast"] = {"status": "pass" if not low else "fail",
                            "elements_checked": checked,
                            "inline_fg_with_stylesheet_bg": bg_unknown,
                            "below_4_5": len(low), "examples": low[:5],
                            "detail": "%d inline-styled text elements with a known inline background checked, %d below 4.5:1; %d more have an inline foreground but a stylesheet background and are not verifiable statically" % (checked, len(low), bg_unknown)}

    # tap targets: cannot be verified from static HTML
    n_targets = len(links) + len(buttons)
    c["tap_targets"] = {"status": "not verified",
                        "total_links_and_buttons": n_targets,
                        "detail": "Rendered size cannot be verified from static HTML; needs a live check at 1440x900 and 390x844"}

    return res


def main():
    results = {"standard": "WCAG 2.1 AA", "method": "static HTML analysis of saved pages; contrast covers inline styles only",
               "pages": []}
    for fname, url, label in PAGES:
        results["pages"].append(check_page(fname, url, label))
    # title uniqueness
    titles = [p["checks"]["title"]["value"] for p in results["pages"]]
    dup_titles = [t for t, n in Counter(titles).items() if n > 1 and t]
    results["title_uniqueness"] = {"status": "pass" if not dup_titles else "fail",
                                   "duplicated_titles": dup_titles,
                                   "detail": "all 6 titles unique" if not dup_titles else "duplicated titles: %s" % dup_titles}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    nfail = sum(1 for p in results["pages"] for ch in p["checks"].values() if ch["status"] == "fail")
    nnot = sum(1 for p in results["pages"] for ch in p["checks"].values() if ch["status"] == "not verified")
    print("pages:", len(results["pages"]), "failed checks:", nfail, "not verified:", nnot)
    for p in results["pages"]:
        fails = [k for k, v in p["checks"].items() if v["status"] == "fail"]
        print(p["label"], "->", "FAIL:" + ",".join(fails) if fails else "all automated checks pass")


if __name__ == "__main__":
    main()
