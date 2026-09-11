import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import html
import base64

# ============================================================
# DACRE ANALYSIS
# Premium Landing Page
# Parent Company: Dacre Global Limited (DGL)
# ============================================================

# ============================================================
# LOGO PATH RESOLUTION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

LOGO_CANDIDATES = [
    "dacre_logo.png",
    "dacre_logo.jpg",
    "dacre_logo.jpeg",
    "DACRE.png",
    "logo.png",
    "assets/dacre_logo.png",
    "assets/logo.png",
]

LOGO_PATH = None
for candidate in LOGO_CANDIDATES:
    candidate_path = BASE_DIR / candidate
    if candidate_path.exists():
        LOGO_PATH = candidate_path
        break

# Fallback if no logo file exists yet
LOGO_EXISTS = LOGO_PATH is not None

def _logo_data_uri():
    """Return the DACRE logo as a data URI for embedding in HTML."""
    if not LOGO_EXISTS:
        return ""
    try:
        raw = LOGO_PATH.read_bytes()
        suffix = LOGO_PATH.suffix.lower()
        mime = "image/png"
        if suffix in (".jpg", ".jpeg"):
            mime = "image/jpeg"
        elif suffix == ".webp":
            mime = "image/webp"
        elif suffix == ".svg":
            mime = "image/svg+xml"
        encoded = base64.b64encode(raw).decode("ascii")
        return f"data:{mime};base64,{encoded}"
    except Exception:
        return ""

LOGO_DATA_URI = _logo_data_uri()


# ============================================================
# PAGE CONFIG — uses the DGL logo as the favicon
# ============================================================

if LOGO_EXISTS:
    # Use the actual logo file as the page icon (favicon)
    st.set_page_config(
        page_title="DACRE Analysis | Turn Your Data Into Decisions",
        page_icon=str(LOGO_PATH),
        layout="wide",
        initial_sidebar_state="collapsed",
    )
else:
    # Graceful fallback if the logo file is not yet present
    st.set_page_config(
        page_title="DACRE Analysis | Turn Your Data Into Decisions",
        page_icon="◆",
        layout="wide",
        initial_sidebar_state="collapsed",
    )


# ============================================================
# BRAND CONFIG
# ============================================================

COMPANY_NAME = "DACRE GLOBAL LIMITED"
PRODUCT_NAME = "DACRE ANALYSIS"

BLUE = "#0B2D5C"
DARK_BLUE = "#07111F"
GOLD = "#D4AF37"
SILVER = "#C7CED8"
WHITE = "#FFFFFF"
BLACK = "#030712"

# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root {{
    --dgl-blue: {BLUE};
    --dgl-dark: {DARK_BLUE};
    --dgl-gold: {GOLD};
    --dgl-silver: {SILVER};
    --dgl-white: {WHITE};
    --dgl-black: {BLACK};
}}

* {{
    box-sizing: border-box;
}}

html {{
    scroll-behavior: smooth;
}}

body {{
    margin: 0;
    background:
        radial-gradient(
            circle at 80% 10%,
            rgba(11,45,92,.32),
            transparent 30%
        ),
        linear-gradient(
            180deg,
            #030712 0%,
            #07111F 45%,
            #030712 100%
        );
    color: white;
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background:
        radial-gradient(
            circle at 15% 15%,
            rgba(11,45,92,.20),
            transparent 25%
        ),
        linear-gradient(
            180deg,
            #030712 0%,
            #07111F 100%
        );
}}

header {{
    visibility: hidden;
}}

.block-container {{
    max-width: 1400px;
    padding-top: 0.5rem;
    padding-bottom: 4rem;
}}

section[data-testid="stSidebar"] {{
    display: none;
}}

button {{
    font-family: 'Inter', sans-serif !important;
}}

a {{
    text-decoration: none !important;
}}

::selection {{
    background: rgba(212,175,55,.35);
    color: white;
}}

/* =========================================================
   NAVIGATION
   ========================================================= */

.dgl-nav {{
    position: sticky;
    top: 0;
    z-index: 999;
    width: 100%;
    padding: 18px 4vw;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(3,7,18,.82);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(199,206,216,.10);
}}

.dgl-brand {{
    display: flex;
    align-items: center;
    gap: 12px;
}}

