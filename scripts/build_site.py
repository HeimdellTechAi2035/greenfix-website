# -*- coding: utf-8 -*-
"""
GreenFix Exterior Care — static site generator.

This is a local authoring tool, not a runtime dependency. It renders plain
.html files from the data tables below; nothing here executes at Netlify
deploy time (netlify.toml build.command is empty, publish = "."). Run:

    python scripts/build_site.py

from the repo root to (re)generate every page listed in SERVICES, SECTORS,
plus index.html, about-greenfix.html and before-after.html.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOMAIN = "https://greenfixexterior-care.co.uk"
BUSINESS_NAME = "GreenFix Exterior Care"
PHONE_DISPLAY = "07447804597"
PHONE_TEL = "+447447804597"
EMAIL = "admin@greenfixexterior-care.co.uk"
ADDRESS_LOCALITY = "Preston"
ADDRESS_REGION = "Lancashire"
AREA_SERVED = ["Preston"]
FOUNDED = "2026"
INSURANCE = "£5M Public Liability Insurance"
WASTE_CARRIER = "Environment Agency registered Waste Carrier"
TRAINED = "Fully trained, experienced team"
FACEBOOK = "https://www.facebook.com/profile.php?id=61589641812157"
LINKEDIN = "https://www.linkedin.com/company/greenfix-exterior-care/"
TIKTOK = "https://www.tiktok.com/@greenfixpreston"
PORTAL_URL = "https://portal.greenfixexterior-care.co.uk"
LOGO_IMG = "Screenshot 2026-05-16 154245.png"

# Geo/map data — sourced from the live Google Business Profile listing for
# "greenfix exterior care" so the embed, schema geo and Maps link all agree
# with each other and with GBP (a real E-E-A-T/local-SEO consistency signal).
STREET_ADDRESS = "11 Lowercroft"
POSTAL_LOCALITY = "Preston"
POSTAL_CODE = "PR1 9DJ"
HOURS_DISPLAY = "Monday - Friday, 9:00am - 5:00pm"
OPENING_HOURS_SPEC = [
    {"@type": "OpeningHoursSpecification",
     "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
     "opens": "09:00", "closes": "17:00"},
]
GEO_LATITUDE = "53.77025605"
GEO_LONGITUDE = "-2.69715175"
GOOGLE_MAPS_CID = "7185723301089874500"
GOOGLE_MAPS_SHARE_URL = f"https://www.google.com/maps?cid={GOOGLE_MAPS_CID}"
GOOGLE_MAPS_EMBED_SRC = (
    "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2360.157296838098"
    "!2d-2.7206403999999997!3d53.7332732!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1"
    "!3m3!1m2!1s0x922e72176a362ef%3A0x63b8d1454fb59244!2sgreenfix%20exterior%20care"
    "!5e0!3m2!1sen!2suk!4v1785751584980!5m2!1sen!2suk"
)

COMPLAINTS_STEPS = [
    ("Contact us", f"Call or WhatsApp {PHONE_DISPLAY}, or email {EMAIL}, as soon as possible after noticing the issue. Please describe the problem and include photos if you can."),
    ("We respond within 24 hours", "We'll acknowledge your complaint and arrange to inspect the work, in person or from photos."),
    ("We put it right", "Where we're at fault, we return to correct the work at no extra charge, on a timeframe agreed directly with you."),
    ("If we can't agree a resolution", "You can raise the matter with the Citizens Advice consumer service or your local Trading Standards office for independent advice."),
]

BUSINESS_ID = f"{DOMAIN}/#business"

# ---------------------------------------------------------------------------
# Cluster / nav definitions
# ---------------------------------------------------------------------------

CLUSTERS = [
    {
        "key": "grounds",
        "label": "Grounds & Garden Care",
        "slugs": ["grounds-maintenance", "garden-maintenance", "lawn-mowing",
                  "hedge-trimming", "garden-tidy-ups", "pressure-washing",
                  "window-cleaning", "internal-window-cleaning", "external-window-cleaning"],
    },
    {
        "key": "repairs",
        "label": "Repairs & Maintenance",
        "slugs": ["exterior-structural-repairs", "repairs-and-maintenance",
                  "brick-repointing", "brick-repairs", "garden-wall-repairs",
                  "fence-repairs", "fence-panel-replacement", "gate-repairs", "patio-repairs",
                  "paving-repairs", "slab-relaying", "roof-tile-repairs",
                  "drain-repairs", "drainage-repairs", "window-repairs",
                  "door-repairs", "residential-property-maintenance",
                  "planned-preventative-maintenance", "drone-property-inspections"],
    },
]

SECTORS = [
    ("commercial-maintenance.html", "Commercial Maintenance"),
    ("factory-warehouse-grounds-maintenance.html", "Factories & Warehouses"),
    ("care-home-grounds-maintenance-preston.html", "Care Homes"),
    ("church-grounds-maintenance-preston.html", "Churches"),
    ("estate-grounds-maintenance-lancashire.html", "Estates & Heritage Grounds"),
    ("event-venue-grounds-maintenance-preston.html", "Events & Venues"),
    ("school-nursery-grounds-maintenance-preston.html", "Schools & Nurseries"),
    ("pub-restaurant-grounds-maintenance-preston.html", "Pubs & Restaurants"),
    ("shop-retail-exterior-maintenance-preston.html", "Shops & Retail Units"),
]

# ---------------------------------------------------------------------------
# SERVICES — the 21 final GBP-aligned URLs + window-cleaning (owner-approved extra)
# Each entry:
#   slug, cluster, h1, tagline, price, price_note, meta_title, meta_description,
#   intro, cards (title, text)x4, faqs (q,a)x3-5, related (slugs), schema_desc
# ---------------------------------------------------------------------------

SERVICES = [
    # ---------------- Grounds & Garden Care ----------------
    dict(
        slug="grounds-maintenance", cluster="grounds",
        h1="Grounds Maintenance in Preston",
        tagline="Regular contract grounds care for larger plots, estates and business premises",
        price="From £40", price_note="per visit, guide price only",
        meta_title="Grounds Maintenance Preston | From £40 | GreenFix",
        meta_description="Grounds maintenance in Preston for estates, business premises and larger plots. Scheduled visits, one point of contact. From £40.",
        intro="GreenFix provides scheduled grounds maintenance for larger residential plots, managed estates, and business premises across Preston. Where garden maintenance covers a single household garden, grounds maintenance is built for bigger areas and ongoing contracts: communal grounds, verges, car park borders, and multi-visit schedules where one point of contact and consistent standards matter more than a one-off visit.",
        cards=[
            ("Scheduled Visits", "Weekly, fortnightly or monthly rounds set up to suit your grounds and the growing season, not a one-size-fits-all schedule."),
            ("One Point of Contact", "A single contact for multi-site or multi-visit contracts, so nothing gets lost between different teams or subcontractors."),
            ("Communal & Managed Areas", "Verges, borders, communal lawns, and shared grounds kept consistently tidy for residents, tenants, staff and visitors."),
            ("Fully Insured Contractor", f"{INSURANCE} and {WASTE_CARRIER}, so green waste is removed and disposed of properly on every visit."),
        ],
        faqs=[
            ("What's the difference between grounds maintenance and garden maintenance?",
             "Grounds maintenance is built for larger or managed sites — estates, business premises, communal areas — usually on a scheduled contract. Garden maintenance is for a single household garden. Call us if you're not sure which fits your site; we'll point you the right way."),
            ("Can you set up a regular contract?",
             "Yes. We can agree a weekly, fortnightly or monthly schedule and keep to it, with one point of contact for the whole contract."),
            ("Do you cover multiple sites for the same client?",
             "Yes. We regularly work with clients who manage more than one site or plot, keeping standards and scheduling consistent across all of them."),
            ("What's included in a typical visit?",
             "Grass cutting, edging, hedge and border upkeep, and general tidying of communal or grounds areas. Tell us what your site needs and we'll quote accordingly."),
        ],
        related=["garden-maintenance", "lawn-mowing", "hedge-trimming", "repairs-and-maintenance"],
        schema_desc="Scheduled grounds maintenance contracts for estates, managed sites and business premises across Preston.",
    ),
    dict(
        slug="garden-maintenance", cluster="grounds",
        h1="Garden Maintenance in Preston",
        tagline="Regular, reliable garden care for your home",
        price="From £40", price_note="per visit, guide price only",
        meta_title="Garden Maintenance Preston | From £40 | GreenFix",
        meta_description="Garden maintenance in Preston for homeowners. Mowing, edging, weeding and seasonal upkeep, on a one-off or regular basis. From £40.",
        intro="GreenFix keeps residential gardens tidy, healthy and under control across Preston. That covers the everyday jobs that keep a garden looking cared-for between the bigger seasonal work: mowing and edging, weeding beds and borders, light pruning, and general upkeep. Book a one-off visit or set up a regular round — whichever suits how you use your garden.",
        cards=[
            ("Regular or One-Off", "Set up a fortnightly or monthly round, or book a single visit when your garden needs bringing back under control."),
            ("Lawns, Beds & Borders", "Mowing, edging, weeding and light pruning to keep the whole garden looking after itself between visits."),
            ("Seasonal Adjustments", "Visit frequency and jobs adjusted through the growing season, so summer growth and autumn tidy-ups are both covered properly."),
            ("Green Waste Removed", f"All cuttings and garden waste taken away and disposed of responsibly — we're a {WASTE_CARRIER}."),
        ],
        faqs=[
            ("Do I need to be in for a garden maintenance visit?",
             "No. As long as we can access the garden safely, most regular garden maintenance visits don't need you to be home."),
            ("Can you take away the cuttings and waste?",
             f"Yes. We remove all garden waste from every visit and dispose of it properly as a {WASTE_CARRIER}."),
            ("What's the difference between this and a garden tidy-up?",
             "Garden maintenance is ongoing upkeep — regular visits that keep an already-reasonable garden looking good. A garden tidy-up is a one-off reset for a garden that's become overgrown or neglected."),
            ("How often should I book a visit?",
             "Most gardens do well on a fortnightly or monthly round through spring and summer, less often over winter. We'll suggest a schedule based on your garden when we quote."),
        ],
        related=["lawn-mowing", "hedge-trimming", "garden-tidy-ups", "grounds-maintenance"],
        schema_desc="Regular and one-off garden maintenance for homeowners across Preston, including mowing, edging, weeding and seasonal upkeep.",
    ),
    dict(
        slug="lawn-mowing", cluster="grounds",
        h1="Lawn Mowing in Preston",
        tagline="A neatly cut lawn, every time",
        price="From £20", price_note="per cut, guide price only",
        meta_title="Lawn Mowing Preston | From £20 | GreenFix",
        meta_description="Professional lawn mowing in Preston. Regular cuts or a one-off, with edging included. From £20 per cut.",
        intro="GreenFix cuts lawns across Preston, from a single overdue mow to a regular weekly or fortnightly round through the growing season. Every cut includes edging so borders and paths stay crisp, and we adjust blade height and frequency as the season changes — shorter, more frequent cuts in peak growth, longer intervals when growth slows.",
        cards=[
            ("Regular Rounds", "Weekly or fortnightly cuts booked in through spring and summer, so you're never chasing an overgrown lawn."),
            ("Edging Included", "Every mow includes edging along borders, paths and driveways for a genuinely finished look."),
            ("One-Off Cuts", "Lawn got away from you? We can bring an overgrown lawn back under control with a first cut, then set up a regular round from there."),
            ("Clippings Handled", "Grass clippings collected and removed as standard, so you're not left to rake and bag them up yourself."),
        ],
        faqs=[
            ("How often should my lawn be cut?",
             "Weekly during peak growth (spring/early summer), fortnightly is usually enough the rest of the season. We'll recommend a schedule when we see your lawn."),
            ("Can you cut a very overgrown lawn?",
             "Yes. Very long or overgrown grass may need a first cut at a higher blade height before we can get it down to a normal length, but we handle this as standard."),
            ("Do you take the clippings away?",
             "Yes, clippings are collected and removed as part of the service."),
            ("Is edging included in the price?",
             "Yes, every cut includes edging along borders, paths and driveway edges."),
        ],
        related=["garden-maintenance", "hedge-trimming", "garden-tidy-ups"],
        schema_desc="Regular and one-off lawn mowing with edging included, for homes across Preston.",
    ),
    dict(
        slug="hedge-trimming", cluster="grounds",
        h1="Hedge Trimming in Preston",
        tagline="Neat, healthy hedges cut to shape",
        price="From £40", price_note="per visit, guide price only",
        meta_title="Hedge Trimming Preston | From £40 | GreenFix",
        meta_description="Professional hedge trimming in Preston. Shaping, height reduction and waste removal, one-off or seasonal. From £40.",
        intro="GreenFix trims and shapes hedges across Preston, from a routine seasonal cut to bringing an overgrown or misshapen hedge back under control. We cut to a clean, even line, reduce height where needed, and clear all the cuttings away — you're left with a tidy hedge and a tidy garden, not a pile of green waste to deal with yourself.",
        cards=[
            ("Shaping & Height Reduction", "Hedges cut to a clean, level line, with height and width brought back under control where they've grown out."),
            ("Right Time of Year", "We time cuts sensibly through the growing season and take care around nesting birds in spring, in line with standard good practice."),
            ("All Hedge Types", "Conifer, privet, beech, laurel and mixed boundary hedges — different growth habits, same tidy finish."),
            ("Waste Cleared Away", f"All cuttings removed and disposed of properly — we're a {WASTE_CARRIER}."),
        ],
        faqs=[
            ("What time of year should hedges be trimmed?",
             "Most hedges benefit from a cut in late spring/early summer and again in early autumn. We'll advise on timing for your specific hedge type when we quote."),
            ("Can you reduce the height of an overgrown hedge?",
             "Yes. Height reduction is a common job — we bring overgrown hedges back down gradually where a hard cut all at once could damage the hedge."),
            ("Do you remove the cuttings?",
             "Yes, all hedge cuttings and waste are cleared away and disposed of after every visit."),
            ("Can you set up a regular hedge trimming schedule?",
             "Yes, we can add hedge trimming to a regular garden maintenance round, or book it as a stand-alone seasonal visit."),
        ],
        related=["garden-maintenance", "lawn-mowing", "garden-tidy-ups"],
        schema_desc="Hedge trimming, shaping and height reduction with waste removal, for homes across Preston.",
    ),
    dict(
        slug="garden-tidy-ups", cluster="grounds",
        h1="Garden Tidy-Ups in Preston",
        tagline="A full reset for an overgrown or neglected garden",
        price="From £80", price_note="per visit, guide price only",
        meta_title="Garden Tidy-Ups Preston | From £80 | GreenFix",
        meta_description="Garden tidy-ups in Preston. A full one-off reset for overgrown gardens — clearing, cutting back and waste removal. From £80.",
        intro="A garden tidy-up is a one-off reset, not a routine visit: for gardens that have been left, overgrown, or need bringing back under control before regular maintenance can take over. We clear overgrown beds, cut back shrubs and brambles, remove weeds, and take away everything we clear — leaving a garden that's actually manageable again.",
        cards=[
            ("Full Garden Reset", "Overgrown beds, borders and lawns cleared and cut back in a single visit, not a partial tidy."),
            ("Cutting Back & Clearing", "Brambles, self-seeded growth, dead plants and overgrown shrubs cut back and cleared."),
            ("All Waste Removed", f"Everything we clear is taken away and disposed of responsibly — we're a {WASTE_CARRIER}, so nothing is left in bags for you to sort out."),
            ("A Fresh Starting Point", "Once a garden's been reset, we can set up a regular garden maintenance round to keep it that way."),
        ],
        faqs=[
            ("How is this different from garden maintenance?",
             "A garden tidy-up is a one-off deep clear for a garden that's become overgrown or neglected. Garden maintenance is the regular, ongoing upkeep that keeps a garden looking good once it's already in reasonable shape."),
            ("Do you take away everything you clear?",
             f"Yes. All green waste, cuttings and cleared material is removed and disposed of properly — we're a {WASTE_CARRIER}."),
            ("Can you deal with a very overgrown or neglected garden?",
             "Yes, this is exactly the job a garden tidy-up is for. Tell us the current state of the garden when you call and we'll quote accordingly."),
            ("Can I set up regular maintenance after the tidy-up?",
             "Yes, many clients book a one-off tidy-up first and then move onto a regular garden maintenance round once the garden is back under control."),
        ],
        related=["garden-maintenance", "lawn-mowing", "hedge-trimming"],
        schema_desc="One-off garden tidy-ups and overgrown garden clearance for homes across Preston.",
    ),
    dict(
        slug="pressure-washing", cluster="grounds",
        h1="Pressure Washing in Preston",
        tagline="Restore patios, driveways and paths",
        price="From £95", price_note="per visit, guide price only",
        meta_title="Pressure Washing Preston | From £95 | GreenFix",
        meta_description="Professional pressure washing in Preston. Patios, driveways, paths and walls cleaned of moss, algae and grime. From £95.",
        intro="GreenFix pressure washes patios, driveways, paths and exterior walls across Preston, removing built-up moss, algae, grime and staining. This is a cleaning service — restoring the surface you already have to look its best — not a structural repair. If a surface is actually cracked, sunken or damaged rather than just dirty, see our patio repairs, paving repairs or slab relaying pages instead.",
        cards=[
            ("Patios & Driveways", "Block paving, slabs, concrete and tarmac cleaned of moss, algae, oil marks and general grime."),
            ("Paths & Walkways", "Slippery, moss-covered paths cleaned back to a safe, presentable surface."),
            ("Walls & Boundaries", "Garden walls and exterior surfaces cleaned as part of a full property tidy-up."),
            ("Correct Pressure for the Surface", "The right pressure and technique for each surface type, so cleaning doesn't damage joints, pointing or block paving sand."),
        ],
        faqs=[
            ("Will pressure washing damage my patio or driveway?",
             "No, when done correctly. We match pressure and technique to the surface — block paving, natural stone and concrete all need slightly different handling."),
            ("Can you remove green algae and moss?",
             "Yes, this is one of the most common reasons people book pressure washing, and it's straightforward to remove and makes surfaces safer underfoot."),
            ("What if my patio is actually cracked or sunken, not just dirty?",
             "That's a repair job rather than a cleaning job — see our patio repairs, paving repairs or slab relaying pages, or call us and we'll point you the right way."),
            ("Do you clean driveways as well as patios?",
             "Yes, we clean driveways, patios, paths and garden walls."),
        ],
        related=["patio-repairs", "paving-repairs", "slab-relaying", "garden-maintenance"],
        schema_desc="Pressure washing for patios, driveways, paths and walls across Preston, removing moss, algae and grime.",
    ),
    dict(
        slug="window-cleaning", cluster="grounds",
        h1="Window Cleaning in Preston",
        tagline="Domestic and commercial window cleaning",
        price="Free Quote", price_note="price depends on property size and frequency",
        meta_title="Window Cleaning Preston | GreenFix",
        meta_description="Domestic and commercial window cleaning in Preston. Regular rounds or one-off cleans, frames and sills included. Free quote.",
        intro="GreenFix provides window cleaning for homes and businesses across Preston, as a regular round or a one-off clean. Frames and sills are cleaned as standard, not just the glass, so you get a genuinely finished result rather than streak-free panes surrounded by grubby frames.",
        cards=[
            ("Domestic Rounds", "Regular monthly or fortnightly window cleaning for houses, or a one-off clean when you need it."),
            ("Commercial Window Cleaning", "Shopfronts, offices and commercial premises cleaned on a schedule that fits your trading hours."),
            ("Frames & Sills Included", "We clean frames and sills as part of every visit, not just the glass."),
            ("Reliable Scheduling", "Set up a regular round and we turn up when we say we will — no chasing needed."),
        ],
        faqs=[
            ("Do you offer regular window cleaning rounds?",
             "Yes, monthly or fortnightly rounds are available, as well as one-off cleans."),
            ("Do you clean commercial and shop windows?",
             "Yes, we clean shopfronts, office windows and commercial premises as well as domestic homes."),
            ("How much does window cleaning cost?",
             "Pricing depends on property size and how often you'd like it done. Call for a free, no-obligation quote."),
            ("Is this the same as window repairs?",
             "No — window cleaning is cleaning the glass, frames and sills. If a window itself is damaged, stuck, or the glazing seal has failed, see our window repairs page instead."),
        ],
        related=["external-window-cleaning", "internal-window-cleaning", "window-repairs"],
        schema_desc="Domestic and commercial window cleaning across Preston, regular rounds or one-off cleans.",
    ),
    # ---------------- Repairs & Maintenance ----------------
    dict(
        slug="exterior-structural-repairs", cluster="repairs",
        h1="Exterior Structural Repairs in Preston",
        tagline="Masonry, walls and structural brickwork put right",
        price="Quotation Required", price_note="every structural job is assessed individually",
        meta_title="Exterior Structural Repairs Preston | GreenFix",
        meta_description="Exterior structural repairs in Preston: brickwork, garden walls and masonry. Every job assessed and quoted individually. Call for a survey.",
        intro="Exterior structural repairs cover the bigger masonry and brickwork jobs — cracked or failing brickwork, leaning or unstable garden walls, and other structural issues on the outside of a property. Because the scope of a structural repair varies so much from one property to the next, we assess every job individually before quoting rather than working to a fixed guide price. If you know exactly what needs doing, our brick repointing, brick repairs and garden wall repairs pages cover the more specific, defined jobs.",
        cards=[
            ("Free Site Assessment", "We visit, assess the extent of the issue, and explain what's actually needed before any work starts."),
            ("Brickwork & Masonry", "Cracked, spalled or unstable brickwork assessed and repaired to restore both appearance and structural integrity."),
            ("Garden & Boundary Walls", "Leaning, cracked or partially collapsed walls assessed for safe, lasting repair."),
            ("Clear, Honest Quotes", "A written quote before any work begins, so you know exactly what you're agreeing to."),
        ],
        faqs=[
            ("Why is this quotation-only rather than a fixed price?",
             "Structural repairs vary enormously in scope — a hairline crack and a partially collapsed wall are very different jobs. We assess each one individually so the quote actually reflects the work needed."),
            ("Do you do a free assessment?",
             "Yes, we'll visit, assess the issue, and provide a written quote before any work starts."),
            ("What's the difference between this and brick repairs or garden wall repairs?",
             "This page is for bigger or less clear-cut structural issues that need assessing first. If you already know it's specifically a repointing job, a few damaged bricks, or a garden wall repair, those pages have guide prices to start from."),
            ("Is this covered by insurance?",
             f"We hold {INSURANCE} for all work we carry out. Whether a specific repair is covered by your own buildings insurance depends on your policy and the cause of the damage."),
        ],
        related=["brick-repairs", "brick-repointing", "garden-wall-repairs", "repairs-and-maintenance"],
        schema_desc="Structural brickwork, masonry and garden wall repair assessment and quotation across Preston.",
    ),
    dict(
        slug="repairs-and-maintenance", cluster="repairs",
        h1="Repairs and Maintenance in Preston",
        tagline="General exterior upkeep, from small fixes to ongoing contracts",
        price="Quotation Required", price_note="scope varies job to job",
        meta_title="Repairs and Maintenance Preston | GreenFix",
        meta_description="General exterior repairs and maintenance in Preston — gutter clearing, bin store upkeep and general property fixes. Call for a quote.",
        intro="Repairs and Maintenance is our general property upkeep service — for the smaller, ongoing exterior jobs that don't need a dedicated specialist page of their own, and for clients who'd rather have one contractor handle a list of odd jobs than book several separate trades. That includes tasks like gutter clearing and bin store area upkeep, general exterior tidying, and small fixes around a property, either as a one-off visit or an ongoing maintenance arrangement.",
        cards=[
            ("Gutter Clearing", "Blocked gutters cleared of leaves and debris so rainwater drains away properly instead of overflowing."),
            ("Bin Store & Communal Areas", "Bin storage areas and shared exterior spaces kept clean and presentable for managed or commercial sites."),
            ("General Property Fixes", "Smaller exterior maintenance jobs that don't fit neatly into a single trade, handled as part of a wider visit."),
            ("One-Off or Ongoing", "Book a single visit to work through a list of jobs, or set up a regular maintenance arrangement."),
        ],
        faqs=[
            ("Do you clear gutters as part of this service?",
             "Yes, gutter clearing is one of the most common jobs we handle under general repairs and maintenance."),
            ("Can you look after bin store or communal areas for a managed site?",
             "Yes, we work with managed and commercial sites to keep bin storage and shared exterior areas clean and presentable."),
            ("What if I have several small jobs that don't fit one category?",
             "That's exactly what this service is for — tell us the list and we'll quote for the visit as a whole rather than needing you to book separate trades."),
            ("Can this become a regular arrangement?",
             "Yes, many clients start with a one-off visit and move onto a regular maintenance schedule once we know their site."),
        ],
        related=["exterior-structural-repairs", "grounds-maintenance", "gate-repairs"],
        schema_desc="General exterior repairs and maintenance including gutter clearing and bin store upkeep, across Preston.",
    ),
    dict(
        slug="brick-repointing", cluster="repairs",
        h1="Brick Repointing in Preston",
        tagline="Restoring worn or crumbling mortar joints",
        price="From £30 per m²", price_note="guide price only, confirmed after assessment",
        meta_title="Brick Repointing Preston | From £30/m² | GreenFix",
        meta_description="Brick repointing in Preston. Repair eroded or crumbling mortar joints and restore weatherproofing. From £30 per m².",
        intro="Repointing repairs the mortar joints between bricks, not the bricks themselves. Over time, mortar erodes, crumbles or falls out, letting water into the wall and weakening it. We rake out the damaged mortar and repoint with a matching mix, restoring both the weatherproofing and the appearance of the brickwork. If the bricks themselves are cracked or damaged rather than the mortar, see our brick repairs page instead.",
        cards=[
            ("Mortar Joint Repair", "Eroded, crumbling or missing mortar raked out and repointed to stop water getting into the wall."),
            ("Matched Mortar Mix", "Mortar colour and mix matched to the existing brickwork wherever possible, for a consistent finish."),
            ("Weatherproofing Restored", "Properly repointed brickwork keeps water out and prevents the frost damage that follows once mortar has failed."),
            ("Priced Per Square Metre", "Priced by area, so you get a clear guide cost based on how much brickwork actually needs repointing."),
        ],
        faqs=[
            ("How do I know if I need repointing?",
             "Signs include mortar that's crumbling, cracked, or missing between bricks, and damp patches appearing on internal walls near affected brickwork."),
            ("Is this the same as brick repairs?",
             "No. Repointing repairs the mortar between bricks. Brick repairs deals with damaged, cracked, or spalled bricks themselves. Often a wall needs one or the other, sometimes both — we'll advise after an assessment."),
            ("Will the new mortar match my existing brickwork?",
             "We match the mortar mix and colour to the existing pointing as closely as possible for a consistent finish."),
            ("How is repointing priced?",
             "From £30 per m² as a guide price, confirmed once we've assessed the area and extent of the work needed."),
        ],
        related=["brick-repairs", "garden-wall-repairs", "exterior-structural-repairs"],
        schema_desc="Brick repointing to repair eroded or crumbling mortar joints, priced per square metre, across Preston.",
    ),
    dict(
        slug="brick-repairs", cluster="repairs",
        h1="Brick Repairs in Preston",
        tagline="Repairing damaged, cracked or missing bricks",
        price="From £50 minimum", price_note="guide price only, confirmed after assessment",
        meta_title="Brick Repairs Preston | From £50 | GreenFix",
        meta_description="Brick repairs in Preston — replacing damaged, cracked or spalled bricks. From £50 minimum, guide price.",
        intro="Brick repairs deal with the bricks themselves, not just the mortar between them: cracked, spalled (flaking) or missing bricks caused by frost damage, impact, or age. We remove and replace the damaged bricks, matching the size, colour and bond of the surrounding brickwork as closely as possible. Where the surrounding mortar has also failed, we'd usually recommend repointing alongside the repair.",
        cards=[
            ("Cracked & Spalled Bricks", "Damaged bricks removed and replaced, addressing frost damage, impact damage or general deterioration."),
            ("Matched Replacement Bricks", "New bricks matched to the existing wall's size, colour and bond wherever possible."),
            ("Minimum Callout Applies", "A minimum charge applies to brick repair jobs to reflect the setup and matching work involved, even for a small number of bricks."),
            ("Combined with Repointing", "Where surrounding mortar has also failed, we'll flag this and quote for repointing alongside the brick repair."),
        ],
        faqs=[
            ("What causes bricks to crack or spall?",
             "Frost damage is the most common cause — water gets into a brick, freezes, and expands, causing the surface to flake or crack. Impact damage and age also contribute."),
            ("Will the replacement bricks match the rest of the wall?",
             "We match size, colour and bond as closely as possible, though an exact match isn't always available for older or reclaimed brick types."),
            ("Why is there a minimum charge?",
             "Sourcing matching bricks and setting up for a brick repair takes similar time whether it's one brick or several, so a minimum charge applies from £50."),
            ("Do I need repointing as well as brick repairs?",
             "Sometimes — if the mortar around the damaged bricks has also failed, we'll point this out and quote for both."),
        ],
        related=["brick-repointing", "garden-wall-repairs", "exterior-structural-repairs"],
        schema_desc="Repair and replacement of damaged, cracked or spalled bricks, matched to existing brickwork, across Preston.",
    ),
    dict(
        slug="garden-wall-repairs", cluster="repairs",
        h1="Garden Wall Repairs in Preston",
        tagline="Rebuilding and repairing freestanding boundary walls",
        price="From £50", price_note="guide price only, confirmed after assessment",
        meta_title="Garden Wall Repairs Preston | From £50 | GreenFix",
        meta_description="Garden wall repairs in Preston. Leaning, cracked or collapsed boundary walls rebuilt and repaired. From £50.",
        intro="Garden and boundary walls take a lot of punishment — ground movement, weather, and simple age can leave them leaning, cracked, or with sections partially collapsed. We repair and rebuild freestanding garden and boundary walls, including coping stones and wall piers, restoring both stability and appearance. This is specifically for standalone garden/boundary walls, as distinct from a house's structural brickwork (see brick repairs) or fencing (see fence repairs).",
        cards=[
            ("Leaning & Unstable Walls", "Walls that have started to lean or move assessed for safe rebuilding or partial reconstruction."),
            ("Cracked & Collapsed Sections", "Damaged or collapsed sections rebuilt to match the rest of the wall."),
            ("Coping Stones & Piers", "Damaged coping stones and wall piers repaired or replaced as part of the job."),
            ("Boundary & Garden Walls Only", "Specifically for freestanding garden and boundary walls — for a house's structural brickwork, see our brick repairs page."),
        ],
        faqs=[
            ("My garden wall is leaning — is that dangerous?",
             "A leaning wall can be a safety concern, especially near a path or boundary with public access. We'd recommend having it assessed promptly rather than waiting."),
            ("Can you rebuild just the damaged section, not the whole wall?",
             "In many cases, yes — we assess how much of the wall actually needs rebuilding versus what can be repaired in place."),
            ("Do you repair coping stones as well as the brickwork?",
             "Yes, coping stones and wall piers are repaired or replaced as part of a garden wall repair where needed."),
            ("Is this the same as fence repairs?",
             "No — this page covers brick, block or stone garden walls. For timber or panel fencing, see our fence repairs page instead."),
        ],
        related=["brick-repairs", "brick-repointing", "fence-repairs", "exterior-structural-repairs"],
        schema_desc="Repair and rebuilding of freestanding garden and boundary walls, including coping stones and piers, across Preston.",
    ),
    dict(
        slug="fence-repairs", cluster="repairs",
        h1="Fence Repairs in Preston",
        tagline="Panels, posts and boundary fencing repaired",
        price="From £85", price_note="guide price only, confirmed after assessment",
        meta_title="Fence Repairs Preston | From £85 | GreenFix",
        meta_description="Fence repairs in Preston — broken panels, damaged posts and boundary fencing repaired for homes and businesses. From £85.",
        intro="GreenFix repairs fences for homes and businesses across Preston: broken or blown-down panels, rotten or leaning posts, loose boards, and general boundary fence repairs. Fences take the worst of the weather, so a repair now — rather than waiting — usually costs a lot less than replacing the whole run later.",
        cards=[
            ("Panels & Boards", "Broken, blown-down or rotten panels and individual boards replaced to match the rest of the fence line."),
            ("Posts & Foundations", "Leaning, rotten or snapped posts replaced and properly re-set, since a failing post is usually why a fence keeps coming down."),
            ("Storm Damage", "Fences blown down or damaged in high winds repaired promptly — we know these jobs often can't wait."),
            ("Domestic & Commercial", "Garden fences, boundary fencing and commercial site fencing, all repaired to the same standard."),
        ],
        faqs=[
            ("Can you repair just one section, not the whole fence?",
             "Yes, most fence repairs are for a specific damaged section or post rather than the whole run — we'll only replace what actually needs it."),
            ("My fence blew down in a storm — can you fix it quickly?",
             "Yes, storm-damaged fencing is one of the most common jobs we get and we prioritise it where we can."),
            ("Why has my fence post rotted but not the panels?",
             "Posts sit in or near the ground and take the most moisture, so they often fail before the panels above them. Replacing a rotten post properly usually solves recurring fence problems."),
            ("How much does a fence repair cost?",
             "From £85 as a guide price, depending on what needs repairing — a single panel is a smaller job than a rotten post that needs digging out and resetting."),
        ],
        related=["fence-panel-replacement", "gate-repairs", "garden-wall-repairs"],
        schema_desc="Fence panel, post and boundary fence repairs for homes and businesses across Preston.",
    ),
    dict(
        slug="gate-repairs", cluster="repairs",
        h1="Gate Repairs in Preston",
        tagline="Hinges, latches and gate alignment fixed",
        price="From £65", price_note="guide price only, confirmed after assessment",
        meta_title="Gate Repairs Preston | From £65 | GreenFix",
        meta_description="Gate repairs in Preston. Sticking, sagging or damaged gates, hinges and latches repaired for homes and businesses. From £65.",
        intro="A gate that sticks, sags, or won't latch properly is usually a hinge, alignment or frame problem rather than something that needs a full replacement. We repair and adjust garden and boundary gates, timber and metal, for homes and businesses across Preston — fixing hinges, latches, and alignment so the gate opens, closes and locks the way it should.",
        cards=[
            ("Hinges & Latches", "Worn, rusted or broken hinges and latches replaced so the gate operates smoothly again."),
            ("Sagging & Sticking Gates", "Misaligned gates adjusted and re-hung so they swing freely and close properly."),
            ("Timber & Metal Gates", "Garden gates, driveway gates and metal security gates repaired to suit the material and use."),
            ("Domestic & Commercial", "Residential garden gates and commercial site access gates, repaired to the same standard."),
        ],
        faqs=[
            ("Why is my gate sagging or dragging on the ground?",
             "This is usually a hinge or post problem rather than the gate itself — worn hinges or a settling post let the gate drop out of alignment over time."),
            ("Can you repair the gate instead of replacing it?",
             "In most cases, yes — hinge, latch and alignment problems can usually be fixed without replacing the whole gate."),
            ("Do you repair metal gates as well as timber?",
             "Yes, we repair both timber and metal garden, driveway and site access gates."),
            ("How much does a gate repair cost?",
             "From £65 as a guide price, depending on what needs fixing — a hinge adjustment is a smaller job than replacing a full gate frame."),
        ],
        related=["fence-repairs", "door-repairs", "repairs-and-maintenance"],
        schema_desc="Gate hinge, latch and alignment repairs for homes and businesses across Preston.",
    ),
    dict(
        slug="patio-repairs", cluster="repairs",
        h1="Patio Repairs in Preston",
        tagline="Cracked, sunken or loose patio slabs repaired",
        price="From £95", price_note="guide price only, confirmed after assessment",
        meta_title="Patio Repairs Preston | From £95 | GreenFix",
        meta_description="Patio repairs in Preston — cracked, sunken or loose slabs fixed. From £95. This is a structural repair, not patio cleaning.",
        intro="Patio repairs deal with a patio that's actually damaged — cracked, sunken, loose or unstable slabs — rather than one that just needs cleaning. We re-bed loose slabs, replace cracked ones, and correct sunken areas so the surface is safe and level again. If your patio just looks dirty or mossy rather than damaged, our pressure washing service is the quicker, cheaper fix.",
        cards=[
            ("Cracked & Damaged Slabs", "Individual cracked or damaged slabs lifted and replaced to match the surrounding patio."),
            ("Sunken & Uneven Areas", "Sunken sections re-bedded and levelled, removing trip hazards and standing water."),
            ("Loose & Rocking Slabs", "Loose slabs re-bedded on a proper base so they no longer rock or shift underfoot."),
            ("Repair, Not Cleaning", "If your patio is dirty rather than damaged, see our pressure washing page — a much quicker and cheaper fix."),
        ],
        faqs=[
            ("How do I know if I need a repair or just a clean?",
             "If slabs are cracked, sunken, loose or rocking, that's a repair job. If the patio is just discoloured, mossy or slippery but structurally sound, pressure washing will sort it."),
            ("Can you fix just the damaged slabs, not the whole patio?",
             "Yes, in most cases we can lift and replace or re-bed specific damaged or sunken slabs without redoing the whole patio."),
            ("What causes a patio to sink or slabs to come loose?",
             "Usually a failing or unstable base underneath — poor original installation, ground movement, or water washing out the bedding material over time."),
            ("Do you match the replacement slabs to my existing patio?",
             "We match slab type and size wherever possible; exact colour matching depends on whether your original slabs are still available."),
        ],
        related=["paving-repairs", "slab-relaying", "pressure-washing"],
        schema_desc="Repair of cracked, sunken or loose patio slabs across Preston, distinct from patio cleaning.",
    ),
    dict(
        slug="paving-repairs", cluster="repairs",
        h1="Paving Repairs in Preston",
        tagline="Driveways and paths repaired, not just cleaned",
        price="From £65", price_note="guide price only, confirmed after assessment",
        meta_title="Paving Repairs Preston | From £65 | GreenFix",
        meta_description="Paving repairs in Preston — cracked block paving, potholes and sunken driveway or path areas fixed. From £65.",
        intro="Paving repairs cover driveways, paths and walkways where the paving itself has failed — cracked block paving, small potholes, sunken sections, or edging that's come loose and let the paving spread. We lift, re-lay or replace the affected paving and restore proper edge restraint so the repair actually lasts, rather than sinking again within a season.",
        cards=[
            ("Cracked Block Paving", "Individual cracked or damaged blocks lifted and replaced to match the surrounding paving."),
            ("Sunken Areas & Potholes", "Sunken driveway or path sections re-based and re-laid to remove trip hazards and pooling water."),
            ("Edge Restraint Repairs", "Loose or missing edging replaced — this is often why paving has started spreading or sinking in the first place."),
            ("Driveways & Paths", "Domestic driveways, footpaths and walkways, in block paving, tarmac patch repair, or slabbed surfaces."),
        ],
        faqs=[
            ("What's the difference between paving repairs and patio repairs?",
             "Paving repairs covers driveways and paths; patio repairs covers patio areas specifically. The underlying problems (cracking, sinking, loose edges) are similar, so if you're not sure which applies, just call us and describe the area."),
            ("Why has my driveway started sinking in one spot?",
             "Usually a localised base failure — often from water getting under the paving through a gap, or from loose edge restraint letting the blocks spread and settle."),
            ("Can you match new blocks to my existing driveway?",
             "We match block type, size and colour as closely as possible; older or discontinued block ranges may not be an exact match."),
            ("Do you repair tarmac driveways too?",
             "Yes, we can patch-repair cracked or sunken tarmac areas as well as block paving and slabbed surfaces."),
        ],
        related=["patio-repairs", "slab-relaying", "pressure-washing"],
        schema_desc="Repair of cracked, sunken or poorly edged driveway and path paving across Preston.",
    ),
    dict(
        slug="slab-relaying", cluster="repairs",
        h1="Slab Relaying in Preston",
        tagline="Lifting and relaying uneven or poorly-laid slabs",
        price="From £95", price_note="guide price only, confirmed after assessment",
        meta_title="Slab Relaying Preston | From £95 | GreenFix",
        meta_description="Slab relaying in Preston — uneven or poorly-laid patio and path slabs lifted, re-based and relaid level. From £95.",
        intro="Slab relaying is about levelling: lifting existing slabs that have become uneven, don't drain properly, or were poorly laid in the first place, and relaying them on a corrected, properly-fallen base. Unlike patio or paving repairs, the slabs themselves aren't necessarily damaged — the problem is how they're sitting, not the slab material.",
        cards=[
            ("Uneven & Rocking Slabs", "Slabs that rock, sit unevenly, or have settled at different heights lifted and relaid level."),
            ("Poor Drainage Falls", "Slabs corrected to the proper fall so water drains away from the house rather than pooling or running the wrong way."),
            ("Existing Slabs Reused", "Where the slabs themselves are in good condition, we relay the same slabs rather than replacing them — keeping cost down."),
            ("Proper Base Preparation", "A corrected, well-compacted base underneath, so the relaid area stays level rather than moving again."),
        ],
        faqs=[
            ("How is this different from patio or paving repairs?",
             "Those pages are for damaged (cracked, sunken, broken) slabs or blocks. Slab relaying is for slabs that are still sound but sitting unevenly, badly, or with poor drainage falls — the fix is relaying them properly, not replacing them."),
            ("Do you reuse my existing slabs?",
             "Where the slabs are in good condition, yes — we lift, re-base and relay the same slabs, which is usually more cost-effective than full replacement."),
            ("Why is water pooling on my patio or path?",
             "Usually the slabs weren't laid with the correct fall (slope) to direct water away, or the base has settled unevenly since installation. Relaying corrects this."),
            ("Can you relay just part of a patio or path?",
             "Yes, we can relay a specific uneven section rather than the whole area, where that's all that needs correcting."),
        ],
        related=["patio-repairs", "paving-repairs", "drainage-repairs"],
        schema_desc="Lifting and relaying uneven or poorly-drained patio and path slabs across Preston.",
    ),
    dict(
        slug="roof-tile-repairs", cluster="repairs",
        h1="Roof Tile Repairs in Preston",
        tagline="Slipped, cracked or missing tiles refitted",
        price="From £250", price_note="guide price only, confirmed after assessment",
        meta_title="Roof Tile Repairs Preston | From £250 | GreenFix",
        meta_description="Roof tile repairs in Preston. Slipped, cracked or missing roof and ridge tiles refitted or replaced. From £250.",
        intro="Slipped, cracked or missing roof tiles are more than a cosmetic problem — they let water into the roof structure, and a small repair now is far cheaper than the damp or timber damage that follows if it's left. We refit slipped tiles, replace cracked or missing ones, and repair ridge tiles, matching tile type where possible to keep the roof looking consistent.",
        cards=[
            ("Slipped Tiles Refitted", "Tiles that have slipped out of position refitted and properly secured, before wind gets underneath them and causes further damage."),
            ("Cracked & Missing Tiles", "Damaged or missing tiles replaced, matched to the existing roof covering wherever possible."),
            ("Ridge Tile Repairs", "Loose or cracked ridge tiles re-bedded and repointed, a common source of roof leaks."),
            ("Assessed for Safety", "All roof work carried out with proper access equipment and safety precautions."),
        ],
        faqs=[
            ("How do I know if I have a slipped or missing tile?",
             "Often it's spotted from the ground — a gap or an oddly-angled tile — or after noticing a damp patch appearing inside near the roofline. We can assess from the ground or by safe access."),
            ("Is a small number of tiles worth repairing, or should I wait?",
             "It's worth repairing promptly. A single slipped or missing tile lets water into the roof structure, and what starts as a small repair can become a much bigger (and more expensive) one if left."),
            ("Can you match the replacement tiles to my roof?",
             "We match tile type, profile and colour as closely as possible; exact matches depend on whether your existing tile type is still available."),
            ("Do you repair ridge tiles as well as the main roof?",
             "Yes, ridge tile repointing and re-bedding is a common part of roof tile repair work."),
        ],
        related=["drainage-repairs", "drain-repairs", "exterior-structural-repairs"],
        schema_desc="Repair and replacement of slipped, cracked or missing roof and ridge tiles across Preston.",
    ),
    dict(
        slug="drain-repairs", cluster="repairs",
        h1="Drain Repairs in Preston",
        tagline="Blocked, cracked or collapsed drains fixed",
        price="From £95", price_note="guide price only, confirmed after assessment",
        meta_title="Drain Repairs Preston | From £95 | GreenFix",
        meta_description="Drain repairs in Preston — blocked, cracked or collapsed drain runs, downpipes and gullies fixed. From £95.",
        intro="Drain repairs cover an individual drain, downpipe or gulley that's blocked, cracked, or has collapsed — the kind of problem that shows up as slow-draining water, a bad smell, or water surfacing where it shouldn't. We diagnose the specific cause, clear blockages, and repair or reseal damaged pipework and joints. For broader surface-water or land drainage issues, see our drainage repairs page instead.",
        cards=[
            ("Blocked Drains Cleared", "Blockages in drain runs, downpipes and gullies cleared so water flows away properly again."),
            ("Cracked & Collapsed Pipework", "Damaged sections of drain pipe repaired or replaced where a blockage is caused by physical damage rather than debris."),
            ("Gullies & Downpipe Connections", "Leaking or poorly-sealed joints between downpipes and drains resealed and reconnected."),
            ("Individual Drains, Not Whole Systems", "For a single problem drain. If water is pooling more broadly across a garden or driveway, see drainage repairs."),
        ],
        faqs=[
            ("How do I know if a drain is blocked or actually damaged?",
             "A simple blockage usually clears with rodding; if the problem keeps coming back at the same spot, that often points to a cracked or collapsed section of pipe needing repair rather than just clearing."),
            ("What's the difference between drain repairs and drainage repairs?",
             "Drain repairs is for a specific drain, downpipe or gulley that's blocked or damaged. Drainage repairs covers broader surface-water problems — waterlogged lawns, poor land drainage — that aren't about one single pipe."),
            ("What causes drains to crack or collapse?",
             "Ground movement, tree root ingress, age, and sometimes the original installation being poor quality can all cause pipework to crack or collapse over time."),
            ("Can you fix a smell coming from a drain?",
             "Often, yes — a bad smell is frequently caused by a blockage, a dried-out trap, or a damaged seal, all of which we can diagnose and fix."),
        ],
        related=["drainage-repairs", "roof-tile-repairs", "repairs-and-maintenance"],
        schema_desc="Repair of blocked, cracked or collapsed individual drains, downpipes and gullies across Preston.",
    ),
    dict(
        slug="drainage-repairs", cluster="repairs",
        h1="Drainage Repairs in Preston",
        tagline="Waterlogged gardens and surface water put right",
        price="From £95", price_note="guide price only, confirmed after assessment",
        meta_title="Drainage Repairs Preston | From £95 | GreenFix",
        meta_description="Drainage repairs in Preston — waterlogged gardens, poor surface water drainage and soakaways fixed. From £95.",
        intro="Drainage repairs deal with broader surface-water problems — waterlogged lawns, patios or driveways that hold water long after rain has stopped, and land or garden drainage that isn't working properly. Rather than a single blocked pipe (see drain repairs), this is about how water moves, or fails to move, across a whole area: soakaways, French drains, and channel drains that need repairing, clearing, or installing to solve the problem properly.",
        cards=[
            ("Waterlogged Lawns & Gardens", "Areas that stay wet or boggy long after rain assessed and fitted with proper land drainage."),
            ("Soakaways & French Drains", "Existing soakaways and French drains that have stopped working cleared, repaired, or replaced."),
            ("Channel Drains", "Surface channel drains across driveways and patios repaired or unblocked so water is carried away rather than pooling."),
            ("Diagnose the Actual Cause", "We identify why water isn't draining properly before recommending a fix, rather than guessing."),
        ],
        faqs=[
            ("Why does part of my garden stay waterlogged after rain?",
             "Usually poor natural drainage in that area, a failed or missing soakaway, or ground that's become compacted over time. We assess the specific cause before recommending a fix."),
            ("What's a soakaway and how do I know if mine has failed?",
             "A soakaway is an underground structure that lets water disperse into the surrounding ground. If it's failed — often through silting up — water will surface or pool nearby instead of draining away."),
            ("Is this the same as drain repairs?",
             "No — drain repairs is for a specific blocked or damaged drain pipe. Drainage repairs is for broader surface-water and land drainage issues affecting a garden, patio or driveway area."),
            ("Can you install a new drainage solution, not just repair an old one?",
             "Yes, where an existing system has failed beyond repair or there's no drainage in place at all, we can recommend and install a suitable solution such as a French drain or soakaway."),
        ],
        related=["drain-repairs", "slab-relaying", "grounds-maintenance"],
        schema_desc="Repair of waterlogged gardens, failed soakaways and surface-water drainage across Preston.",
    ),
    dict(
        slug="window-repairs", cluster="repairs",
        h1="Window Repairs in Preston",
        tagline="Frames, seals and hardware repaired — not cleaning",
        price="From £65", price_note="guide price only, confirmed after assessment",
        meta_title="Window Repairs Preston | From £65 | GreenFix",
        meta_description="Window repairs in Preston — damaged frames, failed seals, hinges and handles fixed. From £65. This is repair work, not window cleaning.",
        intro="Window repairs fix the window itself — damaged or rotten frames, failed glazing seals letting in draughts, and worn or broken hinges and handles that stop a window opening, closing or locking properly. This is a repair service, distinct from our window cleaning page, which covers cleaning glass, frames and sills rather than fixing them.",
        cards=[
            ("Frame Repairs", "Damaged or rotten window frame sections repaired, avoiding the cost of a full window replacement where possible."),
            ("Failed Seals & Draughts", "Failed glazing seals and draught-letting gaps repaired to restore weatherproofing and comfort."),
            ("Hinges & Handles", "Worn, stiff or broken hinges and handles replaced so windows open, close and lock properly again."),
            ("Not Window Cleaning", "This page is for repairing a damaged window. For cleaning glass, frames and sills, see our window cleaning page."),
        ],
        faqs=[
            ("My window won't close properly — is that a repair job?",
             "Yes, this is a common window repair issue, usually down to worn hinges, a warped frame, or the window having dropped slightly out of alignment."),
            ("Can you fix a draughty window without replacing it?",
             "Often, yes — failed seals and gaps around the frame can usually be repaired, which is considerably cheaper than a full window replacement."),
            ("Do you repair timber and uPVC windows?",
             "Yes, we repair both timber and uPVC window frames, hinges and handles."),
            ("Is this the same as window cleaning?",
             "No — window repairs fixes a damaged window (frame, seal, hinge, handle). Window cleaning cleans the glass, frame and sill of a window that's otherwise working fine."),
        ],
        related=["door-repairs", "window-cleaning", "repairs-and-maintenance"],
        schema_desc="Repair of damaged window frames, seals, hinges and handles across Preston.",
    ),
    dict(
        slug="door-repairs", cluster="repairs",
        h1="Door Repairs in Preston",
        tagline="Sticking, damaged or draughty exterior doors fixed",
        price="From £65", price_note="guide price only, confirmed after assessment",
        meta_title="Door Repairs Preston | From £65 | GreenFix",
        meta_description="Exterior door repairs in Preston — sticking doors, damaged frames, hinges and locks fixed. From £65.",
        intro="A sticking, dragging or draughty exterior door is usually a hinge, frame, or alignment problem rather than something needing a full replacement. We repair external doors for homes and businesses across Preston — fixing hinges, locks, damaged frame sections, and worn weatherproofing seals so the door opens, closes and locks properly again.",
        cards=[
            ("Sticking & Dragging Doors", "Doors that stick, drag on the floor, or won't close properly adjusted and re-hung correctly."),
            ("Damaged Frames", "Rotten or damaged sections of door frame repaired, avoiding the cost of a full frame replacement where possible."),
            ("Hinges & Locks", "Worn hinges and faulty locks replaced so the door is secure and functions properly."),
            ("Draught & Weather Seals", "Worn weatherproofing seals replaced to stop draughts and water getting in around the door."),
        ],
        faqs=[
            ("Why does my door stick or drag on the floor?",
             "Usually worn hinges or a frame that's shifted slightly out of alignment — both are repairable without replacing the door."),
            ("Can you fix a door instead of replacing it?",
             "In most cases, yes. Hinge, lock, frame and seal problems can usually be repaired, which is considerably cheaper than a full door replacement."),
            ("Do you repair both front doors and back/side doors?",
             "Yes, we repair all exterior doors, domestic and commercial."),
            ("How much does a door repair cost?",
             "From £65 as a guide price, depending on what needs fixing — a hinge adjustment is a smaller job than a damaged frame section."),
        ],
        related=["window-repairs", "gate-repairs", "repairs-and-maintenance"],
        schema_desc="Repair of sticking, damaged or draughty exterior doors for homes and businesses across Preston.",
    ),
    dict(
        slug="internal-window-cleaning", cluster="grounds",
        h1="Internal Window Cleaning in Preston",
        tagline="Streak-free window cleaning from the inside",
        price="Free Quote", price_note="price depends on property size and access",
        meta_title="Internal Window Cleaning Preston | GreenFix",
        meta_description="Internal window cleaning in Preston for homes, offices, schools and healthcare facilities. Streak-free glass cleaned from the inside. Free quote.",
        intro="Some windows can only be reached and finished properly from the inside — high-level glazing, windows next to furniture or fittings, or properties where external access isn't practical. We provide dedicated internal window cleaning for homes, offices, schools and healthcare facilities across Preston, working carefully around furniture and fixtures to leave glass streak-free without disturbing the room.",
        cards=[
            ("Homes & Offices", "Internal glass cleaned in houses, offices and commercial premises, working around furniture and fittings."),
            ("Schools & Healthcare Facilities", "Internal window cleaning for schools, nurseries and healthcare settings, fitted around your working hours."),
            ("High-Level & Awkward Glazing", "Internal-only access windows and hard-to-reach glazing cleaned safely from inside."),
            ("Careful, Tidy Work", "Dust sheets and care taken around furniture, flooring and fittings on every visit."),
        ],
        faqs=[
            ("Why would I need internal as well as external window cleaning?",
             "Some windows only show streaks or grime on the inside, or can only be safely accessed from indoors — internal cleaning covers what external cleaning alone can't reach."),
            ("Do you clean internal windows in schools and healthcare settings?",
             "Yes, we clean internal glazing in schools, nurseries and healthcare facilities, scheduled around your operating hours."),
            ("Will you need to move my furniture?",
             "We work carefully around existing furniture and fittings; let us know in advance about anything particularly delicate or hard to move."),
            ("How much does internal window cleaning cost?",
             "Pricing depends on property size and how many windows need doing. Call for a free, no-obligation quote."),
        ],
        related=["external-window-cleaning", "window-cleaning", "window-repairs"],
        schema_desc="Internal window cleaning for homes, offices, schools and healthcare facilities across Preston.",
    ),
    dict(
        slug="external-window-cleaning", cluster="grounds",
        h1="External Window Cleaning in Preston",
        tagline="Purified water window cleaning, from £1.10 per pane",
        price="From £1.10 per pane", price_note="guide price only, confirmed after assessment",
        meta_title="External Window Cleaning Preston | From £1.10/pane | GreenFix",
        meta_description="External window cleaning in Preston using purified water systems for a spotless, streak-free finish. From £1.10 per pane.",
        intro="We clean the outside of windows using purified water fed through a pole system, reaching upper floors safely from ground level without ladders leaning against the property. Purified water dries completely clear with no soap residue, leaving glass, frames and sills spotless.",
        cards=[
            ("Purified Water System", "Pole-fed purified water reaches upper-floor windows safely from the ground, with no residue left behind on drying."),
            ("Frames & Sills Included", "Frames and sills cleaned as standard, not just the glass, for a genuinely finished result."),
            ("Domestic & Commercial", "Houses, shopfronts, offices and commercial premises, on a one-off or regular scheduled basis."),
            ("Regular Rounds Available", "Set up a monthly or fortnightly round and we turn up when we say we will."),
        ],
        faqs=[
            ("What's a purified water system and why use it?",
             "Water is purified to remove minerals, so it dries completely clear with no soap or residue, and reaches upper floors safely via a pole system rather than a ladder."),
            ("How is external window cleaning priced?",
             "From £1.10 per pane as a guide price, depending on the number and size of panes and ease of access — confirmed after a quick assessment."),
            ("Do you offer regular external cleaning rounds?",
             "Yes, monthly or fortnightly rounds are available as well as one-off cleans."),
            ("Is this the same as internal window cleaning?",
             "No — this covers the outside of the glass, frames and sills. For cleaning from indoors, see our internal window cleaning page."),
        ],
        related=["internal-window-cleaning", "window-cleaning", "pressure-washing"],
        schema_desc="External window cleaning using purified water systems for homes and businesses across Preston, from £1.10 per pane.",
    ),
    dict(
        slug="fence-panel-replacement", cluster="repairs",
        h1="Fence Panel Replacement in Preston",
        tagline="Damaged or blown-down panels replaced to match",
        price="From £85", price_note="guide price only, confirmed after assessment",
        meta_title="Fence Panel Replacement Preston | From £85 | GreenFix",
        meta_description="Fence panel replacement in Preston — broken, rotten or storm-damaged panels replaced to match the rest of the fence line. From £85.",
        intro="When a specific panel has broken, rotted through, or blown down in a storm, replacing just that panel is usually all that's needed rather than the whole fence run. We replace individual fence panels for homes and businesses across Preston, matching style and height to the rest of the fence wherever possible.",
        cards=[
            ("Like-for-Like Matching", "New panels matched to style, height and finish of the existing fence line wherever possible."),
            ("Storm-Damaged Panels", "Blown-down or wind-damaged panels replaced promptly, since a gap in a boundary fence can't always wait."),
            ("Posts Checked Too", "Posts and fixings checked as part of the job, since a failing post is often why a panel came down in the first place."),
            ("Domestic & Commercial", "Garden fence panels and commercial site fencing, replaced to the same standard."),
        ],
        faqs=[
            ("Do you replace just one panel, or the whole fence?",
             "Just the damaged panel in most cases — there's no need to replace a whole fence run for one broken or storm-damaged section."),
            ("Can you match the new panel to my existing fence?",
             "We match panel style, height and finish as closely as possible; exact matches depend on whether your existing style is still available."),
            ("My panel blew down in a storm — can this be done quickly?",
             "Yes, storm-damaged panels are one of the most common jobs we get and we prioritise them where we can."),
            ("Is this different from general fence repairs?",
             "Fence panel replacement is specifically swapping a damaged panel; our fence repairs page also covers posts, hinges and other fence problems that don't need a full panel swap."),
        ],
        related=["fence-repairs", "gate-repairs", "garden-wall-repairs"],
        schema_desc="Fence panel replacement for homes and businesses across Preston, matching style and height to the existing fence line.",
    ),
    dict(
        slug="residential-property-maintenance", cluster="repairs",
        h1="Residential Property Maintenance in Preston",
        tagline="One contractor for the inside-out upkeep of your home",
        price="Quotation Required", price_note="tailored to your property and needs",
        meta_title="Residential Property Maintenance Preston | GreenFix",
        meta_description="Residential property maintenance in Preston for homeowners and landlords — grounds care and exterior repairs from one reliable contractor.",
        intro="Keeping a home looking good and working properly usually means juggling several different trades — a gardener for the grounds, someone else for fencing, another for guttering or brickwork. We provide residential property maintenance as a single point of contact for homeowners and landlords across Preston, covering both regular grounds and garden care and one-off exterior repairs, so you're not managing multiple contractors for the outside of your property.",
        cards=[
            ("One Point of Contact", "A single contractor for grounds care and exterior repairs, rather than coordinating several different trades yourself."),
            ("Homeowners & Landlords", "Suited to owner-occupied homes and rental properties, including routine upkeep between tenancies."),
            ("Grounds & Garden Care", "Lawn mowing, hedge trimming, garden tidy-ups and pressure washing, on a one-off or regular basis."),
            ("Exterior Repairs", "Brickwork, fencing, gates, paving, roofing, drainage, windows and doors repaired as and when needed."),
        ],
        faqs=[
            ("What's included in residential property maintenance?",
             "It covers both regular grounds and garden care and one-off exterior repairs for your home — effectively any outside maintenance job, from one contractor."),
            ("Is this only for owner-occupiers, or landlords too?",
             "Both — we work with homeowners and landlords, including routine upkeep between tenancies."),
            ("Do I need a contract, or can I book jobs as they come up?",
             "Either — some customers set up a regular grounds care schedule, others call us as specific repairs come up. There's no obligation to commit to ongoing work."),
            ("How is this priced?",
             "It depends entirely on what's needed — a quote is tailored to your property and the specific jobs involved."),
        ],
        related=["repairs-and-maintenance", "grounds-maintenance", "planned-preventative-maintenance"],
        schema_desc="Residential property maintenance for homeowners and landlords across Preston, covering grounds care and exterior repairs from one contractor.",
    ),
    dict(
        slug="planned-preventative-maintenance", cluster="repairs",
        h1="Planned Preventative Maintenance in Preston",
        tagline="Scheduled inspections to catch problems before they grow",
        price="Quotation Required", price_note="tailored to your property and needs",
        meta_title="Planned Preventative Maintenance Preston | GreenFix",
        meta_description="Planned preventative maintenance programmes in Preston — scheduled property inspections to catch and resolve problems early, for homes and businesses.",
        intro="Most repair jobs are cheaper and simpler the earlier they're caught — a slipped tile spotted early is a small repair; left through a wet winter, it can mean far more extensive damage. Planned preventative maintenance means scheduled inspections of your property's exterior, identifying developing problems (roofing, drainage, brickwork, fencing) before they turn into bigger, more expensive jobs.",
        cards=[
            ("Scheduled Inspections", "Regular visits to check roofing, drainage, brickwork, fencing and other exterior elements for early signs of wear."),
            ("Catch Problems Early", "Small issues identified and fixed before they develop into more extensive, costlier repairs."),
            ("Homes & Businesses", "Suited to homeowners, landlords and commercial or managed sites wanting to avoid reactive, emergency repairs."),
            ("Tailored Schedule", "Inspection frequency set to suit your property, rather than a one-size-fits-all programme."),
        ],
        faqs=[
            ("How is this different from a one-off repair?",
             "A one-off repair fixes a problem you've already noticed; planned preventative maintenance is about spotting problems before they're obvious, through scheduled inspections."),
            ("What does an inspection actually check?",
             "Typically roofing, drainage, brickwork, fencing and other exterior elements most prone to gradual wear — the exact scope is agreed based on your property."),
            ("Is this only for larger commercial sites?",
             "No — it suits any property owner who'd rather catch small issues early than deal with a bigger repair later, homes included."),
            ("How often are inspection visits?",
             "Frequency is set to suit your property and budget; we'll agree a schedule that makes sense for you rather than applying a fixed interval to everyone."),
        ],
        related=["repairs-and-maintenance", "exterior-structural-repairs", "drone-property-inspections"],
        schema_desc="Planned preventative maintenance inspection programmes for homes and businesses across Preston, catching exterior problems early.",
    ),
    dict(
        slug="drone-property-inspections", cluster="repairs",
        h1="Drone Property Inspections in Preston",
        tagline="Aerial imagery and video for roofs and hard-to-reach areas",
        price="Quotation Required", price_note="tailored to your property and needs",
        meta_title="Drone Property Inspections Preston | GreenFix",
        meta_description="Drone property inspections in Preston — high-resolution aerial imagery and video of roofs and hard-to-reach areas, without scaffolding or ladders.",
        intro="Some parts of a property — roofs, chimneys, high gutters, tall boundary trees — are difficult and sometimes risky to inspect up close without scaffolding or ladder access. We provide drone property inspections across Preston, capturing high-resolution aerial imagery and video so problems can be identified and assessed safely from the ground, before deciding what access (if any) is needed to fix them.",
        cards=[
            ("Roof & Ridge Inspections", "Aerial imagery of roof coverings, ridge tiles and chimneys, spotting slipped or damaged tiles without ladder access."),
            ("High-Level & Hard-to-Reach Areas", "Gutters, high brickwork and tall trees inspected safely from the air rather than risky close-up access."),
            ("High-Resolution Imagery & Video", "Clear photo and video footage supplied, useful for insurance, surveys or simply seeing the full picture before work starts."),
            ("Safer Assessment First", "Identify the actual scope of a job by air before committing to scaffolding or access equipment that may not be needed."),
        ],
        faqs=[
            ("What can a drone inspection actually show me?",
             "High-resolution photos and video of roofs, chimneys, gutters and other high or hard-to-reach areas, clear enough to spot slipped tiles, damaged pointing or blocked gutters."),
            ("Is this useful if I just want to check before getting a full quote?",
             "Yes — a drone inspection is a good way to see the actual condition of a roof or high area before deciding what work, if any, is needed."),
            ("Do you need special access or permission to fly a drone at my property?",
             "We operate within standard UK drone flying rules and will discuss anything site-specific (like nearby restricted areas) before the visit."),
            ("Can I get footage or images afterwards?",
             "Yes, footage and images are provided, which can also be useful for insurance or survey purposes."),
        ],
        related=["planned-preventative-maintenance", "roof-tile-repairs", "exterior-structural-repairs"],
        schema_desc="Drone property inspections providing high-resolution aerial imagery and video of roofs and hard-to-reach areas across Preston.",
    ),
]

SERVICE_BY_SLUG = {s["slug"]: s for s in SERVICES}


# ---------------------------------------------------------------------------
# Shared rendering helpers
# ---------------------------------------------------------------------------

def esc(text):
    """Minimal HTML-escape for text we interpolate (data above is trusted,
    but this guards against stray & characters breaking markup)."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def cluster_label(slug):
    for c in CLUSTERS:
        if slug in c["slugs"]:
            return c["label"]
    return None


