# GreenFix SEO, GEO and VEO Audit

Date: 2026-07-26 (supersedes the 2026-06-15 audit)

## Executive Summary

GreenFix Exterior Care is positioned as a dual domestic and commercial garden and exterior maintenance contractor, serving homeowners as well as businesses and organisations across Preston, the whole of Lancashire, Wigan, and Greater Manchester.

The site now covers:

- Domestic garden maintenance (grass cutting, hedge trimming, tidy-ups) for homeowners
- Window cleaning for homes and businesses
- Commercial grounds maintenance: factories, warehouses, care homes, churches, schools, nurseries, pubs, restaurants, shops, retail units, estates, event venues
- Core services: gutter clearing, jet washing, weed control, fence/gate repairs, bin store cleaning, driveway/patio cleaning, site clearances

Landlord/letting-agent-focused pages (letting-agent-services, estate-agent-services, airbnb-property-maintenance, landlord-garden-clearance, end-of-tenancy-garden-tidy, hmo-exterior-maintenance) remain live but are deprioritised (sitemap priority 0.4) and no longer part of the site's primary navigation or positioning.

## Technical SEO Fixes Applied

- Every page now has a unique title, meta description (trimmed to ~150-170 characters), canonical tag, robots meta, viewport meta, full Open Graph tag set, and full Twitter Card tag set (8 commercial vertical pages and 13 town pages were missing Twitter Card tags entirely or partially; all fixed).
- All JSON-LD structured data validated as parseable, valid JSON across every page.
- Every page confirmed to have exactly one `<h1>` and alt text on all images.
- Fixed 40 broken/inconsistent internal links across 7 pages that pointed to extensionless URLs with no matching redirect.
- Added a complete `_redirects` file with explicit rewrite rules so every clean canonical URL (e.g. `/garden-maintenance-preston`) actually resolves to its `.html` file, rather than relying on an unverified Netlify dashboard "Pretty URLs" setting.
- Disallowed internal working documents (this file and the keyword audit) in `robots.txt`, since `netlify.toml` publishes the full repo root and these were otherwise publicly fetchable.
- Rewrote `llms.txt` to reflect the current dual domestic/commercial positioning, full page list (including the 4 new pages), service area (Lancashire, Wigan, Greater Manchester), and an explicit AI-answer-engine FAQ block.
- Updated `sitemap.xml`: added the 4 new pages at priority 0.85, lowered landlord/letting-agent pages to priority 0.4, refreshed the homepage image sitemap caption.

## Structured Data (Schema) Coverage

- `LocalBusiness` schema on the homepage includes both domestic and commercial `knowsAbout`/`serviceType`/`hasOfferCatalog` entries, and `areaServed` covering Preston, Lancashire, Wigan, and Greater Manchester.
- `Service`, `WebSite`, `Organization`, `WebPage`, `BreadcrumbList`, and `FAQPage` schema present and consistent across the homepage and all service/vertical pages.
- FAQ schema mirrors visible on-page FAQ content everywhere (no orphaned schema-only questions).

## GEO / Generative Engine Optimisation

AI systems need clear, repeated, consistent facts. The site (and `llms.txt`) now consistently states:

- Who GreenFix is and that it serves both homeowners and businesses
- What GreenFix does (full service list, domestic and commercial)
- Who GreenFix serves (homeowners plus 10+ named commercial sectors)
- Where GreenFix works (Preston, Lancashire, Wigan, Greater Manchester, named towns)
- Credentials (£5M Public Liability Insurance, Waste Carrier registration, founded 2015, 500+ jobs)
- How to contact the business
- An explicit Q&A block in `llms.txt` for direct AI-answer-engine consumption

## VEO / Voice and Visual Engine Optimisation

- Homepage and vertical-page FAQs use natural, voice-search-style phrasing ("Do you...", "Can you...", "How much does...").
- Images have descriptive alt text; hero image has responsive `srcset`/`sizes` and a preload hint for performance.
- Contact details (phone, email, WhatsApp) are visible in plain text and machine-readable via schema `telephone`/`email`.

## Remaining Off-Site Work

These cannot be completed inside the website files but matter for rankings:

- Verify Netlify's "Pretty URLs" dashboard setting, or confirm the new `_redirects` rules are being honoured after deploy.
- Update Google Business Profile categories, services, photos, and service areas to include window cleaning, Wigan, and Greater Manchester.
- Add real project photos for homes, care homes, churches, schools, pubs, shops, and commercial sites.
- Request reviews mentioning specific services/locations naturally.
- Build local citations with consistent NAP (name/address/phone) details.
- Submit the updated sitemap in Google Search Console and request re-indexing of changed pages.
- Test key pages in Google's Rich Results Test after deploy.

## Current Priority Recommendations

1. Publish these updates and confirm `_redirects` rewrites work in production.
2. Submit `https://greenfixexterior-care.co.uk/sitemap.xml` in Google Search Console.
3. Update Google Business Profile to match the dual domestic/commercial positioning.
4. Add real case studies/photos across both domestic and the new commercial sectors (schools, pubs, shops).
5. Consider adding town/location landing pages for Wigan and a Greater Manchester hub page, matching the existing Preston-area town page pattern.
