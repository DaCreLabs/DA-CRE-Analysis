import os
import pandas as pd
import streamlit as st


# ============================================================
# DACREGLOBAL LIMITED
# DACRE ANALYSIS
# ============================================================

LOGO_PATH = "assets/dacre_logo.png"

# Use the real DACRE logo as the browser/page icon.
# If the logo is temporarily missing, the app will still start.
PAGE_ICON = LOGO_PATH if os.path.isfile(LOGO_PATH) else "📊"

st.set_page_config(
    page_title="DACREglobal limited | DACRE Analysis",
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# PREMIUM DACRE DESIGN
# ============================================================

st.markdown(
    """
<style>

@import url(
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap'
);

:root {
    --black: #030508;
    --black2: #080c12;
    --blue: #1677ff;
    --blue-light: #55b8ff;
    --gold: #e7b84b;
    --gold-light: #ffdc73;
    --green: #49e58a;
    --purple: #a875ff;
    --white: #ffffff;
    --muted: #9aa5b8;
}

html {
    scroll-behavior: smooth;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(22,119,255,0.16),
            transparent 25%
        ),
        radial-gradient(
            circle at 90% 5%,
            rgba(231,184,75,0.13),
            transparent 23%
        ),
        radial-gradient(
            circle at 50% 65%,
            rgba(73,229,138,0.05),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #020304 0%,
            #070b12 45%,
            #05070a 75%,
            #0b0905 100%
        );

    color: white;
    font-family: 'Inter', sans-serif;
}

.main .block-container {
    max-width: 1450px;
    padding-top: 0.7rem;
    padding-bottom: 4rem;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* ============================================================
   NAVIGATION
   ============================================================ */

.dacre-nav {
    border-bottom: 1px solid rgba(255,255,255,0.08);
    padding: 8px 0 17px 0;
    margin-bottom: 15px;
}

.brand {
    color: #ffffff;
    font-size: 1.12rem;
    font-weight: 900;
    letter-spacing: -0.04em;
}

.brand span {
    color: var(--gold);
}

.brand-sub {
    color: #718096;
    font-size: 0.58rem;
    letter-spacing: 0.24em;
    margin-top: 3px;
}

.nav-item {
    color: #aeb8c8;
    font-size: 0.8rem;
    font-weight: 600;
    padding-top: 10px;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    min-height: 44px;
    border-radius: 12px !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    background: rgba(255,255,255,0.045) !important;
    border: 1px solid rgba(255,255,255,0.13) !important;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    border-color: rgba(231,184,75,0.55) !important;
    box-shadow: 0 15px 40px rgba(0,0,0,0.35);
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    text-align: center;
    padding: 75px 15px 25px;
}

.hero-badge {
    display: inline-block;
    padding: 9px 18px;
    border-radius: 50px;

    border: 1px solid rgba(231,184,75,0.35);

    background:
        linear-gradient(
            90deg,
            rgba(231,184,75,0.10),
            rgba(22,119,255,0.08)
        );

    color: var(--gold-light);
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.2em;
}

.hero-title {
    margin-top: 25px;
    font-size: clamp(3.4rem, 8vw, 7rem);
    line-height: 0.92;
    font-weight: 900;
    letter-spacing: -0.07em;

    background:
        linear-gradient(
            100deg,
            #ffffff 0%,
            #ffffff 25%,
            #55b8ff 45%,
            #1677ff 62%,
            #ffdc73 82%,
            #ffffff 100%
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-tagline {
    margin-top: 25px;
    color: white;
    font-size: clamp(1.25rem, 2.6vw, 2rem);
    font-weight: 750;
}

.hero-description {
    max-width: 800px;
    margin: 20px auto 0;
    color: var(--muted);
    line-height: 1.85;
    font-size: 0.98rem;
}


/* ============================================================
   DASHBOARD
   ============================================================ */

.dashboard {
    margin-top: 60px;
    padding: 20px;
    border-radius: 25px;

    border: 1px solid rgba(255,255,255,0.10);

    background:
        linear-gradient(
            135deg,
            rgba(17,24,38,0.96),
            rgba(6,9,14,0.98)
        );

    box-shadow:
        0 35px 100px rgba(0,0,0,0.55),
        0 0 80px rgba(22,119,255,0.06);
}

.dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 3px 5px 17px;
}

.dashboard-title {
    color: white;
    font-size: 0.9rem;
    font-weight: 800;
}

.dashboard-subtitle {
    color: #758198;
    font-size: 0.68rem;
    margin-top: 3px;
}

.system-ready {
    color: var(--green);
    font-size: 0.67rem;
    font-weight: 800;
    letter-spacing: 0.08em;
}

.metric {
    min-height: 120px;
    padding: 19px;
    border-radius: 17px;
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.075);
}

.metric-label {
    color: #7d899e;
    font-size: 0.64rem;
    font-weight: 800;
    letter-spacing: 0.13em;
}

.metric-number {
    color: white;
    font-size: 1.75rem;
    font-weight: 900;
    margin-top: 8px;
}

.metric-up {
    color: var(--green);
    font-size: 0.7rem;
    font-weight: 700;
}

.metric-gold {
    color: var(--gold-light);
    font-size: 0.7rem;
    font-weight: 700;
}

.metric-blue {
    color: var(--blue-light);
    font-size: 0.7rem;
    font-weight: 700;
}


/* ============================================================
   SECTIONS
   ============================================================ */

.section {
    padding-top: 105px;
}

.section-label {
    color: var(--gold);
    font-size: 0.67rem;
    font-weight: 850;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 13px;
}

.section-title {
    color: white;
    font-size: clamp(2rem, 4vw, 3.6rem);
    line-height: 1.05;
    letter-spacing: -0.05em;
    font-weight: 900;
}

.section-description {
    color: #919daf;
    max-width: 760px;
    line-height: 1.8;
    margin-top: 18px;
}


/* ============================================================
   FEATURES
   ============================================================ */

.feature-card {
    min-height: 255px;
    height: 100%;
    padding: 28px;
    border-radius: 21px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.055),
            rgba(255,255,255,0.018)
        );

    border: 1px solid rgba(255,255,255,0.08);

    transition: 0.25s ease;
}

.feature-card:hover {
    transform: translateY(-6px);
    border-color: rgba(231,184,75,0.35);
    box-shadow: 0 22px 60px rgba(0,0,0,0.3);
}

.feature-icon {
    width: 52px;
    height: 52px;
    border-radius: 15px;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 1.25rem;
    margin-bottom: 20px;
}

.blue-icon {
    background: rgba(22,119,255,0.13);
    border: 1px solid rgba(85,184,255,0.23);
}

.gold-icon {
    background: rgba(231,184,75,0.12);
    border: 1px solid rgba(231,184,75,0.24);
}

.green-icon {
    background: rgba(73,229,138,0.10);
    border: 1px solid rgba(73,229,138,0.21);
}

.purple-icon {
    background: rgba(168,117,255,0.11);
    border: 1px solid rgba(168,117,255,0.23);
}

.feature-title {
    color: white;
    font-size: 1.04rem;
    font-weight: 800;
}

.feature-text {
    color: #8995a9;
    font-size: 0.84rem;
    line-height: 1.75;
    margin-top: 10px;
}


/* ============================================================
   DEMO
   ============================================================ */

.demo-panel {
    padding: 23px;
    border-radius: 22px;
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.08);
}

.demo-label {
    color: #7e8ba1;
    font-size: 0.68rem;
    letter-spacing: 0.13em;
    font-weight: 800;
    margin-bottom: 15px;
}


/* ============================================================
   DI
   ============================================================ */

.di-panel {
    margin-top: 105px;
    padding: 55px;

    border-radius: 28px;

    border: 1px solid rgba(231,184,75,0.22);

    background:
        radial-gradient(
            circle at 82% 18%,
            rgba(22,119,255,0.18),
            transparent 29%
        ),
        radial-gradient(
            circle at 15% 85%,
            rgba(231,184,75,0.12),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            rgba(16,21,31,0.97),
            rgba(5,8,12,0.98)
        );

    box-shadow: 0 30px 90px rgba(0,0,0,0.35);
}

.di-title {
    color: white;
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    font-weight: 900;
    letter-spacing: -0.06em;
}

.di-highlight {
    color: var(--gold-light);
}

.di-flow {
    margin-top: 30px;
    color: white;
    font-weight: 750;
}

.di-arrow {
    color: var(--gold);
    padding: 0 8px;
}


/* ============================================================
   TRUST
   ============================================================ */

.trust {
    margin-top: 70px;
    padding: 25px;

    text-align: center;

    border-top: 1px solid rgba(255,255,255,0.07);
    border-bottom: 1px solid rgba(255,255,255,0.07);

    color: #778399;
    font-size: 0.69rem;
    font-weight: 700;
    letter-spacing: 0.1em;
}


/* ============================================================
   SECURITY
   ============================================================ */

.security-card {
    height: 100%;
    padding: 30px;
    border-radius: 20px;
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
}

.security-title {
    color: white;
    font-size: 1rem;
    font-weight: 800;
}

.security-text {
    color: #8995a9;
    line-height: 1.7;
    margin-top: 10px;
}


/* ============================================================
   PRICING
   ============================================================ */

.price-card {
    height: 100%;
    padding: 31px;
    border-radius: 23px;

    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.08);
}

.price-card.featured {
    border-color: rgba(231,184,75,0.38);

    background:
        linear-gradient(
            145deg,
            rgba(231,184,75,0.07),
            rgba(22,119,255,0.05)
        );
}

.price-name {
    color: var(--gold);
    font-size: 0.67rem;
    letter-spacing: 0.16em;
    font-weight: 850;
}

.price {
    color: white;
    font-size: 2.3rem;
    font-weight: 900;
    margin: 13px 0;
}

.price-text {
    color: #8995a9;
}

.price-list {
    color: #c5cedb;
    line-height: 2;
    margin-top: 15px;
}


/* ============================================================
   CTA
   ============================================================ */

.cta {
    margin-top: 110px;
    padding: 80px 25px;

    text-align: center;

    border-radius: 30px;
    border: 1px solid rgba(231,184,75,0.23);

    background:
        radial-gradient(
            circle at center,
            rgba(22,119,255,0.15),
            transparent 48%
        ),
        radial-gradient(
            circle at 75% 100%,
            rgba(231,184,75,0.12),
            transparent 35%
        ),
        #07090d;
}

.cta-title {
    color: white;
    font-size: clamp(2.3rem, 5vw, 4.5rem);
    font-weight: 900;
    letter-spacing: -0.06em;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    margin-top: 100px;
    padding: 42px 0 20px;

    border-top: 1px solid rgba(255,255,255,0.07);

    text-align: center;

    color: #69758a;
    font-size: 0.76rem;
}

.footer strong {
    color: white;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 768px) {

    .hero {
        padding-top: 50px;
    }

    .hero-title {
        font-size: 3.3rem;
    }

    .di-panel {
        padding: 30px;
    }

}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# NAVIGATION
# ============================================================

st.markdown('<div class="dacre-nav">', unsafe_allow_html=True)

nav1, nav2, nav3, nav4, nav5, nav6 = st.columns(
    [2.8, 1, 1, 1, 1, 1.45]
)

with nav1:

    logo_col, brand_col = st.columns([0.45, 2.8])

    with logo_col:
        if os.path.isfile(LOGO_PATH):
            st.image(LOGO_PATH, width=45)

    with brand_col:
        st.markdown(
            """
            <div class="brand">
                DACRE<span>global</span> limited
            </div>

            <div class="brand-sub">
                DACRE ANALYSIS
            </div>
            """,
            unsafe_allow_html=True,
        )

with nav2:
    st.markdown(
        '<div class="nav-item">Product</div>',
        unsafe_allow_html=True,
    )

with nav3:
    st.markdown(
        '<div class="nav-item">Solutions</div>',
        unsafe_allow_html=True,
    )

with nav4:
    st.markdown(
        '<div class="nav-item">Resources</div>',
        unsafe_allow_html=True,
    )

with nav5:
    st.markdown(
        '<div class="nav-item">Company</div>',
        unsafe_allow_html=True,
    )

with nav6:
    st.button(
        "Get Started",
        use_container_width=True,
    )

st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="hero">

    <div class="hero-badge">
        DACREGLOBAL LIMITED
    </div>

    <div class="hero-title">
        DACRE ANALYSIS
    </div>

    <div class="hero-tagline">
        Turn your data into decisions.
    </div>

    <div class="hero-description">
        Powerful data analysis, visualization and
        David Intelligence designed for businesses,
        analysts and organizations.
        Bring your data together, understand what it means,
        and make better decisions from it.
    </div>

</div>
""",
    unsafe_allow_html=True,
)


hero1, hero2, hero3, hero4 = st.columns(
    [1.5, 1, 1, 1.5]
)

with hero2:
    st.button(
        "Start Analyzing",
        use_container_width=True,
        type="primary",
    )

with hero3:
    st.button(
        "See How It Works",
        use_container_width=True,
    )


# ============================================================
# REAL DACRE DASHBOARD
# ============================================================

st.markdown(
    """
<div class="dashboard">

    <div class="dashboard-header">

        <div>

            <div class="dashboard-title">
                REAL DACRE DASHBOARD
            </div>

            <div class="dashboard-subtitle">
                Live analytical environment preview
            </div>

        </div>

        <div class="system-ready">
            ● SYSTEM READY
        </div>

    </div>

</div>
""",
    unsafe_allow_html=True,
)


m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        """
<div class="metric">

    <div class="metric-label">
        TOTAL RECORDS
    </div>

    <div class="metric-number">
        128,420
    </div>

    <div class="metric-up">
        ↑ 12.8%
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

with m2:
    st.markdown(
        """
<div class="metric">

    <div class="metric-label">
        CLEAN DATA
    </div>

    <div class="metric-number">
        96.4%
    </div>

    <div class="metric-gold">
        ↑ 4.2%
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

with m3:
    st.markdown(
        """
<div class="metric">

    <div class="metric-label">
        INSIGHTS
    </div>

    <div class="metric-number">
        2,481
    </div>

    <div class="metric-blue">
        ↑ 18.1%
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

with m4:
    st.markdown(
        """
<div class="metric">

    <div class="metric-label">
        ACCURACY
    </div>

    <div class="metric-number">
        98.7%
    </div>

    <div class="metric-up">
        ↑ 2.6%
    </div>

</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# DASHBOARD CHARTS
# ============================================================

months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]

performance = pd.DataFrame(
    {
        "Performance": [
            430,
            480,
            520,
            570,
            610,
            650,
            700,
            760,
            800,
            850,
            910,
            980,
        ]
    },
    index=months,
)

business = pd.DataFrame(
    {
        "Score": [
            91,
            78,
            86,
            95,
        ]
    },
    index=[
        "Sales",
        "Marketing",
        "Operations",
        "Customers",
    ],
)


chart_left, chart_right = st.columns([1.6, 1])

with chart_left:

    st.markdown(
        """
<div class="demo-panel">

    <div class="demo-label">
        PERFORMANCE OVERVIEW
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    st.line_chart(
        performance,
        height=270,
    )


with chart_right:

    st.markdown(
        """
<div class="demo-panel">

    <div class="demo-label">
        BUSINESS AREAS
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    st.bar_chart(
        business,
        height=270,
    )


# ============================================================
# TRUST
# ============================================================

st.markdown(
    """
<div class="trust">

    BUILT FOR MODERN DATA TEAMS
    &nbsp; • &nbsp;
    ANALYSTS
    &nbsp; • &nbsp;
    BUSINESSES
    &nbsp; • &nbsp;
    ORGANIZATIONS

</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# PLATFORM
# ============================================================

st.markdown(
    """
<div class="section">

    <div class="section-label">
        THE DACRE PLATFORM
    </div>

    <div class="section-title">
        Everything you need to<br>
        understand your data.
    </div>

    <div class="section-description">
        DACRE brings data preparation, analysis,
        visualization, David Intelligence and reporting
        into one professional analytical environment.
    </div>

</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# FEATURES
# ============================================================

features = [
    (
        "blue-icon",
        "✦",
        "Data Cleaning",
        "Detect missing values, duplicates, inconsistent "
        "records and common data-quality problems before "
        "analysis begins.",
    ),
    (
        "gold-icon",
        "▥",
        "Advanced Analysis",
        "Transform raw datasets into meaningful statistics, "
        "trends, patterns and business information.",
    ),
    (
        "green-icon",
        "◉",
        "Visualization",
        "Convert complex information into clear dashboards, "
        "charts and visual reports.",
    ),
    (
        "purple-icon",
        "⚡",
        "Fast Processing",
        "Process analytical workloads efficiently through "
        "a streamlined analytical workflow.",
    ),
    (
        "blue-icon",
        "◆",
        "David Intelligence",
        "David Intelligence helps users interact with data, "
        "ask questions and obtain useful analytical assistance.",
    ),
    (
        "gold-icon",
        "⇩",
        "Export & Reporting",
        "Prepare analytical results for reporting, presentation "
        "and continued business use.",
    ),
]


for start in range(0, len(features), 3):

    current = features[start:start + 3]

    cols = st.columns(3)

    for i, feature in enumerate(current):

        icon_class, icon, title, description = feature

        with cols[i]:

            st.markdown(
                f"""
<div class="feature-card">

    <div class="feature-icon {icon_class}">
        {icon}
    </div>

    <div class="feature-title">
        {title}
    </div>

    <div class="feature-text">
        {description}
    </div>

</div>
""",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# LIVE EXPERIENCE
# ============================================================

st.markdown(
    """
<div class="section">

    <div class="section-label">
        LIVE EXPERIENCE
    </div>

    <div class="section-title">
        See DACRE in action.
    </div>

    <div class="section-description">
        A professional analytical workspace where raw data
        becomes information, information becomes insight,
        and insight supports decisions.
    </div>

</div>
""",
    unsafe_allow_html=True,
)


demo_data = pd.DataFrame(
    {
        "Revenue": [
            82000,
            97000,
            103000,
            118000,
            132000,
            148000,
        ],
        "Customers": [
            420,
            510,
            570,
            640,
            730,
            820,
        ],
        "Orders": [
            280,
            340,
            410,
            470,
            550,
            630,
        ],
    }
)


demo_left, demo_right = st.columns([1.35, 1])

with demo_left:

    st.markdown(
        """
<div class="demo-panel">

    <div class="demo-label">
        ANALYTICAL DATA
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    st.dataframe(
        demo_data,
        use_container_width=True,
        hide_index=True,
    )


with demo_right:

    st.markdown(
        """
<div class="demo-panel">

    <div class="demo-label">
        AUTOMATED OBSERVATIONS
    </div>

    <br>

    <b>Revenue trend</b>
    <br>
    <span style="color:#49e58a;">
        ● Positive
    </span>

    <br><br>

    <b>Customer activity</b>
    <br>
    <span style="color:#55b8ff;">
        ● Increasing
    </span>

    <br><br>

    <b>Data quality</b>
    <br>
    <span style="color:#ffdc73;">
        ● High
    </span>

    <br><br>

    <b>Operational signal</b>
    <br>
    <span style="color:#a875ff;">
        ● Stable
    </span>

</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# DAVID INTELLIGENCE
# ============================================================

st.markdown(
    """
<div class="di-panel">

    <div class="section-label">
        DAVID INTELLIGENCE
    </div>

    <div class="di-title">
        Meet <span class="di-highlight">DI.</span>
    </div>

    <div class="section-description">
        David Intelligence is the intelligence layer of DACRE.
        DI is designed to help users ask questions about their
        information, explore patterns, understand analytical
        results and move from analysis toward informed decisions.
    </div>

    <div class="di-flow">

        Ask questions

        <span class="di-arrow">→</span>

        Analyze

        <span class="di-arrow">→</span>

        Visualize

        <span class="di-arrow">→</span>

        Decide

    </div>

</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SECURITY
# ============================================================

st.markdown(
    """
<div class="section">

    <div class="section-label">
        TRUST
    </div>

    <div class="section-title">
        Security • Reliability • Privacy
    </div>

    <div class="section-description">
        DACRE is being designed with responsible handling
        of data, controlled access and a reliable analytical
        environment as core principles.
    </div>

</div>
""",
    unsafe_allow_html=True,
)


sec1, sec2, sec3 = st.columns(3)

with sec1:
    st.markdown(
        """
<div class="security-card">

    <div class="security-title">
        🔐 Security
    </div>

    <div class="security-text">
        Protect analytical environments with secure
        authentication and controlled access.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

with sec2:
    st.markdown(
        """
<div class="security-card">

    <div class="security-title">
        ⚙️ Reliability
    </div>

    <div class="security-text">
        Build dependable analytical workflows designed
        to operate consistently.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

with sec3:
    st.markdown(
        """
<div class="security-card">

    <div class="security-title">
        🛡️ Privacy
    </div>

    <div class="security-text">
        Give users greater control over their data and
        analytical information.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# PRICING
# ============================================================

st.markdown(
    """
<div class="section">

    <div class="section-label">
        PLANS
    </div>

    <div class="section-title">
        Pricing
    </div>

    <div class="section-description">
        Flexible plans will be introduced as the DACRE
        platform grows.
    </div>

</div>
""",
    unsafe_allow_html=True,
)


price1, price2, price3 = st.columns(3)

with price1:

    st.markdown(
        """
<div class="price-card">

    <div class="price-name">
        STARTER
    </div>

    <div class="price">
        Free
    </div>

    <div class="price-text">
        Explore the DACRE analytical environment.
    </div>

    <div class="price-list">
        ✓ Basic analysis<br>
        ✓ Basic visualization<br>
        ✓ Data exploration<br>
        ✓ DACRE dashboard
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

with price2:

    st.markdown(
        """
<div class="price-card featured">

    <div class="price-name">
        PROFESSIONAL
    </div>

    <div class="price">
        Coming Soon
    </div>

    <div class="price-text">
        Designed for analysts and professional users.
    </div>

    <div class="price-list">
        ✓ Advanced analysis<br>
        ✓ Advanced dashboards<br>
        ✓ David Intelligence<br>
        ✓ Reporting
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

with price3:

    st.markdown(
        """
<div class="price-card">

    <div class="price-name">
        BUSINESS
    </div>

    <div class="price">
        Coming Soon
    </div>

    <div class="price-text">
        Built for teams and organizations.
    </div>

    <div class="price-list">
        ✓ Team analytics<br>
        ✓ Organization dashboards<br>
        ✓ Advanced reporting<br>
        ✓ Enterprise controls
    </div>

</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# FAQ
# ============================================================

st.markdown(
    """
<div class="section">

    <div class="section-label">
        QUESTIONS
    </div>

    <div class="section-title">
        Frequently asked questions.
    </div>

</div>
""",
    unsafe_allow_html=True,
)


with st.expander("What is DACRE Analysis?"):
    st.write(
        "DACRE Analysis is the analytical platform being "
        "developed by DACREglobal limited."
    )

with st.expander("What is David Intelligence?"):
    st.write(
        "David Intelligence, or DI, is the intelligence layer "
        "being developed for the DACRE platform."
    )

with st.expander("Can I upload my own data?"):
    st.write(
        "Yes. DACRE is designed to support user datasets "
        "for analysis and visualization."
    )

with st.expander("Will DACRE have dashboards?"):
    st.write(
        "Yes. Interactive dashboards, charts and analytical "
        "workspaces are part of the DACRE platform."
    )

with st.expander("Can DI use online information?"):
    st.write(
        "When connected to approved online services and APIs, "
        "DI can use external information sources as part "
        "of its knowledge workflow."
    )


# ============================================================
# FINAL CTA
# ============================================================

st.markdown(
    """
<div class="cta">

    <div class="section-label">
        DACREGLOBAL LIMITED
    </div>

    <div class="cta-title">
        Ready to understand your data?
    </div>

    <div class="section-description"
         style="margin:20px auto 30px;">
        Start building a smarter analytical workflow
        with DACRE Analysis.
    </div>

</div>
""",
    unsafe_allow_html=True,
)


_, cta_button, _ = st.columns([1, 1.2, 1])

with cta_button:
    st.button(
        "Get Started with DACRE",
        use_container_width=True,
        type="primary",
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">

    <strong>
        DACREglobal limited
    </strong>

    <br><br>

    DACRE Analysis
    &nbsp; • &nbsp;
    Product
    &nbsp; • &nbsp;
    Solutions
    &nbsp; • &nbsp;
    Resources
    &nbsp; • &nbsp;
    Company
    &nbsp; • &nbsp;
    Contact
    &nbsp; • &nbsp;
    Legal

    <br><br>

    © 2026 DACREglobal limited.
    All rights reserved.

</div>
""",
    unsafe_allow_html=True,
)
