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
    page_title="DA-CRE Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session State Initialization
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
if 'file_vault' not in st.session_state:
    st.session_state['file_vault'] = {}

def generate_strong_password(length=14):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if 'suggested_pw' not in st.session_state:
    st.session_state['suggested_pw'] = generate_strong_password()

# Global Custom CSS Theme
st.markdown("""
    <style>
    /* Dark Obsidian Background */
    .stApp {
        background: #090d16;
        color: #f1f5f9;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Animated Loader Logo */
    .logo-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 75vh;
    }
    .dacre-logo {
        font-size: 3.8rem;
        font-weight: 800;
        letter-spacing: 4px;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: pulseGlow 2.5s ease-in-out infinite;
    }
    .logo-subtext {
        font-size: 1rem;
        color: #64748b;
        letter-spacing: 3px;
        margin-top: 8px;
    }
    @keyframes pulseGlow {
        0% { transform: scale(1); filter: drop-shadow(0 0 10px rgba(56, 189, 248, 0.2)); }
        50% { transform: scale(1.02); filter: drop-shadow(0 0 25px rgba(56, 189, 248, 0.6)); }
        100% { transform: scale(1); filter: drop-shadow(0 0 10px rgba(56, 189, 248, 0.2)); }
    }

    /* LANDING / SIGN-UP PAGE STYLES */
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        line-height: 1.2;
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.8rem;
    }
    .hero-sub {
        font-size: 1.1rem;
        color: #94a3b8;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }
    .feature-badge {
        display: inline-block;
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.25);
        color: #38bdf8;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    /* Landing Left Profile Frame */
    .profile-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 1.8rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }

    /* Pointer Banner (Corrected Direction 👉) */
    .pointer-banner {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.12) 0%, rgba(129, 140, 248, 0.08) 100%);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 16px;
        padding: 1rem 1.2rem;
        margin-top: 1.2rem;
        text-align: center;
    }

    /* Sign-Up Form Glass Card */
    .auth-card {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2.2rem;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }

    /* WORKSPACE TOP NAVBAR */
    .workspace-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 1rem 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
    }
    .my-data-pill {
        background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%);
        color: #ffffff;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9rem;
        box-shadow: 0 4px 14px rgba(14, 165, 233, 0.3);
    }
    .my-data-pill-empty {
        background: #1e293b;
        color: #64748b;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    </style>
""", unsafe_allow_html=True)


# --- 1. FIVE-SECOND ANIMATED HOVERING LOADING SCREEN ---
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


