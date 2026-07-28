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
    page_icon="🪄📊",
    layout="wide"
)

# Initialize Session State Variables
if 'loading_complete' not in st.session_state:
    st.session_state['loading_complete'] = False
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'declined_suggested' not in st.session_state:
    st.session_state['declined_suggested'] = False

def generate_strong_password(length=12):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if 'suggested_pw' not in st.session_state:
    st.session_state['suggested_pw'] = generate_strong_password()

# Custom CSS: Animated Backgrounds & Hovering Logo
st.markdown("""
    <style>
    /* Blue to Dark Blue Background Animation */
    .stApp {
        background: linear-gradient(-45deg, #0d1b2a, #1b263b, #415a77, #1e3c72, #001122);
        background-size: 400% 400%;
        animation: gradientBG 10s ease infinite;
        color: white;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Hovering & Pulsing DACRE Logo Animation */
    .logo-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 70vh;
    }
    .dacre-logo {
        font-size: 4rem;
        font-weight: 900;
        letter-spacing: 4px;
        color: #ffffff;
        background: linear-gradient(90deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 10px 20px rgba(0, 210, 255, 0.4);
        animation: floatAndPulse 2.5s ease-in-out infinite;
    }
    .logo-subtext {
        font-size: 1.2rem;
        color: #e0e1dd;
        margin-top: 15px;
        animation: fadeIn 2s ease-in-out infinite alternate;
    }
    @keyframes floatAndPulse {
        0% { transform: translateY(0px) scale(1); filter: drop-shadow(0 5px 15px rgba(0,210,255,0.3)); }
        50% { transform: translateY(-15px) scale(1.05); filter: drop-shadow(0 20px 30px rgba(0,210,255,0.7)); }
        100% { transform: translateY(0px) scale(1); filter: drop-shadow(0 5px 15px rgba(0,210,255,0.3)); }
    }

    /* Sign-up Card Styling */
    .signup-card {
        background: rgba(13, 27, 42, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }
    
    /* Pointer Animation for Profile */
    .pointer-box {
        text-align: center;
        background: rgba(65, 90, 119, 0.4);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #00d2ff;
        margin-top: 10px;
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
                <div class="logo-subtext">Initializing AI Data Engine...</div>
            </div>
        """, unsafe_allow_html=True)
    
    # 5 Seconds Delay
    time.sleep(5)
    st.session_state['loading_complete'] = True
    placeholder.empty()
    st.rerun()


