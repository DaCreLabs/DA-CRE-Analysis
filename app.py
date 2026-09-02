import streamlit as st
import datetime

# Page Configuration
st.set_page_config(
    page_title="Dacre Analysis | Financial Intelligence Platform", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session States for Dacre Analysis
if "user_session" not in st.session_state:
    st.session_state["user_session"] = None

# Helper: Parse URL Query Parameters for DGL Single Sign-On (SSO)
def check_sso_login():
    query_params = st.query_params
    if "sso_token" in query_params or "email" in query_params:
        # Extracted SSO metadata from main DGL network hub
        email = query_params.get("email", "enterprise@client.com")
        company = query_params.get("company", "DGL Enterprise Member")
        is_vip = query_params.get("vip", "true").lower() == "true"
        
        st.session_state["user_session"] = {
            "email": email,
            "company_name": company,
            "is_vip": is_vip,
            "dgl_id": query_params.get("dgl_id", "DGL-8849"),
            "trial_days": 40 if is_vip else 30,
            "monthly_rate": "30,000",
            "entry_source": "DGL Hub SSO"
        }

check_sso_login()

# ==========================================
# CUSTOM CSS & BRANDING
# ==========================================
st.markdown("""
    <style>
        .main-header { font-size: 28px; font-weight: 800; color: #0f172a; font-family: sans-serif; }
        .sub-header { color: #475569; font-size: 14px; margin-bottom: 20px; }
        .vip-banner {
            background: linear-gradient(135deg, #059669, #10b981);
            color: white;
            padding: 16px 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
            margin-bottom: 25px;
        }
        .standard-banner {
            background: #f1f5f9;
            border-left: 4px solid #0284c7;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 25px;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR NAVIGATION & PORTAL TELEMETRY
# ==========================================
with st.sidebar:
    st.markdown("### 📊 DACRE ANALYSIS")
    st.caption("A Dacre Global Limited (DGL) Platform")
    st.divider()

    # SSO / Login Controller
    if st.session_state["user_session"]:
        session = st.session_state["user_session"]
        st.success(f"Connected: **{session['company_name']}**")
        st.caption(f"Account Email: {session['email']}")
        
        if session["is_vip"]:
            st.markdown("⭐ **VIP PLATFORM STATUS**")
            st.caption("Access Granted via DGL Master Network")
        
        st.divider()
        st.write("**Subscription Parameters:**")
        st.write(f"• **Free Trial:** {session['trial_days']} Days")
        st.write(f"• **Recurring Rate:** ₦{session['monthly_rate']}/mo")
        
        st.divider()
        if st.button("Disconnect Session"):
            st.session_state["user_session"] = None
            st.query_params.clear()
            st.rerun()

    else:
        st.warning("No DGL Session Token Found")
        st.write("Please log in below or enter via the **DGL Main Portal** for automatic VIP onboarding.")
        
        with st.form("manual_login"):
            m_email = st.text_input("Business Email")
            m_comp = st.text_input("Company Name")
            is_dgl = st.checkbox("I am an active DGL Network Member (₦33,500 subscriber)")
            
            if st.form_submit_button("Launch Analysis Portal"):
                st.session_state["user_session"] = {
                    "email": m_email if m_email else "user@company.com",
                    "company_name": m_comp if m_comp else "Standalone Enterprise",
                    "is_vip": is_dgl,
                    "dgl_id": "DGL-DIRECT" if is_dgl else "GUEST-01",
                    "trial_days": 40 if is_dgl else 30,
                    "monthly_rate": "30,000",
                    "entry_source": "Direct Login"
                }
                st.rerun()

# ==========================================
# MAIN DACRE ANALYSIS DASHBOARD
# ==========================================
st.markdown('<div class="main-header">DACRE ANALYSIS PLATFORM</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Advanced Real Estate, Financial Forecasting & Market Analytics Engine</div>', unsafe_allow_html=True)

if not st.session_state["user_session"]:
    st.info("💡 **DGL VIP Benefit Reminder**: Enrolling through **DGL (Dacre Global Limited)** grants you **40 Days Free Trial** instead of 30 days. Log in through the sidebar to continue.")

else:
    session = st.session_state["user_session"]

    # 1. VIP vs. STANDARD BENNER RENDER
    if session["is_vip"]:
        st.markdown(f"""
            <div class="vip-banner">
                <h3 style="margin: 0; font-size: 20px;">👑 VIP Access Activated (DGL Network Member)</h3>
                <p style="margin: 5px 0 0 0; font-size: 14px;">
                    Welcome, <b>{session['company_name']}</b>! Your VIP token was recognized. You have been granted a 
                    <b>{session['trial_days']}-Day Extended Free Trial</b>. Your standard rate of <b>₦{session['monthly_rate']}/month</b> 
                    will activate upon completion of the trial period.
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="standard-banner">
                <h4 style="margin: 0; color: #0369a1;">Standard Access Plan</h4>
                <p style="margin: 5px 0 0 0; color: #334155;">
                    Welcome, <b>{session['company_name']}</b>. You are currently on the <b>30-Day Standard Free Trial</b>. 
                    Subscription automatically renews at <b>₦{session['monthly_rate']}/month</b>. 
                    <i>(Tip: DGL Network Members unlock a 40-Day VIP Trial).</i>
                </p>
            </div>
        """, unsafe_allow_html=True)

    # 2. TELEMETRY & TRIAL METRICS
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Account Tier", "VIP (DGL Hub)" if session["is_vip"] else "Standard")
    c2.metric("Trial Duration", f"{session['trial_days']} Days")
    c3.metric("Monthly Subscription", f"₦{session['monthly_rate']}")
    c4.metric("DGL Sync ID", session["dgl_id"])

    st.divider()

    # 3. ANALYTICS WORKSPACE & TOOLKIT
    st.subheader("📈 Executive Analysis Engine")
    
    t1, t2, t3 = st.tabs(["🏗️ CRE Valuation Model", "📊 Revenue & Yield Simulator", "🛰️ Market Penetration Radar"])

    with t1:
        st.write("#### Commercial Real Estate (CRE) Cash Flow Model")
        col_a, col_b = st.columns(2)
        with col_a:
            asset_val = st.number_input("Asset Acquisition Value (₦)", min_value=1000000, value=150000000, step=5000000)
            rental_yield = st.slider("Expected Annual Cap Rate (%)", 3.0, 20.0, 8.5)
        with col_b:
            lease_term = st.number_input("Holding Period (Years)", 1, 30, 5)
            occupancy = st.slider("Target Occupancy Rate (%)", 50, 100, 90)

        # Calculation Engine
        gross_annual_rev = asset_val * (rental_yield / 100) * (occupancy / 100)
        total_holding_rev = gross_annual_rev * lease_term

        st.markdown("---")
        res1, res2 = st.columns(2)
        res1.metric("Projected Annual NOI", f"₦{gross_annual_rev:,.2f}")
        res2.metric(f"{lease_term}-Year Projected Gross Yield", f"₦{total_holding_rev:,.2f}")

    with t2:
        st.write("#### B2B Subscription & Revenue Projection")
        m_clients = st.number_input("Target Enrolled B2B Clients", value=100)
        m_fee = st.number_input("Monthly Client Fee (₦)", value=30000)
        
        monthly_mrr = m_clients * m_fee
        annual_arr = monthly_mrr * 12

        st.write(f"**Projected Monthly Recurring Revenue (MRR):** ₦{monthly_mrr:,.2f}")
        st.write(f"**Projected Annual Recurring Revenue (ARR):** ₦{annual_arr:,.2f}")

    with t3:
        st.write("#### DGL Cross-Platform Ecosystem Telemetry")
        st.info("This session's metadata is directly mirrored on the **DGL Master Admin Dashboard** for automated auditing.")
        
        st.json({
            "User Company": session["company_name"],
            "Account Email": session["email"],
            "DGL Platform Origin": session["entry_source"],
            "VIP Status": session["is_vip"],
            "Trial Days Allocated": session["trial_days"],
            "Subscription Price": f"₦{session['monthly_rate']}/month",
            "Timestamp": str(datetime.datetime.now())
        })