# --- 2. ELEGANT, HIGH-CONVERSION SIGN-UP LANDING PAGE ---
elif not st.session_state['authenticated']:
    
    # Top Minimalist Brand Header
    st.markdown("""
        <div style="padding: 1rem 0 2rem 0; display:flex; justify-content:space-between; align-items:center;">
            <div style="font-size: 1.5rem; font-weight: 800; letter-spacing: 2px; color: #38bdf8;">⚡ DA-CRE</div>
            <div style="color: #64748b; font-size: 0.9rem;">Enterprise Real Estate Intelligence</div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 1], gap="large")

    # Left Column: Platform Showcase Hero Section
    with col1:
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        st.markdown('<span class="feature-badge">⚡ NEXT-GEN ANALYTICS PLATFORM</span>', unsafe_allow_html=True)
        st.markdown('<div class="hero-title">Commercial Real Estate Intelligence</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-sub">Transform raw datasets, scrape web listings, and instantly export interactive reports to Google Sheets, Excel, and Docs.</div>', unsafe_allow_html=True)
        
        if os.path.exists("david_profile.png"):
            img = Image.open("david_profile.png")
            st.image(img, use_container_width=True)
        else:
            st.info("📷 Profile picture (david_profile.png)")

        # Pointer pointing RIGHT (👉) to the signup card
        st.markdown("""
            <div class="pointer-banner">
                <h4 style="color: #38bdf8; margin:0; font-weight:700;">Ready to Get Started? 👉</h4>
                <p style="margin:4px 0 0 0; color: #cbd5e1; font-size:0.9rem;">Fill out the registration on the right to enter your workspace.</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Right Column: Clean, Modern Registration Card
    with col2:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown("<h2 style='color: #f8fafc; font-weight:700; margin-bottom: 4px;'>Create Your Account</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748b; margin-bottom: 24px; font-size:0.95rem;'>Enter your details to generate your credentials.</p>", unsafe_allow_html=True)
        
        first_name = st.text_input("First Name")
        middle_name = st.text_input("Middle Name (Optional)")
        email = st.text_input("Email Address")

        password_to_use = ""

        email_error = False
        if email and "@" not in email:
            st.error("❌ Invalid Email: Must include '@'")
            email_error = True

        st.write("---")
        
        # Suggested Password Accept/Decline Handling
        if not st.session_state['declined_suggested']:
            st.info(f"🔑 **Suggested Secure Password:** `{st.session_state['suggested_pw']}`")
            
            c_acc, c_dec = st.columns(2)
            with c_acc:
                if st.button("Accept Suggested", use_container_width=True):
                    password_to_use = st.session_state['suggested_pw']
            with c_dec:
                if st.button("Use Own Password", use_container_width=True):
                    st.session_state['declined_suggested'] = True
                    st.rerun()
        else:
            password_to_use = st.text_input("Custom Password", type="password")
            if st.button("Re-enable Suggested Password"):
                st.session_state['declined_suggested'] = False
                st.rerun()

        st.write("---")
        
        if st.button("Unlock Platform Workspace 🚀", use_container_width=True, type="primary"):
            if not first_name:
                st.warning("First name is required.")
            elif not email or email_error:
                st.warning("Please provide a valid email address.")
            elif not password_to_use:
                st.warning("Please specify or accept a password.")
            else:
                st.session_state['user_name'] = f"{first_name} {middle_name}".strip()
                st.session_state['authenticated'] = True
                st.success("Registration successful! Loading workspace...")
                time.sleep(1)
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)


