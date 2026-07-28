import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import secrets
import string
import time
from PIL import Image
import os

# Page Configuration
st.set_page_config(
    page_title="DA-CRE Analysis Platform",
    page_icon="⚡",
    layout="wide"
)

# Initialize Session State
if 'loading_complete' not in st.session_state:
    st.session_state['loading_complete'] = False
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'declined_suggested' not in st.session_state:
    st.session_state['declined_suggested'] = False

def generate_strong_password(length=14):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if 'suggested_pw' not in st.session_state:
    st.session_state['suggested_pw'] = generate_strong_password()

# High-End Modern UI Styling (Glassmorphism & Glowing Elements)
st.markdown("""
    <style>
    /* Background Setup */
    .stApp {
        background: radial-gradient(circle at top left, #1a233a, #0b0e14, #05070a);
        color: #f0f4f8;
        font-family: 'Inter', sans-serif;
    }

    /* Animated Loading Logo */
    .logo-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 75vh;
    }
    .dacre-logo {
        font-size: 4.5rem;
        font-weight: 900;
        letter-spacing: 6px;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: floatAndGlow 2.2s ease-in-out infinite;
    }
    .logo-subtext {
        font-size: 1.1rem;
        color: #94a3b8;
        letter-spacing: 2px;
        margin-top: 10px;
    }
    @keyframes floatAndGlow {
        0% { transform: translateY(0px); filter: drop-shadow(0 0 15px rgba(79, 172, 254, 0.3)); }
        50% { transform: translateY(-12px); filter: drop-shadow(0 0 35px rgba(79, 172, 254, 0.8)); }
        100% { transform: translateY(0px); filter: drop-shadow(0 0 15px rgba(79, 172, 254, 0.3)); }
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(18, 24, 38, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2.2rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(79, 172, 254, 0.4);
    }

    /* Corrected Pointer Box (Points 👉 to the Form) */
    .pointer-box {
        text-align: center;
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.15) 0%, rgba(0, 242, 254, 0.05) 100%);
        padding: 1.2rem;
        border-radius: 16px;
        border: 1px solid rgba(79, 172, 254, 0.4);
        margin-top: 15px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }

    /* Custom Header Banner */
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    .main-header h1 {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)


# --- 1. FIVE-SECOND HOVERING LOADING SCREEN ---
if not st.session_state['loading_complete']:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
            <div class="logo-container">
                <div class="dacre-logo">⚡ DACRE ANALYSIS</div>
                <div class="logo-subtext">INITIALIZING DATA ENGINE...</div>
            </div>
        """, unsafe_allow_html=True)
    
    time.sleep(5)
    st.session_state['loading_complete'] = True
    placeholder.empty()
    st.rerun()


# --- 2. SIGN-UP PAGE WITH ASTONISHING UI & PROPER POINTER ---
elif not st.session_state['authenticated']:
    
    st.markdown("""
        <div class="main-header">
            <h1>DA-CRE Analysis Platform</h1>
            <p style="color: #94a3b8; font-size: 1.1rem;">Commercial Real Estate & Advanced Data Intelligence</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.2], gap="large")

    # Left Column: Profile Card with 👉 pointing RIGHT
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        if os.path.exists("david_profile.png"):
            img = Image.open("david_profile.png")
            st.image(img, use_container_width=True)
        else:
            st.info("📷 Profile photo (david_profile.png)")

        # Fixed 👉 pointing to the right form
        st.markdown("""
            <div class="pointer-box">
                <h3 style="color: #00f2fe; margin:0; font-size: 1.4rem;">Welcome! 👉</h3>
                <p style="margin:8px 0 0 0; color: #cbd5e1;">Fill out the access form on the right to unlock your workspace.</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Right Column: Glassmorphism Sign-Up Form
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h2 style='color: #4facfe; margin-bottom: 20px;'>📝 Create Account</h2>", unsafe_allow_html=True)
        
        first_name = st.text_input("First Name")
        middle_name = st.text_input("Middle Name (Optional)")
        email = st.text_input("Email Address")

        password_to_use = ""

        # Email Validation Check
        email_error = False
        if email and "@" not in email:
            st.error("❌ Invalid Email: Address must include '@'")
            email_error = True

        st.write("---")
        
        # Password Handling Logic
        if not st.session_state['declined_suggested']:
            st.info(f"🔑 **Suggested Password:** `{st.session_state['suggested_pw']}`")
            
            c_acc, c_dec = st.columns(2)
            with c_acc:
                if st.button("Accept Suggested", use_container_width=True):
                    password_to_use = st.session_state['suggested_pw']
            with c_dec:
                if st.button("Decline & Use Own", use_container_width=True):
                    st.session_state['declined_suggested'] = True
                    st.rerun()
        else:
            password_to_use = st.text_input("Custom Password", type="password")
            if st.button("Re-enable Suggested Password"):
                st.session_state['declined_suggested'] = False
                st.rerun()

        st.write("---")
        
        # Complete Signup Button
        if st.button("Complete Registration 🚀", use_container_width=True):
            if not first_name:
                st.warning("First name is required.")
            elif not email or email_error:
                st.warning("Valid email required.")
            elif not password_to_use:
                st.warning("Please specify or accept a password.")
            else:
                st.session_state['user_name'] = f"{first_name} {middle_name}".strip()
                st.session_state['authenticated'] = True
                st.success("Account created! Unlocking platform...")
                time.sleep(1)
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)


