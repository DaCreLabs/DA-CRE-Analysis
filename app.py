import os
import streamlit as st
import numpy as np
import pandas as pd

# ============================================================
# DACREGLOBAL LIMITED
# DACRE ANALYSIS
# APPLICATION CONFIGURATION
# ============================================================

# Exact DACRE logo location
LOGO_PATH = "assets/dacre_logo.png"

# Make sure the actual DACRE logo exists
if not os.path.exists(LOGO_PATH):
    st.error(
        "DACRE LOGO NOT FOUND: Please make sure the exact "
        "DACRE logo is uploaded as assets/dacre_logo.png"
    )
    st.stop()

# ============================================================
# STREAMLIT PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="DACREglobal limited | DACRE Analysis",
    page_icon=LOGO_PATH,
    layout="wide",
    initial_sidebar_state="collapsed",
)
    """
<style>

@import url(
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap'
);

:root {
    --black: #050608;
    --black2: #090c12;
    --blue: #1769ff;
    --blue2: #37a4ff;
    --gold: #e9b949;
    --gold2: #ffd86a;
    --green: #45e58a;
    --white: #ffffff;
    --muted: #9ba5b8;
    --border: rgba(255,255,255,0.09);
}

html {
    scroll-behavior: smooth;
}

body {
    font-family: 'Inter', sans-serif;
}

.stApp {

    background:

        radial-gradient(
            circle at 8% 8%,
            rgba(23,105,255,0.16),
            transparent 25%
        ),

        radial-gradient(
            circle at 88% 12%,
            rgba(233,185,73,0.11),
            transparent 23%
        ),

        radial-gradient(
            circle at 55% 58%,
            rgba(69,229,138,0.055),
            transparent 28%
        ),

        linear-gradient(
            135deg,
            #030405 0%,
            #070a10 38%,
            #05070b 70%,
            #090806 100%
        );

    color: white;
}

.main .block-container {
    max-width: 1450px;
    padding-top: 0.5rem;
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
   TOP NAV
   ============================================================ */

.dacre-nav {

    border-bottom:
        1px solid rgba(255,255,255,0.08);

    padding:
        13px 0 16px 0;

    margin-bottom:
        10px;
}

.brand {

    font-size:
        1.18rem;

    font-weight:
        900;

    letter-spacing:
        -0.035em;

    color:
        white;
}

.brand span {
    color:
        var(--gold);
}

.brand-small {

    font-size:
        0.62rem;

    letter-spacing:
        0.22em;

    color:
        #758096;

    text-transform:
        uppercase;

    margin-top:
        2px;
}

.nav-text {

    color:
        #aeb8c9;

    font-size:
        0.83rem;

    font-weight:
        600;

    padding-top:
        11px;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {

    min-height:
        43px;

    border-radius:
        11px !important;

    font-weight:
        750 !important;

    border:
        1px solid rgba(255,255,255,0.12) !important;

    background:
        rgba(255,255,255,0.045) !important;

    color:
        white !important;

    transition:
        all 0.2s ease;
}

.stButton > button:hover {

    transform:
        translateY(-2px);

    border-color:
        rgba(233,185,73,0.55) !important;

    box-shadow:
        0 10px 30px rgba(0,0,0,0.3);
}


/* ============================================================
   HERO
   ============================================================ */

.hero {

    text-align:
        center;

    padding:
        90px 15px 35px;
}

.hero-kicker {

    display:
        inline-block;

    padding:
        8px 17px;

    border-radius:
        50px;

    border:
        1px solid rgba(233,185,73,0.3);

    background:
        linear-gradient(
            90deg,
            rgba(233,185,73,0.09),
            rgba(23,105,255,0.08)
        );

    color:
        var(--gold2);

    font-size:
        0.69rem;

    font-weight:
        800;

    letter-spacing:
        0.2em;

    text-transform:
        uppercase;

    box-shadow:
        0 0 30px rgba(233,185,73,0.06);
}

.hero-title {

    margin:
        25px 0 0;

    font-size:
        clamp(3.4rem, 8vw, 7rem);

    line-height:
        0.92;

    font-weight:
        900;

    letter-spacing:
        -0.065em;

    background:

        linear-gradient(
            100deg,
            #ffffff 0%,
            #ffffff 28%,
            #5eacff 48%,
            #3d83ff 63%,
            #f4ca61 82%,
            #ffffff 100%
        );

    -webkit-background-clip:
        text;

    -webkit-text-fill-color:
        transparent;

    background-clip:
        text;
}

.hero-subtitle {

    margin-top:
        27px;

    font-size:
        clamp(1.25rem, 2.5vw, 2rem);

    font-weight:
        750;

    color:
        #ffffff;
}

.hero-description {

    max-width:
        790px;

    margin:
        20px auto 0;

    color:
        var(--muted);

    line-height:
        1.8;

    font-size:
        1rem;
}


/* ============================================================
   DASHBOARD
   ============================================================ */

.dashboard {

    margin-top:
        65px;

    padding:
        16px;

    border-radius:
        25px;

    border:
        1px solid rgba(255,255,255,0.1);

    background:

        linear-gradient(
            135deg,
            rgba(20,27,42,0.94),
            rgba(8,10,15,0.97)
        );

    box-shadow:

        0 35px 100px rgba(0,0,0,0.55),

        0 0 80px rgba(23,105,255,0.06),

        inset 0 1px 0
        rgba(255,255,255,0.06);
}

.dashboard-header {

    display:
        flex;

    justify-content:
        space-between;

    align-items:
        center;

    padding:
        7px 8px 17px;
}

.dashboard-name {

    font-weight:
        800;

    font-size:
        0.9rem;

    color:
        white;
}

.dashboard-sub {

    color:
        #77839a;

    font-size:
        0.69rem;

    margin-top:
        3px;
}

.live {

    color:
        var(--green);

    font-size:
        0.68rem;

    font-weight:
        800;

    letter-spacing:
        0.08em;
}

.metric {

    min-height:
        125px;

    border-radius:
        17px;

    border:
        1px solid rgba(255,255,255,0.07);

    padding:
        19px;

    background:
        rgba(255,255,255,0.035);
}

.metric-label {

    color:
        #7f8ba0;

    font-size:
        0.67rem;

    letter-spacing:
        0.13em;

    font-weight:
        700;
}

.metric-value {

    font-size:
        1.75rem;

    font-weight:
        900;

    margin-top:
        9px;

    color:
        white;
}

.metric-green {

    color:
        var(--green);

    font-size:
        0.7rem;

    font-weight:
        700;

    margin-top:
        4px;
}

.metric-gold {

    color:
        var(--gold2);

    font-size:
        0.7rem;

    font-weight:
        700;

    margin-top:
        4px;
}

.metric-blue {

    color:
        var(--blue2);

    font-size:
        0.7rem;

    font-weight:
        700;

    margin-top:
        4px;
}


/* ============================================================
   SECTIONS
   ============================================================ */

.section {
    padding-top:
        105px;
}

.eyebrow {

    color:
        var(--gold);

    font-size:
        0.68rem;

    font-weight:
        850;

    letter-spacing:
        0.2em;

    text-transform:
        uppercase;

    margin-bottom:
        13px;
}

.section-title {

    color:
        white;

    font-size:
        clamp(2rem, 4vw, 3.6rem);

    line-height:
        1.05;

    letter-spacing:
        -0.045em;

    font-weight:
        900;

    margin:
        0;
}

.section-description {

    color:
        #919caf;

    max-width:
        760px;

    line-height:
        1.8;

    margin-top:
        18px;
}


/* ============================================================
   FEATURE CARDS
   ============================================================ */

.feature {

    height:
        100%;

    min-height:
        255px;

    padding:
        28px;

    border-radius:
        21px;

    border:
        1px solid rgba(255,255,255,0.08);

    background:

        linear-gradient(
            145deg,
            rgba(255,255,255,0.055),
            rgba(255,255,255,0.018)
        );

    transition:
        0.25s ease;
}

.feature:hover {

    transform:
        translateY(-6px);

    border-color:
        rgba(233,185,73,0.35);

    box-shadow:
        0 22px 60px rgba(0,0,0,0.3);
}

.icon-blue,
.icon-gold,
.icon-green,
.icon-purple {

    width:
        52px;

    height:
        52px;

    border-radius:
        15px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    font-size:
        1.3rem;

    margin-bottom:
        21px;
}

.icon-blue {

    background:
        rgba(23,105,255,0.13);

    border:
        1px solid rgba(55,164,255,0.23);
}

.icon-gold {

    background:
        rgba(233,185,73,0.12);

    border:
        1px solid rgba(233,185,73,0.24);
}

.icon-green {

    background:
        rgba(69,229,138,0.1);

    border:
        1px solid rgba(69,229,138,0.2);
}

.icon-purple {

    background:
        rgba(146,92,255,0.11);

    border:
        1px solid rgba(146,92,255,0.23);
}

.feature-title {

    font-size:
        1.05rem;

    font-weight:
        800;

    color:
        white;
}

.feature-text {

    color:
        #8995aa;

    font-size:
        0.85rem;

    line-height:
        1.75;

    margin-top:
        10px;
}


/* ============================================================
   DEMO AREA
   ============================================================ */

.demo-panel {

    border-radius:
        23px;

    padding:
        23px;

    border:
        1px solid rgba(255,255,255,0.08);

    background:
        rgba(255,255,255,0.025);
}

.demo-heading {

    font-size:
        0.72rem;

    color:
        #7f8ca2;

    letter-spacing:
        0.13em;

    font-weight:
        800;

    margin-bottom:
        12px;
}


/* ============================================================
   DI PANEL
   ============================================================ */

.di {

    margin-top:
        105px;

    padding:
        55px;

    border-radius:
        28px;

    border:
        1px solid rgba(233,185,73,0.2);

    background:

        radial-gradient(
            circle at 80% 20%,
            rgba(23,105,255,0.17),
            transparent 28%
        ),

        radial-gradient(
            circle at 15% 80%,
            rgba(233,185,73,0.11),
            transparent 28%
        ),

        linear-gradient(
            135deg,
            rgba(16,20,29,0.96),
            rgba(6,8,12,0.97)
        );

    box-shadow:
        0 30px 90px rgba(0,0,0,0.35);
}

.di-title {

    font-size:
        clamp(2.4rem, 5vw, 4.4rem);

    font-weight:
        900;

    letter-spacing:
        -0.055em;

    color:
        white;
}

.di-name {
    color:
        var(--gold2);
}

.di-flow {

    margin-top:
        30px;

    font-weight:
        750;

    color:
        white;
}

.di-flow span {

    color:
        var(--gold);

    padding:
        0 8px;
}


/* ============================================================
   TRUST
   ============================================================ */

.trust {

    margin-top:
        70px;

    padding:
        24px;

    border-top:
        1px solid rgba(255,255,255,0.07);

    border-bottom:
        1px solid rgba(255,255,255,0.07);

    text-align:
        center;

    color:
        #78859a;

    font-size:
        0.72rem;

    letter-spacing:
        0.1em;

    text-transform:
        uppercase;
}


/* ============================================================
   SECURITY
   ============================================================ */

.security {

    height:
        100%;

    padding:
        29px;

    border-radius:
        20px;

    background:
        rgba(255,255,255,0.025);

    border:
        1px solid rgba(255,255,255,0.07);
}

.security h3 {
    color:
        white !important;

    font-size:
        1rem;
}

.security p {
    color:
        #8995aa;
    line-height:
        1.7;
}


/* ============================================================
   PRICING
   ============================================================ */

.price-card {

    height:
        100%;

    padding:
        31px;

    border-radius:
        23px;

    border:
        1px solid rgba(255,255,255,0.08);

    background:
        rgba(255,255,255,0.025);
}

.price-card.featured {

    border-color:
        rgba(233,185,73,0.38);

    background:

        linear-gradient(
            145deg,
            rgba(233,185,73,0.07),
            rgba(23,105,255,0.05)
        );

    box-shadow:
        0 25px 70px rgba(0,0,0,0.28);
}

.price-label {

    color:
        var(--gold);

    font-size:
        0.67rem;

    letter-spacing:
        0.16em;

    font-weight:
        850;
}

.price {

    font-size:
        2.35rem;

    font-weight:
        900;

    margin:
        14px 0;

    color:
        white;
}

.check {
    color:
        #c3cbd9;

    line-height:
        2;
}


/* ============================================================
   CTA
   ============================================================ */

.cta {

    margin-top:
        110px;

    padding:
        80px 25px;

    text-align:
        center;

    border-radius:
        30px;

    border:
        1px solid rgba(233,185,73,0.23);

    background:

        radial-gradient(
            circle at center,
            rgba(23,105,255,0.15),
            transparent 48%
        ),

        radial-gradient(
            circle at 75% 100%,
            rgba(233,185,73,0.11),
            transparent 35%
        ),

        #07090d;
}

.cta-title {

    font-size:
        clamp(2.3rem, 5vw, 4.5rem);

    font-weight:
        900;

    letter-spacing:
        -0.055em;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {

    margin-top:
        100px;

    padding:
        42px 0 20px;

    border-top:
        1px solid rgba(255,255,255,0.07);

    color:
        #69758a;

    font-size:
        0.77rem;

    text-align:
        center;
}

.footer strong {
    color:
        white;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 768px) {

    .hero {
        padding-top:
            55px;
    }

    .hero-title {
        font-size:
            3.3rem;
    }

    .di {
        padding:
            30px;
    }

    .dashboard {
        margin-top:
            40px;
    }

}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# NAVIGATION
# ============================================================

nav1, nav2, nav3, nav4, nav5, nav6 = st.columns(
    [2.7, 1, 1, 1, 1, 1.45]
)

with nav1:

    if os.path.exists(LOGO_PATH):
        st.image(
            LOGO_PATH,
            width=48,
        )

    st.markdown(
        """
        <div class="brand">
            DACRE<span>global</span> limited
        </div>

        <div class="brand-small">
            DACRE Analysis
        </div>
        """,
        unsafe_allow_html=True,
    )

with nav2:
    st.markdown(
        '<div class="nav-text">Product</div>',
        unsafe_allow_html=True,
    )

with nav3:
    st.markdown(
        '<div class="nav-text">Solutions</div>',
        unsafe_allow_html=True,
    )

with nav4:
    st.markdown(
        '<div class="nav-text">Resources</div>',
        unsafe_allow_html=True,
    )

with nav5:
    st.markdown(
        '<div class="nav-text">Company</div>',
        unsafe_allow_html=True,
    )

with nav6:
    st.button(
        "Get Started",
        use_container_width=True,
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="hero">

    <div class="hero-kicker">
        DACREGLOBAL LIMITED
    </div>

    <div class="hero-title">
        DACRE ANALYSIS
    </div>

    <div class="hero-subtitle">
        Turn your data into decisions.
    </div>

    <div class="hero-description">
        A modern data analysis platform for businesses,
        analysts and organizations. Transform raw information
        into clear insights, powerful visualizations and
        decisions that move your work forward.
    </div>

</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HERO BUTTONS
# ============================================================

_, hero_btn1, hero_btn2, _ = st.columns(
    [1.3, 1, 1, 1.3]
)

with hero_btn1:
    st.button(
        "Start Analyzing",
        use_container_width=True,
        type="primary",
    )

with hero_btn2:
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
            <div class="dashboard-name">
                REAL DACRE DASHBOARD
            </div>

            <div class="dashboard-sub">
                Analytical workspace preview
            </div>
        </div>

        <div class="live">
            ● SYSTEM READY
        </div>

    </div>

</div>
""",
    unsafe_allow_html=True,
)


metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.markdown(
        """
<div class="metric">

    <div class="metric-label">
        TOTAL RECORDS
    </div>

    <div class="metric-value">
        128,420
    </div>

    <div class="metric-green">
        ↑ 12.8% this period
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

with metric2:
    st.markdown(
        """
<div class="metric">

    <div class="metric-label">
        DATA QUALITY
    </div>

    <div class="metric-value">
        96.4%
    </div>

    <div class="metric-gold">
        ↑ 4.2% improvement
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

with metric3:
    st.markdown(
        """
<div class="metric">

    <div class="metric-label">
        INSIGHTS
    </div>

    <div class="metric-value">
        2,481
    </div>

    <div class="metric-blue">
        ↑ 18.1% discovered
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

with metric4:
    st.markdown(
        """
<div class="metric">

    <div class="metric-label">
        ANALYSIS ACCURACY
    </div>

    <div class="metric-value">
        98.7%
    </div>

    <div class="metric-green">
        ↑ 2.6% improvement
    </div>

</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# DASHBOARD CHARTS
# ============================================================

np.random.seed(14)

months = [
    "Jan", "Feb", "Mar", "Apr",
    "May", "Jun", "Jul", "Aug",
    "Sep", "Oct", "Nov", "Dec"
]

performance = np.array(
    [470, 530, 510, 620, 680, 650,
     720, 790, 760, 850, 910, 970]
)

performance_data = pd.DataFrame(
    {
        "Month": months,
        "Performance": performance,
    }
)

business_data = pd.DataFrame(
    {
        "Area": [
            "Sales",
            "Marketing",
            "Operations",
            "Customers",
        ],
        "Score": [
            92,
            76,
            84,
            88,
        ],
    }
)

st.markdown("<br>", unsafe_allow_html=True)

chart1, chart2 = st.columns([1.6, 1])

with chart1:

    st.markdown(
        """
<div class="demo-panel">

    <div class="demo-heading">
        PERFORMANCE OVERVIEW
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    st.line_chart(
        performance_data.set_index("Month"),
        height=270,
    )

with chart2:

    st.markdown(
        """
<div class="demo-panel">

    <div class="demo-heading">
        BUSINESS PERFORMANCE
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    st.bar_chart(
        business_data.set_index("Area"),
        height=270,
    )


# ============================================================
# TRUST STRIP
# ============================================================

st.markdown(
    """
<div class="trust">

    MODERN DATA TEAMS
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
# PLATFORM SECTION
# ============================================================

st.markdown(
    """
<div class="section">

    <div class="eyebrow">
        THE DACRE PLATFORM
    </div>

    <div class="section-title">
        Everything you need to<br>
        understand your data.
    </div>

    <div class="section-description">
        DACRE brings data preparation, analysis,
        visualization, intelligence and reporting
        together in one professional environment.
    </div>

</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# FEATURE CARDS
# ============================================================

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown(
        """
<div class="feature">

    <div class="icon-blue">
        ◈
    </div>

    <div class="feature-title">
        Data Cleaning
    </div>

    <div class="feature-text">
        Detect duplicates, missing information,
        inconsistent records and data-quality
        problems before analysis begins.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

with f2:
    st.markdown(
        """
<div class="feature">

    <div class="icon-gold">
        ◇
    </div>

    <div class="feature-title">
        Advanced Analysis
    </div>

    <div class="feature-text">
        Transform raw datasets into meaningful
        statistics, trends, relationships and
        business information.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

with f3:
    st.markdown(
        """
<div class="feature">

    <div class="icon-green">
        ◎
    </div>

    <div class="feature-title">
        Visualization
    </div>

    <div class="feature-text">
        Turn complex information into interactive
        charts, dashboards and visual reports
        that are easier to understand.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )


st.markdown("<br>", unsafe_allow_html=True)


f4, f5, f6 = st.columns(3)

with f4:
    st.markdown(
        """
<div class="feature">

    <div class="icon-purple">
        ⚡
    </div>

    <div class="feature-title">
        Fast Processing
    </div>

    <div class="feature-text">
        Build efficient workflows for processing
        and exploring analytical datasets.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

with f5:
    st.markdown(
        """
<div class="feature">

    <div class="icon-blue">
        ✦
    </div>

    <div class="feature-title">
        David Intelligence
    </div>

    <div class="feature-text">
        DI helps users interact with their data,
        ask questions and receive analytical
        assistance through the DACRE platform.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

with f6:
    st.markdown(
        """
<div class="feature">

    <div class="icon-gold">
        ⇩
    </div>

    <div class="feature-title">
        Export & Reporting
    </div>

    <div class="feature-text">
        Prepare analytical results for reporting,
        presentation and continued business use.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# LIVE EXPERIENCE
# ============================================================

st.markdown(
    """
<div class="section">

    <div class="eyebrow">
        LIVE EXPERIENCE
    </div>

    <div class="section-title">
        See DACRE in action.
    </div>

    <div class="section-description">
        Raw data becomes information.
        Information becomes insight.
        Insight supports decisions.
    </div>

</div>
""",
    unsafe_allow_html=True,
)


demo_left, demo_right = st.columns([1.35, 1])


with demo_left:

    demo = pd.DataFrame(
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

    st.markdown(
        """
<div class="demo-panel">

    <div class="demo-heading">
        ANALYTICAL DATA
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    st.dataframe(
        demo,
        use_container_width=True,
        hide_index=True,
    )


with demo_right:

    st.markdown(
        """
<div class="demo-panel">

    <div class="demo-heading">
        DACRE OBSERVATIONS
    </div>

    <br>

    <b>Revenue trend</b>

    <br>

    <span style="color:#45e58a;">
        ● Positive
    </span>

    <br><br>

    <b>Customer activity</b>

    <br>

    <span style="color:#37a4ff;">
        ● Increasing
    </span>

    <br><br>

    <b>Data quality</b>

    <br>

    <span style="color:#ffd86a;">
        ● High
    </span>

    <br><br>

    <b>Operational signal</b>

    <br>

    <span style="color:#c99cff;">
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
<div class="di">

    <div class="eyebrow">
        DAVID INTELLIGENCE
    </div>

    <div class="di-title">
        Meet <span class="di-name">DI.</span>
    </div>

    <div class="section-description">
        David Intelligence is the intelligence layer of DACRE.
        It is designed to help users ask questions about their
        information, explore patterns, understand analytical
        results and move from information toward decisions.
    </div>

    <div class="di-flow">

        Ask questions
        <span>→</span>
        Analyze
        <span>→</span>
        Visualize
        <span>→</span>
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

    <div class="eyebrow">
        TRUST
    </div>

    <div class="section-title">
        Security • Reliability • Privacy
    </div>

    <div class="section-description">
        DACRE is being designed around responsible data
        handling, controlled access and dependable
        analytical workflows.
    </div>

</div>
""",
    unsafe_allow_html=True,
)


s1, s2, s3 = st.columns(3)

with s1:
    st.markdown(
        """
<div class="security">

    <h3>🔐 Security</h3>

    <p>
        Controlled access and secure application
        architecture for analytical environments.
    </p>

</div>
""",
        unsafe_allow_html=True,
    )

with s2:
    st.markdown(
        """
<div class="security">

    <h3>⚙️ Reliability</h3>

    <p>
        Dependable workflows designed to make
        analysis consistent and efficient.
    </p>

</div>
""",
        unsafe_allow_html=True,
    )

with s3:
    st.markdown(
        """
<div class="security">

    <h3>🛡️ Privacy</h3>

    <p>
        Responsible handling of information with
        user control at the center of the platform.
    </p>

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

    <div class="eyebrow">
        PLANS
    </div>

    <div class="section-title">
        Pricing
    </div>

    <div class="section-description">
        Flexible plans designed to grow with DACRE.
    </div>

</div>
""",
    unsafe_allow_html=True,
)


p1, p2, p3 = st.columns(3)

with p1:
    st.markdown(
        """
<div class="price-card">

    <div class="price-label">
        STARTER
    </div>

    <div class="price">
        Free
    </div>

    <p>
        Explore the DACRE analytical environment.
    </p>

    <div class="check">
        ✓ Basic analysis<br>
        ✓ Basic visualization<br>
        ✓ Data exploration<br>
        ✓ DACRE dashboard
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

with p2:
    st.markdown(
        """
<div class="price-card featured">

    <div class="price-label">
        PROFESSIONAL
    </div>

    <div class="price">
        Coming Soon
    </div>

    <p>
        Designed for analysts and professional users.
    </p>

    <div class="check">
        ✓ Advanced analysis<br>
        ✓ Advanced dashboards<br>
        ✓ David Intelligence<br>
        ✓ Reporting
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

with p3:
    st.markdown(
        """
<div class="price-card">

    <div class="price-label">
        BUSINESS
    </div>

    <div class="price">
        Coming Soon
    </div>

    <p>
        Built for teams and organizations.
    </p>

    <div class="check">
        ✓ Team analytics<br>
        ✓ Organization dashboards<br>
        ✓ Advanced reporting<br>
        ✓ Organization controls
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

    <div class="eyebrow">
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
        "DACRE Analysis is the data analysis platform "
        "being developed by DACREglobal limited."
    )

with st.expander("What does DI mean?"):
    st.write(
        "DI means David Intelligence. It is the intelligence "
        "layer being developed for the DACRE platform."
    )

with st.expander("Can I upload my own data?"):
    st.write(
        "Yes. The next stage of development will connect "
        "the platform to CSV, Excel and other data sources."
    )

with st.expander("Will DACRE have interactive dashboards?"):
    st.write(
        "Yes. Interactive dashboards, charts and analytical "
        "workspaces will be connected to the platform."
    )

with st.expander("Can DI use online information?"):
    st.write(
        "The architecture can connect DI to approved online "
        "services and APIs when the user is online."
    )


# ============================================================
# FINAL CTA
# ============================================================

st.markdown(
    """
<div class="cta">

    <div class="eyebrow">
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


_, final_button, _ = st.columns([1, 1.2, 1])

with final_button:
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
