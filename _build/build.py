#!/usr/bin/env python3
"""Generates the static YK Property Services site into ../site."""
import json, pathlib, re
from urllib.parse import quote_plus as qp

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent  # site root = the folder above _build
SITE_URL = "https://ankushgupta29210.github.io/yk_property_services/"
ORIG = (ROOT / "original.html").read_text(encoding="utf-8")

PHONE1, PHONE1_T = "+1 (705) 500-8455", "+17055008455"
PHONE2, PHONE2_T = "+1 (647) 540-0097", "+16475400097"
EMAIL = "servicesykproperty@gmail.com"
WA = "17055008455"
WA_MSG = "https://wa.me/17055008455?text=Hi%20YK%20Property%20Services%2C%20I%27d%20like%20a%20quote."
HOURS = "Monday to Saturday, 8:00 AM – 6:00 PM"

# ---------------------------------------------------------------- CSS
css = (ROOT / "base.css").read_text(encoding="utf-8") + (ROOT / "additions.css").read_text(encoding="utf-8")
(OUT / "assets").mkdir(parents=True, exist_ok=True)
(OUT / "assets" / "styles.css").write_text("/* YK Property Services */\n" + css.replace("\n  ", "\n"), encoding="utf-8")

# ---------------------------------------------------------------- Sprite (original + new icons)
sprite_orig = re.search(r'(<svg class="sprite".*?</svg>)', ORIG, re.S).group(1)
NEW_ICONS = """
  <symbol id="i-building" viewBox="0 0 24 24"><rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2M10.5 21v-3h3v3"/></symbol>
  <symbol id="i-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/></symbol>
  <symbol id="i-calendar" viewBox="0 0 24 24"><rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/></symbol>
  <symbol id="i-check" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M8 12.3l2.7 2.7L16.2 9.5"/></symbol>
  <symbol id="i-camera" viewBox="0 0 24 24"><path d="M4 8h3l1.6-2.5h6.8L17 8h3a1 1 0 0 1 1 1v9.5a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z"/><circle cx="12" cy="13.3" r="3.6"/></symbol>
  <symbol id="i-snow" viewBox="0 0 24 24"><path d="M12 2.5v19M3.8 7.2l16.4 9.6M3.8 16.8l16.4-9.6M9.5 4.2 12 6.5l2.5-2.3M9.5 19.8 12 17.5l2.5 2.3"/></symbol>
  <symbol id="i-truck" viewBox="0 0 24 24"><path d="M2.5 6h11v10h-11zM13.5 9.5h4l3 3.5v3h-7"/><circle cx="6.5" cy="17.5" r="2"/><circle cx="17" cy="17.5" r="2"/></symbol>
  <symbol id="i-bed" viewBox="0 0 24 24"><path d="M3 19V6M3 15h18v4M21 15v-3a3 3 0 0 0-3-3h-7v6"/><circle cx="7" cy="11" r="2"/></symbol>
  <symbol id="i-clip" viewBox="0 0 24 24"><rect x="5" y="4.5" width="14" height="16.5" rx="2"/><path d="M9 4.5V3h6v1.5M8.5 10.5l1.5 1.5 3-3M8.5 16h7"/></symbol>
  <symbol id="i-doc" viewBox="0 0 24 24"><path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/></symbol>
  <symbol id="i-repeat" viewBox="0 0 24 24"><path d="M4 11V9a3 3 0 0 1 3-3h12l-3-3M20 13v2a3 3 0 0 1-3 3H5l3 3"/></symbol>
  <symbol id="i-users" viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.3"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6M16 5a3.2 3.2 0 0 1 0 6.3M18 14.3c1.8.8 3 2.7 3 5.7"/></symbol>
  <symbol id="i-bolt" viewBox="0 0 24 24"><path d="M13 2.5 4.5 13.5H12l-1 8 8.5-11H12z"/></symbol>
  <symbol id="i-upload" viewBox="0 0 24 24"><path d="M12 15V4M7.5 8.5 12 4l4.5 4.5M4 15v4a1.5 1.5 0 0 0 1.5 1.5h13A1.5 1.5 0 0 0 20 19v-4"/></symbol>
  <symbol id="i-send" viewBox="0 0 24 24"><path d="M21 3 10 14M21 3l-7 18-4-7-7-4z"/></symbol>
  <symbol id="i-plane" viewBox="0 0 24 24"><path d="M3 13.5 21 6l-4.5 13-4-4.5-3 3v-5z"/></symbol>
  <symbol id="i-thermo" viewBox="0 0 24 24"><path d="M10 14.5V5a2 2 0 0 1 4 0v9.5a4 4 0 1 1-4 0z"/><path d="M12 10v7"/></symbol>
  <symbol id="i-leaf" viewBox="0 0 24 24"><path d="M5 19c0-8 5-13 15-14-1 10-6 15-14 15"/><path d="M5 19c3-4 6-6.5 9.5-8"/></symbol>
  <symbol id="i-sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2.5v2.5M12 19v2.5M2.5 12H5M19 12h2.5M5.3 5.3l1.8 1.8M16.9 16.9l1.8 1.8M5.3 18.7l1.8-1.8M16.9 7.1l1.8-1.8"/></symbol>
"""
SPRITE = sprite_orig.replace("</svg>", NEW_ICONS + "</svg>")