.dgl-symbol {{
    width: 42px;
    height: 42px;
    border-radius: 12px;
    display: grid;
    place-items: center;
    background:
        linear-gradient(
            135deg,
            {BLUE},
            #174C91
        );
    border: 1px solid rgba(212,175,55,.65);
    box-shadow:
        0 0 25px rgba(11,45,92,.35);
    color: {GOLD};
    font-weight: 900;
    font-size: 18px;
    overflow: hidden;
}}

/* NEW — Logo image inside the brand mark */
.dgl-symbol-logo {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 12px;
    display: block;
}}

.dgl-brand-name {{
    display: flex;
    flex-direction: column;
    line-height: 1.05;
}}

.dgl-brand-main {{
    font-size: 15px;
    font-weight: 900;
    letter-spacing: 2px;
}}

.dgl-brand-sub {{
    font-size: 8px;
    color: {SILVER};
    letter-spacing: 2px;
    margin-top: 4px;
}}

.dgl-nav-links {{
    display: flex;
    gap: 32px;
    align-items: center;
}}

.dgl-nav-links a {{
    color: #B9C3D1 !important;
    font-size: 13px;
    font-weight: 600;
    transition: .2s ease;
}}

.dgl-nav-links a:hover {{
    color: white !important;
}}

.nav-actions {{
    display: flex;
    gap: 10px;
    align-items: center;
}}

.nav-login {{
    color: #CBD5E1 !important;
    font-size: 13px;
    font-weight: 700;
    padding: 11px 15px;
}}

.nav-start {{
    color: #07111F !important;
    background: linear-gradient(
        135deg,
        {GOLD},
        #F3D77A
    );
    padding: 11px 18px;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 900;
    box-shadow: 0 8px 25px rgba(212,175,55,.18);
}}

@media(max-width: 850px) {{
    .dgl-nav-links {{
        display: none;
    }}

    .nav-login {{
        display: none;
    }}

    .dgl-nav {{
        padding: 14px 18px;
    }}
}}

/* =========================================================
   HERO
   ========================================================= */

.hero {{
    min-height: 730px;
    padding: 110px 4vw 70px;
    position: relative;
    overflow: hidden;
}}

.hero::before {{
    content: "";
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(
            rgba(255,255,255,.025) 1px,
            transparent 1px
        ),
        linear-gradient(
            90deg,
            rgba(255,255,255,.025) 1px,
            transparent 1px
        );
    background-size: 55px 55px;
    mask-image: linear-gradient(
        to bottom,
        black,
        transparent 90%
    );
    pointer-events: none;
}}

.hero-grid {{
    max-width: 1240px;
    margin: auto;
    position: relative;
    z-index: 2;
    display: grid;
    grid-template-columns: 1fr .95fr;
    gap: 70px;
    align-items: center;
}}

.eyebrow {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: {GOLD};
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin-bottom: 20px;
}}

.eyebrow::before {{
    content: "";
    width: 28px;
    height: 1px;
    background: {GOLD};
}}

.hero-title {{
    font-size: clamp(52px, 7vw, 104px);
    line-height: .92;
    letter-spacing: -5px;
    font-weight: 900;
    margin: 0;
    max-width: 850px;
}}

.hero-title .gold {{
    color: {GOLD};
}}

.hero-title .blue {{
    color: #6EA8FF;
}}

.hero-tagline {{
    margin-top: 28px;
    font-size: clamp(22px, 3vw, 34px);
    font-weight: 700;
    color: #E5E7EB;
}}

.hero-description {{
    margin-top: 18px;
    max-width: 650px;
    color: #94A3B8;
    font-size: 16px;
    line-height: 1.8;
}}

.hero-actions {{
    display: flex;
    gap: 14px;
    flex-wrap: wrap;
    margin-top: 34px;
}}

.hero-btn {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 15px 22px;
    border-radius: 11px;
    font-weight: 800;
    font-size: 14px;
}}

.hero-primary {{
    background: linear-gradient(
        135deg,
        {GOLD},
        #F0D36A
    );
    color: #06101D !important;
    box-shadow: 0 15px 40px rgba(212,175,55,.18);
}}

.hero-secondary {{
    border: 1px solid rgba(199,206,216,.22);
    color: white !important;
    background: rgba(255,255,255,.03);
}}

.hero-note {{
    margin-top: 22px;
    color: #64748B;
    font-size: 11px;
}}

