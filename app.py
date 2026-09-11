import streamlit as st
from pathlib import Path
import base64

BASE_DIR = Path(__file__).resolve().parent

LOGO_CANDIDATES = [
    "dacre_logo.png", "dacre_logo.jpg", "dacre_logo.jpeg",
    "DACRE.png", "logo.png",
    "assets/dacre_logo.png", "assets/logo.png", "assets/DACRE.png",
]

LOGO_PATH = None
for candidate in LOGO_CANDIDATES:
    p = BASE_DIR / candidate
    if p.exists():
        LOGO_PATH = p
        break

LOGO_EXISTS = LOGO_PATH is not None

def _logo_data_uri():
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
        return f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"
    except Exception:
        return ""

LOGO_DATA_URI = _logo_data_uri()

if LOGO_EXISTS:
    st.set_page_config(
        page_title="DACRE Analysis | Turn Your Data Into Decisions",
        page_icon=str(LOGO_PATH),
        layout="wide",
        initial_sidebar_state="collapsed",
    )
else:
    st.set_page_config(
        page_title="DACRE Analysis | Turn Your Data Into Decisions",
        page_icon="◆",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

BLUE = "#0B2D5C"
DARK_BLUE = "#07111F"
GOLD = "#D4AF37"
SILVER = "#C7CED8"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root {{
    --dgl-blue: {BLUE};
    --dgl-dark: {DARK_BLUE};
    --dgl-gold: {GOLD};
    --dgl-silver: {SILVER};
}}

* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}