def ico(name, cls="ico"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'

# ---------------------------------------------------------------- Data
S = [  # slug, name, short, colour, light?, icon, colour name
    dict(slug="painting", name="Painting & Finishing", nav="Painting", short="Interior and exterior painting, walls, ceilings, trim, doors, touch-ups and staining.", c="#1D4FB8", cname="Polar Night", icon="roller", quote="Painting & finishing"),
    dict(slug="drywall-repairs", name="Drywall & Repairs", nav="Drywall & Repairs", short="Drywall patching, wall repairs, caulking, flooring, fixtures and general handyman work.", c="#4C4466", cname="Long Night", icon="wrench", quote="Drywall & repairs"),
    dict(slug="property-maintenance", name="Property Maintenance", nav="Maintenance", short="Ongoing residential and commercial property maintenance built around your schedule.", c="#2F5D8A", cname="Great Slave", icon="clip", quote="Property maintenance"),
    dict(slug="rental-turnovers", name="Rental Turnovers", nav="Rental Turnovers", short="Complete, coordinated preparation of rental properties between tenants — the YK Rental Reset.", c="#127A62", cname="Spruce", icon="key", quote="Rental turnover / YK Rental Reset"),
    dict(slug="airbnb-hosts", name="Airbnb Host Services", nav="Airbnb Hosts", short="Guest-ready turnovers, photo reports and winter care for short-term rentals.", c="#6A4FD0", cname="Northern Lights", icon="bed", quote="Airbnb / short-term rental turnover"),
    dict(slug="cleaning", name="Cleaning Services", nav="Cleaning", short="Move-out, move-in, deep, regular and post-renovation cleaning.", c="#57CDA4", cname="Aurora", icon="spark", quote="Cleaning", lt=True),
    dict(slug="seasonal-services", name="Seasonal Services", nav="Seasonal", short="Snow clearing, seasonal property checks, yard cleanup and exterior maintenance.", c="#3E86C6", cname="Frame Lake", icon="snow", quote="Seasonal services"),
    dict(slug="commercial-services", name="Commercial Services", nav="Commercial", short="Maintenance, repairs and painting for offices, retail and commercial properties.", c="#2B3A55", cname="Old Town", icon="shop", quote="Commercial services"),
    dict(slug="junk-removal", name="Junk Removal", nav="Junk Removal", short="Property cleanouts, unwanted items and responsible turnover waste removal.", c="#B85C2C", cname="Bush Pilot", icon="truck", quote="Junk removal"),
]
BY = {s["slug"]: s for s in S}
DD = {'painting': 'Interior, exterior, cabinets &amp; staining', 'drywall-repairs': 'Patching, handyman, flooring &amp; fixtures', 'property-maintenance': 'Repairs, inspections &amp; recurring plans', 'rental-turnovers': 'YK Rental Reset between tenants', 'airbnb-hosts': 'Guest-ready turnovers &amp; photo reports', 'cleaning': 'Move-out, deep &amp; regular cleaning', 'seasonal-services': 'Snow clearing &amp; yard cleanup', 'commercial-services': 'Offices, retail &amp; buildings', 'junk-removal': 'Cleanouts &amp; haul-away'}

QUOTE_SERVICES = [s["quote"] for s in S] + ["Flooring", "Multiple services"]
PROPERTY_TYPES = ["Home", "Rental unit / apartment", "Multi-unit building", "Cabin", "Airbnb / short-term rental", "Commercial"]

PROJECTS = [
    dict(scene="paint", svc="painting", title="Interior painting refresh", text="Surface preparation and a fresh interior finish bring a well-used living space back into focus.", scope=["Patch and sand small wall damage", "Prime repaired areas", "Two coats on walls, fresh trim", "Cleanup and final check"]),
    dict(scene="maint", svc="property-maintenance", title="Entryway repairs & maintenance", text="A repaired wall, secure trim and an aligned door make an entry safer, cleaner and ready for everyday use.", scope=["Re-hang and adjust the door", "Replace loose hardware", "Patch wall damage, reset trim", "Paint touch-ups"]),
    dict(scene="turnover", svc="rental-turnovers", title="Rental unit reset", text="A coordinated transition from move-out wear to a welcoming space for the next tenant.", scope=["Walk through the vacant unit", "Patch and touch up walls", "Clean and remove leftover debris", "Check the finished space before move-in"]),
    dict(scene="clean", svc="cleaning", title="Move-out kitchen clean", text="Move-out debris, grease and surface buildup removed so the space feels fresh and move-in ready.", scope=["Degrease counters and backsplash", "Clean cabinets inside and out", "Appliances and sink", "Floors and baseboards"]),
    dict(scene="commercial", svc="commercial-services", title="Commercial reception refresh", text="Repairs, fresh paint and a clean finish renew a customer-facing workspace with minimal disruption.", scope=["After-hours scheduling", "Wall repair and feature paint", "Desk and trim touch-ups", "Detail clean before opening"]),
    dict(scene="drywall", svc="drywall-repairs", title="Damaged wall made whole", text="Holes and cracked joint compound patched, blended and repainted so the wall reads as one smooth surface.", scope=["Cut and patch holes", "Tape and fill cracks", "Blend texture and sand", "Prime and repaint"]),
    dict(scene="seasonal", svc="seasonal-services", title="Walkway & yard reset", text="Leaves, growth and debris removed so entrances and walkways are clean, safe and welcoming again.", scope=["Rake and bag leaves", "Trim and tidy shrubs", "Clear and sweep the walkway", "Haul away yard waste"]),
    dict(scene="junk", svc="junk-removal", title="Garage cleanout", text="Furniture, boxes and scrap hauled away and the space swept out, ready to actually use.", scope=["Sort items to keep, donate or dispose", "Load and haul away", "Responsible disposal", "Sweep out the space"]),
]

FAQ_HOME = [
    ("Do you work on both homes and commercial properties?", "Yes. Services are structured for homeowners, landlords, property managers and Yellowknife businesses."),
    ("Can you handle several jobs in one visit?", "Yes. Send us your complete list so we can organize painting, repairs, cleaning and maintenance together."),
    ("Do you provide estimates first?", "Yes. Every property is different, so we review the work and provide a clear written estimate before it begins. Estimates are free."),
    ("Can I send photos with my request?", "Yes. The online quote form accepts a project photo, and you can send as many as you like on WhatsApp or by email."),
    ("Do you offer recurring maintenance?", "Yes. Recurring plans can be arranged for homeowners, landlords, property managers and commercial properties."),
    ("Can you paint in winter?", "Yes. Interior painting, drywall and repairs run all year — winter is a great time for indoor work. Exterior painting and staining are booked for the warmer months."),
    ("What are your hours?", "Monday to Saturday, 8:00 AM – 6:00 PM. Closed Sundays, but you can send a quote request or email any time."),
]

# ---------------------------------------------------------------- Layout pieces
def head(title, desc, path, home=False, extra=""):
    canon = SITE_URL + ("" if path == "index.html" else path)
    boot = ("""<script>
  (function () {
    var d = document.documentElement;
    d.classList.add('js');
    if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      d.classList.add('anim-ready');
      setTimeout(function () { if (!window.__heroStarted) d.classList.remove('anim-ready'); }, 3500);
    }
  })();
</script>""" if home else "<script>document.documentElement.classList.add('js');</script>")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta property="og:site_name" content="YK Property Services">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#06132E">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230F2D66'/%3E%3Cpath d='M12 38 32 20 52 38' fill='none' stroke='white' stroke-width='6' stroke-linecap='round' stroke-linejoin='round'/%3E%3Cpath d='M48 5l1.8 5.4 5.4 1.8-5.4 1.8L48 19.4l-1.8-5.4-5.4-1.8 5.4-1.8z' fill='%234EF0B8'/%3E%3Crect x='27' y='40' width='10' height='12' rx='1' fill='white'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=Instrument+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/styles.css">
{boot}{extra}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{SPRITE}
"""

def header(active):
    def cur(slug):
        return ' aria-current="page"' if active == slug else ""
    svc_active = active in BY or active == "services"
    dd_items = "".join(
        f'<a href="{s["slug"]}.html"{cur(s["slug"])}><span class="dot" style="--c:{s["c"]}"></span><strong>{s["name"]}</strong><small>{DD[s["slug"]]}</small></a>'
        for s in S)
    mnav_svcs = "".join(f'<a href="{s["slug"]}.html">{s["nav"]}</a>' for s in S)
    return f"""
<header class="nav" id="nav">
  <div class="topbar">
    <div class="wrap topbar-inner">
      <span class="tb-msg">Local Yellowknife service · Residential &amp; commercial · Free estimates</span>
      <span class="tb-right"><span class="tb-hours">Mon–Sat 8 AM – 6 PM</span><a href="tel:{PHONE1_T}">{ico("phone")}{PHONE1}</a></span>
    </div>
  </div>
  <nav class="wrap nav-inner" aria-label="Main">
    <a class="brand" href="index.html" aria-label="YK Property Services, home">
      <svg aria-hidden="true"><use href="#mark"/></svg>
      <span>YK Property Services</span>
    </a>
    <div class="nav-links">
      <div class="dd">
        <button class="dd-btn" type="button" aria-expanded="false" aria-controls="ddMenu"{' aria-current="page"' if svc_active else ''}>Services</button>
        <div class="dd-menu" id="ddMenu">{dd_items}<a class="all" href="services.html">All services →</a></div>
      </div>
      <a href="rental-turnovers.html"{cur("rental-turnovers")}>Rental Turnovers</a>
      <a href="airbnb-hosts.html"{cur("airbnb-hosts")}>Airbnb Hosts</a>
      <a href="commercial-services.html"{cur("commercial-services")}>Commercial</a>
      <a href="projects.html"{cur("projects")}>Projects</a>
      <a href="about.html"{cur("about")}>About</a>
      <a href="contact.html"{cur("contact")}>Contact</a>
      <a class="btn btn-primary" href="get-a-quote.html">Get a free quote</a>
      <button class="menu-btn" id="menuBtn" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Open menu"><span></span></button>
    </div>
  </nav>
</header>
<div class="mnav" id="mnav">
  <a href="index.html">Home</a>
  <h4>Services</h4>
  <div class="mgrid">{mnav_svcs}</div>
  <a href="services.html" style="font-size:1rem">All services →</a>
  <h4>Company</h4>
  <a href="projects.html">Projects</a>
  <a href="about.html">About</a>
  <a href="service-areas.html">Service area</a>
  <a href="contact.html">Contact</a>
  <a class="btn btn-primary" href="get-a-quote.html">Get a free quote</a>
  <a class="btn btn-ghost" href="tel:{PHONE1_T}">{ico("phone")}Call {PHONE1}</a>
</div>
"""

def footer():
    svc_links = "".join(f'<a href="{s["slug"]}.html">{s["nav"]}</a>' for s in S)
    return f"""
<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand" href="index.html"><svg aria-hidden="true"><use href="#mark"/></svg><span>YK Property Services</span></a>
        <p>One call. Every property need. Reliable painting, repairs, cleaning and maintenance in Yellowknife, Northwest Territories.</p>
        <p class="hours">{HOURS}<br>Yellowknife and surrounding areas</p>
      </div>
      <div>
        <h4>Contact</h4>
        <p><a href="tel:{PHONE1_T}">{PHONE1}</a></p>
        <p><a href="tel:{PHONE2_T}">{PHONE2}</a></p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <p><a href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp</a></p>
        <h4 style="margin-top:1.2rem">Location</h4>
        <p>1000 Gitzel Street</p>
        <p>Yellowknife, NT X1A 2C5</p>
      </div>
      <div>
        <h4>Services</h4>
        <div class="flinks">{svc_links}</div>
      </div>
      <div>
        <h4>Company</h4>
        <div class="flinks">
          <a href="index.html">Home</a><a href="services.html">All services</a><a href="projects.html">Projects</a><a href="about.html">About</a>
          <a href="service-areas.html">Service area</a><a href="contact.html">Contact</a><a href="get-a-quote.html">Get a quote</a>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; <span class="js-year">2026</span> YK Property Services. Serving Yellowknife, Northwest Territories.</p>
      <p class="footer-legal"><a href="privacy.html">Privacy Policy</a><a href="terms.html">Terms</a></p>
      <p class="credit">Website by <a href="https://ankushguptatech.com" target="_blank" rel="noopener">Ankush Gupta Tech</a></p>
    </div>
  </div>
</footer>

<a class="fab" id="fab" href="{WA_MSG}" target="_blank" rel="noopener" aria-label="Message YK Property Services on WhatsApp">{ico("chat")}</a>

<nav class="mbar" aria-label="Quick actions">
  <a href="tel:{PHONE1_T}">{ico("phone")}Call</a>
  <a href="{WA_MSG}" target="_blank" rel="noopener">{ico("chat")}WhatsApp</a>
  <a class="q" href="get-a-quote.html">Get a quote</a>
</nav>

<button class="assist-btn" id="assistBtn" type="button" aria-expanded="false" aria-controls="assist">{ico("spark")}<span>Ask YK</span></button>
<div class="assist" id="assist" role="dialog" aria-label="YK Service Assistant">
  <div class="assist-head">
    <svg class="mk" aria-hidden="true"><use href="#mark"/></svg>
    <div><strong>YK Service Assistant</strong><small>Quick answers about our services</small></div>
    <button class="x" type="button" aria-label="Close assistant">×</button>
  </div>
  <div class="assist-log" aria-live="polite">
    <div class="msg bot intro"><h4>How can we help with your property?</h4><p>Ask about painting, repairs, cleaning, rental turnovers, seasonal work or commercial service.</p></div>
    <div class="sugg">
      <button type="button">How do rental turnovers work?</button>
      <button type="button">Can you paint in winter?</button>
      <button type="button">What can you do for landlords?</button>
      <button type="button">I need a few repairs — where do I start?</button>
    </div>
  </div>
  <form class="assist-form" id="assistForm"><input id="assistInput" autocomplete="off" placeholder="Ask about a service, a repair or a turnover…" aria-label="Your question"><button type="submit" aria-label="Send">{ico("send")}</button></form>
  <div class="assist-foot"><button type="button" id="assistClear">Clear chat</button><span>Estimates are always confirmed by our team. <a href="get-a-quote.html">Get a free quote</a></span></div>
</div>

<script src="assets/site.js" defer></script>
</body>
</html>
"""

def hero_canvas(seed=0, snow="#EEF3F9"):
    return f"""  <canvas id="aurora" aria-hidden="true"></canvas>
  <canvas id="sky" aria-hidden="true"></canvas>
  <svg class="trees far" id="treesFar" viewBox="0 0 1440 220" preserveAspectRatio="xMidYMax slice" aria-hidden="true"></svg>
  <svg class="trees near" id="treesNear" viewBox="0 0 1440 220" preserveAspectRatio="xMidYMax slice" aria-hidden="true"></svg>"""

def headline(lines, roller=False):
    label = " ".join(lines)
    out = []
    for i, ln in enumerate(lines):
        out.append(f'<span class="line" aria-hidden="true" style="--d:{i}"><span class="stroke"></span><span class="txt">{ln}</span></span>')
    return f'<h1 class="headline"{" data-roller" if roller else ""} aria-label="{label}">' + "<br>".join(out) + "</h1>"

def page_hero(eyebrow, lines, lede, crumbs=None, ctas=None, seed=3, snow="#EEF3F9"):
    crumb_html = ""
    if crumbs:
        crumb_html = '<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a>' + "".join(
            f' / <a href="{h}">{t}</a>' if h else f" / <span>{t}</span>" for t, h in crumbs) + "</nav>"
    if ctas is None:
        ctas = f'<a class="btn btn-primary" href="get-a-quote.html">Get a free estimate</a><a class="btn btn-ghost" href="tel:{PHONE1_T}">{ico("phone")}Call {PHONE1}</a>'
    return f"""
<header class="hero page-hero" id="top" data-seed="{seed}" data-snow="{snow}">
{hero_canvas()}
  <div class="wrap hero-inner" id="heroInner">
    {crumb_html}
    <p class="eyebrow">{eyebrow}</p>
    {headline(lines)}
    <p class="lede">{lede}</p>
    <div class="ctas">{ctas}</div>
  </div>
</header>
"""

def sec_head(title, text, eyebrow=None, single=False, center=False):
    cls = "sec-head reveal" + (" single" if single else "") + (" center" if center else "")
    eb = f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else ""
    if single:
        return f'<div class="{cls}"><div>{eb}<h2>{title}</h2></div><p>{text}</p></div>'
    return f'<div class="{cls}"><div>{eb}<h2>{title}</h2></div><p>{text}</p></div>'

def svc_cards(items=S):
    fans = [-5, 0, 5]
    cards = []
    for i, s in enumerate(items):
        lt = " lt" if s.get("lt") else ""
        cards.append(f"""<a class="swatch svc" href="{s["slug"]}.html" style="--i:{i}; --fan:{fans[i % 3]}deg; --c:{s["c"]}">
          <div class="svc-chip{lt}"><span class="cname">{s["cname"]}</span><span class="badge">{ico(s["icon"])}</span><span class="tints"><i></i><i></i><i></i></span></div>
          <div class="svc-body"><h3>{s["name"]}</h3><p>{s["short"]}</p><span class="link-arrow">Explore service</span></div>
        </a>""")
    return '<div class="svc-grid">' + "\n".join(cards) + "</div>"

def ba(scene, label="Before and after comparison"):
    return f"""<div class="ba" data-scene="{scene}">
            <span class="lbl b">BEFORE</span><span class="lbl a">AFTER</span>
            <input type="range" min="0" max="100" value="50" aria-label="{label}: drag to compare">
            <span class="handle"></span>
          </div>"""

BA_NOTE = '<p class="ba-note">Drag to compare. Illustration of the type of work — not a photo of a completed customer job.</p>'

def ba_card(p, scope=False, link=True):
    s = BY[p["svc"]]
    scope_html = ("<ul>" + "".join(f"<li>{x}</li>" for x in p["scope"]) + "</ul>") if scope else ""
    lnk = f'<a class="link-arrow" href="{s["slug"]}.html">{s["name"]}</a>' if link else ""
    return f"""<article class="ba-card reveal" id="{p["scene"]}">
          {ba(p["scene"], p["title"])}
          <div class="meta"><small>{s["name"]} · Illustration</small><h3>{p["title"]}</h3><p>{p["text"]}</p>{scope_html}{lnk}</div>
        </article>"""

def gallery(projects, scope=False):
    return '<div class="ba-grid">' + "\n".join(ba_card(p, scope) for p in projects) + "</div>" + '<p class="svc-note">Illustrations show the type of work we do. They are not photos of completed customer jobs.</p>'

def ba_feature(scene, title, text):
    p = next(x for x in PROJECTS if x["scene"] == scene)
    return f"""
  <section class="section alt">
    <div class="wrap ba-feature">
      <div class="ba-card reveal">{ba(scene, title)}{BA_NOTE}</div>
      <div class="text reveal">
        <p class="eyebrow">Before &amp; after</p>
        <h2>{title}</h2>
        <p>{text}</p>
        <a class="link-arrow" href="projects.html#{scene}">View project details</a>
      </div>
    </div>
  </section>"""

def reviews(cat_label, alt=False):
    stars = "".join('<svg aria-hidden="true"><use href="#star4"/></svg>' for _ in range(5))
    return f"""
  <section class="section{' alt' if alt else ''}" style="padding-block:clamp(3.5rem,7vw,5.5rem)">
    <div class="wrap">
      {sec_head("What customers say", "We only publish real, verified reviews from YK Property Services customers.", "Customer reviews")}
      <div class="reviews reveal">
        <div class="rv-score"><div class="stars">{stars}</div><strong>No verified rating yet</strong><small>Service category</small><span>{cat_label}</span></div>
        <div class="rv-list" data-reviews="{cat_label}">
          <div class="rv-empty"><strong>Verified customer reviews will appear here.</strong><span>No customer statements have been published yet. Worked with us? We'd love to hear how it went — <a href="mailto:{EMAIL}?subject=Review%20for%20YK%20Property%20Services">send us your feedback</a>.</span></div>
        </div>
      </div>
    </div>
  </section>"""

def faq(items, alt=False, title="Good to know before we begin", eyebrow="Common questions"):
    qs = "".join(f"<details><summary>{q}</summary><div><p>{a}</p></div></details>" for q, a in items)
    return f"""
  <section class="section{' alt' if alt else ''}" id="faq">
    <div class="wrap">
      {sec_head(title, "Quick answers to what people ask us most. Anything else, just call or message.", eyebrow, single=True, center=True)}
      <div class="faq reveal">{qs}</div>
    </div>
  </section>"""

def cta_band(title="One call. One dependable local team.", text="Tell us what your property needs and we’ll organize the next steps.", label="Get a free quote", href="get-a-quote.html"):
    return f"""
  <section class="section cta-band">
    <div class="wrap reveal">
      <h2>{title}</h2>
      <p>{text}</p>
      <div class="ctas"><a class="btn btn-primary" href="{href}">{label}</a><a class="btn btn-ghost" href="tel:{PHONE1_T}">{ico("phone")}Call {PHONE1}</a><a class="btn btn-ghost" href="{WA_MSG}" target="_blank" rel="noopener">{ico("chat")}WhatsApp</a></div>
    </div>
  </section>"""

def related(slugs, title="Often booked together"):
    items = [BY[s] for s in slugs]
    return f"""
  <section class="section" style="padding-top:clamp(3.5rem,7vw,5.5rem)">
    <div class="wrap">
      {sec_head(title, "One crew can take care of the whole list in one visit.", "More services")}
      {svc_cards(items)}
    </div>
  </section>"""

def checklist_section(s, title, intro, items, note=None, eyebrow="Full-service support"):
    lis = "".join(f"<li>{x}</li>" for x in items)
    lt = " lt" if s.get("lt") else ""
    note_html = f'<p class="callout">{note}</p>' if note else ""
    return f"""
  <section class="section" style="--c:{s["c"]}">
    <div class="wrap feat-wrap">
      <div class="intro reveal">
        <p class="eyebrow">{eyebrow}</p>
        <h2>{title}</h2>
        <p>{intro}</p>
        {note_html}
        <p style="margin-top:1.4rem"><a class="btn btn-primary" href="get-a-quote.html?service={qp(s["quote"])}#quote">Get a free estimate</a></p>
      </div>
      <ul class="checklist{lt} reveal">{lis}</ul>
    </div>
  </section>"""

def landlords_section():
    perks = [("bolt", "Priority scheduling"), ("doc", "Monthly invoicing"), ("repeat", "Recurring agreements"), ("key", "Coordinated turnovers"), ("camera", "Photo documentation"), ("clip", "Inspections & reports")]
    lis = "".join(f"<li>{ico(i)}{t}</li>" for i, t in perks)
    return f"""
  <section class="section landlords on-dark" id="landlords">
    <div class="wrap ll-grid">
      <div class="intro reveal">
        <p class="eyebrow">For landlords &amp; property managers</p>
        <h2>One reliable contact for your properties.</h2>
        <p>Reduce the number of contractors you coordinate. We handle turnover preparation, painting, cleaning, minor repairs, inspections, seasonal work and photo documentation.</p>
        <ul class="perks">{lis}</ul>
        <a class="btn btn-ghost" href="rental-turnovers.html">Explore rental services</a>
      </div>
      <div class="reset-card reveal">
        <span class="tag">YK Rental Reset</span>
        <h3>One call to get your rental ready.</h3>
        <p>Inspection, patching, painting, cleaning, garbage removal and a final walkthrough — between tenants, coordinated by one team.</p>
        <a class="btn" href="get-a-quote.html?service=Rental+turnover+%2F+YK+Rental+Reset#quote">Book a Rental Reset</a>
      </div>
    </div>
  </section>"""

WHY = [("One call", "Multiple property services through one company."), ("Reliable scheduling", "Clear communication and dependable appointments."),
       ("Local service", "Serving Yellowknife and the surrounding area."), ("Clear estimates", "Know what you’re paying before work starts."),
       ("Residential & commercial", "From single homes to rental and commercial properties."), ("Property manager friendly", "Built for repeat maintenance and turnover work.")]

def why_section(alt=True, title="Property care built around reliability", eyebrow="Why YK"):
    lis = "".join(f'<li><span class="num">0{i+1}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(WHY))
    return f"""
  <section class="section{' alt' if alt else ''}" id="why">
    <div class="wrap">
      {sec_head(title, "Less coordination, more confidence. The things we hold ourselves to on every job.", eyebrow)}
      <ul class="why reveal">{lis}</ul>
    </div>
  </section>"""

def seasons_section(alt=False):
    data = [("Winter", "snow", "#0F2D66", False, ["Snow clearing", "Walkway clearing", "Entrance clearing", "Property checks", "Minor winter maintenance"]),
            ("Spring &amp; Summer", "sun", "#4EF0B8", True, ["Property and yard cleanup", "Exterior painting", "Deck and fence staining", "Pressure washing", "Exterior maintenance"]),
            ("Fall", "leaf", "#B85C2C", False, ["Seasonal property preparation", "Weather stripping", "Property inspections", "Exterior cleanup", "Leaf removal"])]
    cards = "".join(f'<div class="season{" lt" if lt else ""} reveal" style="--bg:{bg}"><h3>{ico(i)}{t}</h3><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul></div>' for t, i, bg, lt, items in data)
    return f"""
  <section class="section{' alt' if alt else ''}">
    <div class="wrap">
      {sec_head("Built for Yellowknife’s seasons", "Freeze-up, deep winter, spring thaw and summer growth — the work changes with the calendar, and so do we.", "Seasonal services")}
      <div class="seasons">{cards}</div>
      <p class="svc-note"><a class="link-arrow" href="seasonal-services.html">See seasonal services</a></p>
    </div>
  </section>"""

def opt(name, value, icon=None, typ="radio"):
    ic = ico(icon) if icon else ""
    return f'<label class="opt"><input type="{typ}" name="{name}" value="{value}">' + f"<span>{ic}{value}</span></label>"

def estimator_section():
    props = [("Single-family home", "house"), ("Rental unit / apartment", "key"), ("Multi-unit building", "building"), ("Commercial space", "shop")]
    servs = [("painting", "Interior painting", "roller"), ("reset", "Full rental reset", "key"), ("repairs", "Handyman & repairs", "wrench"), ("cleaning", "Deep cleaning", "spark"), ("seasonal", "Seasonal prep", "snow"), ("junk", "Junk removal", "truck")]
    sizes = ["1 room / touch-up", "1–2 bedroom unit", "3+ bedroom home", "Commercial suite / multiple units"]
    extras = ["Drywall patching", "Door & hardware adjustment", "Move-out clean", "Debris / junk removal", "Photo documentation"]
    serv_opts = "".join(f'<label class="opt"><input type="radio" name="eServ" value="{k}"><span>{ico(i)}{t}</span></label>' for k, t, i in servs)
    return f"""
  <section class="section" id="estimator">
    <div class="wrap">
      <div class="est reveal" id="est">
        <div class="est-side on-dark">
          <p class="eyebrow">Project estimator</p>
          <h2>Plan your project in 30 seconds.</h2>
          <p>Answer three quick questions to see your project scope and typical turnaround — then send it straight to us for a clear estimate.</p>
          <ol class="est-steps" aria-hidden="true"><li>Property</li><li>Service</li><li>Size</li><li>Summary</li></ol>
        </div>
        <div class="est-main" id="estimator-ui">
          <div class="est-bar" aria-hidden="true"><i></i></div>
          <fieldset class="est-pane" style="border:0;padding:0;margin:0">
            <legend><h3>What type of property is it?</h3></legend>
            <div class="opts">{"".join(opt("eProp", t, i) for t, i in props)}</div>
            <div class="est-nav"><span class="spacer"></span><button class="btn btn-primary" type="button" data-next disabled>Next</button></div>
          </fieldset>
          <fieldset class="est-pane" style="border:0;padding:0;margin:0">
            <legend><h3>What do you need done?</h3></legend>
            <div class="opts">{serv_opts}</div>
            <div class="est-nav"><button class="btn btn-outline" type="button" data-back>Back</button><span class="spacer"></span><button class="btn btn-primary" type="button" data-next disabled>Next</button></div>
          </fieldset>
          <fieldset class="est-pane" style="border:0;padding:0;margin:0">
            <legend><h3>How big is the job?</h3></legend>
            <div class="opts">{"".join(opt("eSize", t) for t in sizes)}</div>
            <h4>Anything else? <span class="muted" style="font-weight:400">(optional)</span></h4>
            <div class="opts chk">{"".join(opt("eExtra", t, typ="checkbox") for t in extras)}</div>
            <div class="est-nav"><button class="btn btn-outline" type="button" data-back>Back</button><span class="spacer"></span><button class="btn btn-primary" type="button" data-next disabled>See my summary</button></div>
          </fieldset>
          <div class="est-pane" aria-live="polite">
            <h3>Your project scope</h3>
            <div class="scope">
              <span class="tier" id="eTier">Standard Project</span>
              <p class="what" id="eWhat"></p>
              <div class="turn">{ico("clock")}<div><small>Typical turnaround</small><strong id="eTurn"></strong></div></div>
              <ul id="eScope"></ul>
            </div>
            <p class="est-disclaim">This is a general guide, not a price. Every property is different — we’ll give you a clear written estimate before any work begins.</p>
            <div class="est-nav"><button class="btn btn-outline" type="button" data-back>Back</button><button class="btn btn-outline" type="button" data-reset>Start over</button><span class="spacer"></span><a class="btn btn-primary" id="eQuote" href="get-a-quote.html">Get my exact quote</a></div>
          </div>
        </div>
      </div>
    </div>
  </section>"""

def select(name, fid, options, label):
    o = "".join(f"<option>{x}</option>" for x in options)
    return f'<div class="field"><label for="{fid}">{label}</label><select id="{fid}" name="{name}">{o}</select></div>'

def quote_form(title="Request a free quote", sub="Send your complete list — we’ll review it and reply with a clear estimate."):
    return f"""<form class="form reveal" id="quoteForm" action="https://formsubmit.co/{EMAIL}" method="POST" enctype="multipart/form-data" novalidate>
        <h3>{title}</h3>
        <p>{sub}</p>
        <input type="hidden" name="_subject" value="New quote request — YK Property Services website">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_next" value="">
        <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
        <div class="row2">
          <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required placeholder="(867) 000-0000"></div>
        </div>
        <div class="row2">
          <div class="field"><label for="f-email">Email <span>(optional)</span></label><input id="f-email" name="email" type="email" autocomplete="email"></div>
          {select("contact_method", "f-contact", ["Phone call", "Text message", "WhatsApp", "Email"], "Preferred contact method")}
        </div>
        <div class="field"><label for="f-address">Property address <span>(or neighbourhood)</span></label><input id="f-address" name="address" autocomplete="street-address" placeholder="e.g. Range Lake, Yellowknife"></div>
        <div class="row2">
          {select("property_type", "f-prop", PROPERTY_TYPES, "Property type")}
          {select("service", "f-service", QUOTE_SERVICES, "Service required")}
        </div>
        <div class="field"><label for="f-date">Preferred service date <span>(optional)</span></label><input id="f-date" name="date" type="date"></div>
        <div class="field"><label for="f-details">Project description</label><textarea id="f-details" name="details" required placeholder="e.g. Repaint two bedrooms and a hallway, patch a few holes in the drywall, and a move-out clean."></textarea>
          <span class="hint">Need several things done? List everything. For ongoing work, mention how often or how many units.</span></div>
        <div class="field">
          <span style="font-weight:600;font-size:.92rem">Project photo <span style="font-weight:400;color:var(--granite)">(optional)</span></span>
          <label class="file-drop"><span class="ibox">{ico("upload")}</span><span><strong>Upload a photo</strong><small>JPG, PNG or WEBP · up to 5 MB. More photos? Send them on WhatsApp.</small></span><input type="file" name="attachment" accept="image/jpeg,image/png,image/webp"></label>
          <span class="file-list" id="fileList"></span>
        </div>
        <div class="form-actions">
          <button class="btn btn-primary" type="submit">{ico("send")} Get my free quote</button>
        </div>
        <p class="or">or send it yourself</p>
        <div class="form-actions">
          <button class="btn btn-outline" type="button" id="waBtn">{ico("chat")}Send on WhatsApp</button>
          <button class="btn btn-outline" type="button" id="emailBtn">{ico("mail")}Send by email</button>
        </div>
        <p class="form-error" id="formError" role="alert" aria-live="polite"></p>
        <p class="form-note">We’ll use your details only to respond to this request. See our <a href="privacy.html">privacy policy</a>.</p>
      </form>"""

def direct_list():
    return f"""<ul class="direct">
          <li><a href="https://wa.me/{WA}" target="_blank" rel="noopener">{ico("chat")}<span><small>WhatsApp</small><strong>Message us</strong></span></a></li>
          <li><a href="tel:{PHONE1_T}">{ico("phone")}<span><small>Call or text</small><strong>{PHONE1}</strong></span></a></li>
          <li><a href="tel:{PHONE2_T}">{ico("phone")}<span><small>Second line</small><strong>{PHONE2}</strong></span></a></li>
          <li><a href="mailto:{EMAIL}">{ico("mail")}<span><small>Email</small><strong>{EMAIL}</strong></span></a></li>
          <li><div>{ico("clock")}<span><small>Business hours</small><strong>Mon–Sat, 8:00 AM – 6:00 PM</strong></span></div></li>
          <li><div>{ico("pin")}<span><small>Serving</small><strong>Yellowknife and surrounding areas</strong></span></div></li>
        </ul>"""

def contact_section(title="Get a quote", intro="Tell us what you need and where. We’ll get back to you with questions or a price.", extra="", sid="contact"):
    return f"""
  <section class="section contact quote-side" id="{sid}">
    <div class="wrap contact-grid">
      <div class="intro reveal">
        <p class="eyebrow light">Free estimates</p>
        <h2>{title}</h2>
        <p>{intro}</p>
        {extra}
        {direct_list()}
      </div>
      {quote_form()}
    </div>
  </section>"""

def page(path, title, desc, active, body, home=False, extra_head=""):
    html = head(title, desc, path, home, extra_head) + header(active) + body + footer()
    (OUT / path).write_text(html, encoding="utf-8")
    return path

pages = []

# ---------------------------------------------------------------- HOME
ticker_items = ["Interior painting", "Rental turnovers", "Deep cleaning", "Drywall repair", "Snow clearing", "Airbnb turnovers", "Junk removal", "Commercial maintenance", "Flooring", "Weatherproofing"]
tick = "".join(f'<span>{t} <svg><use href="#star4"/></svg></span>' for t in ticker_items)
trust = [("pin", "Local Yellowknife service"), ("building", "Residential &amp; commercial"), ("bolt", "Fast, free estimates"), ("calendar", "Reliable scheduling")]
trust_html = "".join(f'<li><span class="ibox">{ico(i)}</span>{t}</li>' for i, t in trust)
winter_sec = re.search(r'(<section class="section winter" id="properties">.*?</section>)', ORIG, re.S).group(1)
winter_sec = winter_sec.replace("<p>We work with owners, landlords and property managers all over town.</p>",
    "<p>We work with homeowners, landlords, property managers, Airbnb hosts and businesses all over town.</p>")
process_sec = re.search(r'(<section class="section" id="process">.*?</section>)', ORIG, re.S).group(1)
process_sec = process_sec.replace("No forms to fill out and no runaround. Send a message and we'll take it from there.",
    "No runaround. Send a message or the quote form and we'll take it from there.").replace(
    "WhatsApp, call or email us. A few photos help us understand it faster.", "Use the quote form, WhatsApp, call or email. A few photos help us understand it faster.")
local_ld = {
    "@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "name": "YK Property Services",
    "description": "Painting, repairs, maintenance, cleaning, rental turnovers and seasonal property services in Yellowknife, NT.",
    "url": SITE_URL, "telephone": PHONE1_T, "email": EMAIL,
    "address": {"@type": "PostalAddress", "streetAddress": "1000 Gitzel Street", "addressLocality": "Yellowknife", "addressRegion": "NT", "postalCode": "X1A 2C5", "addressCountry": "CA"},
    "areaServed": "Yellowknife, Northwest Territories",
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "08:00", "closes": "18:00"}],
}
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ_HOME]}
ld = f'\n<script type="application/ld+json">{json.dumps(local_ld)}</script>\n<script type="application/ld+json">{json.dumps(faq_ld)}</script>'

home_body = f"""
<header class="hero" id="top">
{hero_canvas()}
  <div class="wrap hero-inner" id="heroInner">
    <h1 class="headline" data-roller aria-label="One call. Every property need.">
      <span class="line" aria-hidden="true"><span class="stroke"></span><span class="txt">One call.</span></span><br>
      <span class="line" aria-hidden="true"><span class="stroke"></span><span class="txt">Every property</span></span>
      <span class="line cont" aria-hidden="true"><span class="stroke"></span><span class="txt">need.</span></span>
    </h1>
    <p class="lede">Painting, repairs, cleaning, rental turnovers and property maintenance for homes, rentals, cabins and businesses across Yellowknife.</p>
    <div class="ctas">
      <a class="btn btn-primary" href="{WA_MSG}" target="_blank" rel="noopener">{ico("chat")}Message on WhatsApp</a>
      <a class="btn btn-ghost" href="tel:{PHONE1_T}">{ico("phone")}Call (705) 500-8455</a>
    </div>
    <p class="hero-meta"><span>Mon–Sat, 8 AM – 6 PM · Yellowknife and surrounding areas</span><a href="get-a-quote.html">Get a free quote online →</a></p>
  </div>
</header>

<div class="ticker" aria-hidden="true">
  <div class="ticker-track"><div class="ticker-group">{tick}</div><div class="ticker-group">{tick}</div></div>
</div>

<main id="main">
  <div class="trust"><div class="wrap"><ul>{trust_html}</ul></div></div>

  <section class="section" id="services">
    <div class="wrap">
      {sec_head("One company. More ways to take care of your property.", "Practical, coordinated support for homeowners, landlords, property managers, businesses and contractors. Pick one service, or send us the whole list.", "What we do")}
      {svc_cards()}
      <p class="svc-note"><a class="link-arrow" href="services.html">Explore all services</a></p>
    </div>
  </section>

  {estimator_section().replace('<section class="section" id="estimator">', '<section class="section alt" id="estimator">')}

  {winter_sec}

  {landlords_section()}

  {why_section(alt=False)}

  {process_sec.replace('class="section"', 'class="section alt"', 1)}

  <section class="section" id="projects">
    <div class="wrap">
      {sec_head("Care you can see", "Drag each slider to compare before and after. These illustrations show the type of work we help with.", "Project gallery")}
      {gallery(PROJECTS[:4])}
      <p class="svc-note"><a class="btn btn-outline" href="projects.html">See all project examples</a></p>
    </div>
  </section>

  {reviews("Painting, maintenance, rental turnovers, cleaning &amp; commercial", alt=True)}

  {faq(FAQ_HOME)}

  {contact_section(extra='<p class="callout" style="margin-top:1.4rem"><strong>Need multiple things done?</strong>Include everything in one request and we’ll organize it into as few visits as possible.</p>')}
</main>
"""
pages.append(page("index.html", "YK Property Services | Painting, Cleaning & Maintenance in Yellowknife",
    "Painting, repairs, maintenance, cleaning, rental turnovers and seasonal services in Yellowknife, NT — one reliable local team. Free estimates. Call (705) 500-8455.",
    "home", home_body, home=True, extra_head=ld))

# ---------------------------------------------------------------- SERVICES overview
pages.append(page("services.html", "Property Services Yellowknife | YK Property Services",
    "Painting, repairs, maintenance, cleaning, rental turnovers, Airbnb host services, seasonal work, commercial service and junk removal in Yellowknife.",
    "services", page_hero("YK Property Services", ["Complete property", "services in Yellowknife"],
        "From a single repair to coordinated year-round care, we make it easier to keep your home, rental or commercial property ready.",
        crumbs=[("Services", None)], seed=1) + f"""
<main id="main">
  <section class="section">
    <div class="wrap">
      {sec_head("Nine services, one crew to call", "Each service has its own page with everything included. Not sure which you need? Send us the list and we’ll sort it out.", "Our services")}
      {svc_cards()}
      <p class="svc-note">Illustrations and colours are for navigation only.</p>
    </div>
  </section>
  {estimator_section().replace('class="section"', 'class="section alt"', 1)}
  {seasons_section()}
  {cta_band()}
</main>"""))

# ---------------------------------------------------------------- Service pages
SERVICE_PAGES = {
    "painting": dict(
        title="Painters Yellowknife | Interior & Exterior Painting | YK Property Services",
        desc="Professional interior, exterior, apartment, cabinet and commercial painting in Yellowknife, NT. Careful prep, clean finishes, free estimates.",
        eyebrow="Painting &amp; finishing", lines=["Professional painting", "in Yellowknife"],
        lede="Careful preparation, clean finishes and dependable scheduling for homes, rental units, offices and commercial properties.",
        list_title="What we can take care of", list_intro="Interior painting runs year-round — winter is the perfect time to refresh rooms. Exterior painting and staining are booked for the warmer months. We use low-odour paints indoors and cover floors and furniture.",
        items=["Interior house painting", "Exterior painting", "Apartment painting", "Rental unit painting", "Commercial painting", "Office painting", "Walls and ceilings", "Doors and trim", "Baseboards", "Feature walls", "Cabinet painting &amp; refinishing", "Touch-up painting", "Staining", "Deck and fence staining", "Move-in painting", "Move-out painting", "Drywall preparation before painting", "Trim caulking and sealing"],
        scene="paint", ba_title="A clean interior painting transformation", ba_text="See how careful preparation, repairs and a crisp finish can refresh a well-used room.",
        cat="Painting &amp; finishing", related=["drywall-repairs", "rental-turnovers", "commercial-services"],
        cta=("Refresh your property — get a free painting estimate", "Tell us which rooms or surfaces, and send a few photos if you can.")),
    "drywall-repairs": dict(
        title="Drywall Repair & Handyman Services Yellowknife | YK Property Services",
        desc="Drywall patching, hole repairs, caulking, door adjustments, flooring, light fixtures and general handyman work in Yellowknife homes, rentals and commercial spaces.",
        eyebrow="Drywall &amp; repairs", lines=["Walls fixed right,", "repairs done once"],
        lede="From a single doorknob hole to a full wall after a move-out, we patch, texture, seal and repair so your property looks like the damage never happened.",
        list_title="Repairs we handle", list_intro="Send us your whole repair list — the one that builds up over winter — and we’ll group the work into as few visits as possible.",
        items=["Drywall patching", "Hole and crack repair", "Texture and finish blending", "Caulking and sealing", "Door and hardware adjustment", "Trim and baseboard repair", "Flooring: laminate, vinyl and tile", "Light fixture replacement", "Minor plumbing fixture fixes", "Weatherproofing and draft sealing", "General handyman work", "Move-out damage repairs"],
        scene="drywall", ba_title="A damaged wall made whole again", ba_text="Holes and cracked joint compound are patched, blended and repainted so the wall reads as one smooth surface.",
        cat="Drywall &amp; repairs", related=["painting", "property-maintenance", "rental-turnovers"],
        cta=("Tell us what needs fixing", "List everything, add photos, and we’ll send a clear estimate.")),
    "property-maintenance": dict(
        title="Property Maintenance & Handyman Yellowknife | YK Property Services",
        desc="Reliable home repairs, handyman work, inspections and recurring property maintenance in Yellowknife for homeowners, landlords and commercial properties.",
        eyebrow="Property maintenance", lines=["Reliable maintenance", "without the hassle"],
        lede="A practical local resource for the small repairs, inspections and ongoing work that keep a property functioning well.",
        list_title="What we can take care of", list_intro="One-off visits or a regular schedule — we keep homes, rentals, common areas and commercial spaces in shape.",
        items=["Minor home repairs", "Drywall patching", "Wall repairs", "Door adjustments", "Caulking", "Weather stripping", "Shelving installation", "Fixture installation", "Furniture assembly", "General handyman services", "Property inspections", "Preventative maintenance", "Seasonal maintenance", "Cabin opening &amp; closing", "Commercial maintenance", "Landlord maintenance", "Property manager support"],
        note="<strong>Recurring maintenance plans</strong> are available for rental portfolios, common areas and commercial properties. Choose a schedule that fits your property and priorities.",
        scene="maint", ba_title="Small repairs that restore the whole space", ba_text="A repaired wall, secure trim and an aligned door make an entry safer, cleaner and ready for everyday use.",
        cat="Property maintenance", related=["drywall-repairs", "seasonal-services", "commercial-services"],
        cta=("Take the hassle out of property maintenance", "Tell us about the property and how often you need us.")),
    "rental-turnovers": dict(
        title="Rental Turnover Yellowknife | YK Rental Reset | YK Property Services",
        desc="Coordinated rental turnover painting, repairs, cleaning, garbage removal and inspections in Yellowknife. One call to get your rental ready for the next tenant.",
        eyebrow="YK Rental Reset", lines=["Tenant moved out?", "We’ll handle the rest."],
        lede="Prepare your rental for the next tenant through one coordinated service — fewer calls, clearer scheduling and one point of contact.",
        ctas=f'<a class="btn btn-primary" href="get-a-quote.html?service=Rental+turnover+%2F+YK+Rental+Reset#quote">Book a Rental Reset</a><a class="btn btn-ghost" href="tel:{PHONE1_T}">{ico("phone")}Call {PHONE1}</a>',
        list_title="From move-out to move-in ready", list_intro="YK Rental Reset brings the essential turnover tasks together, helping landlords and property managers reduce downtime and coordination.",
        items=["Unit inspection", "Painting", "Drywall repair", "Wall patching", "Cleaning", "Garbage removal", "Minor repairs", "Door and hardware checks", "Fixture replacement", "Flooring touch-ups", "Final walkthrough", "Photo documentation"],
        list_eyebrow="One coordinated service",
        note="Ask about <strong>priority scheduling and recurring agreements</strong> for multiple units or ongoing property portfolios.",
        extra="landlords",
        scene="turnover", ba_title="From move-out wear to move-in ready", ba_text="A coordinated reset can combine patching, painting, cleanup and a final walkthrough in one clear process.",
        cat="Rental turnovers", related=["cleaning", "junk-removal", "property-maintenance"],
        cta=("Turn the unit around with one reliable team", "Send the move-out date, unit size and anything you already know needs fixing."), cta_label="Book a Rental Reset"),
    "airbnb-hosts": dict(
        title="Airbnb Cleaning & Turnover Yellowknife | YK Property Services",
        desc="Short-term rental turnover cleaning, linen changes, guest-ready checks, photo reports, repairs and winter property care for Airbnb and VRBO hosts in Yellowknife.",
        eyebrow="Airbnb &amp; short-term rental hosts", lines=["Guest-ready", "every time."],
        lede="Turnover cleaning, quick repairs and seasonal property care for Airbnb and VRBO hosts — so you can protect your reviews without coordinating multiple contractors.",
        ctas=f'<a class="btn btn-primary" href="get-a-quote.html?service=Airbnb+%2F+short-term+rental+turnover&property=Airbnb+%2F+short-term+rental#quote">Get a host quote</a><a class="btn btn-ghost" href="{WA_MSG}" target="_blank" rel="noopener">{ico("chat")}WhatsApp us</a>',
        list_title="Every stay, reset properly", list_intro="A consistent checklist after every check-out, with a photo report so you can see the unit from anywhere.",
        list_eyebrow="Turnover checklist",
        items=["Full turnover cleaning", "Bed making &amp; linen change", "Bathroom &amp; kitchen sanitizing", "Restock guest supplies (host-provided)", "Garbage &amp; recycling removal", "Damage &amp; wear check", "Photo report to host", "Minor repairs &amp; touch-ups", "Entrance &amp; walkway snow clearing", "Thermostat &amp; lighting check", "Vacant property checks", "Deep cleans between seasons"],
        extra="airbnb", scene=None, cat="Airbnb host services", related=["cleaning", "seasonal-services", "drywall-repairs"],
        cta=("Keep your listing guest-ready", "Send us your property details, booking frequency and turnover times."), cta_label="Get a host quote"),
    "cleaning": dict(
        title="Cleaning Services Yellowknife | Move-Out & Deep Cleaning | YK Property Services",
        desc="Move-out, move-in, deep, regular, turnover, office and post-renovation cleaning in Yellowknife homes, rentals and businesses.",
        eyebrow="Cleaning services", lines=["A cleaner property,", "ready for what’s next"],
        lede="Thorough, practical cleaning for homes, rentals, cabins, renovation projects and commercial spaces throughout Yellowknife.",
        list_title="What we can take care of", list_intro="One-time, seasonal or ongoing. Get your damage deposit back, hand new tenants a spotless unit, or keep the office fresh every week.",
        items=["Move-out cleaning", "Move-in cleaning", "Deep cleaning", "Rental turnover cleaning", "Regular weekly or monthly cleaning", "Spring &amp; fall seasonal cleans", "Post-construction cleaning", "Post-renovation cleaning", "Office cleaning", "Common-area cleaning", "Cabin cleaning", "Property cleanup"],
        scene="clean", ba_title="A kitchen cleaned for the next occupant", ba_text="Move-out debris, grease and surface buildup are removed so the space feels fresh and move-in ready.",
        cat="Cleaning services", related=["rental-turnovers", "airbnb-hosts", "junk-removal"],
        cta=("Tell us what needs cleaning", "Square footage or number of rooms, and the date you need it done.")),
    "seasonal-services": dict(
        title="Seasonal Property Services Yellowknife | Snow Clearing & Yard Cleanup",
        desc="Snow clearing, entrance clearing, spring and fall yard cleanup, staining, pressure washing, seasonal checks and exterior maintenance in Yellowknife.",
        eyebrow="Seasonal services", lines=["Ready for every", "northern season"],
        lede="Freeze-up, deep winter, spring thaw and summer growth — we keep Yellowknife properties clear, safe and presentable through every season.",
        list_title="Seasonal work we cover", list_intro="One-off visits or a seasonal schedule for homes, rentals, Airbnbs and commercial properties.",
        items=["Snow clearing", "Walkway and entrance clearing", "Spring property and yard cleanup", "Fall cleanup and leaf removal", "Deck and fence staining", "Pressure washing", "Seasonal property inspections", "Weather stripping and draft sealing", "Cabin opening &amp; closing", "Exterior maintenance"],
        extra="seasons", scene="seasonal", ba_title="A walkway cleared and yard reset for the season", ba_text="Leaves, growth and debris are removed so entrances and walkways are clean, safe and welcoming again.",
        cat="Seasonal services", related=["property-maintenance", "painting", "junk-removal"],
        cta=("Plan your seasonal care", "Tell us the property, the season and how often you need us.")),
    "commercial-services": dict(
        title="Commercial Painting & Property Services Yellowknife | YK Property Services",
        desc="Commercial painting, repairs, cleaning and maintenance for Yellowknife offices, retail, restaurants, warehouses and apartment buildings. Service contracts and monthly invoicing.",
        eyebrow="Commercial services", lines=["Property services for", "Yellowknife businesses"],
        lede="Flexible maintenance and improvement support for retail stores, offices, restaurants, warehouses, apartment buildings, commercial landlords and property managers.",
        list_title="What we can take care of", list_intro="We schedule around your hours — after-hours and weekend work can be arranged to keep disruption low.",
        items=["Commercial painting", "Office painting", "Repairs", "Property maintenance", "Cleaning", "Turnover work", "Common-area maintenance", "Scheduled service contracts", "Emergency minor repairs", "Contractor support"],
        note="<strong>Recurring service agreements</strong> can simplify scheduling, documentation and monthly invoicing across one property or an entire portfolio.",
        scene="commercial", ba_title="A more professional first impression", ba_text="Repairs, fresh paint and a clean finish can renew a customer-facing workspace with minimal disruption.",
        cat="Commercial services", related=["painting", "property-maintenance", "cleaning"],
        cta=("Request a commercial service quote", "Tell us about the property, the work and your preferred schedule.")),
    "junk-removal": dict(
        title="Junk Removal Yellowknife | Property Cleanouts | YK Property Services",
        desc="Full property cleanouts, furniture and appliance removal, garage and basement clearouts, renovation debris and rental turnover waste removal in Yellowknife.",
        eyebrow="Junk removal", lines=["Clutter gone,", "space back"],
        lede="Move-outs, estates, renovations and years of stored-up stuff — we clear it out, haul it away and dispose of it responsibly so the space is usable again.",
        list_title="What we haul away", list_intro="Send a few photos of what needs to go and we’ll give you a clear price before we load anything.",
        items=["Full property cleanouts", "Furniture and appliance removal", "Garage and basement clearouts", "Rental turnover waste removal", "Renovation debris haul-away", "Estate and move-out clearing", "Single-item pickup", "Responsible disposal and donation sorting", "Loading and cleanup included"],
        scene="junk", ba_title="A packed garage cleared to a clean floor", ba_text="Furniture, boxes and scrap are hauled away and the space is swept out, ready to actually use.",
        cat="Junk removal", related=["cleaning", "rental-turnovers", "seasonal-services"],
        cta=("Get junk hauled away", "Photos of the pile are the fastest way to a price.")),
}

def airbnb_extra():
    feats = [("bolt", "Same-day turnovers", "Check-out to check-in cleaning so your listing stays guest-ready between bookings."),
             ("camera", "Photo reports", "Photos after each turnover so you can see the unit’s condition from anywhere."),
             ("wrench", "Fast fixes", "Minor repairs, touch-up painting and hardware fixes before small issues show up in reviews."),
             ("snow", "Winter-ready access", "Walkway and entrance clearing so aurora-season guests arrive safely."),
             ("plane", "Out-of-town owners", "Local hands on the ground for hosts who don’t live in Yellowknife."),
             ("thermo", "Vacant-period checks", "Property checks between bookings during the coldest months of the year.")]
    cards = "".join(f'<div class="card reveal"><span class="ibox">{ico(i)}</span><h3>{t}</h3><p>{d}</p></div>' for i, t, d in feats)
    plans = [("Per-turnover service", "Book cleaning and resets as your guests check out. Ideal for occasional bookings or trying us out."),
             ("Recurring host agreement", "Ongoing turnovers, seasonal care and repairs with one point of contact. Pricing is quoted per property.")]
    plan_cards = "".join(f'<div class="card reveal"><span class="ibox">{ico("repeat" if k else "calendar")}</span><h3>{t}</h3><p>{d}</p></div>' for k, (t, d) in enumerate(plans))
    host_faq = [("Can you handle same-day turnovers?", "Tell us your check-out and check-in times when you request a quote and we’ll confirm what scheduling works for your property."),
                ("Do I need to be in Yellowknife?", "No. Photo reports after each visit help out-of-town hosts see the condition of their unit."),
                ("Do you supply linens and guest supplies?", "We can change linens and restock items you provide. Mention your setup in the quote form."),
                ("Can you help in winter?", "Yes. Snow clearing at entrances and walkways and property checks are available for short-term rentals.")]
    return f"""
  <section class="section alt">
    <div class="wrap">
      {sec_head("What busy hosts need from a local team", "Aurora season and summer travel mean frequent turnovers and high guest expectations. We help keep your property ready.", "Built for hosts")}
      <div class="cards">{cards}</div>
    </div>
  </section>""", f"""
  <section class="section" style="padding-top:0">
    <div class="wrap">
      {sec_head("Two ways to work with us", "Start with a single turnover or set up an ongoing agreement.", "Host plans")}
      <div class="cards two">{plan_cards}</div>
    </div>
  </section>
  {faq(host_faq, alt=True, title="Good to know", eyebrow="Host questions")}"""

for slug, d in SERVICE_PAGES.items():
    s = BY[slug]
    hero = page_hero(d["eyebrow"], d["lines"], d["lede"], crumbs=[("Services", "services.html"), (s["name"], None)], ctas=d.get("ctas"), seed=S.index(s) + 2, snow="#FFFFFF" if d.get("extra") == "airbnb" else "#EEF3F9")
    pre, post = "", ""
    if d.get("extra") == "airbnb":
        pre, post = airbnb_extra()
    body = pre + checklist_section(s, d["list_title"], d["list_intro"], d["items"], d.get("note"), d.get("list_eyebrow", "Full-service support"))
    if d.get("extra") == "landlords":
        body += landlords_section()
    if d.get("extra") == "seasons":
        body += seasons_section(alt=True).replace('<p class="svc-note"><a class="link-arrow" href="seasonal-services.html">See seasonal services</a></p>', "")
    body += post
    if d.get("scene"):
        body += ba_feature(d["scene"], d["ba_title"], d["ba_text"])
    body += reviews(d["cat"], alt=not d.get("scene"))
    body += related(d["related"])
    body += cta_band(d["cta"][0], d["cta"][1], d.get("cta_label", "Get a free quote"), f'get-a-quote.html?service={qp(s["quote"])}#quote')
    pages.append(page(f"{slug}.html", d["title"], d["desc"], slug, hero + '\n<main id="main">' + body + "\n</main>"))

# ---------------------------------------------------------------- PROJECTS
pages.append(page("projects.html", "Project Examples | Before & After | YK Property Services Yellowknife",
    "Before-and-after examples of painting, repairs, rental turnovers, cleaning, commercial, seasonal and junk removal work by YK Property Services in Yellowknife.",
    "projects", page_hero("Project gallery", ["Before &amp; after,", "at a glance"],
        "Explore what a thoughtful property refresh can look like across our services. Drag each slider to compare.",
        crumbs=[("Projects", None)], seed=12) + f"""
<main id="main">
  <section class="section">
    <div class="wrap">
      {sec_head("What this kind of work includes", "Each example lists the typical scope. These are illustrations of the work, not documented customer jobs — real project photos will be added as jobs are completed.", "Illustrative examples")}
      {gallery(PROJECTS, scope=True)}
    </div>
  </section>
  {reviews("All services", alt=True)}
  {cta_band("Have a project like this?", "Send us photos and a description and we’ll send a clear estimate.")}
</main>"""))

# ---------------------------------------------------------------- ABOUT
pages.append(page("about.html", "About YK Property Services | Yellowknife, NT",
    "YK Property Services gives Yellowknife property owners one dependable point of contact for painting, repairs, cleaning and maintenance.",
    "about", page_hero("About us", ["Property care built", "for Yellowknife"],
        "YK Property Services was created to make maintaining a property easier — with one dependable point of contact for painting, repairs, cleaning and maintenance.",
        crumbs=[("About", None)], seed=13) + f"""
<main id="main">
  <section class="section">
    <div class="wrap feat-wrap">
      <div class="intro reveal">
        <p class="eyebrow">Our approach</p>
        <h2>Less coordination. More confidence.</h2>
      </div>
      <div class="prose reveal" style="margin:0">
        <p>Instead of calling multiple contractors for painting, repairs, cleaning and maintenance, YK Property Services gives Yellowknife property owners one dependable point of contact.</p>
        <p>We’re building a service company around reliable communication, professional workmanship, clear estimates, respect for customers’ properties and flexible scheduling.</p>
        <p>Our services support individual homeowners as well as landlords, property managers, Airbnb hosts, cabin owners, small businesses, commercial properties and contractors.</p>
        <p>And we know the North: when it’s minus thirty and dark by four, it’s the right time for indoor work — and when the snow melts, there’s a yard to reset.</p>
      </div>
    </div>
  </section>
  {why_section(alt=True, title="Built to be the team you call again", eyebrow="Why choose YK")}
  {process_sec}
  {cta_band()}
</main>"""))

# ---------------------------------------------------------------- CONTACT
tiles = f"""<div class="tiles">
        <div class="tile reveal"><span class="ibox">{ico("phone")}</span><h3>Phone</h3><p><a href="tel:{PHONE1_T}">{PHONE1}</a></p><p><a href="tel:{PHONE2_T}">{PHONE2}</a></p><small>Fastest way to reach the team during business hours. Call or text.</small></div>
        <div class="tile reveal"><span class="ibox">{ico("mail")}</span><h3>Email</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a></p><small>Send project details, photos and timelines any time.</small></div>
        <div class="tile reveal"><span class="ibox">{ico("clock")}</span><h3>Business hours</h3><p><strong>Monday to Saturday</strong></p><p>8:00 AM – 6:00 PM</p><small>Closed on Sundays. Message or email any time.</small></div>
        <div class="tile reveal"><span class="ibox">{ico("pin")}</span><h3>Service area</h3><p><strong>Yellowknife and surrounding areas</strong></p><small>Send your property location and we’ll confirm availability. <a href="service-areas.html">More →</a></small></div>
      </div>"""
pages.append(page("contact.html", "Contact YK Property Services | Yellowknife",
    "Call +1 (705) 500-8455, WhatsApp or email servicesykproperty@gmail.com. Monday to Saturday, 8 AM – 6 PM. Serving Yellowknife and surrounding areas.",
    "contact", page_hero("Contact", ["Let’s talk about", "your property"],
        "Call, message, email or send a quote request. Need multiple things done? Send us your list and we’ll help organize the job.",
        crumbs=[("Contact", None)], seed=14,
        ctas=f'<a class="btn btn-primary" href="tel:{PHONE1_T}">{ico("phone")}Call {PHONE1}</a><a class="btn btn-ghost" href="{WA_MSG}" target="_blank" rel="noopener">{ico("chat")}WhatsApp</a><a class="btn btn-ghost" href="get-a-quote.html">Get a free quote</a>') + f"""
<main id="main">
  <section class="section">
    <div class="wrap">{tiles}</div>
  </section>
  {contact_section("Send us a message", "Use the form, or reach us directly. We reply during business hours.", sid="quote")}
</main>"""))

# ---------------------------------------------------------------- GET A QUOTE
side = """<p class="callout" style="margin-top:1.4rem"><strong>Send your complete list.</strong>Need multiple things done? Include everything in your description. Photos help us understand the condition and scope before following up.</p>
        <p class="callout"><strong>Looking for ongoing support?</strong>Mention recurring maintenance, rental turnover frequency or the number of commercial properties in your request.</p>"""
pages.append(page("get-a-quote.html", "Free Property Service Quote | YK Property Services Yellowknife",
    "Request a free estimate for painting, repairs, maintenance, cleaning, rental turnovers, seasonal work or junk removal in Yellowknife. Upload a photo with your request.",
    "quote", page_hero("Free estimate", ["Tell us what your", "property needs"],
        "Every property is different. Share the details and we’ll provide a clear estimate before work begins.",
        crumbs=[("Get a quote", None)], seed=15, snow="#061430",
        ctas=f'<a class="btn btn-primary" href="#quote">Start your request</a><a class="btn btn-ghost" href="tel:{PHONE1_T}">{ico("phone")}Call {PHONE1}</a>') + f"""
<main id="main">
  {contact_section("A better estimate starts here", "Fill in the form and it goes straight to our team. Prefer to message? Use WhatsApp or email below the form.", side, sid="quote")}
  <section class="section" style="padding-block:clamp(3.5rem,7vw,5rem)">
    <div class="wrap">
      {sec_head("Not sure what you need yet?", "Use the project estimator to see the scope and typical turnaround, then send it to us.", "Project estimator")}
      <p><a class="btn btn-outline" href="index.html#estimator">Open the estimator</a></p>
    </div>
  </section>
</main>"""))

# ---------------------------------------------------------------- SERVICE AREA
pages.append(page("service-areas.html", "Service Area | Property Services Yellowknife, NT | YK Property Services",
    "YK Property Services serves Yellowknife and surrounding areas — homes, rentals, multi-unit buildings and commercial properties. Monday to Saturday, 8 AM – 6 PM.",
    "areas", page_hero("Service area", ["Local property services", "in Yellowknife"],
        "We serve Yellowknife and surrounding areas, and understand the scheduling, seasonal and property-care needs of the North.",
        crumbs=[("Service area", None)], seed=16) + f"""
<main id="main">
  <section class="section">
    <div class="wrap feat-wrap">
      <div class="intro reveal">
        <p class="eyebrow">Where we work</p>
        <h2>Yellowknife and surrounding areas</h2>
        <p>Homes, rentals, cabins, multi-unit buildings and commercial properties across Yellowknife, plus nearby communities around the city. Send your property location and project details and the team will confirm availability.</p>
        <p style="margin-top:1.4rem"><a class="btn btn-primary" href="get-a-quote.html">Check service availability</a></p>
      </div>
      <div class="tiles" style="grid-template-columns:1fr 1fr">
        <div class="tile reveal"><span class="ibox">{ico("clock")}</span><h3>Business hours</h3><p>{HOURS}</p><small>Closed Sundays.</small></div>
        <div class="tile reveal"><span class="ibox">{ico("phone")}</span><h3>Call us</h3><p><a href="tel:{PHONE1_T}">{PHONE1}</a></p><p><a href="tel:{PHONE2_T}">{PHONE2}</a></p><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
      </div>
    </div>
  </section>
  {seasons_section(alt=True)}
  {cta_band()}
</main>"""))

# ---------------------------------------------------------------- PRIVACY / TERMS / THANKS / 404
def simple(path, title, desc, eyebrow, lines, lede, prose, active="legal", ctas=""):
    pages.append(page(path, title, desc, active, page_hero(eyebrow, lines, lede, crumbs=[(eyebrow, None)], seed=17, ctas=ctas) +
        f'\n<main id="main"><section class="section"><div class="wrap"><div class="prose reveal">{prose}</div></div></section></main>'))

simple("privacy.html", "Privacy Policy | YK Property Services", "How information submitted through the YK Property Services website is handled.",
    "Privacy Policy", ["Privacy policy"], "How information submitted through this website is handled.", f"""
      <p>Information you provide through a quote or contact request is used only to assess your project and respond to your inquiry.</p>
      <p>Submitted details may include your name, contact information, property address, project description and any photo you choose to share.</p>
      <p>Quote requests submitted through the online form are delivered to our team by email using the FormSubmit service. If you choose “Send on WhatsApp” or “Send by email”, your message is sent through that app instead. We do not sell or share your information for marketing.</p>
      <p>The YK Service Assistant on this site answers from a fixed list of answers in your browser. It does not store or send what you type.</p>
      <p>To ask about, correct or delete information you submitted, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>""")
simple("terms.html", "Website Terms | YK Property Services", "General information about estimates and use of the YK Property Services website.",
    "Terms", ["Website terms"], "General information about estimates and use of this website.", f"""
      <p>Website content is provided for general information. Service availability, scope, scheduling and pricing are confirmed through a written estimate or service agreement.</p>
      <p>Submitting a quote request does not create a contract or guarantee scheduling. Final terms will be supplied with an accepted estimate.</p>
      <p>Turnaround times shown by the project estimator are general guides, not quotes or guarantees.</p>
      <p>Before-and-after images on this website are illustrations unless stated otherwise. Questions about these terms can be sent to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>""")
simple("thanks.html", "Thanks — Request Received | YK Property Services", "Your quote request has been sent to YK Property Services.",
    "Request received", ["Thanks — we’ve got it."], "Your request is on its way to our team. We’ll follow up during business hours, Monday to Saturday, 8 AM – 6 PM.", f"""
      <h2>What happens next</h2>
      <ul><li>We review your details and any photo you sent.</li><li>We contact you by your preferred method with questions or a written estimate.</li><li>Once you approve, we book a convenient service date.</li></ul>
      <p>Need it sooner? Call <a href="tel:{PHONE1_T}">{PHONE1}</a> or <a href="{WA_MSG}" target="_blank" rel="noopener">message us on WhatsApp</a>.</p>""",
    ctas='<a class="btn btn-primary" href="index.html">Back to home</a>')
simple("404.html", "Page not found | YK Property Services", "This page could not be found.",
    "Page not found", ["This page took", "a wrong turn."], "The page you were looking for isn’t here. Try one of these instead.", """
      <ul><li><a href="index.html">Home</a></li><li><a href="services.html">All services</a></li><li><a href="get-a-quote.html">Get a free quote</a></li><li><a href="contact.html">Contact</a></li></ul>""",
    ctas='<a class="btn btn-primary" href="index.html">Go to home</a>')

# ---------------------------------------------------------------- sitemap / robots
urls = [p for p in pages if p not in ("thanks.html", "404.html")]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{SITE_URL}{'' if p == 'index.html' else p}</loc></url>\n" for p in urls) + "</urlset>\n"
(OUT / "sitemap.xml").write_text(sm, encoding="utf-8")
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8")
print(len(pages), "pages:", ", ".join(pages))
