import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import secrets
import string
import time
from PIL import Image
import os
import io

# Page Configuration
st.set_page_config(
    page_title="DA-CRE Analysis Platform",
    page_icon="⚡",
    layout="wide"
)

# Initialize Session State & Permanent File Vault
if 'loading_complete' not in st.session_state:
    st.session_state['loading_complete'] = False
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'declined_suggested' not in st.session_state:
    st.session_state['declined_suggested'] = False
if 'active_file_name' not in st.session_state:
    st.session_state['active_file_name'] = None
if 'current_data' not in st.session_state:
    st.session_state['current_data'] = None

# Local Storage Vault dictionary to keep all your files saved
if 'file_vault' not in st.session_state:
    st.session_state['file_vault'] = {}

def generate_strong_password(length=14):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if 'suggested_pw' not in st.session_state:
    st.session_state['suggested_pw'] = generate_strong_password()

# Modern UI Styling
st.markdown("""
    <style>
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

    /* Glassmorphism Styling */
    .glass-card {
        background: rgba(18, 24, 38, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2.2rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
    }

    .pointer-box {
        text-align: center;
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.15) 0%, rgba(0, 242, 254, 0.05) 100%);
        padding: 1.2rem;
        border-radius: 16px;
        border: 1px solid rgba(79, 172, 254, 0.4);
        margin-top: 15px;
    }

    .my-data-badge {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        color: #0b0e14;
        padding: 0.6rem 1.2rem;
        border-radius: 20px;
        font-weight: bold;
        display: flex;
        align-items: center;
        gap: 8px;
        float: right;
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


# --- 2. SIGN-UP PAGE ---
elif not st.session_state['authenticated']:
    
    st.markdown("""
        <div style="text-align:center; padding: 1.5rem; margin-bottom: 2rem;">
            <h1 style="background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem;">DA-CRE Analysis Platform</h1>
            <p style="color: #94a3b8; font-size: 1.2rem;">Commercial Real Estate & Advanced Data Intelligence</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.2], gap="large")

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if os.path.exists("david_profile.png"):
            img = Image.open("david_profile.png")
            st.image(img, use_container_width=True)
        else:
            st.info("📷 Profile photo (david_profile.png)")

        st.markdown("""
            <div class="pointer-box">
                <h3 style="color: #00f2fe; margin:0; font-size: 1.4rem;">Welcome! 👉</h3>
                <p style="margin:8px 0 0 0; color: #cbd5e1;">Fill out the access form on the right to unlock your workspace.</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h2 style='color: #4facfe; margin-bottom: 20px;'>📝 Create Account</h2>", unsafe_allow_html=True)
        
        first_name = st.text_input("First Name")
        middle_name = st.text_input("Middle Name (Optional)")
        email = st.text_input("Email Address")

        password_to_use = ""

        email_error = False
        if email and "@" not in email:
            st.error("❌ Invalid Email: Address must include '@'")
            email_error = True

        st.write("---")
        
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


# --- 3. MAIN MULTI-FUNCTION WORKSPACE HUB ---
else:
    # TOP HEADER WITH MY DATA BADGE
    active_file = st.session_state.get('active_file_name', 'No Active File Selected')
    
    col_nav1, col_nav2 = st.columns([2, 1])
    with col_nav1:
        st.markdown("### ⚡ DA-CRE Analysis Workspace")
    with col_nav2:
        if st.session_state['active_file_name']:
            st.markdown(f'<div class="my-data-badge">📂 MY DATA: {active_file}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="my-data-badge" style="background: #334155; color: #94a3b8;">📂 MY DATA: Empty</div>', unsafe_allow_html=True)

    st.write("---")

    # SIDEBAR ACTION DROPDOWN
    st.sidebar.title(f"👤 {st.session_state.get('user_name', 'User')}")
    
    action_choice = st.sidebar.selectbox(
        "Select Platform Action",
        [
            "📂 Open File Vault (Select Active Data)",
            "📥 Add New Files to Vault",
            "🌐 Collect Data from Web",
            "🧹 Clean Active Dataset",
            "📊 Data Visualizations",
            "🚀 Export to Google/Docs/Excel"
        ]
    )

    if st.sidebar.button("🔒 Logout", use_container_width=True):
        st.session_state['authenticated'] = False
        st.session_state['loading_complete'] = True
        st.rerun()

    # ACTION 1: FILE VAULT (SELECT & OPEN SAVED FILES)
    if action_choice == "📂 Open File Vault (Select Active Data)":
        st.subheader("📂 Your Saved Files Library (File Vault)")
        
        vault_files = list(st.session_state['file_vault'].keys())
        
        if len(vault_files) > 0:
            selected_vault_file = st.selectbox("Choose a saved file to open:", vault_files)
            
            if st.button("Open Selected File into MY DATA 🚀", use_container_width=True):
                st.session_state['current_data'] = st.session_state['file_vault'][selected_vault_file]
                st.session_state['active_file_name'] = selected_vault_file
                st.success(f"'{selected_vault_file}' is now set to active in MY DATA!")
                st.rerun()
                
            if st.session_state['current_data'] is not None and st.session_state['active_file_name'] == selected_vault_file:
                st.write("---")
                st.write(f"Previewing **{selected_vault_file}**:")
                st.dataframe(st.session_state['current_data'].head(10))
        else:
            st.info("Your File Vault is currently empty. Go to '📥 Add New Files to Vault' in the left menu to add your files!")

    # ACTION 2: ADD NEW FILES TO VAULT
    elif action_choice == "📥 Add New Files to Vault":
        st.subheader("📥 Save New Files to Your App Library")
        uploaded_files = st.file_uploader("Upload CSV or Excel files from your device", type=["csv", "xlsx"], accept_multiple_files=True)
        
        if uploaded_files:
            for file in uploaded_files:
                try:
                    df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
                    st.session_state['file_vault'][file.name] = df
                    st.success(f"Saved '{file.name}' into your File Vault!")
                except Exception as e:
                    st.error(f"Error reading {file.name}: {e}")
            
            st.info("Switch to '📂 Open File Vault' in the sidebar to view and pick from all your saved files.")

    # ACTION 3: COLLECT DATA FROM WEB
    elif action_choice == "🌐 Collect Data from Web":
        st.subheader("🌐 Scrape Data from Website")
        url_input = st.text_input("Enter URL containing data tables:", "https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue")
        
        if st.button("Extract Data Tables"):
            if url_input:
                try:
                    with st.spinner("Scraping webpage..."):
                        tables = pd.read_html(url_input)
                        st.success(f"Found {len(tables)} tables!")
                        for i, df in enumerate(tables):
                            with st.expander(f"Table #{i+1} ({df.shape[0]} rows x {df.shape[1]} cols)"):
                                st.dataframe(df)
                                file_title = f"Web_Table_{i+1}.csv"
                                if st.button(f"Save Table #{i+1} to File Vault"):
                                    st.session_state['file_vault'][file_title] = df
                                    st.session_state['current_data'] = df
                                    st.session_state['active_file_name'] = file_title
                                    st.success(f"Saved {file_title} to File Vault and set active in MY DATA!")
                                    st.rerun()
                except Exception as e:
                    st.error(f"Scraper error: {e}")

    # ACTION 4: CLEAN DATASET
    elif action_choice == "🧹 Clean Active Dataset":
        st.subheader("🧹 Automated Cleaning")
        if st.session_state['current_data'] is not None:
            df = st.session_state['current_data']
            st.write(f"Editing **{st.session_state['active_file_name']}**:")
            st.dataframe(df.head())
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Remove Duplicates", use_container_width=True):
                    cleaned_df = df.drop_duplicates()
                    st.session_state['current_data'] = cleaned_df
                    st.session_state['file_vault'][st.session_state['active_file_name']] = cleaned_df
                    st.success("Duplicates purged!")
            with c2:
                if st.button("Drop Missing Values", use_container_width=True):
                    cleaned_df = df.dropna()
                    st.session_state['current_data'] = cleaned_df
                    st.session_state['file_vault'][st.session_state['active_file_name']] = cleaned_df
                    st.success("Missing rows removed!")
        else:
            st.info("No active dataset in MY DATA. Open a file from your File Vault first.")

    # ACTION 5: VISUALIZATIONS
    elif action_choice == "📊 Data Visualizations":
        st.subheader("📊 Interactive Visualizations")
        if st.session_state['current_data'] is not None:
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
            st.info("No active dataset selected. Open a file from your File Vault first.")

    # ACTION 6: EXPORT OPTIONS
    elif action_choice == "🚀 Export to Google/Docs/Excel":
        st.subheader("🚀 Export Active Dataset")
        if st.session_state['current_data'] is not None:
            df = st.session_state['current_data']
            
            col_e1, col_e2 = st.columns(2)
            
            with col_e1:
                st.markdown("#### 🟢 Google Ecosystem")
                st.link_button("Open in Google Sheets 🟢", "https://sheets.new", use_container_width=True)
                st.link_button("Open in Google Docs 📄", "https://docs.new", use_container_width=True)
                st.link_button("Open in Google Slides 📊", "https://slides.new", use_container_width=True)

            with col_e2:
                st.markdown("#### 🔵 Local Files")
                csv_bytes = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Excel/CSV File 📥",
                    data=csv_bytes,
                    file_name=f"DA_CRE_{st.session_state['active_file_name']}",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.info("No active dataset in MY DATA to export. Open a file from your File Vault first.")
