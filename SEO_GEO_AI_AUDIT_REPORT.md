# Greenfix Exterior Care SEO, GEO & AI Search Audit

## Executive Summary

The current homepage is broadly average for local SEO and AI search readiness. The page has strong localisation for Preston and Lancashire, clear service language, and consistent contact details. However, there are gaps in schema completeness, FAQ accuracy, page structure, and conversion clarity that hold the site back from ranking well for landlord/agent-focused exterior maintenance searches.

## Priority Fixes

### Critical fixes
- Improve schema completeness: add `WebPage` and `BreadcrumbList`, and fix weak/partial `Service` markup.
- Fix FAQ content duplication and poor question phrasing in visible page copy.
- Ensure the portal CTA and page explain exactly how clients request portal access.
- Replace or improve the current Open Graph image and alt text to use a real exterior maintenance visual.
- Remove the `priceRange` and `openingHours` if not fully accurate, or replace with a disclaimer/realistic business hour structure.

### High priority fixes
- Clarify the hero messaging so it is less generic and more explicitly targeted at landlords, letting agents, and property managers.
- Add more natural mention of local areas beyond Preston/Lancashire in the primary content and FAQ.
- Create stronger service-specific landing page links or anchor copy for top keywords (jet washing, gutter clearing, fence repairs, HMO maintenance).
- Add a distinct `Areas We Cover` section to homepage copy, not just a list of towns.

### Medium priority fixes
- Add a visible `Request Portal Access` explanation near the top of the page.
- Improve heading hierarchy, especially the duplicate `h2` structure in the FAQ and portal sections.
- Add more explicit service list copy in the main content that matches primary keyword themes.
- Improve page accessibility by adding aria labels and reducing inline styling where possible.

### Nice-to-have fixes
- Add testimonials/reviews if available for trust and entity relevance.
- Add a small local business map or a service area graphic.
- Add `BreadcrumbList` schema for better search engine context.
- Add structured `contactPoint` details to visible content to mirror JSON-LD.

## SEO Audit Findings

- `<title>` is strong: `External Maintenance Preston & Lancashire | Greenfix Exterior Care`.
- Meta description is good and includes Preston/Lancashire, but reads a little generic and could be more compelling.
- Homepage has a canonical URL set to `https://greenfixexterior-care.co.uk/`.
- There is exactly one visible `<h1>`.
- Heading structure is acceptable but not ideal: there are several `h2` sections and inline `h3` elements used for bullets.
- Preston and Lancashire are naturally included.
- Services are described, but the visible copy is broad and could use more specific service keyword matches.
- The site explicitly says who the business serves, with good coverage of landlords, letting agents, property managers, HMOs, serviced accommodation operators, businesses, and homeowners.

## Local SEO Findings

- The homepage actively targets Preston and Lancashire.
- Nearby areas are included in content and the `Areas We Cover` section.
- NAP is consistent on the homepage and in JSON-LD:
  - Business name: `GreenFix Exterior Care`
  - Email: `admin@greenfixexterior-care.co.uk`
  - Phone: `07447804597`
  - Website: `https://greenfixexterior-care.co.uk/`
- There is an `Areas We Cover` section with the requested towns.
- Location-based service phrases appear, but could be stronger and more keyword-focused.
- The site is generally suitable for Google Business Profile support, though it would benefit from clearer NAP markup and more localised trust signals.

## GEO / AI Search Findings

- The site clearly states what the business does: external maintenance and exterior property care.
- It clearly states who it serves.
- It clearly states where it operates.
- It lists many services, though the wording is broad.
- Clients can contact the business by phone, email, and a quote form.
- The portal is mentioned and linked correctly to `https://portal.greenfixexterior-care.co.uk`.
- The entity name is consistent.
- The wording is reasonably specific but can be improved for AI citations.
- The site answers many customer questions directly, but some FAQ headings and answers are generic or duplicate.

## Schema Findings