def render_head(*, title, description, canonical_path, og_image=None, extra_schema="", preload_image=None):
    canonical = f"{DOMAIN}{canonical_path}"
    og_image = og_image or f"{DOMAIN}/hero-commercial-grounds.png"
    preload_html = (
        f'\n    <link rel="preload" as="image" href="{preload_image}" type="image/webp">'
        if preload_image else ""
    )
    return f"""<meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(description)}">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
    <meta name="theme-color" content="#1a5d3a">
    <link rel="canonical" href="{canonical}">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <link rel="stylesheet" href="/assets/site.css">{preload_html}
    <meta property="og:title" content="{esc(title)}">
    <meta property="og:description" content="{esc(description)}">
    <meta property="og:type" content="business.business">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{og_image}">
    <meta property="og:site_name" content="{BUSINESS_NAME}">
    <meta property="og:locale" content="en_GB">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{esc(title)}">
    <meta name="twitter:description" content="{esc(description)}">
    <meta name="twitter:image" content="{og_image}">
{extra_schema}"""


def local_business_schema():
    data = {
        "@context": "https://schema.org",
        "@type": ["HomeAndConstructionBusiness", "GeneralContractor", "LandscapingBusiness"],
        "@id": BUSINESS_ID,
        "name": BUSINESS_NAME,
        "description": (
            "GreenFix Exterior Care is a property maintenance and construction "
            "repair contractor serving homeowners and businesses across Preston, "
            "Preston — covering grounds and "
            "garden care alongside structural, brick, roofing, drainage and "
            "exterior repair services."
        ),
        "url": DOMAIN + "/",
        "telephone": PHONE_TEL,
        "email": EMAIL,
        "logo": f"{DOMAIN}/{LOGO_IMG}",
        "image": f"{DOMAIN}/hero-commercial-grounds.png",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": STREET_ADDRESS,
            "addressLocality": POSTAL_LOCALITY,
            "addressRegion": ADDRESS_REGION,
            "postalCode": POSTAL_CODE,
            "addressCountry": "GB",
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": GEO_LATITUDE,
            "longitude": GEO_LONGITUDE,
        },
        "hasMap": GOOGLE_MAPS_SHARE_URL,
        "openingHoursSpecification": OPENING_HOURS_SPEC,
        "areaServed": AREA_SERVED,
        "foundingDate": FOUNDED,
        "priceRange": "$$",
        "sameAs": [FACEBOOK, LINKEDIN, TIKTOK],
        "knowsAbout": [s["h1"].split(" in ")[0] for s in SERVICES],
    }
    return json.dumps(data, indent=2)