@media(max-width: 950px) {{
    .hero {{
        padding-top: 70px;
    }}

    .hero-grid {{
        grid-template-columns: 1fr;
        gap: 45px;
    }}

    .hero-title {{
        letter-spacing: -3px;
    }}
}}

/* =========================================================
   DASHBOARD MOCKUP
   ========================================================= */

.dashboard-shell {{
    position: relative;
    padding: 10px;
    border-radius: 22px;
    background:
        linear-gradient(
            135deg,
            rgba(212,175,55,.55),
            rgba(11,45,92,.7),
            rgba(199,206,216,.2)
        );
    box-shadow:
        0 35px 90px rgba(0,0,0,.55);
}}

.dashboard {{
    background: #08111E;
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,.08);
}}

.dashboard-top {{
    height: 42px;
    display: flex;
    align-items: center;
    gap: 7px;
    padding: 0 15px;
    border-bottom: 1px solid rgba(255,255,255,.07);
}}

.dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #64748B;
}}

.dashboard-body {{
    display: grid;
    grid-template-columns: 130px 1fr;
    min-height: 405px;
}}

.dashboard-side {{
    border-right: 1px solid rgba(255,255,255,.07);
    padding: 18px 12px;
}}

.side-logo {{
    color: {GOLD};
    font-size: 11px;
    font-weight: 900;
    letter-spacing: 1.5px;
    margin-bottom: 22px;
}}

.side-item {{
    padding: 9px;
    margin-bottom: 6px;
    border-radius: 7px;
    color: #64748B;
    font-size: 9px;
}}

.side-item.active {{
    background: rgba(11,45,92,.55);
    color: white;
}}

.dashboard-main {{
    padding: 18px;
}}

.dash-heading {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.dash-heading h3 {{
    margin: 0;
    font-size: 17px;
}}

.dash-heading span {{
    font-size: 8px;
    color: #64748B;
}}

.metric-grid {{
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 9px;
    margin-top: 14px;
}}

.metric {{
    background: rgba(255,255,255,.035);
    border: 1px solid rgba(255,255,255,.07);
    padding: 12px;
    border-radius: 9px;
}}

.metric-label {{
    color: #64748B;
    font-size: 8px;
}}

.metric-value {{
    margin-top: 5px;
    font-size: 16px;
    font-weight: 800;
}}

.metric-change {{
    color: #60A5FA;
    font-size: 8px;
    margin-top: 4px;
}}

.chart-area {{
    margin-top: 12px;
    height: 150px;
    padding: 12px;
    border-radius: 10px;
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(255,255,255,.06);
    position: relative;
    overflow: hidden;
}}

.chart-line {{
    position: absolute;
    left: 10%;
    right: 7%;
    bottom: 30px;
    height: 80px;
}}

.chart-line svg {{
    width: 100%;
    height: 100%;
}}

.chart-label {{
    position: absolute;
    top: 10px;
    left: 12px;
    color: #94A3B8;
    font-size: 8px;
}}

.bottom-grid {{
    display: grid;
    grid-template-columns: 1fr .6fr;
    gap: 10px;
    margin-top: 10px;
}}

.mini-panel {{
    height: 95px;
    border-radius: 10px;
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(255,255,255,.06);
    padding: 11px;
}}

.bar {{
    height: 6px;
    border-radius: 5px;
    background: #16365F;
    margin-top: 12px;
    overflow: hidden;
}}

.bar span {{
    display: block;
    height: 100%;
    background: linear-gradient(
        90deg,
        {BLUE},
        #6EA8FF
    );
}}

@media(max-width:600px) {{
    .dashboard-body {{
        grid-template-columns: 80px 1fr;
    }}

    .dashboard-side {{
        padding: 12px 7px;
    }}

    .metric-grid {{
        grid-template-columns: 1fr;
    }}
}}

/* =========================================================
   TRUST
   ========================================================= */

.trust {{
    max-width: 1150px;
    margin: 0 auto;
    padding: 35px 4vw 80px;
    text-align: center;
}}

.trust-label {{
    color: #64748B;
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
}}

.trust-row {{
    margin-top: 25px;
    display: flex;
    justify-content: center;
    gap: 45px;
    flex-wrap: wrap;
}}

.trust-item {{
    color: #94A3B8;
    font-weight: 800;
    font-size: 12px;
    letter-spacing: 1px;
}}

/* =========================================================
   SECTION
   ========================================================= */

.section {{
    max-width: 1200px;
    margin: auto;
    padding: 100px 4vw;
}}

.section-kicker {{
    color: {GOLD};
    font-size: 10px;
    letter-spacing: 2.5px;
    font-weight: 900;
    text-transform: uppercase;
}}

.section-title {{
    font-size: clamp(34px, 5vw, 58px);
    line-height: 1;
    letter-spacing: -2px;
    margin: 14px 0;
    font-weight: 900;
}}

.section-description {{
    max-width: 680px;
    color: #94A3B8;
    line-height: 1.8;
    font-size: 15px;
}}

/* =========================================================
   CAPABILITIES
   ========================================================= */

.capability-grid {{
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 15px;
    margin-top: 50px;
}}

.capability {{
    min-height: 235px;
    padding: 25px;
    border-radius: 17px;
    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,.045),
            rgba(255,255,255,.015)
        );
    border: 1px solid rgba(199,206,216,.10);
    transition: .25s ease;
}}

