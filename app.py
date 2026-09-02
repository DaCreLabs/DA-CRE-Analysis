import streamlit as st
import datetime

# Page Configuration
st.set_page_config(
    page_title="Dacre Analysis", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "user_session" not in st.session_state:
    st.session_state["user_session"] = None

# Custom CSS Styling
st.markdown("""
    <style>
        .main-title { font-size: 30px; font-weight: 800; color: #0f172a; margin-bottom: 5px; }
        .sub-title { font-size: 15px; color: #64748b; margin-bottom: 25px; }
        .vip-box {
            background-color: #ecfdf5;
            border: 2px solid #10b981;
            padding: 18px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .standard-box {
            background-color: #f8fafc;
            border: 1px solid #cbd5e1;
            padding: 18px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR CONTROL
# ==========================================
with st.sidebar:
    st.title("📊 DACRE ANALYSIS")
    st.caption("Financial Intelligence & Analytics Engine")
    st.divider()

    if st.session_state["user_session"]:
        user = st.session_state["user_session"]
        st.success(f"Company: **{user['company_name']}**")
        st.write(f"**Email:** {user['email']}")
        
        if user["is_vip"]:
            st.markdown("⭐ **VIP Access Active**")
            st.caption("DGL Member Perks Applied")
        
        st.divider()
        st.write(f"• **Free Trial:** {user['trial_days']} Days")
        st.write(f"• **Subscription:** ₦30,000/month")
        
        if st.button("Log Out"):
            st.session_state["user_session"] = None
            st.rerun()

    else:
        st.subheader("Client Portal Login")
        with st.form("dacre_login"):
            comp_name = st.text_input("Company Name")
            email = st.text_input("Business Email")
            is_dgl_vip = st.checkbox("Sign in as DGL Member (VIP)")
            
            if st.form_submit_button("Access Dacre Analysis"):
                if comp_name and email:
                    st.session_state["user_session"] = {
                        "company_name": comp_name,
                        "email": email,
                        "is_vip": is_dgl_vip,
                        "trial_days": 40 if is_dgl_vip else 30,
                        "monthly_rate": 30000
                    }
                    st.rerun()
                else:
                    st.error("Please enter both Company Name and Email.")

# ==========================================
# MAIN APP BODY
# ==========================================
st.markdown('<div class="main-title">DACRE ANALYSIS</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Enterprise Valuation & Market Projections Hub</div>', unsafe_allow_html=True)

if not st.session_state["user_session"]:
    st.info("👋 **Welcome to Dacre Analysis.** Please sign in on the sidebar to access your workspace. Standard clients receive a 30-day free trial; DGL VIPs receive a 40-day free trial (renewing at ₦30,000/month).")

else:
    user = st.session_state["user_session"]

    # 1. VIP vs Standard Status Card
    if user["is_vip"]:
        st.markdown(f"""
            <div class="vip-box">
                <h3 style="margin:0; color:#065f46;">👑 VIP Account Recognized</h3>
                <p style="margin:5px 0 0 0; color:#047857;">
                    Welcome, <b>{user['company_name']}</b>. You have unlocked <b>40 Days Free Trial</b>. 
                    Subscription rate: <b>₦30,000/month</b> after the trial ends.
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="standard-box">
                <h4 style="margin:0; color:#1e293b;">Standard Account Tier</h4>
                <p style="margin:5px 0 0 0; color:#475569;">
                    Welcome, <b>{user['company_name']}</b>. You are on a <b>30-Day Free Trial</b>. 
                    Renewal rate: <b>₦30,000/month</b>.
                </p>
            </div>
        """, unsafe_allow_html=True)

    # 2. Account Telemetry Cards
    c1, c2, c3 = st.columns(3)
    c1.metric("Tier Status", "VIP Tier" if user["is_vip"] else "Standard Tier")
    c2.metric("Trial Duration", f"{user['trial_days']} Days")
    c3.metric("Monthly Renewal", f"₦{user['monthly_rate']:,}")

    st.divider()

    # 3. Dacre Analysis Calculators
    st.subheader("📈 Financial Models")
    tab1, tab2 = st.tabs(["Commercial Real Estate Model", "B2B Revenue Calculator"])

    with tab1:
        st.write("#### Commercial Asset Net Yield Model")
        col_a, col_b = st.columns(2)
        with col_a:
            asset_val = st.number_input("Asset Valuation (₦)", min_value=1000000, value=50000000, step=5000000)
            cap_rate = st.slider("Expected Cap Rate (%)", 3.0, 20.0, 8.5)
        with col_b:
            years = st.number_input("Forecast Period (Years)", 1, 30, 5)
            occ_rate = st.slider("Occupancy Rate (%)", 50, 100, 95)

        # Calculations
        annual_noi = asset_val * (cap_rate / 100) * (occ_rate / 100)
        total_yield = annual_noi * years

        st.markdown("---")
        res1, res2 = st.columns(2)
        res1.metric("Annual Operating Income (NOI)", f"₦{annual_noi:,.2f}")
        res2.metric(f"{years}-Year Gross Yield", f"₦{total_yield:,.2f}")

    with tab2:
        st.write("#### Monthly Subscription MRR Forecast")
        client_count = st.number_input("Target Subscribed Clients", min_value=1, value=50)
        subscription_price = user["monthly_rate"]

        mrr = client_count * subscription_price
        arr = mrr * 12

        st.metric("Projected Monthly Recurring Revenue (MRR)", f"₦{mrr:,.2f}")
        st.metric("Projected Annual Recurring Revenue (ARR)", f"₦{arr:,.2f}")