def service_schema(service):
    data = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": service["h1"].split(" in ")[0],
        "description": service["schema_desc"],
        "provider": {"@id": BUSINESS_ID},
        "areaServed": AREA_SERVED,
        "url": f"{DOMAIN}/{service['slug']}",
    }
    if not service["price"].lower().startswith(("quotation", "free quote")):
        # Extract a leading numeric guide price for structured data.
        import re as _re
        m = _re.search(r"\d+", service["price"])
        if m:
            data["offers"] = {
                "@type": "Offer",
                "priceCurrency": "GBP",
                "price": m.group(0),
                "description": f"{service['price']} — {service['price_note']}",
            }
    return json.dumps(data, indent=2)


def breadcrumb_schema(items):
    """items: list of (name, path_or_None) tuples, last item has path=None"""
    elements = []
    for i, (name, path) in enumerate(items, 1):
        el = {"@type": "ListItem", "position": i, "name": name}
        if path is not None:
            el["item"] = f"{DOMAIN}{path}"
        elements.append(el)
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": elements,
    }, indent=2)


def faq_schema(faqs):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }, indent=2)


def render_breadcrumb_html(items):
    """items: list of (name, path_or_None)"""
    lis = []
    for name, path in items:
        if path is None:
            lis.append(f'<li aria-current="page">{esc(name)}</li>')
        else:
            lis.append(f'<li><a href="{path}">{esc(name)}</a></li>')
    return f"""    <nav class="breadcrumb" aria-label="Breadcrumb">
        <ol>{''.join(lis)}</ol>
    </nav>
"""