.capability:hover {{
    transform: translateY(-5px);
    border-color: rgba(212,175,55,.45);
    box-shadow: 0 25px 50px rgba(0,0,0,.25);
}}

.capability-number {{
    color: {GOLD};
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
}}

.capability h3 {{
    margin-top: 28px;
    font-size: 21px;
}}

.capability p {{
    color: #7E8CA0;
    line-height: 1.7;
    font-size: 13px;
}}

@media(max-width:800px) {{
    .capability-grid {{
        grid-template-columns: 1fr;
    }}
}}

/* =========================================================
   WORKFLOW
   ========================================================= */

.workflow {{
    margin-top: 55px;
    display: grid;
    grid-template-columns: repeat(5,1fr);
    gap: 10px;
}}

.workflow-step {{
    position: relative;
    padding: 20px;
    min-height: 160px;
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 14px;
    background: rgba(255,255,255,.025);
}}

.workflow-step .number {{
    color: {GOLD};
    font-family: 'JetBrains Mono';
    font-size: 11px;
}}

.workflow-step h4 {{
    margin-top: 25px;
    margin-bottom: 8px;
}}

.workflow-step p {{
    color: #718096;
    font-size: 11px;
    line-height: 1.6;
}}

@media(max-width:900px) {{
    .workflow {{
        grid-template-columns: 1fr;
    }}
}}

/* =========================================================
   NATURAL LANGUAGE / CODE
   ========================================================= */

.code-section {{
    max-width: 1200px;
    margin: 40px auto;
    padding: 70px 4vw;
}}

.code-layout {{
    display: grid;
    grid-template-columns: .9fr 1.1fr;
    gap: 50px;
    align-items: center;
}}

.code-window {{
    border-radius: 17px;
    overflow: hidden;
    border: 1px solid rgba(199,206,216,.12);
    background: #050A12;
    box-shadow: 0 30px 80px rgba(0,0,0,.4);
}}

.code-header {{
    padding: 12px 15px;
    border-bottom: 1px solid rgba(255,255,255,.07);
    color: #64748B;
    font-size: 9px;
    font-family: 'JetBrains Mono';
}}

.code-content {{
    padding: 22px;
    font-family: 'JetBrains Mono';
    font-size: 11px;
    line-height: 1.9;
    color: #CBD5E1;
}}

.code-green {{
    color: #6EA8FF;
}}

.code-gold {{
    color: {GOLD};
}}

.code-blue {{
    color: #60A5FA;
}}

.output {{
    margin-top: 15px;
    padding: 15px;
    border-radius: 10px;
    background: rgba(11,45,92,.25);
    border: 1px solid rgba(96,165,250,.20);
}}

.output-title {{
    color: #60A5FA;
    font-size: 9px;
    letter-spacing: 1px;
    margin-bottom: 8px;
}}

.output-value {{
    font-size: 23px;
    font-weight: 900;
}}

@media(max-width:850px) {{
    .code-layout {{
        grid-template-columns: 1fr;
    }}
}}

/* =========================================================
   VISUALIZATION
   ========================================================= */

.visual-grid {{
    display: grid;
    grid-template-columns: 1.4fr .8fr;
    gap: 15px;
    margin-top: 50px;
}}

.viz-card {{
    padding: 22px;
    border-radius: 16px;
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(255,255,255,.08);
    min-height: 250px;
}}

.viz-card:hover {{
    border-color: rgba(212,175,55,.40);
}}