# --- 2. SIGN-UP PAGE (WITH ANIMATED BACKGROUND & PROFILE GUIDE) ---
elif not st.session_state['authenticated']:
    
    st.markdown("<h1 style='text-align: center; color: #00d2ff; margin-bottom: 30px;'>Welcome to DA-CRE Analysis Platform</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.2], gap="large")

    # Left Column: Profile Picture pointing to Sign Up
    with col1:
        st.markdown('<div class="signup-card">', unsafe_allow_html=True)
        
        # Load David Profile Picture if present in GitHub repo
        if os.path.exists("david_profile.png"):
            img = Image.open("david_profile.png")
            st.image(img, use_container_width=True)
        else:
            st.info("📷 Profile photo (david_profile.png)")

        st.markdown("""
            <div class="pointer-box">
                <h3 style="color: #00d2ff; margin:0;">👈 Welcome!</h3>
                <p style="margin:5px 0 0 0;">Please fill out the form on the right to complete your sign up and unlock full access.</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Right Column: Animated Sign-Up Form
    with col2:
        st.markdown('<div class="signup-card">', unsafe_allow_html=True)
        st.subheader("📝 Create Your Account")
        
        first_name = st.text_input("First Name")
        middle_name = st.text_input("Middle Name (Optional)")
        email = st.text_input("Email Address")

        password_to_use = ""

        # Email Validation Check
        email_error = False
        if email and "@" not in email:
            st.error("❌ Invalid Email: Your email address must contain an '@' symbol.")
            email_error = True

        # Password Suggestion & Decline logic
        st.write("---")
        if not st.session_state['declined_suggested']:
            st.info(f"💡 **Suggested Secure Password:** `{st.session_state['suggested_pw']}`")
            
            c_acc, c_dec = st.columns(2)
            with c_acc:
                if st.button("Use Suggested Password"):
                    password_to_use = st.session_state['suggested_pw']
            with c_dec:
                if st.button("Decline & Set Custom"):
                    st.session_state['declined_suggested'] = True
                    st.rerun()
        else:
            password_to_use = st.text_input("Set Your Own Password", type="password")
            if st.button("Re-enable Suggested Password"):
                st.session_state['declined_suggested'] = False
                st.rerun()

        st.write("---")
        
        # Complete Sign Up Button
        if st.button("Complete Sign Up & Access Platform"):
            if not first_name:
                st.warning("Please enter your First Name.")
            elif not email or email_error:
                st.warning("Please enter a valid Email Address containing '@'.")
            elif not password_to_use:
                st.warning("Please select or type a password.")
            else:
                st.session_state['user_name'] = f"{first_name} {middle_name}".strip()
                st.session_state['authenticated'] = True
                st.success("Registration Successful! Loading Dashboard...")
                time.sleep(1)
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)


# --- 3. MAIN APPLICATION PLATFORM ---
else:
    st.sidebar.title(f"👤 Welcome, {st.session_state.get('user_name', 'User')}!")
    if st.sidebar.button("🔒 Sign Out"):
        st.session_state['authenticated'] = False
        st.session_state['loading_complete'] = True
        st.rerun()

    st.markdown("""
        <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 1.5rem; border-radius: 10px; text-align: center; margin-bottom: 20px;">
            <h1>DA-CRE Analysis Platform</h1>
            <p>AI-Powered Commercial Real Estate & Data Analytics Engine</p>
        </div>
    """, unsafe_allow_html=True)

    app_mode = st.sidebar.radio(
        "Choose Module",
        ["🌐 1. Web Data Extractor", "📁 2. File Upload (CSV/Excel)", "🧹 3. Data Cleaning", "📊 4. Visual Analytics"]
    )

    # MODULE 1: WEB SCRAPER
    if app_mode == "🌐 1. Web Data Extractor":
        st.subheader("🌐 Website Data Extraction")
        url_input = st.text_input("Enter Website URL:", "https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue")
        
        if st.button("Extract Tables"):
            if url_input:
                try:
                    with st.spinner("Extracting data tables..."):
                        tables = pd.read_html(url_input)
                        st.success(f"Successfully found {len(tables)} tables!")
                        for i, df in enumerate(tables):
                            with st.expander(f"Table {i+1} ({df.shape[0]} rows, {df.shape[1]} cols)"):
                                st.dataframe(df)
                                csv = df.to_csv(index=False).encode('utf-8')
                                st.download_button(f"Download Table {i+1} CSV", csv, f'table_{i+1}.csv', 'text/csv')
                except Exception as e:
                    st.error(f"Error extracting tables: {e}")

    # MODULE 2: FILE UPLOADER
    elif app_mode == "📁 2. File Upload (CSV/Excel)":
        st.subheader("📁 Upload Local Data Files")
        uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                st.session_state['current_data'] = df
                st.success(f"Loaded {uploaded_file.name}!")
                st.dataframe(df.head(10))
            except Exception as e:
                st.error(f"Error: {e}")

    # MODULE 3: DATA CLEANING
    elif app_mode == "🧹 3. Data Cleaning":
        st.subheader("🧹 Automated Data Cleaning Engine")
        if 'current_data' in st.session_state:
            df = st.session_state['current_data']
            st.dataframe(df.head())
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Remove Duplicates"):
                    st.session_state['current_data'] = df.drop_duplicates()
                    st.success("Duplicates Removed!")
            with c2:
                if st.button("Drop Missing Values"):
                    st.session_state['current_data'] = df.dropna()
                    st.success("Missing Values Dropped!")
        else:
            st.info("Upload data in Module 2 first.")

    # MODULE 4: VISUAL ANALYTICS
    elif app_mode == "📊 4. Visual Analytics":
        st.subheader("📊 Visual Analytics Engine")
        if 'current_data' in st.session_state:
            df = st.session_state['current_data']
            num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            all_cols = df.columns.tolist()
            
            if num_cols and len(all_cols) >= 2:
                x_axis = st.selectbox("Select X-Axis", all_cols)
                y_axis = st.selectbox("Select Y-Axis", num_cols)
                chart_type = st.radio("Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot"])
                
                if chart_type == "Bar Chart":
                    fig = px.bar(df, x=x_axis, y=y_axis)
                elif chart_type == "Line Chart":
                    fig = px.line(df, x=x_axis, y=y_axis)
                else:
                    fig = px.scatter(df, x=x_axis, y=y_axis)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Need numeric columns to create chart.")
        else:
            st.info("Load data in Module 1 or 2 first.")