def render_nav_item(label, slugs, current_slug=None):
    links = []
    for slug in slugs:
        svc = SERVICE_BY_SLUG.get(slug)
        if svc:
            links.append(f'<a href="/{slug}">{esc(svc["h1"].split(" in ")[0])}</a>')
    panel = "\n                ".join(links)
    return f"""<div class="nav-item">
                <span class="nav-label" tabindex="0">{esc(label)}</span>
                <div class="mega-panel">
                {panel}
                </div>
            </div>"""


def render_header():
    grounds = next(c for c in CLUSTERS if c["key"] == "grounds")
    repairs = next(c for c in CLUSTERS if c["key"] == "repairs")
    sector_links = "\n                ".join(
        f'<a href="/{fname}">{esc(label)}</a>' for fname, label in SECTORS
    )
    return f"""    <a href="#main-content" class="skip-link">Skip to main content</a>
    <header>
        <div class="header-content">
            <div class="header-row">
                <a href="/" class="logo">
                    <img src="/{LOGO_IMG}" alt="{BUSINESS_NAME} logo" width="190" height="52" loading="eager">
                </a>
                <div class="header-actions">
                    <a href="tel:{PHONE_TEL}" class="phone-link">\U0001F4DE <span class="phone-link-full">Call GreenFix</span><span class="phone-link-short">Call</span></a>
                    <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="primary-nav" onclick="var n=document.getElementById('primary-nav');var open=n.classList.toggle('is-open');this.setAttribute('aria-expanded',open);">Menu ▾</button>
                </div>
            </div>
            <nav class="primary-nav" id="primary-nav" aria-label="Main navigation">
                {render_nav_item(grounds["label"], grounds["slugs"])}
                {render_nav_item(repairs["label"], repairs["slugs"])}
                <div class="nav-item">
                    <span class="nav-label" tabindex="0">Sectors We Work With</span>
                    <div class="mega-panel">
                {sector_links}
                    </div>
                </div>
                <a href="/blog">Blog</a>
                <a href="/about-greenfix">About</a>
                <a href="/before-after">Gallery</a>
                <a href="/#quote-form">Get a Quote</a>
            </nav>
        </div>
    </header>
"""


def render_footer():
    grounds = next(c for c in CLUSTERS if c["key"] == "grounds")
    repairs = next(c for c in CLUSTERS if c["key"] == "repairs")

    def col_links(slugs):
        return "\n                    ".join(
            f'<li><a href="/{s}">{esc(SERVICE_BY_SLUG[s]["h1"].split(" in ")[0])}</a></li>'
            for s in slugs
        )

    sector_lis = "\n                    ".join(
        f'<li><a href="/{fname}">{esc(label)}</a></li>' for fname, label in SECTORS
    )

    return f"""    <footer>
        <div class="footer-grid">
            <div class="footer-col">
                <h4>Grounds &amp; Garden Care</h4>
                <ul>
                    {col_links(grounds["slugs"])}
                </ul>
            </div>
            <div class="footer-col">
                <h4>Repairs &amp; Maintenance</h4>
                <ul>
                    {col_links(repairs["slugs"])}
                </ul>
            </div>
            <div class="footer-col">
                <h4>Sectors We Work With</h4>
                <ul>
                    {sector_lis}
                </ul>
            </div>
            <div class="footer-col">
                <h4>Company</h4>
                <ul>
                    <li><a href="/about-greenfix">About GreenFix</a></li>
                    <li><a href="/about-greenfix#complaints">Complaints Procedure</a></li>
                    <li><a href="/blog">Blog</a></li>
                    <li><a href="/before-after">Before &amp; After Gallery</a></li>
                    <li><a href="tel:{PHONE_TEL}">\U0001F4DE {PHONE_DISPLAY}</a></li>
                    <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
                    <li><a href="{FACEBOOK}" target="_blank" rel="noopener noreferrer">Facebook</a></li>
                    <li><a href="{LINKEDIN}" target="_blank" rel="noopener noreferrer">LinkedIn</a></li>
                    <li><a href="{TIKTOK}" target="_blank" rel="noopener noreferrer">TikTok</a></li>
                    <li><a href="{PORTAL_URL}">Client Portal</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-map">
            <h4>Find Us</h4>
            <p>{STREET_ADDRESS}, {POSTAL_LOCALITY}, {POSTAL_CODE}</p>
            <p>Open: {HOURS_DISPLAY}</p>
            <div class="map-embed map-embed--compact">
                <iframe src="{GOOGLE_MAPS_EMBED_SRC}" width="600" height="450" style="border:0;" allowfullscreen loading="lazy" referrerpolicy="strict-origin-when-cross-origin" title="{esc(BUSINESS_NAME)} on Google Maps"></iframe>
            </div>
            <p><a href="{GOOGLE_MAPS_SHARE_URL}" target="_blank" rel="noopener">Get Directions on Google Maps &rarr;</a></p>
        </div>
        <div class="footer-bottom">
            <p><strong>{BUSINESS_NAME}</strong> &mdash; Property maintenance and construction repairs across Preston.</p>
            <p>{INSURANCE} &middot; {TRAINED} &middot; {WASTE_CARRIER} &middot; Prices shown are guide prices only.</p>
        </div>
    </footer>
"""


def render_trust_strip():
    return f"""    <section class="section-white" style="padding-top:0;">
        <div class="container">
            <div class="trust-strip">
                <span>✓ <strong>{INSURANCE}</strong></span>
                <span>✓ <strong>{TRAINED}</strong></span>
                <span>✓ <strong>{WASTE_CARRIER}</strong></span>
                <span>✓ <strong>New for {FOUNDED}</strong></span>
            </div>
        </div>
    </section>
"""


def render_blog_callout(service_slug):
    """Two-way link: if a blog post covers this service, surface it here.
    BLOG_BY_SERVICE is defined later in the file but resolved at call time,
    once build_service_pages() actually runs from main()."""
    post_slug = BLOG_BY_SERVICE.get(service_slug)
    if not post_slug:
        return ""
    post = BLOG_BY_SLUG[post_slug]
    return f"""    <section class="section-white">
        <div class="container" style="max-width:760px;text-align:center;">
            <h2 class="center">From the Blog</h2>
            <div class="card" style="text-align:left;">
                <h3><a href="/blog/{post_slug}" style="text-decoration:none;color:var(--dark-green);">{esc(post["title"])}</a></h3>
                <p>{esc(post["answer"])}</p>
                <p style="margin-top:0.75rem;"><a href="/blog/{post_slug}" style="color:var(--dark-green);font-weight:700;">Read the full answer &rarr;</a></p>
            </div>
        </div>
    </section>
"""


def render_page(*, head_html, body_html, extra_script=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html}
</head>
<body>
{render_header()}
{body_html}
{render_footer()}
{extra_script}    <script src="/assets/chatbot.js" defer></script>
</body>
</html>
"""


def write_page(filename, html):
    path = os.path.join(ROOT, filename)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    print(f"wrote {filename} ({len(html)} bytes)")


# ---------------------------------------------------------------------------
# Service page rendering
# ---------------------------------------------------------------------------

def render_service_page(service):
    cluster = cluster_label(service["slug"])
    canonical_path = f"/{service['slug']}"
    schema = "\n".join([
        f'    <script type="application/ld+json">\n{local_business_schema()}\n    </script>',
        f'    <script type="application/ld+json">\n{breadcrumb_schema([("Home", "/"), (cluster, None), (service["h1"].split(" in ")[0], None)])}\n    </script>',
        f'    <script type="application/ld+json">\n{service_schema(service)}\n    </script>',
        f'    <script type="application/ld+json">\n{faq_schema(service["faqs"])}\n    </script>',
    ])
    head = render_head(
        title=service["meta_title"],
        description=service["meta_description"],
        canonical_path=canonical_path,
        extra_schema=schema,
    )

    breadcrumb = render_breadcrumb_html([
        ("Home", "/"), (cluster, None), (service["h1"].split(" in ")[0], None)
    ])

    cards_html = "\n                ".join(
        f'<div class="card"><h3>{esc(t)}</h3><p>{esc(txt)}</p></div>'
        for t, txt in service["cards"]
    )

    faqs_html = "\n                ".join(
        f'<div class="faq-item"><h3>{esc(q)}</h3><p>{esc(a)}</p></div>'
        for q, a in service["faqs"]
    )

    related_html = "\n                ".join(
        f'<a href="/{slug}">{esc(SERVICE_BY_SLUG[slug]["h1"].split(" in ")[0])}</a>'
        for slug in service["related"] if slug in SERVICE_BY_SLUG
    )

    price_note_html = f'<span class="price-note">{esc(service["price_note"])}</span>' if service.get("price_note") else ""

    body = f"""{breadcrumb}
    <section id="main-content" class="hero">
        <div class="hero-content">
            <h1>{esc(service["h1"])}</h1>
            <p class="tagline">{esc(service["tagline"])}</p>
            <div class="price-badge">{esc(service["price"])}{price_note_html}</div>
            <div class="button-group">
                <a href="tel:{PHONE_TEL}" class="btn btn-primary">\U0001F4DE Call {PHONE_DISPLAY}</a>
                <a href="/#quote-form" class="btn btn-secondary">Request a Free Quote</a>
            </div>
        </div>
    </section>

    <section class="section-white">
        <div class="container">
            <p class="lede">{esc(service["intro"])}</p>
        </div>
    </section>
{render_trust_strip()}
    <section class="section-grey">
        <div class="container">
            <h2 class="center">Why Choose GreenFix</h2>
            <div class="grid grid-2">
                {cards_html}
            </div>
        </div>
    </section>

    <section class="section-white">
        <div class="container">
            <h2 class="center">Frequently Asked Questions</h2>
            <div class="grid grid-2">
                {faqs_html}
            </div>
        </div>
    </section>

    <section class="section-grey">
        <div class="container">
            <h2 class="center">Related Services</h2>
            <div class="related-links" style="justify-content:center;">
                {related_html}
            </div>
        </div>
    </section>
{render_blog_callout(service["slug"])}
    <section class="final-cta">
        <div class="container">
            <h2>Get a Free Quote for {esc(service["h1"].split(" in ")[0])}</h2>
            <p>Call {PHONE_DISPLAY} or fill in our quote form &mdash; we respond within 24 hours.</p>
            <div class="button-group">
                <a href="tel:{PHONE_TEL}" class="btn btn-primary">\U0001F4DE Call {PHONE_DISPLAY}</a>
                <a href="/#quote-form" class="btn btn-secondary">Request a Free Quote</a>
            </div>
        </div>
    </section>
"""

    return render_page(head_html=head, body_html=body)


def build_service_pages():
    for service in SERVICES:
        html = render_service_page(service)
        write_page(f"{service['slug']}.html", html)


import datetime as _datetime
TODAY_ISO = _datetime.date.today().isoformat()

QUOTE_FORM_HTML = f"""    <section class="section-white" id="quote-form">
        <div class="form-container">
            <h2 class="center">Request a Free Quote or Book a Site Visit</h2>
            <p class="lede center" style="margin-bottom:1.5rem;">Grounds and garden care, or a structural repair? Tell us what needs doing, and a preferred date if you'd like us to come and see you — we'll confirm by phone within 24 hours.</p>
            <form class="quote-form" name="quote-request" method="POST" action="/thank-you.html" data-netlify="true" netlify-honeypot="bot-field" id="quoteForm">
                <input type="hidden" name="form-name" value="quote-request" />
                <input type="text" name="bot-field" class="bot-field" />
                <div class="form-group">
                    <label for="fullname">Full Name <span class="required">*</span></label>
                    <input type="text" id="fullname" name="full_name" required>
                </div>
                <div class="form-group">
                    <label for="phone">Phone Number <span class="required">*</span></label>
                    <input type="tel" id="phone" name="phone_number" required placeholder="07xxx xxxxxx">
                </div>
                <div class="form-group">
                    <label for="address">Property Address or Area <span class="required">*</span></label>
                    <input type="text" id="address" name="property_address" required placeholder="E.g., Preston / 123 High Street">
                </div>
                <div class="form-group">
                    <label for="message">What work needs doing? <span class="required">*</span></label>
                    <textarea id="message" name="message" required placeholder="E.g., lawn mowing round, hedge trimming, brick repointing, fence repair, blocked drain, roof tile repair..."></textarea>
                </div>
                <div class="form-group">
                    <label for="visit-date">Preferred Visit Date <span style="font-weight:400;color:var(--grey);">(optional)</span></label>
                    <input type="date" id="visit-date" name="preferred_visit_date" min="{TODAY_ISO}">
                </div>
                <div class="form-group">
                    <label for="visit-time">Preferred Time of Day</label>
                    <select id="visit-time" name="preferred_time_of_day">
                        <option value="">No preference</option>
                        <option value="morning">Morning</option>
                        <option value="afternoon">Afternoon</option>
                        <option value="either">Either — whatever's soonest</option>
                    </select>
                </div>
                <div class="form-note">
                    <strong>Booking a visit?</strong> A preferred date isn't a guaranteed slot — we'll call or text you to confirm it works before it's locked in.
                </div>
                <div class="form-group">
                    <label>Property Type</label>
                    <div class="checkbox-group">
                        <label><input type="checkbox" name="property_type[]" value="residential"> Home / Residential</label>
                        <label><input type="checkbox" name="property_type[]" value="care-home"> Care Home / Supported Living</label>
                        <label><input type="checkbox" name="property_type[]" value="factory-warehouse"> Factory / Warehouse</label>
                        <label><input type="checkbox" name="property_type[]" value="estate-heritage"> Estate / Heritage Grounds</label>
                        <label><input type="checkbox" name="property_type[]" value="church"> Church / Community Building</label>
                        <label><input type="checkbox" name="property_type[]" value="school-nursery"> School / Nursery</label>
                        <label><input type="checkbox" name="property_type[]" value="pub-restaurant"> Pub / Restaurant</label>
                        <label><input type="checkbox" name="property_type[]" value="shop-retail"> Shop / Retail Unit</label>
                        <label><input type="checkbox" name="property_type[]" value="event-venue"> Event Site / Venue</label>
                        <label><input type="checkbox" name="property_type[]" value="commercial-unit"> Commercial Unit / Business</label>
                        <label><input type="checkbox" name="property_type[]" value="other"> Other</label>
                    </div>
                </div>
                <div class="consent-checkbox">
                    <input type="checkbox" id="consent" name="consent" value="yes" required>
                    <p><label for="consent">I agree for {BUSINESS_NAME} to contact me about this quote request.</label></p>
                </div>
                <div class="form-note">
                    <strong>Have photos?</strong> WhatsApp them to <strong>{PHONE_DISPLAY}</strong> for a faster quote. We'll respond the same day.
                </div>
                <button type="submit" class="btn-submit btn">Get My Free Quote</button>
            </form>
        </div>
    </section>