### Exists
- `LocalBusiness` schema exists and is valid JSON.
- `WebSite` schema exists.
- `Service` schema exists.
- `Organization` schema exists.
- `FAQPage` schema exists.

### Missing / weak
- `WebPage` schema is missing.
- `BreadcrumbList` schema is missing.
- `Service` schema is weak: it lists only some services and uses generic `serviceType` values.
- `FAQPage` schema appears valid, but some visible FAQ headings/answers are duplicated or mismatched and could confuse AI.
- `LocalBusiness` includes `openingHours` and `priceRange` that could be inaccurate or misleading if not verified.
- There is no explicit `sameAs` link beyond one Facebook URL.
- There is no structured `contactPoint` in a way that maps to visible page copy beyond JSON-LD.

### Specific schema notes
- `LocalBusiness` includes Preston and Lancashire and the right phone/email.
- `LocalBusiness` areaServed covers many towns, which is good.
- `Service` schema uses areaServed and audience, but could be more detailed and should include the full service list.
- `FAQPage` is present and valuable for AI answer engines.

## Content Findings

- Copy is mostly clear, localised, and professional.
- Some sections feel too broad and generic for high-intent landlord/agency searches.
- There is strong local coverage, but the language should be tightened around specific services and buyer personas.
- The hero is good but would benefit from more direct service mentions like `gutter clearing Preston`, `fence repairs Preston`, `HMO exterior maintenance`, and `serviced accommodation maintenance`.
- The FAQ answers are generally helpful but the visible FAQ has one broken heading character and inconsistent phrasing (`â“ How much does it cost?`).
- The `Who We Work With` section is strong for trust and targeting.
- The `Areas We Cover` section is present, but the copy should include the full list in sentences, not only cards.
- The portal explanation is present, but the wording could be more explicit: "Approved clients request portal access via the quote form or by calling 07447804597."

## Conversion Findings

- Strong CTAs are present: `Request Portal Access`, `Client Portal Login`, `Call GreenFix`, and `Get My FREE Quote`.
- The main CTA is visible above the fold.
- The client portal is explained, but the path to request access could be clearer.
- The portal login button does link to `https://portal.greenfixexterior-care.co.uk` correctly.
- The email is correctly shown as `admin@greenfixexterior-care.co.uk`.
- The homepage CTA mix is good, but the page has too many separate CTA sections that dilute focus.

## Technical SEO Findings

- `viewport` meta tag is present.
- `robots.txt` exists and includes a sitemap reference.
- `sitemap.xml` exists with a good page list.
- `404.html` exists.
- Favicon files are referenced.
- Internal links are present and appear strong.
- No obvious broken links were found in homepage content.
- Image alt text exists on the hero image.
- The hero image file names are not ideal (`hero image.png`, `ChatGPT Image...`) and are not descriptive.
- There is some inline CSS and styling, which is not ideal but acceptable for a static page.
- Mobile responsiveness appears likely due to responsive container styles, but no explicit mobile audit was performed.
- There are no visible aria label issues from the homepage source, but more accessibility polish is possible.
- There is no `rel="canonical"` issue on the homepage.
- The `robots.txt` disallows unusual site files such as `_redirects` and `netlify.toml`; this is fine.

## Image SEO Findings

- The hero image has alt text, which is good.
- Filenames are not descriptive and include spaces and `ChatGPT Image`, which is bad for SEO.
- The hero image alt text is relevant but could be more specific about services/locations.
- There is no explicit lazy loading rule for the hero image; it is okay on a static page but could help speed.
- The overall image strategy is weak because it relies on generic asset names.

## AI Citation / Answer Engine Improvements

- The site has a solid entity signal for GreenFix Exterior Care.
- The service list is present but could be made more conversational and answer-focused.
- The FAQ schema and question-answer format is a strong asset.
- The site needs clearer "What we do", "Who we serve", and "Where we operate" sections with natural language.
- The content should include explicit answers to the key AI questions, especially around portal access and HMO property services.
- More local references to Preston, Lancashire, and nearby towns in full sentences would help citation.
- The current business description is good, but the homepage should echo it in visible copy more directly.

