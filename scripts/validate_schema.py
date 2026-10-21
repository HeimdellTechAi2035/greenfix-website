"""
Post-build QA check: validates every generated .html page in the repo root.
Run after scripts/build_site.py. Reports H1 count, JSON-LD validity, and
required meta tags for every page (excluding utility pages).
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

SKIP = {
    "404.html",
    "thank-you.html",
    "googlec72ca5999f108be1.html",
    # noindex HTML redirect stubs, not content pages
    "garden-maintenance-preston.html",
    "driveway-cleaning-preston.html",
    "window-cleaning-preston.html",
    "estate-agent-services.html",
    "garden-clearance-penwortham.html",
}

def breadcrumb_issues(data):
    """Google: every ListItem needs position, name, and an absolute item URL.
    The last item may omit item."""
    nodes = data if isinstance(data, list) else [data]
    issues = []
    for node in nodes:
        if not isinstance(node, dict) or node.get("@type") != "BreadcrumbList":
            continue
        items = node.get("itemListElement")
        if not isinstance(items, list) or not items:
            issues.append("BreadcrumbList has no itemListElement")
            continue
        for idx, item in enumerate(items):
            pos = idx + 1
            if not isinstance(item, dict) or item.get("@type") != "ListItem":
                issues.append(f"breadcrumb position {pos} is not a ListItem")
                continue
            if item.get("position") != pos:
                issues.append(f"breadcrumb position {pos} has position={item.get('position')!r}")
            name = item.get("name")
            if not isinstance(name, str) or not name.strip():
                issues.append(f"breadcrumb position {pos} is missing name")
            url = item.get("item")
            is_last = idx == len(items) - 1
            if url is None:
                if not is_last:
                    issues.append(f"breadcrumb position {pos} ({name!r}) is missing item")
                continue
            if not isinstance(url, str) or not url.startswith(("http://", "https://")):
                issues.append(f"breadcrumb position {pos} item is not an absolute URL: {url!r}")
    return issues


REQUIRED_TAGS = [
    ('<title>', "title"),
    ('name="description"', "meta description"),
    ('rel="canonical"', "canonical"),
    ('name="robots"', "robots meta"),
    ('property="og:title"', "og:title"),
    ('property="og:description"', "og:description"),
    ('name="twitter:card"', "twitter:card"),
]

total_issues = 0
files = sorted(glob.glob("*.html")) + sorted(glob.glob("blog/*.html"))

for f in files:
    if f in SKIP:
        continue
    try:
        content = open(f, encoding="utf-8").read()
    except UnicodeDecodeError as e:
        total_issues += 1
        print(f"{f}:")
        print(f"  - not valid UTF-8: {e}")
        continue
    issues = []

    h1s = re.findall(r"<h1[\s>]", content)
    if len(h1s) != 1:
        issues.append(f"H1 count = {len(h1s)} (expected 1)")

    for needle, label in REQUIRED_TAGS:
        if needle not in content:
            issues.append(f"missing {label}")

    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.S)
    if not blocks:
        issues.append("no JSON-LD blocks found")
    for i, b in enumerate(blocks):
        try:
            data = json.loads(b.strip())
        except json.JSONDecodeError as e:
            issues.append(f"invalid JSON-LD block {i}: {e}")
            continue
        issues.extend(breadcrumb_issues(data))

    if issues:
        total_issues += len(issues)
        print(f"{f}:")
        for issue in issues:
            print(f"  - {issue}")

print(f"\nChecked {len([f for f in files if f not in SKIP])} pages. {total_issues} issues found.")