"""


HOMEPAGE_FAQS = [
    ("Do you only do garden work, or repairs as well?",
     "Both. GreenFix covers grounds and garden care (mowing, hedges, tidy-ups, pressure washing) and exterior property repairs (brickwork, fencing, gates, paving, roofing, drainage, windows and doors) for homes and businesses."),
    ("What areas do you cover?",
     f"Preston."),
    ("Are you insured?",
     f"Yes, {BUSINESS_NAME} holds {INSURANCE} and is a {WASTE_CARRIER}."),
    ("How does pricing work?",
     "Most services have a guide 'from' price shown on their page. The final price depends on the size and specifics of the job, confirmed after a free assessment or quote."),
    ("Do you work with businesses as well as homeowners?",
     "Yes, alongside residential work we support care homes, churches, schools, pubs, restaurants, shops, factories, warehouses, estates and event venues."),
    ("How do I get a quote?",
     f"Call or WhatsApp {PHONE_DISPLAY}, or use the quote form on this site. We respond within 24 hours."),
]


def render_homepage():
    grounds = next(c for c in CLUSTERS if c["key"] == "grounds")
    repairs = next(c for c in CLUSTERS if c["key"] == "repairs")

    def service_card(slug):
        s = SERVICE_BY_SLUG[slug]
        name = s["h1"].split(" in ")[0]
        return (f'<a class="card" style="text-decoration:none;display:block;" href="/{slug}">'
                f'<h3>{esc(name)}</h3><p>{esc(s["tagline"])}</p>'
                f'<p style="color:var(--dark-green);font-weight:700;margin-top:0.5rem;">{esc(s["price"])}</p></a>')

    grounds_cards = "\n                ".join(service_card(s) for s in grounds["slugs"])
    repairs_cards = "\n                ".join(service_card(s) for s in repairs["slugs"])

    sector_cards = "\n                ".join(
        f'<a class="card" style="text-decoration:none;display:block;" href="/{fname}"><h3>{esc(label)}</h3></a>'
        for fname, label in SECTORS
    )

    faqs_html = "\n                ".join(
        f'<div class="faq-item"><h3>{esc(q)}</h3><p>{esc(a)}</p></div>' for q, a in HOMEPAGE_FAQS
    )

    schema = "\n".join([
        f'    <script type="application/ld+json">\n{local_business_schema()}\n    </script>',
        f'    <script type="application/ld+json">\n{faq_schema(HOMEPAGE_FAQS)}\n    </script>',
    ])

    head = render_head(
        title="Property Maintenance & Construction Repairs Preston | GreenFix",
        description="GreenFix Exterior Care: grounds & garden maintenance and exterior repairs for homes and businesses across Preston.",
        canonical_path="/",
        extra_schema=schema,
        preload_image="/hero-commercial-1200w.webp",
    )

    body = f"""    <section id="main-content" class="hero">
        <div class="hero-content">
            <picture>
                <source type="image/webp" srcset="/hero-commercial-480w.webp 480w, /hero-commercial-800w.webp 800w, /hero-commercial-1200w.webp 1200w" sizes="(max-width: 480px) 100vw, (max-width: 800px) 80vw, 1200px">
                <img class="hero-image" src="/hero-commercial-1200w.webp" alt="GreenFix Exterior Care team carrying out grounds maintenance in Preston" width="1200" height="630" loading="eager" fetchpriority="high">
            </picture>
            <h1>Property Maintenance &amp; Construction Repairs Across Preston</h1>
            <p class="tagline">Grounds &amp; Garden Care and Exterior Repairs, for Homes and Businesses</p>
            <p class="hero-desc">GreenFix Exterior Care keeps properties looking after themselves and in good repair &mdash; from lawn mowing and hedge trimming to brickwork, fencing, roofing, drainage and general exterior repairs. One reliable contractor for the outside of your property.</p>
            <div class="button-group">
                <a href="#quote-form" class="btn btn-primary">Request a Free Quote</a>
                <a href="{PORTAL_URL}" class="btn btn-secondary">Client Portal Login</a>
            </div>
        </div>
    </section>

    <section class="section-white">
        <div class="container">
            <h2 class="center">Grounds &amp; Garden Care</h2>
            <p class="lede center" style="margin-bottom:1.5rem;">Regular garden care and ground maintenance for homes and larger sites.</p>
            <div class="grid grid-3">
                {grounds_cards}
            </div>
        </div>
    </section>

    <section class="section-grey">
        <div class="container">
            <h2 class="center">Repairs &amp; Maintenance</h2>
            <p class="lede center" style="margin-bottom:1.5rem;">Structural, brick, roofing, drainage and general exterior repairs.</p>
            <div class="grid grid-3">
                {repairs_cards}
            </div>
        </div>
    </section>

    <section class="section-white">
        <div class="container">
            <h2 class="center">Sectors We Work With</h2>
            <p class="lede center" style="margin-bottom:1.5rem;">Alongside homeowners, we support these sectors across Preston.</p>
            <div class="grid grid-3">
                {sector_cards}
            </div>
        </div>
    </section>

    <section class="section-grey">
        <div class="container">
            <h2 class="center">Why Choose GreenFix</h2>
            <div class="trust-strip">
                <span>✓ <strong>{INSURANCE}</strong></span>
                <span>✓ <strong>{TRAINED}</strong></span>
                <span>✓ <strong>{WASTE_CARRIER}</strong></span>
                <span>✓ <strong>New for {FOUNDED}</strong></span>
            </div>
        </div>
    </section>

{QUOTE_FORM_HTML}
    <section class="section-grey">
        <div class="container">
            <h2 class="center">Frequently Asked Questions</h2>
            <div class="grid grid-2">
                {faqs_html}
            </div>
        </div>
    </section>

    <section class="final-cta">
        <div class="container">
            <h2>Get a Free Quote Today</h2>
            <p>Grounds work or a repair job &mdash; call {PHONE_DISPLAY} or WhatsApp photos for a fast estimate.</p>
            <div class="button-group">
                <a href="tel:{PHONE_TEL}" class="btn btn-primary">\U0001F4DE Call {PHONE_DISPLAY}</a>
            </div>
        </div>
    </section>
"""
    return render_page(head_html=head, body_html=body)


def build_homepage():
    write_page("index.html", render_homepage())


# ---------------------------------------------------------------------------
# About page
# ---------------------------------------------------------------------------

def render_about():
    schema = "\n".join([
        f'    <script type="application/ld+json">\n{local_business_schema()}\n    </script>',
        f'    <script type="application/ld+json">\n{breadcrumb_schema([("Home", "/"), ("About GreenFix", None)])}\n    </script>',
    ])
    head = render_head(
        title="About GreenFix | Property Maintenance & Construction Preston",
        description=f"About {BUSINESS_NAME} — property maintenance and construction repairs for homes and businesses across Preston since {FOUNDED}.",
        canonical_path="/about-greenfix",
        extra_schema=schema,
    )
    breadcrumb = render_breadcrumb_html([("Home", "/"), ("About GreenFix", None)])
    body = f"""{breadcrumb}
    <section id="main-content" class="hero">
        <div class="hero-content">
            <h1>About GreenFix Exterior Care</h1>
            <p class="tagline">Property Maintenance &amp; Construction Repairs Since {FOUNDED}</p>
        </div>
    </section>

    <section class="section-white">
        <div class="container">
            <h2>Who We Are</h2>
            <p class="lede">{BUSINESS_NAME} launched in {FOUNDED}, covering two sides of keeping a property looking good and working properly: regular grounds and garden care, and exterior construction repairs &mdash; brickwork, fencing, gates, paving, roofing, drainage, windows and doors. We're built on turning up when we say we will and doing the job properly, every time.</p>
            <p class="lede" style="margin-top:1rem;"><strong>Address:</strong> {STREET_ADDRESS}, {POSTAL_LOCALITY}, {POSTAL_CODE}</p>
            <p class="lede" style="margin-top:0.35rem;"><strong>Hours:</strong> {HOURS_DISPLAY}</p>
        </div>
    </section>

    <section class="section-grey">
        <div class="container">
            <h2 class="center">What We Cover</h2>
            <div class="grid grid-2">
                <div class="card">
                    <h3>Grounds &amp; Garden Care</h3>
                    <p>Lawn mowing, hedge trimming, garden tidy-ups, grounds maintenance for larger sites, pressure washing and window cleaning.</p>
                </div>
                <div class="card">
                    <h3>Repairs &amp; Maintenance</h3>
                    <p>Structural and brick repairs, garden wall and fence repairs, paving and patio repairs, roof tile repairs, drainage repairs, and window and door repairs.</p>
                </div>
            </div>
        </div>
    </section>

    <section class="section-white">
        <div class="container">
            <h2 class="center">Fully Insured &amp; Compliant</h2>
            <div class="trust-strip">
                <span>✓ <strong>{INSURANCE}</strong></span>
                <span>✓ <strong>{TRAINED}</strong></span>
                <span>✓ <strong>{WASTE_CARRIER}</strong></span>
                <span>✓ <strong>New for {FOUNDED}</strong></span>
            </div>
        </div>
    </section>

    <section class="section-grey" id="complaints">
        <div class="container">
            <h2 class="center">Complaints Procedure</h2>
            <p class="lede center" style="margin-bottom:1.5rem;">We aim to get every job right first time. If something isn't right, here's what happens:</p>
            <div class="grid grid-2">
                {"".join(f'<div class="card"><h3>{i+1}. {esc(t)}</h3><p>{esc(d)}</p></div>' for i, (t, d) in enumerate(COMPLAINTS_STEPS))}
            </div>
        </div>
    </section>

    <section class="final-cta">
        <div class="container">
            <h2>Get a Free Quote</h2>
            <p>Call {PHONE_DISPLAY} or use our quote form &mdash; we respond within 24 hours.</p>
            <div class="button-group">
                <a href="tel:{PHONE_TEL}" class="btn btn-primary">\U0001F4DE Call {PHONE_DISPLAY}</a>
                <a href="/#quote-form" class="btn btn-secondary">Request a Free Quote</a>
            </div>
        </div>
    </section>
"""
    return render_page(head_html=head, body_html=body)


def build_about():
    write_page("about-greenfix.html", render_about())


# ---------------------------------------------------------------------------
# Gallery / recent work page
# ---------------------------------------------------------------------------

GALLERY_CATEGORIES = [
    ("Garden Clearance & Tidy-Ups", "Overgrown gardens cleared and reset, ready for regular maintenance."),
    ("Lawn Mowing & Restoration", "Neglected lawns brought back to a healthy, well-kept finish."),
    ("Hedge & Shrub Trimming", "Overgrown hedges shaped and height-reduced."),
    ("Patio & Driveway Pressure Washing", "Moss, algae and grime removed from patios and driveways."),
    ("Fence & Gate Repairs", "Damaged panels, posts, hinges and latches repaired."),
    ("Brick & Wall Repairs", "Repointing, brick repairs and garden wall rebuilding."),
]


def render_gallery():
    schema = "\n".join([
        f'    <script type="application/ld+json">\n{local_business_schema()}\n    </script>',
        f'    <script type="application/ld+json">\n{breadcrumb_schema([("Home", "/"), ("Recent Work", None)])}\n    </script>',
    ])
    head = render_head(
        title="Recent Work | GreenFix Exterior Care Preston",
        description="The range of grounds care and exterior repair work GreenFix carries out for homes and businesses across Preston.",
        canonical_path="/before-after",
        extra_schema=schema,
    )
    breadcrumb = render_breadcrumb_html([("Home", "/"), ("Recent Work", None)])
    cards = "\n                ".join(
        f'<div class="card"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in GALLERY_CATEGORIES
    )
    body = f"""{breadcrumb}
    <section id="main-content" class="hero">
        <div class="hero-content">
            <h1>Recent Work</h1>
            <p class="tagline">The kind of jobs we handle across Preston</p>
        </div>
    </section>

    <section class="section-white">
        <div class="container">
            <p class="lede center">We're building up a photo library of completed jobs across both grounds care and repair work. In the meantime, here's the range of work we regularly carry out &mdash; call us and we're happy to share examples relevant to your job.</p>
        </div>
    </section>

    <section class="section-grey">
        <div class="container">
            <div class="grid grid-3">
                {cards}
            </div>
        </div>
    </section>

    <section class="final-cta">
        <div class="container">
            <h2>Get a Free Quote</h2>
            <p>Call {PHONE_DISPLAY} or use our quote form &mdash; we respond within 24 hours.</p>
            <div class="button-group">
                <a href="tel:{PHONE_TEL}" class="btn btn-primary">\U0001F4DE Call {PHONE_DISPLAY}</a>
                <a href="/#quote-form" class="btn btn-secondary">Request a Free Quote</a>
            </div>
        </div>
    </section>
