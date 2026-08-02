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

SKIP = {"404.html", "thank-you.html", "googlec72ca5999f108be1.html"}

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
    content = open(f, encoding="utf-8").read()
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
            json.loads(b.strip())
        except json.JSONDecodeError as e:
            issues.append(f"invalid JSON-LD block {i}: {e}")

    if issues:
        total_issues += len(issues)
        print(f"{f}:")
        for issue in issues:
            print(f"  - {issue}")

print(f"\nChecked {len([f for f in files if f not in SKIP])} pages. {total_issues} issues found.")