## Competitor Readiness

The site is moderately strong for the target local keywords, but not yet competitive enough for top local slots in Preston and Lancashire for landlord/property manager searches. It needs more content depth, stronger local signals, better schema, and clearer service landing pages to compete for:
- `external maintenance Preston`
- `garden maintenance Preston`
- `gutter clearing Preston`
- `fence repairs Preston`
- `property maintenance for landlords Preston`
- `exterior maintenance for letting agents Lancashire`

## Recommended Fix Plan

### Phase 1
- Enhance homepage metadata and OG image.
- Add `WebPage` and `BreadcrumbList` schema.
- Improve visible portal access language and CTA clarity.
- Fix the FAQ section headings and one broken character.
- Update service copy to include exact target keywords.

### Phase 2
- Strengthen homepage content with explicit local area sentences and more specific service calls.
- Add a stronger `Areas We Cover` narrative.
- Add a clearer local business contact block on the homepage.
- Add better service-specific anchor text and internal links.

### Phase 3
- Improve technical SEO: rename images, add lazy loading, remove inline CSS where possible, validate mobile performance.
- Add accessibility improvements: aria labels, button contrast, form labels.
- Review `robots.txt` and sitemap coverage for all service pages.

### Phase 4
- Add AI-friendly answer-style content for key questions.
- Add more natural entity signals and trust data.
- Add structured local business details in visible copy (NAP block, service area list, sameAs links).

## Exact Recommended Changes

- `index.html`:
  - Keep current title but refine description to include the strongest keyword phrases and more action.
  - Add a short `h2` near the top: `External maintenance for landlords, letting agents and property managers in Preston & Lancashire`.
  - Replace the hero service list with a stronger benefit statement.
  - Add a visible portal access sentence immediately under the hero CTA.
  - Improve the FAQ section headings and correct the broken typography.
  - Rename image assets to SEO-friendly names like `preston-exterior-maintenance.jpg` and `preston-exterior-maintenance-og.png`.
  - Add a local business contact block with `Phone`, `Email`, and `Service areas`.

- `index.html` JSON-LD:
  - Add `@type: WebPage` schema.
  - Add `BreadcrumbList` schema for homepage context.
  - Expand `Service` schema with all key service names and area coverage.
  - Remove or confirm `openingHours` and `priceRange`.
  - Add `logo` and additional `sameAs` links if available.

- `robots.txt`:
  - Keep the sitemap entry.
  - Consider removing `Disallow: /NETLIFY_DEPLOYMENT.md` if not necessary for crawlers.

- `sitemap.xml`:
  - Keep current entries and ensure all main service pages are listed.
  - Add any missing service/location pages.

## Final Score

- Traditional SEO: 70/100
- Local SEO: 72/100
- GEO / AI Search Readiness: 65/100
- Conversion Readiness: 72/100
- Technical SEO: 68/100

---

### Files Inspected
- `index.html`
- `robots.txt`
- `sitemap.xml`

### Report Status
- `SEO_GEO_AI_AUDIT_REPORT.md` has been created.

### Top 10 Fixes in Plain English
1. Add missing `WebPage` and `BreadcrumbList` schema.
2. Make the hero copy more specific to Preston/Lancashire landlords, letting agents, and property managers.
3. Improve FAQ wording and fix the broken heading text.
4. Add a clearer visible explanation of how to request portal access.
5. Rename and improve image assets and OG image metadata.
6. Add a stronger local area coverage paragraph with the target towns.
7. Expand the homepage service copy to include exact keyword phrases like `gutter clearing Preston` and `HMO exterior maintenance`.
8. Add a visible contact block with phone, email, and service area details.
9. Review and update `robots.txt` disallow rules if needed.
10. Confirm the portal login CTA remains correct and make it more prominent.