"""
    return render_page(head_html=head, body_html=body)


def build_gallery():
    write_page("before-after.html", render_gallery())


# ---------------------------------------------------------------------------
# Sector pages (owner-approved extras, kept alongside the final 21+1)
# ---------------------------------------------------------------------------

SECTOR_PAGES = [
    dict(
        filename="commercial-maintenance.html",
        h1="Commercial Property Maintenance in Preston",
        tagline="Grounds care and exterior repairs for commercial premises",
        meta_title="Commercial Property Maintenance Preston | GreenFix",
        meta_description="Commercial property maintenance in Preston: grounds care, car park upkeep, and exterior repairs for offices, retail units and business premises.",
        intro="GreenFix provides property maintenance for commercial premises across Preston, covering both grounds care (car park borders, communal grounds, general tidiness) and exterior repairs (fencing, paving, brickwork, drainage) that keep a business premises presentable and in good repair.",
        cards=[
            ("Grounds & Exterior Upkeep", "Scheduled grounds maintenance and exterior tidiness for offices, retail units and business premises."),
            ("Car Parks & Access Routes", "Weed control, paving repairs and general upkeep for car parks and customer-facing access routes."),
            ("Structural & Repair Work", "Fencing, gates, brickwork and paving repaired as needed, alongside routine maintenance."),
            ("One Point of Contact", "A single contractor for scheduled maintenance and one-off repairs, rather than juggling separate trades."),
        ],
        faqs=[
            ("Do you offer regular maintenance contracts for commercial premises?",
             "Yes, we can set up a scheduled grounds and exterior maintenance contract, plus handle one-off repairs as they come up."),
            ("Can you repair damaged fencing, paving or brickwork on a commercial site?",
             "Yes, alongside grounds maintenance we carry out fence repairs, paving repairs and brick repairs for commercial premises."),
            ("Do you invoice for commercial accounts?",
             "Yes, we provide professional invoices and can discuss account arrangements for regular commercial clients."),
        ],
        related=["grounds-maintenance", "repairs-and-maintenance", "fence-repairs", "paving-repairs"],
    ),
    dict(
        filename="factory-warehouse-grounds-maintenance.html",
        h1="Factory & Warehouse Grounds Maintenance in Preston",
        tagline="Yards, car parks and boundary repairs for industrial sites",
        meta_title="Factory & Warehouse Grounds Maintenance Preston | GreenFix",
        meta_description="Grounds maintenance and exterior repairs for factories and warehouses in Preston — yards, car parks, fencing and drainage.",
        intro="Factories and warehouses need practical, low-maintenance grounds and reliable boundary security. GreenFix handles scheduled grounds maintenance for yards and car parks, along with the fence, gate and drainage repairs that keep an industrial site secure and properly draining.",
        cards=[
            ("Yards & Car Parks", "Weed control, grounds tidiness and paving upkeep for yards, loading areas and staff car parks."),
            ("Boundary Fencing & Gates", "Site security fencing and access gates repaired promptly to keep the site secure."),
            ("Drainage & Surface Water", "Blocked drains and poor surface-water drainage across yards and access routes repaired."),
            ("Scheduled or Reactive", "Set up a regular grounds contract, and call us as needed for reactive repair work."),
        ],
        faqs=[
            ("Can you maintain grounds across a large industrial site?",
             "Yes, we work with factories, warehouses and industrial estates on scheduled grounds maintenance contracts."),
            ("Do you repair site security fencing and gates?",
             "Yes, fence and gate repairs are a common job for industrial sites, alongside routine grounds work."),
            ("Can you fix drainage problems in yards and car parks?",
             "Yes, we diagnose and repair blocked drains and poor surface-water drainage on industrial sites."),
        ],
        related=["grounds-maintenance", "fence-repairs", "gate-repairs", "drainage-repairs"],
    ),
    dict(
        filename="care-home-grounds-maintenance-preston.html",
        h1="Care Home Grounds Maintenance in Preston",
        tagline="Safe, well-kept outdoor spaces for residents, staff and visitors",
        meta_title="Care Home Grounds Maintenance Preston | GreenFix",
        meta_description="Care home grounds maintenance in Preston — safe garden care, path repairs and grounds upkeep for residents, staff and visitors.",
        intro="Care homes need outdoor spaces that are safe, presentable and properly maintained for residents, staff and visitors. GreenFix provides grounds maintenance and exterior repairs sympathetic to that setting — from regular garden care to path and paving repairs that keep walkways safe underfoot.",
        cards=[
            ("Resident-Friendly Garden Care", "Grass cutting, hedge trimming and garden tidy-ups carried out carefully around residents and visitors."),
            ("Safe Paths & Walkways", "Paving and slab repairs to remove trip hazards from paths and outdoor walkways."),
            ("Inspection Preparation", "Grounds and exterior tidied ahead of care inspections, open days and family visits."),
            ("Fully Insured Contractor", f"{INSURANCE}, professional invoices and clear communication for care home managers."),
        ],
        faqs=[
            ("Do you work around residents and daily routines?",
             "Yes, we work respectfully around residents, staff, visitors and the daily routine of a care home."),
            ("Can you fix uneven or cracked paths that are a trip hazard?",
             "Yes, paving and slab repairs are a common job for care home grounds, specifically to remove trip hazards."),
            ("Can you prepare grounds before an inspection or visit?",
             "Yes, we can carry out a tidy-up and any needed repairs ahead of inspections, open days or family visits."),
        ],
        related=["garden-maintenance", "paving-repairs", "slab-relaying", "grounds-maintenance"],
    ),
    dict(
        filename="church-grounds-maintenance-preston.html",
        h1="Church Grounds Maintenance in Preston",
        tagline="Churchyard care and respectful exterior upkeep",
        meta_title="Church Grounds Maintenance Preston | GreenFix",
        meta_description="Church grounds maintenance in Preston — churchyard care, path repairs and respectful exterior upkeep around services and events.",
        intro="GreenFix maintains churchyards and church grounds across Preston, working reliably and respectfully around services and events. That covers regular grounds care as well as the masonry and path repairs that older church buildings and boundary walls often need.",
        cards=[
            ("Churchyard Grounds Care", "Grass cutting, hedge trimming and grounds tidiness for churchyards and parish grounds."),
            ("Path & Entrance Repairs", "Paving and path repairs for safe, presentable entrances and walkways."),
            ("Boundary Wall & Masonry Repairs", "Garden wall repairs and brick repointing for boundary walls and older masonry."),
            ("Around Your Schedule", "Work planned around services, events and the church calendar."),
        ],
        faqs=[
            ("Can you work around church services and events?",
             "Yes, we plan grounds and repair work around your service times and any events."),
            ("Do you repair boundary walls and older masonry?",
             "Yes, garden wall repairs and brick repointing are common jobs for churchyards and older church buildings."),
            ("Can you prepare grounds before a service or event?",
             "Yes, we can tidy and prepare churchyard grounds ahead of services, weddings and other events."),
        ],
        related=["garden-maintenance", "garden-wall-repairs", "brick-repointing", "paving-repairs"],
    ),
    dict(
        filename="estate-grounds-maintenance-lancashire.html",
        h1="Estate & Heritage Grounds Maintenance in Lancashire",
        tagline="Grounds care and masonry repairs for large or heritage sites",
        meta_title="Estate Grounds Maintenance Lancashire | GreenFix",
        meta_description="Estate and heritage grounds maintenance in Lancashire — grounds care, boundary wall repairs and masonry work for stately homes and large estates.",
        intro="Large estates and heritage sites need grounds care that scales to the size of the property, and masonry repair work carried out carefully on older structures. GreenFix covers both: scheduled grounds maintenance across large plots, and structural repairs — garden walls, brickwork, paving — sympathetic to heritage buildings.",
        cards=[
            ("Large-Scale Grounds Care", "Grounds maintenance scheduled to suit large estates, heritage sites and visitor grounds."),
            ("Heritage-Sensitive Masonry Repairs", "Brick repointing, brick repairs and garden wall repairs carried out carefully on older structures."),
            ("Paths & Visitor Areas", "Paving and slab repairs for visitor-facing paths and grounds."),
            ("Event Preparation", "Grounds and access routes prepared ahead of visitor days and events."),
        ],
        faqs=[
            ("Can you maintain grounds across a large estate?",
             "Yes, we schedule grounds maintenance to suit the size of large estates and heritage grounds."),
            ("Do you have experience with older or heritage masonry?",
             "Yes, brick repointing, brick repairs and garden wall repairs are carried out carefully on older brick and stone structures."),
            ("Can you prepare grounds before a visitor day or event?",
             "Yes, we can prepare grounds, paths and access routes ahead of events and public visitor days."),
        ],
        related=["grounds-maintenance", "brick-repointing", "garden-wall-repairs", "paving-repairs"],
    ),
    dict(
        filename="event-venue-grounds-maintenance-preston.html",
        h1="Event & Venue Grounds Maintenance in Preston",
        tagline="Visitor-ready grounds before events, tidied after",
        meta_title="Event & Venue Grounds Maintenance Preston | GreenFix",
        meta_description="Event and venue grounds maintenance in Preston — grounds prepared before events, patios and paths pressure washed and repaired.",
        intro="Venues and event sites need grounds that look their best before guests arrive, and a quick turnaround to tidy up afterwards. GreenFix prepares grounds, patios and access routes before events, and can also handle the pressure washing and paving repairs that keep outdoor spaces customer-ready between events.",
        cards=[
            ("Pre-Event Preparation", "Grounds, paths and outdoor areas tidied and prepared before weddings, functions and events."),
            ("Patios & Outdoor Seating", "Pressure washing to keep patios and outdoor seating areas clean and welcoming."),
            ("Paths & Car Parks", "Paving repairs and grounds maintenance for visitor-facing paths and car parks."),
            ("Fast Turnaround", "Quick post-event tidy-ups so the venue is ready for the next booking."),
        ],
        faqs=[
            ("Can you prepare grounds before a specific event date?",
             "Yes, we can schedule a grounds and exterior tidy-up ahead of a confirmed event date."),
            ("Do you pressure wash patios and outdoor seating areas?",
             "Yes, pressure washing is a common job for venues to keep outdoor seating and patio areas presentable."),
            ("Can you turn a site around quickly after an event?",
             "Yes, we can schedule a fast post-event tidy-up where turnaround time matters."),
        ],
        related=["pressure-washing", "grounds-maintenance", "paving-repairs"],
    ),
    dict(
        filename="school-nursery-grounds-maintenance-preston.html",
        h1="School & Nursery Grounds Maintenance in Preston",
        tagline="Safe grounds and repairs, scheduled around term time",
        meta_title="School & Nursery Grounds Maintenance Preston | GreenFix",
        meta_description="School and nursery grounds maintenance in Preston. Playing field care, fence repairs and grounds upkeep scheduled around term time.",
        intro="Schools and nurseries need safe, well-kept grounds, and work scheduled to avoid disrupting the school day. GreenFix provides grounds maintenance for playing fields and gardens, and can carry out fence, gate and paving repairs during holidays or after hours where needed.",
        cards=[
            ("Playing Fields & Grounds", "Grass cutting, hedge trimming and grounds tidiness for playing fields and outdoor learning areas."),
            ("Fencing & Boundary Repairs", "Fence and gate repairs to keep grounds secure and safe."),
            ("Holiday & Out-of-Hours Scheduling", "Repair and grounds work planned around holidays or after hours to avoid disrupting the school day."),
            ("Fully Insured Contractor", f"{INSURANCE}, professional invoices and clear communication for site and facilities managers."),
        ],
        faqs=[
            ("Can you work outside school hours?",
             "Yes, we can schedule work during holidays, weekends or after hours to avoid disrupting the school day."),
            ("Do you repair school boundary fencing?",
             "Yes, fence and gate repairs are common jobs for schools, alongside routine grounds maintenance."),
            ("Can you prepare grounds before an open day or inspection?",
             "Yes, we can tidy and prepare outdoor areas ahead of open days, inspections and events."),
        ],
        related=["grounds-maintenance", "fence-repairs", "gate-repairs"],
    ),
    dict(
        filename="pub-restaurant-grounds-maintenance-preston.html",
        h1="Pub & Restaurant Grounds Maintenance in Preston",
        tagline="Beer gardens, patios and car parks kept customer-ready",
        meta_title="Pub & Restaurant Grounds Maintenance Preston | GreenFix",
        meta_description="Grounds maintenance and pressure washing for pubs and restaurants in Preston — beer gardens, patios and car parks kept customer-ready.",
        intro="Pubs and restaurants need outdoor areas that stay customer-ready, worked around opening hours. GreenFix maintains beer gardens, patios and car parks, and pressure washes outdoor seating areas to keep them clean and welcoming for customers.",
        cards=[
            ("Beer Gardens & Outdoor Seating", "Grounds maintenance and pressure washing to keep outdoor seating areas customer-ready."),
            ("Car Parks & Entrances", "Weed control, paving repairs and grounds tidiness for car parks and entrances."),
            ("Fence & Boundary Repairs", "Boundary fencing and gates repaired as needed."),
            ("Around Opening Hours", "Work scheduled early morning or on quieter days to avoid disrupting trade."),
        ],
        faqs=[
            ("Can you work around our opening hours?",
             "Yes, we can schedule visits early morning or on quieter trading days to avoid disrupting service."),
            ("Do you pressure wash beer gardens and patios?",
             "Yes, pressure washing is one of the most common jobs we do for pubs and restaurants."),
            ("Can you prepare the venue before a busy season or event?",
             "Yes, we can tidy and prepare grounds and outdoor areas ahead of busy seasonal trading or events."),
        ],
        related=["pressure-washing", "grounds-maintenance", "paving-repairs"],
    ),
    dict(
        filename="shop-retail-exterior-maintenance-preston.html",
        h1="Shop & Retail Unit Exterior Maintenance in Preston",
        tagline="Presentable shopfronts, car parks and service areas",
        meta_title="Shop & Retail Exterior Maintenance Preston | GreenFix",
        meta_description="Exterior maintenance for shops and retail units in Preston — pressure washing, grounds care and repairs for business parks.",
        intro="Shops, retail units and business parks need exterior areas that stay presentable for customers, with work scheduled to avoid disrupting trade. GreenFix pressure washes shopfronts and entrances, maintains grounds and car parks, and carries out paving and fencing repairs as needed.",
        cards=[
            ("Shopfront & Entrance Presentation", "Pressure washing to keep shopfronts and entrances clean and welcoming."),
            ("Car Parks & Customer Areas", "Grounds maintenance and paving repairs for car parks and customer-facing areas."),
            ("Business Parks", "Scheduled maintenance across business parks with multiple retail units."),
            ("Before or After Trading Hours", "Work scheduled before opening or out of hours to avoid disrupting customers."),
        ],
        faqs=[
            ("Can you clean shopfronts and entrances?",
             "Yes, pressure washing shopfronts and entrances is a common job for retail units."),
            ("Do you work with business parks with multiple units?",
             "Yes, we work with individual shops as well as business parks and managed retail sites with multiple units."),
            ("Can you work before opening hours?",
             "Yes, we can schedule visits early morning or out of hours to avoid disrupting trading."),
        ],
        related=["pressure-washing", "grounds-maintenance", "paving-repairs"],
    ),
]


def render_sector_page(sector):
    canonical_path = "/" + sector["filename"][:-5]
    schema = "\n".join([
        f'    <script type="application/ld+json">\n{local_business_schema()}\n    </script>',
        f'    <script type="application/ld+json">\n{breadcrumb_schema([("Home", "/"), ("Sectors We Work With", None), (sector["h1"].split(" in ")[0], None)])}\n    </script>',
        f'    <script type="application/ld+json">\n{faq_schema(sector["faqs"])}\n    </script>',
    ])
    head = render_head(
        title=sector["meta_title"],
        description=sector["meta_description"],
        canonical_path=canonical_path,
        extra_schema=schema,
    )
    breadcrumb = render_breadcrumb_html([
        ("Home", "/"), ("Sectors We Work With", None), (sector["h1"].split(" in ")[0], None)
    ])
    cards_html = "\n                ".join(
        f'<div class="card"><h3>{esc(t)}</h3><p>{esc(txt)}</p></div>' for t, txt in sector["cards"]
    )
    faqs_html = "\n                ".join(
        f'<div class="faq-item"><h3>{esc(q)}</h3><p>{esc(a)}</p></div>' for q, a in sector["faqs"]
    )
    related_html = "\n                ".join(
        f'<a href="/{slug}">{esc(SERVICE_BY_SLUG[slug]["h1"].split(" in ")[0])}</a>'
        for slug in sector["related"] if slug in SERVICE_BY_SLUG
    )
    body = f"""{breadcrumb}
    <section id="main-content" class="hero">
        <div class="hero-content">
            <h1>{esc(sector["h1"])}</h1>
            <p class="tagline">{esc(sector["tagline"])}</p>
            <div class="button-group">
                <a href="tel:{PHONE_TEL}" class="btn btn-primary">\U0001F4DE Call {PHONE_DISPLAY}</a>
                <a href="/#quote-form" class="btn btn-secondary">Request a Free Quote</a>
            </div>
        </div>
    </section>

    <section class="section-white">
        <div class="container">
            <p class="lede">{esc(sector["intro"])}</p>
        </div>
    </section>
{render_trust_strip()}
    <section class="section-grey">
        <div class="container">
            <h2 class="center">How We Help</h2>
            <div class="grid grid-2">
                {cards_html}
            </div>
        </div>
    </section>

    <section class="section-white">
        <div class="container">
            <h2 class="center">Frequently Asked Questions</h2>
            <div class="grid grid-2">
                {faqs_html}
            </div>
        </div>
    </section>

    <section class="section-grey">
        <div class="container">
            <h2 class="center">Relevant Services</h2>
            <div class="related-links" style="justify-content:center;">
                {related_html}
            </div>
        </div>
    </section>

    <section class="final-cta">
        <div class="container">
            <h2>Get a Free Quote</h2>
            <p>Call {PHONE_DISPLAY} or use our quote form &mdash; we respond within 24 hours.</p>
            <div class="button-group">
                <a href="tel:{PHONE_TEL}" class="btn btn-primary">\U0001F4DE Call {PHONE_DISPLAY}</a>
                <a href="/#quote-form" class="btn btn-secondary">Request a Free Quote</a>
            </div>
        </div>
    </section>