# --- 3. MAIN APPLICATION DASHBOARD ---
else:
    st.sidebar.title(f"👤 {st.session_state.get('user_name', 'User')}")
    if st.sidebar.button("🔒 Logout", use_container_width=True):
        st.session_state['authenticated'] = False
        st.session_state['loading_complete'] = True
        st.rerun()

    st.markdown("""
        <div class="main-header">
            <h1>DA-CRE Analysis Workspace</h1>
            <p style="color: #94a3b8;">Active Session | Data Analytics & Scraper Engine</p>
        </div>
    """, unsafe_allow_html=True)

    app_mode = st.sidebar.radio(
        "Navigation",
        ["🌐 1. Web Scraper", "📁 2. File Upload", "🧹 3. Data Cleaner", "📊 4. Analytics Engine"]
    )

    # MODULE 1: WEB SCRAPER
    if app_mode == "🌐 1. Web Scraper":
        st.subheader("🌐 Web Data Scraper")
        url_input = st.text_input("Enter URL containing data tables:", "https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue")
        
        if st.button("Extract Data"):
            if url_input:
                try:
                    with st.spinner("Scraping webpage..."):
                        tables = pd.read_html(url_input)
                        st.success(f"Found {len(tables)} tables!")
                        for i, df in enumerate(tables):
                            with st.expander(f"Table #{i+1} ({df.shape[0]} rows x {df.shape[1]} cols)"):
                                st.dataframe(df)
                                csv = df.to_csv(index=False).encode('utf-8')
                                st.download_button(f"Export CSV", csv, f'table_{i+1}.csv', 'text/csv')
                except Exception as e:
                    st.error(f"Scraper error: {e}")

    # MODULE 2: FILE UPLOADER
    elif app_mode == "📁 2. File Upload":
        st.subheader("📁 Upload Local Datasets")
        uploaded_file = st.file_uploader("Choose CSV or Excel file", type=["csv", "xlsx"])
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                st.session_state['current_data'] = df
                st.success(f"Loaded: {uploaded_file.name}")
                st.dataframe(df.head(10))
            except Exception as e:
                st.error(f"Upload error: {e}")

    # MODULE 3: DATA CLEANER
    elif app_mode == "🧹 3. Data Cleaner":
        st.subheader("🧹 Automated Cleaning")
        if 'current_data' in st.session_state:
            df = st.session_state['current_data']
            st.dataframe(df.head())
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Remove Duplicates", use_container_width=True):
                    st.session_state['current_data'] = df.drop_duplicates()
                    st.success("Duplicates purged!")
            with c2:
                if st.button("Drop Missing Values", use_container_width=True):
                    st.session_state['current_data'] = df.dropna()
                    st.success("Missing rows removed!")
        else:
            st.info("Upload or scrape data first.")

    # MODULE 4: ANALYTICS
    elif app_mode == "📊 4. Analytics Engine":
        st.subheader("📊 Interactive Visualizations")
        if 'current_data' in st.session_state:
            df = st.session_state['current_data']
            num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            all_cols = df.columns.tolist()
            
            if num_cols and len(all_cols) >= 2:
                x_axis = st.selectbox("X-Axis", all_cols)
                y_axis = st.selectbox("Y-Axis", num_cols)
                chart_type = st.radio("Chart Style", ["Bar Chart", "Line Chart", "Scatter Plot"])
                
                if chart_type == "Bar Chart":
                    fig = px.bar(df, x=x_axis, y=y_axis, template="plotly_dark")
                elif chart_type == "Line Chart":
                    fig = px.line(df, x=x_axis, y=y_axis, template="plotly_dark")
                else:
                    fig = px.scatter(df, x=x_axis, y=y_axis, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Numeric columns required for charting.")
        else:
            st.info("Load data in Module 1 or 2 first.")