.viz-title {{
    font-size: 13px;
    font-weight: 800;
}}

.fake-bars {{
    display: flex;
    align-items: end;
    gap: 13px;
    height: 170px;
    margin-top: 20px;
}}

.fake-bar {{
    flex: 1;
    background: linear-gradient(
        180deg,
        #6EA8FF,
        #0B2D5C
    );
    border-radius: 5px 5px 0 0;
}}

.donut {{
    width: 145px;
    height: 145px;
    border-radius: 50%;
    margin: 25px auto;
    background:
        conic-gradient(
            {GOLD} 0deg 125deg,
            #6EA8FF 125deg 235deg,
            #64748B 235deg 360deg
        );
    position: relative;
}}

.donut::after {{
    content: "";
    position: absolute;
    inset: 32px;
    background: #07111F;
    border-radius: 50%;
}}

@media(max-width:800px) {{
    .visual-grid {{
        grid-template-columns: 1fr;
    }}
}}

/* =========================================================
   PRICING
   ========================================================= */

.pricing-card {{
    max-width: 560px;
    margin: 50px auto 0;
    padding: 42px;
    text-align: center;
    border-radius: 22px;
    background:
        linear-gradient(
            145deg,
            rgba(11,45,92,.35),
            rgba(255,255,255,.035)
        );
    border: 1px solid rgba(212,175,55,.28);
    box-shadow: 0 30px 80px rgba(0,0,0,.35);
}}

.pricing-label {{
    color: {GOLD};
    font-size: 11px;
    letter-spacing: 2px;
    font-weight: 900;
}}

.price {{
    font-size: 58px;
    font-weight: 900;
    margin-top: 15px;
}}

.price span {{
    font-size: 15px;
    color: #64748B;
}}

.pricing-note {{
    color: #94A3B8;
    line-height: 1.7;
    font-size: 13px;
}}

.pricing-list {{
    text-align: left;
    margin: 28px auto;
    max-width: 360px;
}}

.pricing-list div {{
    padding: 9px 0;
    color: #CBD5E1;
    font-size: 13px;
}}

.pricing-list div::before {{
    content: "✓";
    color: {GOLD};
    font-weight: 900;
    margin-right: 9px;
}}

/* =========================================================
   FINAL CTA
   ========================================================= */

.final-cta {{
    max-width: 1100px;
    margin: 80px auto;
    padding: 70px 35px;
    text-align: center;
    border-radius: 25px;
    background:
        radial-gradient(
            circle at 50% 0%,
            rgba(11,45,92,.55),
            transparent 60%
        ),
        #07111F;
    border: 1px solid rgba(199,206,216,.10);
}}

.final-cta h2 {{
    font-size: clamp(36px,5vw,65px);
    margin: 0;
    letter-spacing: -3px;
}}

.final-cta p {{
    color: #94A3B8;
    max-width: 580px;
    margin: 18px auto 30px;
    line-height: 1.7;
}}

/* =========================================================
   FOOTER
   ========================================================= */

.footer {{
    border-top: 1px solid rgba(255,255,255,.08);
    padding: 45px 4vw 25px;
    max-width: 1400px;
    margin: auto;
}}

.footer-grid {{
    display: grid;
    grid-template-columns: 1.4fr repeat(3,1fr);
    gap: 35px;
}}

.footer-brand {{
    color: white;
    font-size: 18px;
    font-weight: 900;
    letter-spacing: 2px;
}}

.footer-description {{
    color: #64748B;
    font-size: 12px;
    line-height: 1.7;
    max-width: 300px;
    margin-top: 12px;
}}

.footer h4 {{
    font-size: 11px;
    color: #CBD5E1;
    letter-spacing: 1px;
}}

.footer a {{
    display: block;
    color: #64748B !important;
    font-size: 11px;
    margin: 10px 0;
}}

.footer-bottom {{
    margin-top: 45px;
    padding-top: 20px;
    border-top: 1px solid rgba(255,255,255,.06);
    color: #475569;
    font-size: 10px;
    display: flex;
    justify-content: space-between;
    gap: 15px;
    flex-wrap: wrap;
}}

@media(max-width:750px) {{
    .footer-grid {{
        grid-template-columns: 1fr 1fr;
    }}
}}

</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# NAVIGATION — now uses the DGL logo image
# ============================================================