"""
    return render_page(head_html=head, body_html=body)


def build_sector_pages():
    for sector in SECTOR_PAGES:
        write_page(sector["filename"], render_sector_page(sector))


# ---------------------------------------------------------------------------
# Blog — one post per priced service, phrased as the actual question a
# homeowner would search, with a direct answer up front (for featured
# snippets / AI answer engines) followed by more detail. The two
# quotation-only hub pages (exterior-structural-repairs, repairs-and-
# maintenance) don't get a post since they're not a single "problem".
# ---------------------------------------------------------------------------

BLOG_PUBLISH_DATE = "2026-08-02"

BLOG_POSTS = [
    dict(
        slug="how-often-should-you-cut-your-lawn",
        title="How Often Should You Cut Your Lawn?",
        service="lawn-mowing",
        meta_description="How often to mow your lawn in the UK, by season — plus why cutting too short or too rarely both cause problems.",
        answer="In the UK growing season (roughly April to September), most lawns need cutting weekly. Over autumn and early spring, fortnightly is usually enough. In winter, when grass growth slows right down, mowing mostly stops altogether.",
        body=[
            "The right frequency depends more on growth rate than the calendar. A mild, wet spring can mean grass needs cutting weekly by April; a dry summer can slow growth right down even in July. The general rule is: never remove more than about a third of the grass blade length in one cut. Cutting too much off in one go stresses the lawn and can leave it patchy or more vulnerable to weeds.",
            "Letting a lawn go too long between cuts causes its own problems — long grass shades out the base of the sward, encourages moss and weeds, and makes the eventual cut harder on the lawn (and the mower). If a lawn has been left for several weeks, it often needs a first cut at a higher blade height, then a second, lower cut a few days later, rather than scalping it back to normal length in one go.",
            "A regular round takes the guesswork out of it — the mower turns up on a schedule that suits the season, rather than you trying to judge it yourself. Preston's mild but wet climate means growth can pick up quickly after a rainy spell, which is exactly why a scheduled round tends to suit gardens in this area better than trying to judge it yourself.",
        ],
    ),
    dict(
        slug="how-much-does-garden-maintenance-cost",
        title="How Much Does Garden Maintenance Cost?",
        service="garden-maintenance",
        meta_description="Guide prices for garden maintenance in the UK and what affects the cost — garden size, how overgrown it is, and how often you want visits.",
        answer="Garden maintenance typically starts from around £40 per visit for a standard residential garden, though the exact price depends on the size of the garden, how much work is needed, and whether it's a one-off or a regular round.",
        body=[
            "Three things drive the price more than anything else: the size of the garden, its current condition, and the frequency of visits. A small, well-kept garden on a fortnightly round costs less per visit than a large or neglected garden needing a longer session to bring it back under control.",
            "One-off visits are usually priced slightly higher per visit than a regular arrangement, since there's more unpredictability in exactly what's needed and no ongoing relationship with the garden. Regular customers often find the price per visit settles once a maintenance routine is established, because the gardener isn't starting from scratch each time.",
            "It's worth getting a specific quote rather than assuming a generic guide price applies — a garden that's mostly lawn costs less to maintain than one with several beds, borders and hedges needing attention on every visit. Gardens across Preston vary a lot in size and layout, so a specific quote for your own garden is always more accurate than a generic figure.",
        ],
    ),
    dict(
        slug="whats-included-in-a-grounds-maintenance-contract",
        title="What's Included in a Grounds Maintenance Contract",
        service="grounds-maintenance",
        meta_description="What a typical grounds maintenance contract covers for estates, business premises and larger sites, and how it differs from one-off garden work.",
        answer="A grounds maintenance contract typically covers scheduled grass cutting, hedge and border upkeep, and general tidiness of communal or site-wide areas, delivered on a set visit schedule rather than as one-off jobs.",
        body=[
            "The key difference from ad-hoc garden work is the contract structure: visits are scheduled in advance (weekly, fortnightly or monthly, depending on the site and season), and the same standard is maintained across every visit rather than being reassessed each time. This matters most for sites where consistency is visible to residents, tenants, staff or visitors — a managed estate or business premises that looks different every few weeks reflects badly on whoever's responsible for it.",
            "Contracts are also useful where there are multiple areas to keep on top of — verges, communal lawns, borders around a car park, access routes — that would be inefficient to book separately. Having one contractor and one point of contact for the whole site avoids the coordination overhead of managing several different visits or subcontractors.",
            "Most contracts can flex with the seasons — more frequent visits during peak growth, less during winter — rather than being a rigid year-round schedule that doesn't match actual growth. This is especially relevant for larger sites and estates across Preston, where consistency across multiple visits matters more than it would for a single household garden.",
        ],
    ),
    dict(
        slug="best-time-of-year-to-trim-hedges",
        title="When Is the Best Time of Year to Trim Hedges?",
        service="hedge-trimming",
        meta_description="The best time of year to trim hedges in the UK, and why timing matters for both hedge health and nesting birds.",
        answer="Most UK hedges are best trimmed in late spring/early summer and again in early autumn, avoiding the main bird nesting season (roughly March to August) for anything more than light, careful trimming.",
        body=[
            "Timing matters for two reasons. First, hedges respond differently depending on when they're cut — cutting right after a flush of new growth helps keep a tidy shape without checking the plant's growth too hard, while cutting too late in the season on some species can remove the next year's flowering wood. Second, many hedges provide nesting habitat for birds, and it's an offence under UK law to damage or destroy an active bird's nest, so hedge cutting is generally avoided or done very carefully during the nesting season.",
            "Fast-growing hedges like privet or leylandii may need two or three trims a year to stay tidy, while slower-growing types like beech or yew often need just one good cut annually. An overgrown hedge that needs serious height or width reduction is usually best tackled gradually over more than one visit, rather than cut back hard in a single session, which can shock the plant and leave bare, woody patches that take a long time to green up again.",
            "If a hedge has been left for a long time and needs significant reduction, it's worth getting it assessed first — the right approach depends on the hedge type and how much it's grown out. Hedges are a common boundary choice across Preston gardens, so getting the timing and technique right matters for a huge number of properties in the area.",
        ],
    ),
    dict(
        slug="garden-completely-overgrown-where-to-start",
        title="My Garden's Overgrown — Where Do I Start?",
        service="garden-tidy-ups",
        meta_description="What to do with a badly overgrown or neglected garden — how a garden tidy-up works and what to expect from the first visit.",
        answer="Start with a full garden tidy-up rather than trying to bring an overgrown garden back under control through routine maintenance visits — a tidy-up is a one-off reset designed specifically for this situation.",
        body=[
            "An overgrown garden usually has several problems layered on top of each other: grass that's grown too long to simply mow, beds lost under weeds and self-seeded growth, hedges or shrubs that have spread well beyond their space, and general accumulated debris. Trying to fix all of this through a normal fortnightly maintenance visit doesn't work — there's simply too much to do in a standard visit, and a garden that's this far gone needs a different kind of session.",
            "A proper tidy-up clears the overgrowth in one focused visit (or occasionally two, for a very large or badly overgrown garden): cutting back brambles and overgrown shrubs, clearing weeds from beds and borders, getting the lawn back down to a manageable length over more than one cut if needed, and removing everything that's cleared rather than leaving it in piles.",
            "Once a garden's been reset this way, it's usually straightforward to move onto a regular garden maintenance schedule to keep it that way — the hard part is the initial reset, not keeping on top of it afterwards. This is one of the most requested jobs we see across Preston, particularly after a house move or a long period where a garden's been left unattended.",
        ],
    ),
    dict(
        slug="can-pressure-washing-damage-patio-or-driveway",
        title="Can Pressure Washing Damage a Patio or Driveway?",
        service="pressure-washing",
        meta_description="Whether pressure washing can damage patios, driveways or block paving, and how the right technique avoids it.",
        answer="Pressure washing shouldn't damage a patio or driveway if the pressure and technique are matched to the surface — but using too high a pressure, the wrong nozzle, or holding the jet too close can damage joints, pointing and softer materials.",
        body=[
            "The main risk isn't the water pressure itself but how it's applied. Block paving has sand-filled joints between the blocks that can be blasted out by an aggressive, close-up jet, leaving the paving looser and more prone to shifting. Natural stone and older or softer paving can be etched or have its surface damaged by excessive pressure. Mortar joints in an older patio can also be eroded by a jet held too close for too long.",
            "Used correctly — the right pressure, the right nozzle, kept moving rather than held in one spot, and with joint sand re-applied afterwards where needed — pressure washing is a safe and effective way to remove moss, algae, grime and staining without damaging the surface underneath.",
            "If a patio or driveway is already cracked, sunken, or has loose slabs rather than just being dirty, pressure washing won't fix that — that's a repair job, not a cleaning one, and pushing a jet washer over damaged paving can make loose sections worse rather than better. Preston's damp climate means algae and moss build up on patios and driveways faster here than in drier parts of the country, which is why pressure washing is such a regularly requested job across the area.",
        ],
    ),
    dict(
        slug="how-often-should-windows-be-cleaned",
        title="How Often Should Windows Be Cleaned?",
        service="window-cleaning",
        meta_description="How often windows should be cleaned for homes and businesses in the UK, and what affects the right frequency.",
        answer="Most homes do well with windows cleaned every four to eight weeks; businesses with customer-facing windows, or homes near busy roads or trees, often benefit from a more frequent round.",
        body=[
            "Location makes a real difference. Windows near a busy road pick up traffic grime faster; homes surrounded by trees deal with sap, pollen and bird droppings more often; coastal properties get salt residue that builds up faster than inland homes. A shopfront or office relies on clean windows for how the business presents to customers, so a monthly or even fortnightly round is common for commercial premises, while many homes are happy with a round every six to eight weeks.",
            "Frames and sills collect grime just as much as the glass does, and are often skipped by a quick DIY clean — a proper window clean covers both, not just the glass, for a result that actually looks finished rather than clean panes surrounded by grubby frames.",
            "A regular round tends to work out easier than one-off cleans booked irregularly, since windows cleaned to a schedule never get bad enough to need extra work to bring them back up to standard. Properties near busier roads in and around Preston often benefit from a slightly more frequent round than the general guide above.",
        ],
    ),
    dict(
        slug="fence-needs-repairing-or-replacing",
        title="Does My Fence Need Repairing or Replacing?",
        service="fence-repairs",
        meta_description="How to tell if a damaged fence just needs repairing, or if it's time to replace it — and why posts matter more than panels.",
        answer="If the posts are sound and it's the panels, boards or a hinge that's failed, a repair usually sorts it. If multiple posts are rotten or leaning, a full replacement is often more cost-effective than repeated repairs.",
        body=[
            "Posts are the part that matters most. A fence with solid posts but a blown-down or rotten panel is a straightforward, relatively cheap repair — the panel is replaced and the fence is back to normal. A fence where the posts themselves have rotted at ground level, or where several posts are leaning, is a different problem: propping up panels against failing posts doesn't hold for long, and repairing one post at a time on an old fence often just moves the problem along the fence line.",
            "Age and extent both matter too. A fence that's mostly sound with one damaged section is worth repairing. A fence that's uniformly old, with rot or damage appearing in multiple places at once, is often approaching the point where full replacement makes more sense than an ongoing series of repairs.",
            "If it's not obvious which category a fence falls into, it's worth having it looked at — the cost difference between a repair and a replacement is significant, and it's not always visually obvious from the panels alone whether the posts underneath are still sound. Fencing across Preston takes a battering from regular wind and rain, which is why fence repairs are one of the most common call-outs we see in the area.",
        ],
    ),
    dict(
        slug="why-wont-my-gate-close-properly",
        title="Why Won't My Gate Close Properly?",
        service="gate-repairs",
        meta_description="The most common reasons a garden or driveway gate won't close, latch or swing properly, and whether it needs repairing or replacing.",
        answer="A gate that won't close properly is usually a hinge, alignment or post problem rather than an issue with the gate itself — worn hinges or a settling post let the gate drop or twist out of true over time.",
        body=[
            "Gates are supported at just two or three points (the hinges), so any wear or movement there has an outsized effect on how the whole gate hangs. Worn or rusted hinges let a gate sag on its hinge side, which is why a gate often drags on the ground or won't reach the latch — it's dropped slightly out of its original position, not necessarily grown or warped.",
            "The post the gate is hung from matters just as much as the hinges. If a gate post has started to lean or move in the ground, no amount of hinge adjustment will fully fix the problem, since the whole reference point for the gate has shifted. This is more common with timber posts set in ground that gets waterlogged, or older posts nearing the end of their life.",
            "In most cases a gate can be repaired — re-hung, hinges replaced, or the post reset — without needing a full replacement gate, which is usually the more expensive part of the job. This is a common repair across Preston gardens, particularly on older timber gates that have been in place for many years.",
        ],
    ),
    dict(
        slug="how-much-does-brick-repointing-cost",
        title="How Much Does Brick Repointing Cost?",
        service="brick-repointing",
        meta_description="Guide prices for brick repointing in the UK, priced per square metre, and what affects the cost of the job.",
        answer="Brick repointing is typically priced per square metre of wall, from around £30 per m² as a guide price, with the final cost depending on how much of the wall needs repointing and how accessible it is.",
        body=[
            "Repointing is priced by area rather than as a flat fee because the amount of work scales directly with how much wall needs doing — a small patch of failed mortar around a single window is a much smaller job than repointing an entire elevation. The condition of the existing mortar matters too: raking out mortar that's already crumbling and loose is quicker than removing mortar that's still largely sound but just needs refreshing.",
            "Access affects price as well. Ground-floor walls are more straightforward than upper storeys needing scaffolding or tower access, and this is usually factored into the quote once the extent and location of the work is known.",
            "It's worth getting an actual assessment rather than assuming a guide price applies to your wall — the per-square-metre rate is a starting point, and the final figure depends on the real area and condition once it's been properly looked at. Older housing stock across Preston, especially Victorian and Edwardian terraces, often reaches this point in the mortar's lifespan, which is why repointing is such a regular job in the area.",
        ],
    ),
    dict(
        slug="what-causes-bricks-to-crack-or-spall",
        title="What Causes Bricks to Crack or Spall?",
        service="brick-repairs",
        meta_description="Why bricks crack or spall (flake) over time, and what to do about damaged brickwork.",
        answer="Frost damage is the most common cause of cracked or spalled (flaking) bricks: water gets into the brick, freezes, expands, and breaks the surface apart. Impact damage and general age also contribute.",
        body=[
            "Bricks are porous, so they absorb some moisture from rain and damp ground. In cold weather, that moisture can freeze inside the brick. Water expands as it freezes, and that expansion, repeated over many freeze-thaw cycles each winter, is what causes the surface of a brick to flake away (spalling) or crack. Older bricks, softer brick types, and bricks that stay damp for longer (for example, near a leaking gutter or at ground level where they're more exposed to standing water) are more prone to this.",
            "Once a brick has started to spall, the problem tends to get worse over time rather than stay the same, because the newly exposed surface is more porous and holds even more water than the original brick face did. This is why a small area of frost damage left unaddressed often spreads to neighbouring bricks over a few winters.",
            "The fix is straightforward: damaged bricks are removed and replaced with matching bricks, and if the surrounding mortar has also failed, repointing that area at the same time stops water getting back into the new brickwork the same way. This is a common issue on older brick properties across Preston, where many buildings have been standing through decades of freeze-thaw winters.",
        ],
    ),
    dict(
        slug="garden-wall-leaning-is-it-dangerous",
        title="My Garden Wall Is Leaning — Is It Dangerous?",
        service="garden-wall-repairs",
        meta_description="Whether a leaning garden or boundary wall is dangerous, and what to do about it.",
        answer="A leaning garden wall can be dangerous, especially if it's near a path, driveway, public footpath, or anywhere people or vehicles pass close by — it's worth having it assessed promptly rather than waiting to see if it gets worse.",
        body=[
            "Garden and boundary walls lean for a few common reasons: the ground underneath has moved or settled unevenly, the original foundations were shallow or inadequate, water has washed out material from behind or beneath the wall over time, or age has simply weakened the mortar and structure. A wall that's leaning has already lost some of the structural integrity that kept it upright and stable, and leaning walls don't generally correct themselves — the lean tends to increase over time, sometimes slowly and sometimes suddenly after a period of wet weather or ground movement.",
            "The risk depends heavily on location and height. A low wall leaning slightly in a spot nobody walks past is a lower priority than a taller wall leaning over a path, pavement, or anywhere children play. Taller walls also store more energy if they do fail, making a sudden collapse more serious.",
            "In many cases only the affected section needs rebuilding, not the whole wall — but that's a judgement that needs an actual assessment of the wall's condition, not a guess from how it looks from a distance. Garden and boundary walls are a common feature on properties across Preston, particularly older housing stock, which is why we're regularly asked to assess and repair them.",
        ],
    ),
    dict(
        slug="why-is-my-patio-sinking-or-cracking",
        title="Why Is My Patio Sinking or Cracking?",
        service="patio-repairs",
        meta_description="Why patio slabs sink, crack or become loose over time, and how patio repairs differ from patio cleaning.",
        answer="Patios sink or crack when the base underneath fails — through poor original installation, ground movement, or water washing out the material the slabs are bedded on — rather than through a problem with the slabs themselves.",
        body=[
            "A patio is only as stable as what's underneath it. If the sub-base wasn't properly compacted when the patio was laid, or if water has found a way to erode the bedding material over the years, individual slabs lose their support and start to rock, sink, or crack under normal weight. Tree roots growing underneath a patio can cause similar movement, lifting some slabs while others stay in place.",
            "It's worth being clear on the difference between a patio that's damaged and one that's just dirty. Green algae, moss and general grime don't affect the structure of a patio at all — that's a cleaning job, and pressure washing sorts it. Cracked, sunken, loose or rocking slabs are a different problem entirely, caused by what's happening beneath the surface, and cleaning won't fix any of it.",
            "Repairing a patio properly means addressing the base, not just replacing the visible slab — otherwise the same section is likely to sink again within a season or two. This is one of the most common repair enquiries we get from homeowners across Preston, especially on patios more than a few years old.",
        ],
    ),
    dict(
        slug="how-to-fix-a-pothole-or-sunken-driveway",
        title="How Do I Fix a Pothole or Sunken Driveway?",
        service="paving-repairs",
        meta_description="How sunken driveways and potholes in block paving or tarmac are fixed properly, rather than just patched over.",
        answer="A sunken driveway area or pothole is fixed by lifting the affected paving, correcting the base underneath, and relaying or patching the surface — simply filling the dip doesn't address why it sank in the first place.",
        body=[
            "Sunken patches in a driveway almost always come from a problem below the surface: the base wasn't compacted well enough originally, water has got underneath and washed material away, or the edge restraint (the border that holds paving blocks in place) has failed and let the paving spread and settle. Filling a pothole from the top, without addressing what caused it, tends to be a short-term fix — the same spot often sinks again within a season.",
            "A proper repair lifts the affected area, corrects or re-compacts the base, and relays the blocks or patches the tarmac properly. Where the problem is edge restraint failure rather than the base itself, refitting or replacing the edging is often what actually stops the paving spreading and sinking again, even more than the pothole repair itself.",
            "Matching the replacement blocks or tarmac to the existing driveway is usually possible, though an exact colour match depends on how available the original material still is. This is a frequent issue on driveways across Preston, particularly older block paving laid before modern edge-restraint standards became common.",
        ],
    ),
    dict(
        slug="why-do-patio-slabs-become-uneven-over-time",
        title="Why Do Patio Slabs Become Uneven Over Time?",
        service="slab-relaying",
        meta_description="Why patio and path slabs become uneven or hold water over time, and how slab relaying differs from a full patio repair.",
        answer="Slabs become uneven when the ground or bedding material underneath settles unevenly over time — the slabs themselves are often still perfectly sound, they're just no longer sitting level or draining correctly.",
        body=[
            "This is a subtly different problem from a damaged patio. Ground settles at different rates in different spots, especially where drainage isn't even across an area, and over several years this can leave a patio or path with slabs at slightly different heights, or with a \"fall\" (slope) that no longer directs rainwater away from the house the way it should have originally. None of this necessarily means the slabs are cracked or broken — they're simply not sitting the way they were laid.",
            "This is why slab relaying is a distinct job from patio or paving repairs: instead of replacing damaged material, the existing (still sound) slabs are lifted, the base underneath is corrected and properly compacted, and the same slabs are relaid level and with the right fall for drainage. This is usually more cost-effective than full replacement, since the slabs themselves don't need to be new — just properly re-based.",
            "A common sign it's needed: water pooling on a patio or path well after rain has stopped, rather than draining away within a reasonable time. This is a common job across Preston gardens, especially on patios and paths laid more than five or so years ago.",
        ],
    ),
    dict(
        slug="how-do-i-know-if-i-have-a-slipped-roof-tile",
        title="How Do I Know If I Have a Slipped Roof Tile?",
        service="roof-tile-repairs",
        meta_description="How to spot a slipped, cracked or missing roof tile, and why it's worth fixing quickly.",
        answer="A slipped roof tile is often visible from the ground as a gap, an oddly angled tile, or a tile that looks out of line with the rest of the roof — it's frequently first noticed after noticing a damp patch appearing inside near the roofline.",
        body=[
            "Roof tiles are held in place partly by their own weight and shape and partly by fixings, battens and the tiles around them. Wind, age, or a fixing failing can let a tile slip out of its original position, creating a gap where wind-driven rain can get into the roof structure underneath. From the ground, this often looks like a tile sitting at a slightly different angle to its neighbours, or an actual visible gap in the tile pattern.",
            "Because roofs aren't inspected day to day, a slipped tile is often first noticed indirectly — a damp patch on a ceiling or upper wall, a slight drip during heavy rain, or (less obviously) a tile found on the ground after a windy spell, which is a clear sign at least one tile has come loose somewhere on the roof.",
            "It's worth acting quickly once a slipped or missing tile is suspected. A single tile is a small, inexpensive repair; the water damage that follows a gap being left over a wet season is considerably more expensive to put right than the original tile. Preston's exposed, often windy weather means roof tiles across the area are more prone to slipping than in more sheltered parts of the country.",
        ],
    ),
    dict(
        slug="why-is-my-drain-blocked-again-after-clearing-it",
        title="Why Is My Drain Blocked Again After Clearing It?",
        service="drain-repairs",
        meta_description="Why a drain keeps blocking at the same spot after clearing, and when a repair is needed instead of just rodding it again.",
        answer="A drain that blocks repeatedly at the same spot usually has a physical problem — a cracked, misaligned or partially collapsed section of pipe — rather than just a debris blockage that keeps coming back by chance.",
        body=[
            "Clearing a blocked drain (rodding, jetting) removes whatever's causing the blockage at that moment, but it doesn't fix a damaged pipe. If the same spot blocks again within weeks or months, that's a strong signal the pipe itself has an issue: a crack or gap letting tree roots in, a section that's sunk out of alignment and now holds debris instead of letting it flow through, or a partially collapsed section narrowing the pipe.",
            "Tree root ingress is one of the most common repeat-blockage causes — roots seek out the moisture inside a drain and can enter through even a small crack or joint gap, then grow inside the pipe and catch debris every time water flows past. Clearing the blockage removes the immediate obstruction but leaves the roots (and the crack that let them in) in place, so it happens again.",
            "If a drain has blocked more than once at the same location, it's worth having the actual pipe assessed and repaired rather than continuing to clear the same blockage repeatedly — the repeat call-outs usually end up costing more than fixing the underlying pipe issue once. This is one of the most common repeat call-outs we see across Preston, particularly on older properties with mature trees nearby.",
        ],
    ),
    dict(
        slug="why-does-my-garden-stay-waterlogged-after-rain",
        title="Why Does My Garden Stay Waterlogged After Rain?",
        service="drainage-repairs",
        meta_description="Why parts of a garden stay waterlogged long after rain, and how proper drainage repairs fix it.",
        answer="A garden stays waterlogged after rain when water has nowhere to go — usually because of poor natural drainage in that spot, a soakaway that's stopped working, or ground that's become compacted over time.",
        body=[
            "Some gardens simply have heavier, less free-draining soil in places, especially clay-heavy ground, which holds water far longer than sandier soil. But a spot that used to drain fine and now doesn't often points to something specific changing: a soakaway (an underground structure designed to let water disperse into the surrounding ground) silting up and losing its capacity, a French drain or channel drain blocking or being damaged, or the ground itself becoming compacted from repeated foot traffic or heavy use, which reduces how well water can soak away naturally.",
            "This is a different problem from a single blocked drain pipe. Drainage repairs address the wider system — or lack of one — across a waterlogged area, rather than one specific pipe. That might mean clearing and repairing an existing soakaway or French drain, or in some cases installing proper drainage where there wasn't an adequate system in the first place.",
            "The right fix depends on identifying the actual cause for that specific spot, rather than guessing — the same symptom (standing water) can have quite different underlying causes from one garden to the next. Heavier clay soil is common across parts of Preston, which is exactly the kind of ground that holds water longer than it should without proper drainage in place.",
        ],
    ),
    dict(
        slug="why-wont-my-window-close-properly",
        title="Why Won't My Window Close Properly?",
        service="window-repairs",
        meta_description="Common reasons a window won't close, latch or seal properly, and whether it needs repairing or replacing.",
        answer="A window that won't close properly is usually down to worn hinges, a frame that's warped or shifted slightly out of alignment, or a build-up of paint or debris in the frame — all of which are normally repairable without replacing the whole window.",
        body=[
            "Timber window frames can swell with damp weather and shrink back in dry conditions, which over time can leave a frame slightly out of true even if it was fitted perfectly originally. uPVC frames don't suffer from swelling in the same way, but their hinges and mechanisms wear over time just like any moving part, and can drop or stiffen enough to stop a window closing and locking cleanly.",
            "A window that closes but lets in a draught is a slightly different problem, usually down to a failed or perished seal around the glazing or frame rather than an alignment issue — the window closes fine, but no longer seals against the weather the way it did when new.",
            "In most cases these are repairable: adjusting or replacing hinges, correcting the frame alignment, or replacing a failed seal. Full window replacement is really only necessary where the frame itself is significantly rotten or structurally damaged, which is a smaller proportion of cases than people often assume. This is a common repair across both older and newer properties in Preston, since hinges and seals wear out regardless of a property's age.",
        ],
    ),
    dict(
        slug="why-does-my-door-stick-or-drag-on-the-floor",
        title="Why Does My Door Stick or Drag on the Floor?",
        service="door-repairs",
        meta_description="Why exterior doors stick or drag on the floor, and whether it's a repair job or a sign the door needs replacing.",
        answer="A door that sticks or drags on the floor is almost always a hinge or frame alignment problem, not a sign the door itself has grown or changed shape — the door has usually dropped slightly on worn hinges rather than the door being the wrong size.",
        body=[
            "Doors are heavy, and they hang entirely on their hinges. Over time, hinges wear, screws holding them can work loose in the frame, and the door gradually drops on the hinge side — often by only a few millimetres, but enough to catch on the floor or stick against the frame on the opposite side. This is why an exterior door that closed perfectly for years can start sticking without anything obvious having changed.",
            "Timber doors and frames can also be affected by seasonal moisture changes, swelling slightly in damp weather and shrinking back in dry conditions, which can make sticking worse at certain times of year even with sound hinges.",
            "Tightening or replacing worn hinges, and correcting the frame alignment where needed, resolves the great majority of sticking or dragging doors. Full door or frame replacement is usually only needed where there's actual rot or structural damage, which is a different (and less common) problem from ordinary hinge wear. This is one of the most frequent repair call-outs we get from homes across Preston, since every exterior door takes daily use.",
        ],
    ),
]

BLOG_BY_SERVICE = {p["service"]: p["slug"] for p in BLOG_POSTS}
BLOG_BY_SLUG = {p["slug"]: p for p in BLOG_POSTS}


def render_blog_post(post):
    service = SERVICE_BY_SLUG[post["service"]]
    service_name = service["h1"].split(" in ")[0]
    canonical_path = f"/blog/{post['slug']}"

    article_schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post["title"],
        "description": post["meta_description"],
        "datePublished": BLOG_PUBLISH_DATE,
        "dateModified": BLOG_PUBLISH_DATE,
        "author": {"@type": "Organization", "name": BUSINESS_NAME},
        "publisher": {"@type": "Organization", "name": BUSINESS_NAME,
                       "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/{LOGO_IMG}"}},
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{DOMAIN}{canonical_path}"},
        "image": f"{DOMAIN}/hero-commercial-grounds.png",
    }

    schema = "\n".join([
        f'    <script type="application/ld+json">\n{local_business_schema()}\n    </script>',
        f'    <script type="application/ld+json">\n{breadcrumb_schema([("Home", "/"), ("Blog", "/blog"), (post["title"], None)])}\n    </script>',
        f'    <script type="application/ld+json">\n{json.dumps(article_schema, indent=2)}\n    </script>',
    ])

    head = render_head(
        title=f"{post['title']} | GreenFix Blog",
        description=post["meta_description"],
        canonical_path=canonical_path,
        extra_schema=schema,
    )

    breadcrumb = render_breadcrumb_html([("Home", "/"), ("Blog", "/blog"), (post["title"], None)])

    body_html = "\n            ".join(f'<p>{esc(p)}</p>' for p in post["body"])

    related_posts = [p for p in BLOG_POSTS if p["slug"] != post["slug"]][:3]
    related_html = "\n                ".join(
        f'<a href="/blog/{p["slug"]}">{esc(p["title"])}</a>' for p in related_posts
    )

    body = f"""{breadcrumb}
    <section id="main-content" class="hero">
        <div class="hero-content">
            <h1>{esc(post["title"])}</h1>
        </div>
    </section>

    <section class="section-white">
        <div class="container">
            <p class="lede" style="font-size:1.1rem;font-weight:600;color:var(--charcoal);">{esc(post["answer"])}</p>
        </div>
    </section>

    <section class="section-white" style="padding-top:0;">
        <div class="container" style="max-width:760px;">
            {body_html}
        </div>
    </section>

    <section class="section-grey">
        <div class="container" style="max-width:760px;text-align:center;">
            <h2>Need Help With This?</h2>
            <p class="lede center" style="margin-bottom:1.25rem;">GreenFix provides {esc(service_name.lower())} across Preston. {esc(service["price"])} ({esc(service["price_note"])}).</p>
            <div class="button-group">
                <a href="/{service['slug']}" class="btn btn-dark">See {esc(service_name)}</a>
                <a href="tel:{PHONE_TEL}" class="btn btn-secondary" style="background:var(--dark-green);">\U0001F4DE Call {PHONE_DISPLAY}</a>
            </div>
        </div>
    </section>

    <section class="section-white">
        <div class="container">
            <h2 class="center">More From the Blog</h2>
            <div class="related-links" style="justify-content:center;">
                {related_html}
            </div>
        </div>
    </section>
"""
    return render_page(head_html=head, body_html=body)


def render_blog_index():
    schema = "\n".join([
        f'    <script type="application/ld+json">\n{local_business_schema()}\n    </script>',
        f'    <script type="application/ld+json">\n{breadcrumb_schema([("Home", "/"), ("Blog", None)])}\n    </script>',
    ])
    head = render_head(
        title="Blog | Garden & Property Repair Advice | GreenFix",
        description="Straight answers to common questions about garden maintenance, lawns, hedges, brickwork, fencing, paving, roofing, drainage and more.",
        canonical_path="/blog",
        extra_schema=schema,
    )
    breadcrumb = render_breadcrumb_html([("Home", "/"), ("Blog", None)])

    def post_card(p):
        return (f'<a class="card" style="text-decoration:none;display:block;" href="/blog/{p["slug"]}">'
                f'<h3>{esc(p["title"])}</h3><p>{esc(p["meta_description"])}</p></a>')

    grounds_slugs = {s for s in next(c for c in CLUSTERS if c["key"] == "grounds")["slugs"]}
    grounds_posts = [p for p in BLOG_POSTS if p["service"] in grounds_slugs]
    repair_posts = [p for p in BLOG_POSTS if p["service"] not in grounds_slugs]

    grounds_cards = "\n                ".join(post_card(p) for p in grounds_posts)
    repair_cards = "\n                ".join(post_card(p) for p in repair_posts)

    body = f"""{breadcrumb}
    <section id="main-content" class="hero">
        <div class="hero-content">
            <h1>The GreenFix Blog</h1>
            <p class="tagline">Straight answers to real questions about gardens, grounds and property repairs</p>
        </div>
    </section>

    <section class="section-white">
        <div class="container">
            <h2 class="center">Grounds &amp; Garden Care Questions</h2>
            <div class="grid grid-3">
                {grounds_cards}
            </div>
        </div>
    </section>

    <section class="section-grey">
        <div class="container">
            <h2 class="center">Repairs &amp; Maintenance Questions</h2>
            <div class="grid grid-3">
                {repair_cards}
            </div>
        </div>
    </section>

    <section class="final-cta">
        <div class="container">
            <h2>Can't Find Your Answer?</h2>
            <p>Ask {BOT_NAME} using the chat button, or call {PHONE_DISPLAY} directly.</p>
            <div class="button-group">
                <a href="tel:{PHONE_TEL}" class="btn btn-primary">\U0001F4DE Call {PHONE_DISPLAY}</a>
                <a href="/#quote-form" class="btn btn-secondary">Request a Free Quote</a>
            </div>
        </div>
    </section>