# --- 3. MAIN APPLICATION DASHBOARD WORKSPACE ---
else:
    # Top Navigation Header with Active Data Badge
    col_nav1, col_nav2 = st.columns([2, 1])
    with col_nav1:
        st.markdown("### ⚡ DA-CRE Analysis Hub")
    with col_nav2:
        if st.session_state['active_file_name']:
            st.markdown(f'<div class="my-data-pill">📂 MY DATA: {st.session_state["active_file_name"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="my-data-pill-empty">📂 MY DATA: Empty</div>', unsafe_allow_html=True)

    st.write("---")

    # Navigation Controls in Sidebar
    st.sidebar.title(f"👤 {st.session_state.get('user_name', 'User')}")
    
    action_choice = st.sidebar.selectbox(
        "Platform Navigation",
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

    # SECTION 1: OPEN FILE VAULT
    if action_choice == "📂 Open File Vault (Select Active Data)":
        st.subheader("📂 Saved File Library (File Vault)")
        
        vault_files = list(st.session_state['file_vault'].keys())
        
        if len(vault_files) > 0:
            selected_vault_file = st.selectbox("Select a saved file to activate:", vault_files)
            
            if st.button("Set as Active in MY DATA 🚀", use_container_width=True):
                st.session_state['current_data'] = st.session_state['file_vault'][selected_vault_file]
                st.session_state['active_file_name'] = selected_vault_file
                st.success(f"'{selected_vault_file}' is now set to active!")
                st.rerun()
                
            if st.session_state['current_data'] is not None and st.session_state['active_file_name'] == selected_vault_file:
                st.write("---")
                st.write(f"Active Dataset Preview (**{selected_vault_file}**):")
                if isinstance(st.session_state['current_data'], pd.DataFrame):
                    st.dataframe(st.session_state['current_data'].head(10))
                else:
                    st.write(st.session_state['current_data'])
        else:
            st.info("Your File Vault is currently empty. Go to '📥 Add New Files to Vault' in the left menu to add your files!")

    # SECTION 2: ADD NEW FILES TO VAULT
    elif action_choice == "📥 Add New Files to Vault":
        st.subheader("📥 Add Files to Your Workspace")
        
        uploaded_files = st.file_uploader(
            "Select any file from your device or Google Drive", 
            accept_multiple_files=True
        )
        
        if uploaded_files:
            for file in uploaded_files:
                file_ext = file.name.split('.')[-1].lower()
                try:
                    if file_ext == 'csv':
                        df = pd.read_csv(file)
                        st.session_state['file_vault'][file.name] = df
                        st.success(f"Loaded CSV: '{file.name}' into Vault!")
                    elif file_ext in ['xlsx', 'xls']:
                        df = pd.read_excel(file)
                        st.session_state['file_vault'][file.name] = df
                        st.success(f"Loaded Excel Sheet: '{file.name}' into Vault!")
                    elif file_ext in ['txt', 'json', 'md']:
                        content = file.read().decode('utf-8')
                        st.session_state['file_vault'][file.name] = content
                        st.success(f"Loaded Document: '{file.name}' into Vault!")
                    else:
                        st.session_state['file_vault'][file.name] = file
                        st.success(f"Saved File: '{file.name}' into Vault!")
                except Exception as e:
                    st.error(f"Error loading {file.name}: {e}")
            
            st.info("Switch to '📂 Open File Vault' in the sidebar dropdown to view and open your saved files!")

    # SECTION 3: WEB SCRAPER
    elif action_choice == "🌐 Collect Data from Web":
        st.subheader("🌐 Web Scraper Engine")
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
                                    st.success(f"Saved {file_title} to File Vault and set as active!")
                                    st.rerun()
                except Exception as e:
                    st.error(f"Scraper error: {e}")

    # SECTION 4: CLEAN ACTIVE DATASET
    elif action_choice == "🧹 Clean Active Dataset":
        st.subheader("🧹 Automated Cleaning Options")
        if st.session_state['current_data'] is not None and isinstance(st.session_state['current_data'], pd.DataFrame):
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
            st.info("No active tabular dataset in MY DATA. Open a CSV/Excel file from your File Vault first.")

    # SECTION 5: DATA VISUALIZATIONS
    elif action_choice == "📊 Data Visualizations":
        st.subheader("📊 Interactive Visualizations")
        if st.session_state['current_data'] is not None and isinstance(st.session_state['current_data'], pd.DataFrame):
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
                st.warning("Numeric columns are required to generate graphs.")
        else:
            st.info("No active tabular dataset selected. Open a file from your File Vault first.")

    # SECTION 6: EXPORT OPTIONS
    elif action_choice == "🚀 Export to Google/Docs/Excel":
        st.subheader("🚀 Export Options")
        if st.session_state['current_data'] is not None:
            col_e1, col_e2 = st.columns(2)
            
            with col_e1:
                st.markdown("#### 🟢 Google Apps")
                st.link_button("Open Google Sheets 🟢", "https://sheets.new", use_container_width=True)
                st.link_button("Open Google Docs 📄", "https://docs.new", use_container_width=True)
                st.link_button("Open Google Slides 📊", "https://slides.new", use_container_width=True)

            with col_e2:
                st.markdown("#### 🔵 Local Export")
                if isinstance(st.session_state['current_data'], pd.DataFrame):
                    csv_bytes = st.session_state['current_data'].to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download Cleaned CSV/Excel File 📥",
                        data=csv_bytes,
                        file_name=f"DA_CRE_{st.session_state['active_file_name']}",
                        mime="text/csv",
                        use_container_width=True
                    )
        else:
            st.info("No active dataset in MY DATA to export. Open a file from your File Vault first.")