body {{
    margin: 0;
    background: radial-gradient(circle at 80% 10%, rgba(11,45,92,.32), transparent 30%),
                linear-gradient(180deg, #030712 0%, #07111F 45%, #030712 100%);
    color: white;
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background: radial-gradient(circle at 15% 15%, rgba(11,45,92,.20), transparent 25%),
                linear-gradient(180deg, #030712 0%, #07111F 100%);
}}

header {{ visibility: hidden; }}
.block-container {{ max-width: 1400px; padding-top: 0.5rem; padding-bottom: 4rem; }}
section[data-testid="stSidebar"] {{ display: none; }}
button {{ font-family: 'Inter', sans-serif !important; }}
a {{ text-decoration: none !important; }}
::selection {{ background: rgba(212,175,55,.35); color: white; }}

.dgl-nav {{
    position: sticky; top: 0; z-index: 999; width: 100%;
    padding: 18px 4vw; display: flex; align-items: center;
    justify-content: space-between;
    background: rgba(3,7,18,.82);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(199,206,216,.10);
}}

.dgl-brand {{ display: flex; align-items: center; gap: 12px; }}

.dgl-symbol {{
    width: 42px; height: 42px; border-radius: 12px;
    display: grid; place-items: center;
    background: linear-gradient(135deg, {BLUE}, #174C91);
    border: 1px solid rgba(212,175,55,.65);
    box-shadow: 0 0 25px rgba(11,45,92,.35);
    color: {GOLD}; font-weight: 900; font-size: 18px;
    overflow: hidden;
}}

.dgl-symbol-logo {{ width: 100%; height: 100%; object-fit: cover; border-radius: 12px; display: block; }}

.dgl-brand-name {{ display: flex; flex-direction: column; line-height: 1.05; }}
.dgl-brand-main {{ font-size: 15px; font-weight: 900; letter-spacing: 2px; }}
.dgl-brand-sub {{ font-size: 8px; color: {SILVER}; letter-spacing: 2px; margin-top: 4px; }}

.dgl-nav-links {{ display: flex; gap: 32px; align-items: center; }}
.dgl-nav-links a {{ color: #B9C3D1 !important; font-size: 13px; font-weight: 600; transition: .2s ease; }}
.dgl-nav-links a:hover {{ color: white !important; }}

.nav-actions {{ display: flex; gap: 10px; align-items: center; }}
.nav-login {{ color: #CBD5E1 !important; font-size: 13px; font-weight: 700; padding: 11px 15px; }}
.nav-start {{
    color: #07111F !important;
    background: linear-gradient(135deg, {GOLD}, #F3D77A);
    padding: 11px 18px; border-radius: 10px;
    font-size: 13px; font-weight: 900;
    box-shadow: 0 8px 25px rgba(212,175,55,.18);
}}

@media(max-width: 850px) {{
    .dgl-nav-links {{ display: none; }}
    .nav-login {{ display: none; }}
    .dgl-nav {{ padding: 14px 18px; }}
}}

.hero {{
    min-height: 730px; padding: 110px 4vw 70px;
    position: relative; overflow: hidden;
}}

.hero::before {{
    content: ""; position: absolute; inset: 0;
    background-image: linear-gradient(rgba(255,255,255,.025) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(255,255,255,.025) 1px, transparent 1px);
    background-size: 55px 55px;
    mask-image: linear-gradient(to bottom, black, transparent 90%);
    pointer-events: none;
}}

.hero-grid {{
    max-width: 1240px; margin: auto; position: relative; z-index: 2;
    display: grid; grid-template-columns: 1fr .95fr;
    gap: 70px; align-items: center;
}}

.eyebrow {{
    display: inline-flex; align-items: center; gap: 8px;
    color: {GOLD}; font-size: 11px; font-weight: 800;
    letter-spacing: 2.5px; text-transform: uppercase;
    margin-bottom: 20px;
}}

.eyebrow::before {{ content: ""; width: 28px; height: 1px; background: {GOLD}; }}

.hero-title {{
    font-size: clamp(52px, 7vw, 104px);
    line-height: .92; letter-spacing: -5px;
    font-weight: 900; margin: 0; max-width: 850px;
}}

.hero-title .gold {{ color: {GOLD}; }}
.hero-title .blue {{ color: #6EA8FF; }}

.hero-tagline {{
    margin-top: 28px;
    font-size: clamp(22px, 3vw, 34px);
    font-weight: 700; color: #E5E7EB;
}}

.hero-description {{
    margin-top: 18px; max-width: 650px;
    color: #94A3B8; font-size: 16px; line-height: 1.8;
}}

.hero-actions {{ display: flex; gap: 14px; flex-wrap: wrap; margin-top: 34px; }}

.hero-btn {{
    display: inline-flex; align-items: center; justify-content: center;
    padding: 15px 22px; border-radius: 11px;
    font-weight: 800; font-size: 14px;
}}

.hero-primary {{
    background: linear-gradient(135deg, {GOLD}, #F0D36A);
    color: #06101D !important;
    box-shadow: 0 15px 40px rgba(212,175,55,.18);
}}

.hero-secondary {{
    border: 1px solid rgba(199,206,216,.22);
    color: white !important;
    background: rgba(255,255,255,.03);
}}

.hero-note {{ margin-top: 22px; color: #64748B; font-size: 11px; }}

@media(max-width: 950px) {{
    .hero {{ padding-top: 70px; }}
    .hero-grid {{ grid-template-columns: 1fr; gap: 45px; }}
    .hero-title {{ letter-spacing: -3px; }}
}}

.dashboard-shell {{
    position: relative; padding: 10px; border-radius: 22px;
    background: linear-gradient(135deg, rgba(212,175,55,.55), rgba(11,45,92,.7), rgba(199,206,216,.2));
    box-shadow: 0 35px 90px rgba(0,0,0,.55);
}}

.dashboard {{
    background: #08111E; border-radius: 16px; overflow: hidden;
    border: 1px solid rgba(255,255,255,.08);
}}

.dashboard-top {{
    height: 42px; display: flex; align-items: center; gap: 7px;
    padding: 0 15px;
    border-bottom: 1px solid rgba(255,255,255,.07);
}}

.dot {{ width: 8px; height: 8px; border-radius: 50%; background: #64748B; }}

.dashboard-body {{
    display: grid; grid-template-columns: 130px 1fr;
    min-height: 405px;
}}

.dashboard-side {{
    border-right: 1px solid rgba(255,255,255,.07);
    padding: 18px 12px;
}}

.side-logo {{
    color: {GOLD}; font-size: 11px; font-weight: 900;
    letter-spacing: 1.5px; margin-bottom: 22px;
}}

.side-item {{
    padding: 9px; margin-bottom: 6px; border-radius: 7px;
    color: #64748B; font-size: 9px;
}}

.side-item.active {{ background: rgba(11,45,92,.55); color: white; }}

.dashboard-main {{ padding: 18px; }}

.dash-heading {{ display: flex; justify-content: space-between; align-items: center; }}
.dash-heading h3 {{ margin: 0; font-size: 17px; }}
.dash-heading span {{ font-size: 8px; color: #64748B; }}

.metric-grid {{
    display: grid; grid-template-columns: repeat(3,1fr);
    gap: 9px; margin-top: 14px;
}}

.metric {{
    background: rgba(255,255,255,.035);
    border: 1px solid rgba(255,255,255,.07);
    padding: 12px; border-radius: 9px;
}}

.metric-label {{ color: #64748B; font-size: 8px; }}
.metric-value {{ margin-top: 5px; font-size: 16px; font-weight: 800; }}
.metric-change {{ color: #60A5FA; font-size: 8px; margin-top: 4px; }}

.chart-area {{
    margin-top: 12px; height: 150px; padding: 12px;
    border-radius: 10px;
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(255,255,255,.06);
    position: relative; overflow: hidden;
}}

.chart-line {{
    position: absolute; left: 10%; right: 7%; bottom: 30px; height: 80px;
}}

.chart-line svg {{ width: 100%; height: 100%; }}

.chart-label {{
    position: absolute; top: 10px; left: 12px;
    color: #94A3B8; font-size: 8px;
}}

.bottom-grid {{ display: grid; grid-template-columns: 1fr .6fr; gap: 10px; margin-top: 10px; }}

.mini-panel {{
    height: 95px; border-radius: 10px;
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(255,255,255,.06);
    padding: 11px;
}}

.bar {{
    height: 6px; border-radius: 5px;
    background: #16365F; margin-top: 12px;
    overflow: hidden;
}}

.bar span {{
    display: block; height: 100%;
    background: linear-gradient(90deg, {BLUE}, #6EA8FF);
}}

@media(max-width:600px) {{
    .dashboard-body {{ grid-template-columns: 80px 1fr; }}
    .dashboard-side {{ padding: 12px 7px; }}
    .metric-grid {{ grid-template-columns: 1fr; }}
}}

.trust {{
    max-width: 1150px; margin: 0 auto;
    padding: 35px 4vw 80px; text-align: center;
}}

.trust-label {{
    color: #64748B; font-size: 10px;
    letter-spacing: 2px; text-transform: uppercase;
}}

.trust-row {{
    margin-top: 25px;
    display: flex; justify-content: center;
    gap: 45px; flex-wrap: wrap;
}}

.trust-item {{
    color: #94A3B8; font-weight: 800;
    font-size: 12px; letter-spacing: 1px;
}}

.section {{ max-width: 1200px; margin: auto; padding: 100px 4vw; }}

.section-kicker {{
    color: {GOLD}; font-size: 10px;
    letter-spacing: 2.5px; font-weight: 900;
    text-transform: uppercase;
}}

.section-title {{
    font-size: clamp(34px, 5vw, 58px);
    line-height: 1; letter-spacing: -2px;
    margin: 14px 0; font-weight: 900;
}}

.section-description {{
    max-width: 680px; color: #94A3B8;
    line-height: 1.8; font-size: 15px;
}}

.capability-grid {{
    display: grid; grid-template-columns: repeat(3,1fr);
    gap: 15px; margin-top: 50px;
}}

.capability {{
    min-height: 235px; padding: 25px; border-radius: 17px;
    background: linear-gradient(145deg, rgba(255,255,255,.045), rgba(255,255,255,.015));
    border: 1px solid rgba(199,206,216,.10);
    transition: .25s ease;
}}

.capability:hover {{
    transform: translateY(-5px);
    border-color: rgba(212,175,55,.45);
    box-shadow: 0 25px 50px rgba(0,0,0,.25);
}}

.capability-number {{
    color: {GOLD}; font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
}}

.capability h3 {{ margin-top: 28px; font-size: 21px; }}
.capability p {{ color: #7E8CA0; line-height: 1.7; font-size: 13px; }}

@media(max-width:800px) {{
    .capability-grid {{ grid-template-columns: 1fr; }}
}}

.workflow {{
    margin-top: 55px;
    display: grid; grid-template-columns: repeat(5,1fr);
    gap: 10px;
}}

.workflow-step {{
    position: relative; padding: 20px;
    min-height: 160px;
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 14px;
    background: rgba(255,255,255,.025);
}}

.workflow-step .number {{
    color: {GOLD}; font-family: 'JetBrains Mono';
    font-size: 11px;
}}

.workflow-step h4 {{ margin-top: 25px; margin-bottom: 8px; }}
.workflow-step p {{ color: #718096; font-size: 11px; line-height: 1.6; }}

@media(max-width:900px) {{
    .workflow {{ grid-template-columns: 1fr; }}
}}

.code-section {{ max-width: 1200px; margin: 40px auto; padding: 70px 4vw; }}

.code-layout {{
    display: grid; grid-template-columns: .9fr 1.1fr;
    gap: 50px; align-items: center;
}}

.code-window {{
    border-radius: 17px; overflow: hidden;
    border: 1px solid rgba(199,206,216,.12);
    background: #050A12;
    box-shadow: 0 30px 80px rgba(0,0,0,.4);
}}

.code-header {{
    padding: 12px 15px;
    border-bottom: 1px solid rgba(255,255,255,.07);
    color: #64748B; font-size: 9px;
    font-family: 'JetBrains Mono';
}}

.code-content {{
    padding: 22px;
    font-family: 'JetBrains Mono';
    font-size: 11px; line-height: 1.9;
    color: #CBD5E1;
}}

.code-green {{ color: #6EA8FF; }}
.code-gold {{ color: {GOLD}; }}
.code-blue {{ color: #60A5FA; }}

.output {{
    margin-top: 15px; padding: 15px; border-radius: 10px;
    background: rgba(11,45,92,.25);
    border: 1px solid rgba(96,165,250,.20);
}}

.output-title {{
    color: #60A5FA; font-size: 9px;
    letter-spacing: 1px; margin-bottom: 8px;
}}

.output-value {{ font-size: 23px; font-weight: 900; }}

@media(max-width:850px) {{
    .code-layout {{ grid-template-columns: 1fr; }}
}}

.visual-grid {{
    display: grid; grid-template-columns: 1.4fr .8fr;
    gap: 15px; margin-top: 50px;
}}

.viz-card {{
    padding: 22px; border-radius: 16px;
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(255,255,255,.08);
    min-height: 250px;
}}

.viz-card:hover {{ border-color: rgba(212,175,55,.40); }}
.viz-title {{ font-size: 13px; font-weight: 800; }}

.fake-bars {{
    display: flex; align-items: end; gap: 13px;
    height: 170px; margin-top: 20px;
}}

.fake-bar {{
    flex: 1;
    background: linear-gradient(180deg, #6EA8FF, #0B2D5C);
    border-radius: 5px 5px 0 0;
}}

.donut {{
    width: 145px; height: 145px; border-radius: 50%;
    margin: 25px auto;
    background: conic-gradient({GOLD} 0deg 125deg, #6EA8FF 125deg 235deg, #64748B 235deg 360deg);
    position: relative;
}}

.donut::after {{
    content: ""; position: absolute; inset: 32px;
    background: #07111F; border-radius: 50%;
}}

@media(max-width:800px) {{
    .visual-grid {{ grid-template-columns: 1fr; }}
}}

.pricing-card {{
    max-width: 560px; margin: 50px auto 0;
    padding: 42px; text-align: center;
    border-radius: 22px;
    background: linear-gradient(145deg, rgba(11,45,92,.35), rgba(255,255,255,.035));
    border: 1px solid rgba(212,175,55,.28);
    box-shadow: 0 30px 80px rgba(0,0,0,.35);
}}

.pricing-label {{
    color: {GOLD}; font-size: 11px;
    letter-spacing: 2px; font-weight: 900;
}}

.price {{ font-size: 58px; font-weight: 900; margin-top: 15px; }}
.price span {{ font-size: 15px; color: #64748B; }}
.pricing-note {{ color: #94A3B8; line-height: 1.7; font-size: 13px; }}

.pricing-list {{ text-align: left; margin: 28px auto; max-width: 360px; }}
.pricing-list div {{ padding: 9px 0; color: #CBD5E1; font-size: 13px; }}
.pricing-list div::before {{
    content: "✓"; color: {GOLD}; font-weight: 900; margin-right: 9px;
}}

.final-cta {{
    max-width: 1100px; margin: 80px auto;
    padding: 70px 35px; text-align: center;
    border-radius: 25px;
    background: radial-gradient(circle at 50% 0%, rgba(11,45,92,.55), transparent 60%), #07111F;
    border: 1px solid rgba(199,206,216,.10);
}}

.final-cta h2 {{
    font-size: clamp(36px,5vw,65px);
    margin: 0; letter-spacing: -3px;
}}

.final-cta p {{
    color: #94A3B8; max-width: 580px;
    margin: 18px auto 30px; line-height: 1.7;
}}

.footer {{
    border-top: 1px solid rgba(255,255,255,.08);
    padding: 45px 4vw 25px; max-width: 1400px; margin: auto;
}}

.footer-grid {{
    display: grid; grid-template-columns: 1.4fr repeat(3,1fr);
    gap: 35px;
}}

.footer-brand {{
    color: white; font-size: 18px;
    font-weight: 900; letter-spacing: 2px;
}}

.footer-description {{
    color: #64748B; font-size: 12px;
    line-height: 1.7; max-width: 300px; margin-top: 12px;
}}

.footer h4 {{ font-size: 11px; color: #CBD5E1; letter-spacing: 1px; }}
.footer a {{ display: block; color: #64748B !important; font-size: 11px; margin: 10px 0; }}

.footer-bottom {{
    margin-top: 45px; padding-top: 20px;
    border-top: 1px solid rgba(255,255,255,.06);
    color: #475569; font-size: 10px;
    display: flex; justify-content: space-between;
    gap: 15px; flex-wrap: wrap;
}}

@media(max-width:750px) {{
    .footer-grid {{ grid-template-columns: 1fr 1fr; }}
}}
</style>
""", unsafe_allow_html=True)

if LOGO_EXISTS and LOGO_DATA_URI:
    _brand_mark_inner = f'<img src="{LOGO_DATA_URI}" alt="DACRE" class="dgl-symbol-logo" />'
else:
    _brand_mark_inner = "D"

st.markdown(f"""
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
""", unsafe_allow_html=True)

if LOGO_EXISTS and LOGO_DATA_URI:
    _hero_logo_block = (
        f'<div style="margin-bottom:22px;">'
        f'<img src="{LOGO_DATA_URI}" alt="DACRE Analysis Logo" '
        f'style="width:118px;height:118px;object-fit:contain;'
        f'filter:drop-shadow(0 10px 30px rgba(212,175,55,.28));'
        f'border-radius:22px;" />'
        f'</div>'
    )
else:
    _hero_logo_block = ""

st.markdown(f"""
<section class="hero" id="product">
<div class="hero-grid">
<div>
{_hero_logo_block}
<div class="eyebrow">DGL DATA INTELLIGENCE PLATFORM</div>
<h1 class="hero-title">
DACRE<br>
<span class="gold">ANALYSIS</span>
</h1>
<div class="hero-tagline">Turn your data into decisions.</div>
<div class="hero-description">
Powerful data analysis, visualization and DI intelligence
for businesses, analysts and organizations.
Transform complex data into clear insight, dynamic
presentations and decisions you can act on.
</div>
<div class="hero-actions">
<a class="hero-btn hero-primary" href="#start">Start Analyzing</a>
<a class="hero-btn hero-secondary" href="#how">See How It Works</a>
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
<polyline points="0,100 60,88 110,94 165,58 220,68 280,40 335,48 390,20 450,30 500,5" fill="none" stroke="#D4AF37" stroke-width="4" />
</svg>
</div>
</div>
<div class="bottom-grid">
<div class="mini-panel">
<div class="metric-label">DATA QUALITY</div>
<div class="bar"><span style="width:91%"></span></div>
<div class="metric-change">91% clean</div>
</div>
<div class="mini-panel">
<div class="metric-label">STATUS</div>
<div style="margin-top:14px;font-size:12px;color:#6EA8FF;">● Analysis ready</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</section>
""", unsafe_allow_html=True)

st.markdown("""
<div class="trust">
<div class="trust-label">Designed for modern data teams</div>
<div class="trust-row">
<div class="trust-item">BUSINESSES</div>
<div class="trust-item">ANALYSTS</div>
<div class="trust-item">ORGANIZATIONS</div>
<div class="trust-item">DATA TEAMS</div>
<div class="trust-item">DECISION MAKERS</div>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<section class="section" id="capabilities">
<div class="section-kicker">What DACRE does</div>
<h2 class="section-title">
From raw data to<br>
<span style="color:#D4AF37;">clear decisions.</span>
</h2>
<p class="section-description">
DACRE Analysis brings the essential data-work process into one
professional environment — from cleaning and analysis to
visualization and presentation.
</p>
<div class="capability-grid">
<div class="capability">
<div class="capability-number">01 / DATA</div>
<h3>Data Cleaning</h3>
<p>Clean, structure and prepare datasets so your analysis starts from reliable information rather than messy spreadsheets.</p>
</div>
<div class="capability">
<div class="capability-number">02 / DI</div>
<h3>DI Analysis</h3>
<p>Use David Intelligence to help transform your requests and data into meaningful analytical work.</p>
</div>
<div class="capability">
<div class="capability-number">03 / VISUAL</div>
<h3>Visualization</h3>
<p>Turn complex datasets into professional charts, dashboards and visual stories that are easier to understand.</p>
</div>
<div class="capability">
<div class="capability-number">04 / PRESENT</div>
<h3>Presentations</h3>
<p>Create clear data presentations that help businesses communicate findings and make informed decisions.</p>
</div>
<div class="capability">
<div class="capability-number">05 / CONNECT</div>
<h3>Power BI Connection</h3>
<p>Connect your data workflows with Power BI and extend your analytical environment.</p>
</div>
<div class="capability">
<div class="capability-number">06 / VAULT</div>
<h3>File Vault</h3>
<p>Keep important analysis outputs and generated work organized inside your DACRE workspace.</p>
</div>
</div>
</section>
""", unsafe_allow_html=True)

st.markdown("""
<section class="section" id="workflow">
<div class="section-kicker">The DACRE workflow</div>
<h2 class="section-title">
Ask naturally.<br>
<span style="color:#6EA8FF;">Analyse intelligently.</span>
</h2>
<p class="section-description">
You don't need to write complex analytical instructions.
Describe what you want to do and DACRE's DI workflow can
translate the request into executable analytical work.
</p>
<div class="workflow">
<div class="workflow-step">
<div class="number">01</div>
<h4>Ask</h4>
<p>Type or speak what you want to discover.</p>
</div>
<div class="workflow-step">
<div class="number">02</div>
<h4>Prociel</h4>
<p>Prociel processes the request and prepares the analytical code.</p>
</div>
<div class="workflow-step">
<div class="number">03</div>
<h4>Run Code</h4>
<p>Execute the generated analytical operation.</p>
</div>
<div class="workflow-step">
<div class="number">04</div>
<h4>Exiel</h4>
<p>Exiel presents the resulting analytical output.</p>
</div>
<div class="workflow-step">
<div class="number">05</div>
<h4>File Vault</h4>
<p>Add useful outputs to your workspace for later use.</p>
</div>
</div>
</section>
""", unsafe_allow_html=True)

st.markdown("""
<section class="code-section" id="how">
<div class="code-layout">
<div>
<div class="section-kicker">Natural language → analytical code</div>
<h2 class="section-title">
You describe it.<br>
<span style="color:#D4AF37;">DACRE builds it.</span>
</h2>
<p class="section-description">
Write a normal request instead of manually constructing every
analytical operation. Prociel prepares the code, you run it,
and Exiel presents the result.
</p>
</div>
<div class="code-window">
<div class="code-header">PROCIEL / ANALYTICAL WORKSPACE</div>
<div class="code-content">
<span class="code-gold">USER:</span><br>
"Show me monthly revenue growth and identify
the strongest month."
<br><br>
<span class="code-blue">PROCIEL processing your data...</span>
<br><br>
<span class="code-gold">GENERATED ANALYSIS</span><br>
<span class="code-green">
revenue_by_month =<br>
&nbsp;&nbsp;df.groupby("month")["revenue"].sum()<br><br>
growth = revenue_by_month.pct_change()<br>
strongest_month = growth.idxmax()
</span>
<div class="output">
<div class="output-title">EXIEL • ANALYSIS RESULT</div>
<div class="output-value">+18.7%</div>
<div style="color:#94A3B8;font-size:10px;margin-top:5px;">
Strongest growth detected in September.
</div>
</div>
</div>
</div>
</div>
</section>
""", unsafe_allow_html=True)

st.markdown("""
<section class="section">
<div class="section-kicker">Make data visible</div>
<h2 class="section-title">
Charts that make<br>
<span style="color:#D4AF37;">the story obvious.</span>
</h2>
<p class="section-description">
Build clear visual representations of your data for analysis,
reporting and decision-making.
</p>
<div class="visual-grid">
<div class="viz-card">
<div class="viz-title
