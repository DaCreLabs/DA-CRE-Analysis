import os
import streamlit as st
import pandas as pd
import numpy as np


# ============================================================
# DACREGLOBAL LIMITED
# DACRE ANALYSIS PLATFORM
# Main Streamlit Application
# ============================================================

st.set_page_config(
    page_title="DACREglobal limited | DACRE Analysis",
    page_icon="assets/dacre_logo.png" if os.path.exists("assets/dacre_logo.png") else "📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       MAIN APPLICATION
    -------------------------------------------------------- */

    .stApp {
        background:
            radial-gradient(
                circle at 20% 10%,
                rgba(0, 102, 255, 0.08),
                transparent 28%
            ),
            radial-gradient(
                circle at 80% 30%,
                rgba(0, 220, 180, 0.05),
                transparent 25%
            ),
            #030814;
        color: #ffffff;
    }

    .main .block-container {
        max-width: 1450px;
        padding-top: 1rem;
        padding-bottom: 3rem;
    }

    /* Hide Streamlit branding */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* --------------------------------------------------------
       TEXT
    -------------------------------------------------------- */

    h1, h2, h3, h4 {
        color: #ffffff !important;
        letter-spacing: -0.03em;
    }

    p {
        color: #b8c2d8;
    }

    .muted {
        color: #8793aa;
    }

    .blue-text {
        color: #2f8cff;
    }

    .green-text {
        color: #6df58c;
    }

    /* --------------------------------------------------------
       TOP NAVIGATION
    -------------------------------------------------------- */

    .top-nav {
        width: 100%;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        padding: 12px 0 15px 0;
        margin-bottom: 20px;
    }

    .company-name {
        font-size: 1.15rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.03em;
    }

    .company-subtitle {
        font-size: 0.67rem;
        color: #71809b;
        letter-spacing: 0.18em;
        text-transform: uppercase;
    }

    .nav-item {
        color: #aab5ca;
        font-size: 0.88rem;
        text-decoration: none;
        padding: 8px 10px;
    }

    .nav-item:hover {
        color: #ffffff;
    }

    /* --------------------------------------------------------
       LOGO FALLBACK
    -------------------------------------------------------- */

    .logo-box {
        display: flex;
        align-items: center;
        gap: 11px;
    }

    .logo-symbol {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        background:
            linear-gradient(
                135deg,
                #0a50ff,
                #00a9ff 50%,
                #6df58c
            );
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 18px;
        font-weight: 900;
        box-shadow:
            0 0 25px rgba(0,132,255,0.35);
    }

    /* --------------------------------------------------------
       HERO
    -------------------------------------------------------- */

    .hero {
        padding: 75px 10px 45px 10px;
        text-align: center;
    }

    .hero-badge {
        display: inline-block;
        padding: 7px 15px;
        border-radius: 50px;
        border: 1px solid rgba(57,143,255,0.25);
        background: rgba(15,50,100,0.22);
        color: #62adff;
        font-size: 0.74rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 20px;
    }

    .hero-title {
        font-size: clamp(3rem, 7vw, 6.4rem);
        line-height: 0.95;
        font-weight: 900;
        margin: 0;
        background:
            linear-gradient(
                100deg,
                #ffffff 10%,
                #72b8ff 45%,
                #7dff9d 90%
            );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-tagline {
        font-size: clamp(1.3rem, 2.5vw, 2rem);
        font-weight: 700;
        color: #ffffff;
        margin-top: 22px;
    }

    .hero-description {
        max-width: 780px;
        margin: 20px auto 30px auto;
        font-size: 1.04rem;
        line-height: 1.8;
        color: #9da9bf;
    }

    /* --------------------------------------------------------
       DASHBOARD PREVIEW
    -------------------------------------------------------- */

    .dashboard-shell {
        margin-top: 55px;
        border: 1px solid rgba(77,126,202,0.25);
        background:
            linear-gradient(
                145deg,
                rgba(12,25,51,0.97),
                rgba(3,9,21,0.97)
            );
        border-radius: 24px;
        padding: 18px;
        box-shadow:
            0 30px 100px rgba(0,0,0,0.45),
            inset 0 1px 0 rgba(255,255,255,0.04);
    }

    .dashboard-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 7px 5px 16px 5px;
    }

    .dashboard-title {
        font-size: 0.92rem;
        font-weight: 800;
        color: #ffffff;
    }

    .status {
        color: #6df58c;
        font-size: 0.72rem;
        font-weight: 700;
    }

    .dashboard-card {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 18px;
        min-height: 110px;
    }

    .metric-label {
        color: #7d8ba4;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .metric-number {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 850;
        margin-top: 7px;
    }

    .metric-change {
        color: #6df58c;
        font-size: 0.73rem;
        margin-top: 5px;
    }

    /* --------------------------------------------------------
       SECTION
    -------------------------------------------------------- */

    .section {
        padding: 90px 0 35px 0;
    }

    .section-label {
        color: #4098ff;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        font-size: 0.72rem;
        font-weight: 800;
        margin-bottom: 12px;
    }

    .section-title {
        font-size: clamp(2rem, 4vw, 3.5rem);
        font-weight: 850;
        margin-bottom: 15px;
    }

    .section-description {
        max-width: 760px;
        color: #8e9bb2;
        line-height: 1.8;
        font-size: 1rem;
    }

    /* --------------------------------------------------------
       FEATURE CARDS
    -------------------------------------------------------- */

    .feature-card {
        height: 100%;
        min-height: 245px;
        border-radius: 20px;
        padding: 27px;
        border: 1px solid rgba(255,255,255,0.07);
        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.045),
                rgba(255,255,255,0.018)
            );
        transition: 0.25s ease;
    }

    .feature-card:hover {
        transform: translateY(-5px);
        border-color: rgba(51,143,255,0.4);
        box-shadow:
            0 20px 55px rgba(0,0,0,0.28);
    }

    .feature-icon {
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 15px;
        background: rgba(36,115,255,0.13);
        border: 1px solid rgba(55,143,255,0.2);
        font-size: 1.4rem;
        margin-bottom: 20px;
    }

    .feature-title {
        font-size: 1.08rem;
        font-weight: 800;
        color: white;
        margin-bottom: 10px;
    }

    .feature-text {
        color: #8996ad;
        line-height: 1.7;
        font-size: 0.88rem;
    }

    /* --------------------------------------------------------
       TRUST STRIP
    -------------------------------------------------------- */

    .trust-strip {
        margin-top: 70px;
        padding: 25px;
        border-top: 1px solid rgba(255,255,255,0.06);
        border-bottom: 1px solid rgba(255,255,255,0.06);
        text-align: center;
        color: #7e8ca4;
        font-size: 0.8rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    /* --------------------------------------------------------
       DI SECTION
    -------------------------------------------------------- */

    .di-panel {
        border: 1px solid rgba(70,145,255,0.22);
        background:
            radial-gradient(
                circle at 75% 30%,
                rgba(0,120,255,0.14),
                transparent 32%
            ),
            rgba(5,15,32,0.9);
        border-radius: 26px;
        padding: 45px;
        overflow: hidden;
    }

    .di-title {
        font-size: clamp(2rem, 4vw, 3.4rem);
        font-weight: 900;
    }

    .di-flow {
        margin-top: 25px;
        color: #dbe6f8;
        font-weight: 700;
        font-size: 1rem;
    }

    .di-flow span {
        color: #3d9bff;
        padding: 0 8px;
    }

    /* --------------------------------------------------------
       SECURITY
    -------------------------------------------------------- */

    .security-card {
        padding: 28px;
        border-radius: 20px;
        border: 1px solid rgba(109,245,140,0.12);
        background: rgba(109,245,140,0.025);
    }

    /* --------------------------------------------------------
       PRICING
    -------------------------------------------------------- */

    .pricing-card {
        border-radius: 23px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.025);
        padding: 30px;
        height: 100%;
    }

    .pricing-card.featured {
        border-color: rgba(50,145,255,0.42);
        box-shadow: 0 25px 70px rgba(0,70,180,0.13);
    }

    .price {
        font-size: 2.7rem;
        font-weight: 900;
        color: white;
        margin: 15px 0;
    }

    .price-small {
        font-size: 0.85rem;
        color: #7f8da6;
    }

    /* --------------------------------------------------------
       CTA
    -------------------------------------------------------- */

    .cta {
        text-align: center;
        margin-top: 100px;
        padding: 75px 25px;
        border-radius: 30px;
        border: 1px solid rgba(54,143,255,0.2);
        background:
            radial-gradient(
                circle at center,
                rgba(0,103,255,0.14),
                transparent 60%
            ),
            rgba(7,15,29,0.85);
    }

    .cta-title {
        font-size: clamp(2.2rem, 4vw, 4rem);
        font-weight: 900;
    }

    /* --------------------------------------------------------
       FOOTER
    -------------------------------------------------------- */

    .footer {
        margin-top: 90px;
        padding: 40px 0 20px 0;
        border-top: 1px solid rgba(255,255,255,0.07);
        color: #6e7b91;
        font-size: 0.8rem;
    }

    /* --------------------------------------------------------
       STREAMLIT BUTTONS
    -------------------------------------------------------- */

    .stButton > button {
        border-radius: 10px !important;
        min-height: 42px !important;
        font-weight: 750 !important;
        border: 1px solid rgba(77,150,255,0.25) !important;
    }

    .stButton > button:hover {
        border-color: rgba(77,150,255,0.65) !important;
        transform: translateY(-1px);
    }

    /* --------------------------------------------------------
       MOBILE
    -------------------------------------------------------- */

    @media (max-width: 768px) {

        .hero {
            padding-top: 45px;
        }

        .hero-title {
            font-size: 3.2rem;
        }

        .di-panel {
            padding: 28px;
        }

        .dashboard-shell {
            padding: 10px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "started" not in st.session_state:
    st.session_state.started = False


# ============================================================
# NAVIGATION HEADER
# ============================================================

nav1, nav2, nav3, nav4, nav5, nav6 = st.columns(
    [2.7, 1, 1, 1, 1, 1.4]
)

with nav1:
    logo_path = "assets/dacre_logo.png"

    if os.path.exists(logo_path):
        st.image(
            logo_path,
            width=45,
        )

    st.markdown(
        """
        <div class="company-name">
            DACREglobal limited
        </div>
        <div class="company-subtitle">
            DACRE Analysis
        </div>
        """,
        unsafe_allow_html=True,
    )

with nav2:
    if st.button("Product", use_container_width=True):
        st.session_state.page = "product"

with nav3:
    if st.button("Solutions", use_container_width=True):
        st.session_state.page = "solutions"

with nav4:
    if st.button("Resources", use_container_width=True):
        st.session_state.page = "resources"

with nav5:
    if st.button("Company", use_container_width=True):
        st.session_state.page = "company"

with nav6:
    c1, c2 = st.columns(2)

    with c1:
        if st.button("Sign in", use_container_width=True):
            st.session_state.page = "signin"

    with c2:
        if st.button("Get Started", use_container_width=True):
            st.session_state.started = True


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <section class="hero">

        <div class="hero-badge">
            DACREGLOBAL LIMITED
        </div>

        <h1 class="hero-title">
            DACRE ANALYSIS
        </h1>

        <div class="hero-tagline">
            Turn your data into decisions.
        </div>

        <div class="hero-description">
            Powerful data analysis, visualization and DI intelligence
            designed for businesses, analysts and organizations.
            Bring your data together, understand what it means,
            and make better decisions from it.
        </div>

    </section>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HERO BUTTONS
# ============================================================

b1, b2, b3 = st.columns([1, 1.1, 1])

with b1:
    st.write("")

with b2:
    x1, x2 = st.columns(2)

    with x1:
        if st.button(
            "Start Analyzing",
            use_container_width=True,
            type="primary",
        ):
            st.session_state.started = True

    with x2:
        if st.button(
            "See How It Works",
            use_container_width=True,
        ):
            st.session_state.page = "product"

with b3:
    st.write("")


# ============================================================
# STARTED MESSAGE
# ============================================================

if st.session_state.started:

    st.success(
        "DACRE Analysis is ready. Your analysis workspace will be connected here."
    )

    if st.button("Open DACRE Workspace"):
        st.session_state.page = "workspace"


# ============================================================
# DASHBOARD PREVIEW
# ============================================================

st.markdown(
    """
    <div class="dashboard-shell">

        <div class="dashboard-top">

            <div>
                <div class="dashboard-title">
                    REAL DACRE DASHBOARD
                </div>

                <div class="muted">
                    Live analytical environment preview
                </div>
            </div>

            <div class="status">
                ● SYSTEM READY
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DASHBOARD METRICS
# ============================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        """
        <div class="dashboard-card">
            <div class="metric-label">Records</div>
            <div class="metric-number">128,420</div>
            <div class="metric-change">↑ 12.8%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m2:
    st.markdown(
        """
        <div class="dashboard-card">
            <div class="metric-label">Clean Data</div>
            <div class="metric-number">96.4%</div>
            <div class="metric-change">↑ 4.2%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m3:
    st.markdown(
        """
        <div class="dashboard-card">
            <div class="metric-label">Insights</div>
            <div class="metric-number">2,481</div>
            <div class="metric-change">↑ 18.1%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m4:
    st.markdown(
        """
        <div class="dashboard-card">
            <div class="metric-label">Accuracy</div>
            <div class="metric-number">98.7%</div>
            <div class="metric-change">↑ 2.6%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SAMPLE DYNAMIC DATA
# ============================================================

np.random.seed(7)

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

values = np.random.randint(
    450,
    1000,
    size=12,
)

chart_data = pd.DataFrame(
    {
        "Month": months,
        "Performance": values,
    }
)

st.markdown("<br>", unsafe_allow_html=True)

chart_left, chart_right = st.columns([1.65, 1])

with chart_left:

    st.markdown(
        """
        <div class="dashboard-card">
            <div class="metric-label">
                PERFORMANCE OVERVIEW
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.line_chart(
        chart_data.set_index("Month"),
        height=260,
    )

with chart_right:

    category_data = pd.DataFrame(
        {
            "Category": [
                "Sales",
                "Customers",
                "Operations",
                "Marketing",
            ],
            "Value": [
                82,
                67,
                74,
                91,
            ],
        }
    )

    st.markdown(
        """
        <div class="dashboard-card">
            <div class="metric-label">
                BUSINESS AREAS
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.bar_chart(
        category_data.set_index("Category"),
        height=260,
    )


# ============================================================
# TRUST
# ============================================================

st.markdown(
    """
    <div class="trust-strip">
        Built for modern data teams &nbsp; • &nbsp;
        Analysts &nbsp; • &nbsp;
        Businesses &nbsp; • &nbsp;
        Organizations
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# EVERYTHING YOU NEED
# ============================================================

st.markdown(
    """
    <section class="section">

        <div class="section-label">
            THE DACRE PLATFORM
        </div>

        <div class="section-title">
            Everything you need to<br>
            understand your data.
        </div>

        <div class="section-description">
            DACRE brings data preparation, analysis, visualization,
            intelligence and reporting into one professional
            analytical environment.
        </div>

    </section>
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
        <div class="feature-card">

            <div class="feature-icon">
                🧹
            </div>

            <div class="feature-title">
                Data Cleaning
            </div>

            <div class="feature-text">
                Detect missing values, duplicates, inconsistent
                records and common data-quality problems before
                analysis begins.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

with f2:
    st.markdown(
        """
        <div class="feature-card">

            <div class="feature-icon">
                📊
            </div>

            <div class="feature-title">
                Advanced Analysis
            </div>

            <div class="feature-text">
                Transform raw datasets into meaningful statistics,
                trends, patterns and business information.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

with f3:
    st.markdown(
        """
        <div class="feature-card">

            <div class="feature-icon">
                📈
            </div>

            <div class="feature-title">
                Visualization
            </div>

            <div class="feature-text">
                Convert complex information into clear dashboards,
                charts and visual reports that are easier to
                understand.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SECOND FEATURE ROW
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

f4, f5, f6 = st.columns(3)

with f4:
    st.markdown(
        """
        <div class="feature-card">

            <div class="feature-icon">
                ⚡
            </div>

            <div class="feature-title">
                Fast Processing
            </div>

            <div class="feature-text">
                Process analytical workloads efficiently and
                provide users with a streamlined workflow.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

with f5:
    st.markdown(
        """
        <div class="feature-card">

            <div class="feature-icon">
                🧠
            </div>

            <div class="feature-title">
                DI Intelligence
            </div>

            <div class="feature-text">
                David Intelligence is designed to help users
                interact with their data and obtain useful
                analytical assistance.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

with f6:
    st.markdown(
        """
        <div class="feature-card">

            <div class="feature-icon">
                📤
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
# SEE DACRE IN ACTION
# ============================================================

st.markdown(
    """
    <section class="section">

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

    </section>
    """,
    unsafe_allow_html=True,
)


demo_left, demo_right = st.columns([1.4, 1])

with demo_left:

    demo_data = pd.DataFrame(
        {
            "Revenue": np.random.randint(
                50000,
                150000,
                12,
            ),
            "Customers": np.random.randint(
                200,
                900,
                12,
            ),
            "Orders": np.random.randint(
                100,
                700,
                12,
            ),
        }
    )

    st.markdown(
        """
        <div class="dashboard-card">

            <div class="metric-label">
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
        <div class="dashboard-card">

            <div class="metric-label">
                AUTOMATED OBSERVATIONS
            </div>

            <br>

            <b>Revenue trend</b>
            <br>
            <span class="green-text">
                Positive
            </span>

            <br><br>

            <b>Customer activity</b>
            <br>
            <span class="blue-text">
                Increasing
            </span>

            <br><br>

            <b>Data quality</b>
            <br>
            <span class="green-text">
                High
            </span>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# DI INTELLIGENCE
# ============================================================

st.markdown(
    """
    <section class="section">

        <div class="di-panel">

            <div class="section-label">
                DAVID INTELLIGENCE
            </div>

            <div class="di-title">
                DI Intelligence
            </div>

            <div class="section-description">
                Ask questions about your data, explore patterns,
                understand results and move from analysis toward
                informed decisions.
            </div>

            <div class="di-flow">
                Ask questions
                <span>→</span>
                analyze
                <span>→</span>
                visualize
                <span>→</span>
                decide
            </div>

        </div>

    </section>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SECURITY
# ============================================================

st.markdown(
    """
    <section class="section">

        <div class="section-label">
            TRUST
        </div>

        <div class="section-title">
            Security • Reliability • Privacy
        </div>

        <div class="section-description">
            DACRE is being designed with responsible handling of
            data, controlled access and a reliable analytical
            environment as core principles.
        </div>

    </section>
    """,
    unsafe_allow_html=True,
)


s1, s2, s3 = st.columns(3)

with s1:
    st.markdown(
        """
        <div class="security-card">
            <h3>🔐 Security</h3>
            <p>
                Protect analytical environments with secure
                authentication and controlled access.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with s2:
    st.markdown(
        """
        <div class="security-card">
            <h3>⚙️ Reliability</h3>
            <p>
                Build dependable analytical workflows designed
                to operate consistently.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with s3:
    st.markdown(
        """
        <div class="security-card">
            <h3>🛡️ Privacy</h3>
            <p>
                Give users greater control over their data and
                analytical information.
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
    <section class="section">

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

    </section>
    """,
    unsafe_allow_html=True,
)


p1, p2, p3 = st.columns(3)

with p1:
    st.markdown(
        """
        <div class="pricing-card">

            <div class="metric-label">
                STARTER
            </div>

            <div class="price">
                Free
            </div>

            <p>
                Explore the DACRE analytical environment.
            </p>

            <br>

            ✓ Basic analysis<br>
            ✓ Basic visualization<br>
            ✓ Data exploration<br>
            ✓ DACRE dashboard

        </div>
        """,
        unsafe_allow_html=True,
    )

with p2:
    st.markdown(
        """
        <div class="pricing-card featured">

            <div class="metric-label">
                PROFESSIONAL
            </div>

            <div class="price">
                Coming Soon
            </div>

            <p>
                Designed for analysts and professional users.
            </p>

            <br>

            ✓ Advanced analysis<br>
            ✓ Advanced dashboards<br>
            ✓ DI Intelligence<br>
            ✓ Reporting

        </div>
        """,
        unsafe_allow_html=True,
    )

with p3:
    st.markdown(
        """
        <div class="pricing-card">

            <div class="metric-label">
                BUSINESS
            </div>

            <div class="price">
                Coming Soon
            </div>

            <p>
                Built for teams and organizations.
            </p>

            <br>

            ✓ Team analytics<br>
            ✓ Organization dashboards<br>
            ✓ Advanced reporting<br>
            ✓ Enterprise controls

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# FAQ
# ============================================================

st.markdown(
    """
    <section class="section">

        <div class="section-label">
            QUESTIONS
        </div>

        <div class="section-title">
            Frequently asked questions.
        </div>

    </section>
    """,
    unsafe_allow_html=True,
)


with st.expander("What is DACRE Analysis?"):
    st.write(
        "DACRE Analysis is the analytical platform being developed "
        "by DACREglobal limited for data preparation, analysis, "
        "visualization and DI-assisted analytical workflows."
    )

with st.expander("What is DI Intelligence?"):
    st.write(
        "DI means David Intelligence. It is the intelligence layer "
        "we will build into DACRE to help users interact with data "
        "and obtain analytical assistance."
    )

with st.expander("Can I upload my own data?"):
    st.write(
        "Yes. The next development stage will add CSV, Excel and "
        "other supported data-upload workflows."
    )

with st.expander("Will DACRE have dashboards?"):
    st.write(
        "Yes. Interactive dashboards and visualization tools will "
        "be added to the DACRE workspace."
    )

with st.expander("Will DI work with online information?"):
    st.write(
        "The architecture can later connect DI to approved online "
        "services and APIs when the user is online."
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

        <p class="section-description" style="margin: 20px auto 30px auto;">
            Start building a smarter analytical workflow with
            DACRE Analysis.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


cta1, cta2, cta3 = st.columns([1, 1.1, 1])

with cta1:
    st.write("")

with cta2:

    if st.button(
        "Get Started with DACRE",
        use_container_width=True,
        type="primary",
    ):
        st.session_state.started = True

with cta3:
    st.write("")


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        <div style="text-align:center;">

            <strong style="color:#ffffff;">
                DACREglobal limited
            </strong>

            <br><br>

            DACRE Analysis
            &nbsp; • &nbsp;
            Product
            &nbsp; • &nbsp;
            Company
            &nbsp; • &nbsp;
            Resources
            &nbsp; • &nbsp;
            Contact
            &nbsp; • &nbsp;
            Legal

            <br><br>

            © 2026 DACREglobal limited.
            All rights reserved.

        </div>

    </div>
    """,
    unsafe_allow_html=True,
)