# Build the brand-mark content depending on whether the logo exists
if LOGO_EXISTS and LOGO_DATA_URI:
    _brand_mark_inner = (
        f'<img src="{LOGO_DATA_URI}" alt="DACRE Analysis" class="dgl-symbol-logo" />'
    )
else:
    _brand_mark_inner = "D"

st.markdown(
    f"""
<nav class="dgl-nav">
    <div class="dgl-brand">
        <div class="dgl-symbol">{_brand_mark_inner}</div>
        <div class="dgl-brand-name">
            <div class="dgl-brand-main">DGL</div>
            <div class="dgl-brand-sub">DACRE GLOBAL LIMITED</div>
        </div>
    </div>

    <div class="dgl-nav-links">
        <a href="#product">Product</a>
        <a href="#capabilities">Solutions</a>
        <a href="#workflow">Resources</a>
        <a href="#company">Company</a>
    </div>

    <div class="nav-actions">
        <a class="nav-login" href="#login">Sign in</a>
        <a class="nav-start" href="#start">Get Started</a>
    </div>
</nav>
""",
    unsafe_allow_html=True,
)

# ============================================================
# HERO — with DGL logo emblem above the hero heading
# ============================================================

if LOGO_EXISTS and LOGO_DATA_URI:
    _hero_logo_block = f"""
    <div style="margin-bottom:22px;">
        <img src="{LOGO_DATA_URI}"
             alt="DACRE Analysis Logo"
             style="
                width: 118px;
                height: 118px;
                object-fit: contain;
                filter: drop-shadow(0 10px 30px rgba(212,175,55,.28));
                border-radius: 22px;
             " />
    </div>
    """
else:
    _hero_logo_block = ""

st.markdown(
    f"""
<section class="hero" id="product">

<div class="hero-grid">

<div>

{_hero_logo_block}

<div class="eyebrow">DGL DATA INTELLIGENCE PLATFORM</div>

<h1 class="hero-title">
DACRE<br>
<span class="gold">ANALYSIS</span>
</h1>

<div class="hero-tagline">
Turn your data into decisions.
</div>

<div class="hero-description">
Powerful data analysis, visualization and DI intelligence
for businesses, analysts and organizations.
Transform complex data into clear insight, dynamic
presentations and decisions you can act on.
</div>

<div class="hero-actions">
<a class="hero-btn hero-primary" href="#start">
Start Analyzing
</a>

<a class="hero-btn hero-secondary" href="#how">
See How It Works
</a>
</div>

<div class="hero-note">
Built by Dacre Global Limited • Data intelligence for modern organizations
</div>

</div>

<div class="dashboard-shell">

<div class="dashboard">

<div class="dashboard-top">
<span class="dot"></span>
<span class="dot"></span>
<span class="dot"></span>
</div>

<div class="dashboard-body">

<div class="dashboard-side">
<div class="side-logo">DACRE</div>
<div class="side-item active">Overview</div>
<div class="side-item">Data</div>
<div class="side-item">Analysis</div>
<div class="side-item">Charts</div>
<div class="side-item">Presentations</div>
<div class="side-item">File Vault</div>
</div>

<div class="dashboard-main">

<div class="dash-heading">
<h3>Data Intelligence</h3>
<span>REAL DACRE DASHBOARD</span>
</div>

<div class="metric-grid">

<div class="metric">
<div class="metric-label">TOTAL RECORDS</div>
<div class="metric-value">248,930</div>
<div class="metric-change">+12.8%</div>
</div>

<div class="metric">
<div class="metric-label">ANALYSED</div>
<div class="metric-value">94.6%</div>
<div class="metric-change">+8.4%</div>
</div>

<div class="metric">
<div class="metric-label">INSIGHTS</div>
<div class="metric-value">1,284</div>
<div class="metric-change">+24.1%</div>
</div>

</div>

<div class="chart-area">
<div class="chart-label">Performance trend</div>

<div class="chart-line">
<svg viewBox="0 0 500 120" preserveAspectRatio="none">
<polyline
points="0,100 60,88 110,94 165,58 220,68 280,40 335,48 390,20 450,30 500,5"
fill="none"
stroke="#D4AF37"
stroke-width="4"
/>
</svg>
</div>
</div>

<div class="bottom-grid">

<div class="mini-panel">
<div class="metric-label">DATA QUALITY</div>
<div class="bar"><span style="width:91%"></span></div>
<div class="metric-change">91% clean</div