"""
    return render_page(head_html=head, body_html=body)


def build_blog():
    os.makedirs(os.path.join(ROOT, "blog"), exist_ok=True)
    for post in BLOG_POSTS:
        path = os.path.join("blog", f"{post['slug']}.html")
        write_page(path, render_blog_post(post))
    write_page(os.path.join("blog", "index.html"), render_blog_index())


# ---------------------------------------------------------------------------
# Retired-page 301 map (old slug -> new clean URL). Kept explicit rather than
# inferred, since these are one-time historical mappings, not derived from
# the SERVICES table.
# ---------------------------------------------------------------------------

RETIRED_301_MAP = [
    # 12 town garden-maintenance pages -> /garden-maintenance
    *[(f"/garden-maintenance-{t}", "/garden-maintenance") for t in [
        "bamber-bridge", "blackburn", "blackpool", "chorley", "freckleton",
        "fulwood", "kirkham", "leyland", "longton", "penwortham", "preston",
        "walton-le-dale",
    ]],
    ("/grass-cutting-preston", "/lawn-mowing"),
    ("/grass-cutting-leyland", "/lawn-mowing"),
    ("/hedge-trimming-preston", "/hedge-trimming"),
    ("/garden-clearance-preston", "/garden-tidy-ups"),
    ("/garden-clearance-penwortham", "/garden-tidy-ups"),
    ("/garden-clearance-leyland", "/garden-tidy-ups"),
    ("/weed-control-preston", "/garden-maintenance"),
    ("/gutter-clearing-preston", "/repairs-and-maintenance"),
    ("/jet-washing-preston", "/pressure-washing"),
    ("/driveway-cleaning-preston", "/pressure-washing"),
    ("/patio-cleaning-preston", "/pressure-washing"),
    ("/bin-store-cleaning-preston", "/repairs-and-maintenance"),
    ("/fence-repairs-preston", "/fence-repairs"),
    ("/gate-repairs-preston", "/gate-repairs"),
    ("/window-cleaning-preston", "/window-cleaning"),
    ("/letting-agent-services", "/"),
    ("/estate-agent-services", "/"),
    ("/airbnb-property-maintenance", "/"),
    ("/landlord-garden-clearance-preston", "/"),
    ("/end-of-tenancy-garden-tidy-preston", "/"),
    ("/hmo-exterior-maintenance-preston", "/"),
]


def build_redirects():
    lines = [
        "# GreenFix Exterior Care — Netlify redirects",
        "# Generated by scripts/build_site.py — do not hand-edit; update the",
        "# SERVICES / SECTOR_PAGES / RETIRED_301_MAP tables instead and rerun.",
        "",
        "# --- 301s: retired pages -> their nearest current equivalent ---",
    ]
    for old, new in RETIRED_301_MAP:
        lines.append(f"{old}  {new}  301")
        lines.append(f"{old}.html  {new}  301")

    lines += ["", "# --- 200 rewrites: clean URLs for current pages ---"]
    for service in SERVICES:
        lines.append(f"/{service['slug']}  /{service['slug']}.html  200")
    for fname, _ in SECTORS:
        clean = "/" + fname[:-5]
        lines.append(f"{clean}  /{fname}  200")
    lines.append("/about-greenfix  /about-greenfix.html  200")
    lines.append("/before-after  /before-after.html  200")
    lines.append("/thank-you  /thank-you.html  200")
    lines.append("/blog  /blog/index.html  200")
    for post in BLOG_POSTS:
        lines.append(f"/blog/{post['slug']}  /blog/{post['slug']}.html  200")

    lines += ["", "# --- Custom 404 ---", "/*  /404.html  404", ""]

    path = os.path.join(ROOT, "_redirects")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))
    print(f"wrote _redirects ({len(lines)} lines)")


def build_sitemap():
    from datetime import date
    today = date.today().isoformat()
    urls = [("/", "1.0")]
    for service in SERVICES:
        urls.append((f"/{service['slug']}", "0.8"))
    for fname, _ in SECTORS:
        urls.append(("/" + fname[:-5], "0.8"))
    urls.append(("/about-greenfix", "0.6"))
    urls.append(("/before-after", "0.6"))
    urls.append(("/blog", "0.7"))
    for post in BLOG_POSTS:
        urls.append((f"/blog/{post['slug']}", "0.7"))

    entries = []
    for path, priority in urls:
        entries.append(f"""  <url>
    <loc>{DOMAIN}{path}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{priority}</priority>
  </url>""")

    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(entries) + "\n</urlset>\n")
    path = os.path.join(ROOT, "sitemap.xml")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(xml)
    print(f"wrote sitemap.xml ({len(urls)} URLs)")


# ---------------------------------------------------------------------------
# Chatbot widget — rule-based FAQ matching, built entirely from the same
# SERVICES / SECTOR_PAGES / COMPLAINTS_STEPS data used everywhere else, so it
# can never state a price, service or policy that isn't already published
# elsewhere on the site. No API, no server, no hallucination risk.
# ---------------------------------------------------------------------------

STOPWORDS = set("""
a an the is are was were be been being do does did doing have has had having
i you he she it we they me him her us them my your his its our their this
that these those to of in on at for with from by about as into like through
after over between out against during without before under around among
and or but if then so than too very can will just don't do you doesn't
what when where who whom which why how all any both each few more most
other some such no nor not only own same so than too very s t can will
just should now
""".split())


def tokenize(text):
    words = re.findall(r"[a-z0-9']+", text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 1]


def build_chatbot_kb():
    entries = []

    # Per-service: price + FAQs
    for service in SERVICES:
        name = service["h1"].split(" in ")[0]
        name_tokens = tokenize(name)
        entries.append({
            "k": sorted(set(name_tokens + ["price", "cost", "much", "charge"])),
            "a": (f"{name}: {service['price']} ({service['price_note']}). "
                  f"{service['tagline']}. See /{service['slug']} or call {PHONE_DISPLAY} for an exact quote."),
        })
        for q, a in service["faqs"]:
            entries.append({
                "k": sorted(set(name_tokens + tokenize(q))),
                "a": a + f" (See /{service['slug']}.)",
            })

    # Sector pages
    for sector in SECTOR_PAGES:
        name = sector["h1"].split(" in ")[0]
        name_tokens = tokenize(name)
        for q, a in sector["faqs"]:
            entries.append({"k": sorted(set(name_tokens + tokenize(q))), "a": a})

    # Homepage general FAQs
    for q, a in HOMEPAGE_FAQS:
        entries.append({"k": sorted(set(tokenize(q))), "a": a})

    # Complaints
    complaints_answer = ("If something isn't right: 1) " + COMPLAINTS_STEPS[0][1] + " 2) " +
                          COMPLAINTS_STEPS[1][1] + " 3) " + COMPLAINTS_STEPS[2][1] +
                          " Full details: /about-greenfix#complaints")
    entries.append({
        "k": ["complain", "complaint", "complaints", "unhappy", "problem", "issue",
              "dispute", "wrong", "fault", "faulty", "refund"],
        "a": complaints_answer,
    })

    # Areas covered
    entries.append({
        "k": ["area", "areas", "cover", "coverage", "location", "locations", "where",
              "preston", "lancashire", "wigan", "manchester", "greater"],
        "a": f"We cover Preston.",
    })

    # Insurance / credentials
    entries.append({
        "k": ["insured", "insurance", "liability", "waste", "carrier", "licence",
              "license", "registered", "credentials", "qualified", "trained",
              "experienced", "experience", "skilled"],
        "a": f"Yes — we hold {INSURANCE} and are a {WASTE_CARRIER}. We're a {TRAINED.lower()}.",
    })

    # Contact
    entries.append({
        "k": ["contact", "phone", "number", "email", "call", "whatsapp", "reach", "quote"],
        "a": f"Call or WhatsApp {PHONE_DISPLAY}, email {EMAIL}, or use the quote form on this page — we respond within 24 hours.",
    })

    # Booking a site visit
    entries.append({
        "k": ["book", "booking", "visit", "appointment", "schedule", "arrange", "come",
              "see", "date", "meeting", "slot", "when", "available"],
        "a": ('Yes — fill in the quote form on this page and add your preferred date and time of day. '
              'It\'s not a guaranteed slot until we confirm by phone, but we\'ll get back to you within 24 hours. '
              '<a href="/#quote-form" style="color:inherit;text-decoration:underline;font-weight:700;">Jump to the booking form &rarr;</a>'),
    })

    # What do you do (general)
    grounds = next(c for c in CLUSTERS if c["key"] == "grounds")
    repairs = next(c for c in CLUSTERS if c["key"] == "repairs")
    grounds_names = ", ".join(SERVICE_BY_SLUG[s]["h1"].split(" in ")[0] for s in grounds["slugs"])
    repairs_names = ", ".join(SERVICE_BY_SLUG[s]["h1"].split(" in ")[0] for s in repairs["slugs"])
    entries.append({
        "k": ["what", "do", "services", "offer", "work", "gardening", "construction", "repairs"],
        "a": f"We cover Grounds & Garden Care ({grounds_names}) and Repairs & Maintenance ({repairs_names}). Ask about a specific service or its price.",
    })

    return entries


BOT_NAME = "Basil"

FLOWER_POT_SVG = """<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">
  <path class="gf-stem" d="M32 36 L32 20" stroke="#2d7a52" stroke-width="2.5" stroke-linecap="round" fill="none"/>
  <path class="gf-stem" d="M32 32 L20 22" stroke="#2d7a52" stroke-width="2.5" stroke-linecap="round" fill="none"/>
  <path class="gf-stem" d="M32 32 L44 22" stroke="#2d7a52" stroke-width="2.5" stroke-linecap="round" fill="none"/>
  <ellipse cx="26" cy="29" rx="4.5" ry="2.2" fill="#2d7a52" transform="rotate(-35 26 29)"/>
  <ellipse cx="38" cy="29" rx="4.5" ry="2.2" fill="#2d7a52" transform="rotate(35 38 29)"/>
  <g class="gf-bloom" transform="translate(20,22)">
    <circle r="1" fill="none"/>
    <g>
      <ellipse rx="3.6" ry="2.3" fill="#f2a9d0" transform="rotate(0)"/>
      <ellipse rx="3.6" ry="2.3" fill="#f2a9d0" transform="rotate(72)"/>
      <ellipse rx="3.6" ry="2.3" fill="#f2a9d0" transform="rotate(144)"/>
      <ellipse rx="3.6" ry="2.3" fill="#f2a9d0" transform="rotate(216)"/>
      <ellipse rx="3.6" ry="2.3" fill="#f2a9d0" transform="rotate(288)"/>
      <circle r="2.2" fill="#ffd54f"/>
    </g>
  </g>
  <g class="gf-bloom" transform="translate(32,15)">
    <g>
      <ellipse rx="4.2" ry="2.7" fill="#ff8f6b" transform="rotate(0)"/>
      <ellipse rx="4.2" ry="2.7" fill="#ff8f6b" transform="rotate(72)"/>
      <ellipse rx="4.2" ry="2.7" fill="#ff8f6b" transform="rotate(144)"/>
      <ellipse rx="4.2" ry="2.7" fill="#ff8f6b" transform="rotate(216)"/>
      <ellipse rx="4.2" ry="2.7" fill="#ff8f6b" transform="rotate(288)"/>
      <circle r="2.6" fill="#ffd54f"/>
    </g>
  </g>
  <g class="gf-bloom" transform="translate(44,22)">
    <g>
      <ellipse rx="3.6" ry="2.3" fill="#b39ddb" transform="rotate(0)"/>
      <ellipse rx="3.6" ry="2.3" fill="#b39ddb" transform="rotate(72)"/>
      <ellipse rx="3.6" ry="2.3" fill="#b39ddb" transform="rotate(144)"/>
      <ellipse rx="3.6" ry="2.3" fill="#b39ddb" transform="rotate(216)"/>
      <ellipse rx="3.6" ry="2.3" fill="#b39ddb" transform="rotate(288)"/>
      <circle r="2.2" fill="#ffd54f"/>
    </g>
  </g>
  <rect x="17" y="33" width="30" height="6" rx="2.5" fill="#a85c30"/>
  <path d="M19 38 L45 38 L41 57 L23 57 Z" fill="#c2703d" stroke="#8a4a26" stroke-width="1"/>
  <path d="M24 44 L40 44" stroke="#a85c30" stroke-width="1.5" opacity="0.6"/>
</svg>"""


CHATBOT_JS_TEMPLATE = """// GreenFix FAQ chatbot — rule-based keyword matching only.
// Knowledge base generated by scripts/build_site.py from the same data
// used to build the site pages, so it can't drift from published prices/FAQs.
(function () {
  var KB = __KB_JSON__;
  var STOPWORDS = new Set(__STOPWORDS_JSON__);
  var PHONE = __PHONE_JSON__;
  var BOT_NAME = __BOT_NAME_JSON__;
  var POT_SVG = __POT_SVG_JSON__;
  var GREETING = "Hello, I'm " + BOT_NAME + " \\uD83C\\uDF3B \\u2014 think of me as GreenFix's resident green thumb. Ask me about our services, prices, the areas we cover, or how to make a complaint.";
  var TEASER_TEXT = "Hi, I'm " + BOT_NAME + "! Need a price or have a question? Just ask.";

  function tokenize(text) {
    var words = text.toLowerCase().match(/[a-z0-9']+/g) || [];
    return words.filter(function (w) { return !STOPWORDS.has(w) && w.length > 1; });
  }

  function bestMatch(input) {
    var tokens = tokenize(input);
    if (!tokens.length) return null;
    var best = null, bestScore = 0;
    for (var i = 0; i < KB.length; i++) {
      var entry = KB[i];
      var score = 0;
      for (var j = 0; j < tokens.length; j++) {
        if (entry.k.indexOf(tokens[j]) !== -1) score++;
      }
      // >= (not >) so that on a tie, the later entry wins. General-intent
      // entries (contact, booking, insurance, areas) are appended after the
      // per-service/per-post FAQ entries specifically so they win ties
      // against FAQs that coincidentally share a word (e.g. "visit").
      if (score >= bestScore && score > 0) { bestScore = score; best = entry; }
    }
    return bestScore >= 1 ? best : null;
  }

  var QUICK_REPLIES = [
    "Book a site visit",
    "What services do you offer?",
    "How much does it cost?",
    "What areas do you cover?",
    "Are you insured?",
    "What's your complaints procedure?",
  ];

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html !== undefined) e.innerHTML = html;
    return e;
  }

  function init() {
    var toggle = el("button", "gf-chat-toggle");
    toggle.type = "button";
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-controls", "gf-chat-panel");
    toggle.setAttribute("aria-label", "Chat with " + BOT_NAME + ", the GreenFix garden assistant");
    var toggleIcon = el("span", "gf-pot-icon", POT_SVG);
    toggle.appendChild(toggleIcon);
    toggle.appendChild(el("span", "gf-chat-toggle-label", "Chat"));

    var teaser = el("div", "gf-chat-teaser");
    var teaserBubble = el("button", "gf-chat-teaser-bubble", TEASER_TEXT);
    teaserBubble.type = "button";
    var teaserClose = el("button", "gf-chat-teaser-close", "\\u00D7");
    teaserClose.type = "button";
    teaserClose.setAttribute("aria-label", "Dismiss");
    teaser.appendChild(teaserBubble);
    teaser.appendChild(teaserClose);

    var panel = el("div", "gf-chat-panel");
    panel.id = "gf-chat-panel";
    panel.setAttribute("role", "dialog");
    panel.setAttribute("aria-label", BOT_NAME + ", the GreenFix garden assistant");
    panel.hidden = true;

    var header = el("div", "gf-chat-header");
    var headerIcon = el("span", "gf-pot-icon gf-pot-icon-sm", POT_SVG);
    var headerTitle = el("div", "gf-chat-header-title");
    headerTitle.appendChild(el("strong", null, BOT_NAME));
    headerTitle.appendChild(el("span", "gf-chat-header-sub", "GreenFix Garden Assistant"));
    header.appendChild(headerIcon);
    header.appendChild(headerTitle);
    var closeBtn = el("button", "gf-chat-close", "\\u00D7");
    closeBtn.type = "button";
    closeBtn.setAttribute("aria-label", "Close chat");
    header.appendChild(closeBtn);
    panel.appendChild(header);

    var log = el("div", "gf-chat-log");
    panel.appendChild(log);

    var quick = el("div", "gf-chat-quick");
    panel.appendChild(quick);

    var form = el("form", "gf-chat-form");
    var input = el("input", "gf-chat-input");
    input.type = "text";
    input.placeholder = "Ask " + BOT_NAME + " a question...";
    input.setAttribute("aria-label", "Type your question");
    var send = el("button", "gf-chat-send", "Send");
    send.type = "submit";
    form.appendChild(input);
    form.appendChild(send);
    panel.appendChild(form);

    document.body.appendChild(toggle);
    document.body.appendChild(teaser);
    document.body.appendChild(panel);

    function addMessage(text, who) {
      var row = el("div", "gf-chat-row gf-chat-row-" + who);
      if (who === "bot") {
        row.appendChild(el("span", "gf-pot-icon gf-pot-icon-xs", POT_SVG));
      }
      row.appendChild(el("div", "gf-chat-msg gf-chat-" + who, text));
      log.appendChild(row);
      log.scrollTop = log.scrollHeight;
    }

    function renderQuickReplies() {
      quick.innerHTML = "";
      QUICK_REPLIES.forEach(function (q) {
        var b = el("button", "gf-chat-chip", q);
        b.type = "button";
        b.addEventListener("click", function () { handleQuestion(q); });
        quick.appendChild(b);
      });
    }

    function handleQuestion(text) {
      addMessage(text, "user");
      var match = bestMatch(text);
      if (match) {
        addMessage(match.a, "bot");
      } else {
        addMessage("I'm not quite sure about that one \\u2014 give the team a call or WhatsApp on " + PHONE + ", or use the quote form, and they'll help directly.", "bot");
      }
    }

    function openPanel() {
      panel.hidden = false;
      toggle.setAttribute("aria-expanded", "true");
      teaser.hidden = true;
      input.focus();
      if (!log.childNodes.length) {
        addMessage(GREETING, "bot");
        renderQuickReplies();
      }
    }

    toggle.addEventListener("click", function () {
      if (panel.hidden) {
        openPanel();
      } else {
        panel.hidden = true;
        toggle.setAttribute("aria-expanded", "false");
      }
    });

    closeBtn.addEventListener("click", function () {
      panel.hidden = true;
      toggle.setAttribute("aria-expanded", "false");
      toggle.focus();
    });

    teaserBubble.addEventListener("click", openPanel);
    teaserClose.addEventListener("click", function (e) {
      e.stopPropagation();
      teaser.hidden = true;
      try { sessionStorage.setItem("gfChatTeaserSeen", "1"); } catch (err) {}
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var val = input.value.trim();
      if (!val) return;
      input.value = "";
      handleQuestion(val);
    });

    // Basil starts the conversation: a proactive teaser bubble appears
    // shortly after page load (once per browser session), rather than
    // waiting for the visitor to click first.
    var alreadySeen = false;
    try { alreadySeen = sessionStorage.getItem("gfChatTeaserSeen") === "1"; } catch (err) {}
    if (!alreadySeen) {
      teaser.hidden = true;
      setTimeout(function () {
        if (panel.hidden) {
          teaser.hidden = false;
          try { sessionStorage.setItem("gfChatTeaserSeen", "1"); } catch (err) {}
        }
      }, 1800);
    } else {
      teaser.hidden = true;
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
"""


def build_chatbot_assets():
    kb = build_chatbot_kb()
    js = (CHATBOT_JS_TEMPLATE
          .replace("__KB_JSON__", json.dumps(kb, separators=(",", ":")))
          .replace("__STOPWORDS_JSON__", json.dumps(sorted(STOPWORDS)))
          .replace("__PHONE_JSON__", json.dumps(PHONE_DISPLAY))
          .replace("__BOT_NAME_JSON__", json.dumps(BOT_NAME))
          .replace("__POT_SVG_JSON__", json.dumps(FLOWER_POT_SVG)))
    path = os.path.join(ROOT, "assets", "chatbot.js")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(js)
    print(f"wrote assets/chatbot.js ({len(kb)} knowledge-base entries, {len(js)} bytes)")


def main():
    print(f"Loaded {len(SERVICES)} services across {len(CLUSTERS)} clusters.")
    for c in CLUSTERS:
        print(f"  {c['label']}: {len(c['slugs'])} services")
        missing = [s for s in c["slugs"] if s not in SERVICE_BY_SLUG]
        if missing:
            print(f"    !! MISSING FROM SERVICES: {missing}")
    build_chatbot_assets()
    build_service_pages()
    build_homepage()
    build_about()
    build_gallery()
    build_sector_pages()
    build_blog()
    build_redirects()
    build_sitemap()
    print("Done.")


if __name__ == "__main__":
    main()
