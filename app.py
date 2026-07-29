import streamlit as st
import pandas as pd
import numpy as np
import hashlib
import time
import io
import json
import os
import base64
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# DACRE ANALYSIS 2026 PROFESSIONAL EDITION
# ==========================================================

APP_NAME = "DACRE ANALYSIS"
APP_VERSION = "Enterprise 2026"

PRIMARY_LOGO_FILENAME = "ChatGPT Image Jul 29, 2026, 02_27_41 PM.png"
RAW_GITHUB_LOGO_URL = "https://raw.githubusercontent.com/DaCreLabs/DA-CRE-Analysis/main/ChatGPT%20Image%20Jul%2029%2C%202026%2C%2002_27_41%20PM.png"

# ---------------- PAGE CONFIG WITH FAVICON LOGO ----------------
st.set_page_config(
    page_title="DACRE ANALYSIS",
    page_icon=RAW_GITHUB_LOGO_URL,
    layout="wide",
    initial_sidebar_state="expanded"
)

ADMIN_SECRET_KEY = "theWORDofGOD"

# ---------------- LOGO RENDER ENGINE ----------------
def get_logo_html(width=260):
    if os.path.exists(PRIMARY_LOGO_FILENAME):
        try:
            with open(PRIMARY_LOGO_FILENAME, "rb") as img_file:
                b64 = base64.b64encode(img_file.read()).decode()
                return f'<div style="text-align:center; position:relative; z-index:2; margin-bottom:15px;"><img src="data:image/png;base64,{b64}" style="max-width:{width}px; border-radius:12px; box-shadow:0 8px 20px rgba(0,0,0,0.5);"></div>'
        except Exception:
            pass
    return f'<div style="text-align:center; position:relative; z-index:2; margin-bottom:15px;"><img src="{RAW_GITHUB_LOGO_URL}" style="max-width:{width}px; border-radius:12px; box-shadow:0 8px 20px rgba(0,0,0,0.5);"></div>'

# ---------------- INITIAL 5-SECOND LOADING EFFECT ----------------
if 'app_loaded' not in st.session_state:
    st.session_state['app_loaded'] = False

if not st.session_state['app_loaded']:
    loading_placeholder = st.empty()
    with loading_placeholder.container():
        st.markdown(f"""
        <div style="
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 80vh;
            text-align: center;
        ">
            <img src="{RAW_GITHUB_LOGO_URL}" style="width: 180px; border-radius: 20px; animation: pulse 1.5s infinite ease-in-out; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
            <h1 style="color: #ffffff; font-weight: 900; font-size: 50px; font-family: sans-serif; letter-spacing: 2px; margin-top: 20px;">DACRE ANALYSIS</h1>
            <p style="color: #94a3b8; font-weight: 600; font-size: 18px;">Initializing Enterprise Environment...</p>
            <div style="
                border: 4px solid rgba(255,255,255,0.1);
                border-left-color: #38bdf8;
                border-radius: 50%;
                width: 45px;
                height: 45px;
                animation: spin 1s linear infinite;
                margin-top: 20px;
            "></div>
        </div>
        <style>
            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
            @keyframes pulse {{
                0% {{ transform: scale(1); opacity: 0.8; }}
                50% {{ transform: scale(1.08); opacity: 1; }}
                100% {{ transform: scale(1); opacity: 0.8; }}
            }}
        </style>
        """, unsafe_allow_html=True)
        time.sleep(5)
    loading_placeholder.empty()
    st.session_state['app_loaded'] = True

# ---------------- THEME & CUSTOM STYLING ----------------
st.markdown("""
<style>
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* BACKGROUND & SKY ANIMATION */
.stApp {
    background: radial-gradient(circle at 50% 20%, #0d1b2a, #0b131f, #050a0f);
    color: #ffffff;
    overflow-x: hidden;
}

.sky-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}

.cloud {
    position: absolute;
    background: radial-gradient(circle, rgba(56, 189, 248, 0.15) 0%, rgba(2, 132, 199, 0) 70%);
    border-radius: 50%;
    animation: floatSky 12s infinite ease-in-out;
}

.cloud-1 { width: 350px; height: 350px; top: 10%; left: -5%; animation-duration: 16s; }
.cloud-2 { width: 450px; height: 450px; top: 55%; right: -10%; animation-duration: 20s; animation-delay: -5s; }
.cloud-3 { width: 250px; height: 250px; top: 30%; left: 60%; animation-duration: 14s; animation-delay: -8s; }

@keyframes floatSky {
    0% { transform: translateY(0px) translateX(0px) scale(1); opacity: 0.4; }
    50% { transform: translateY(-30px) translateX(20px) scale(1.1); opacity: 0.8; }
    100% { transform: translateY(0px) translateX(0px) scale(1); opacity: 0.4; }
}

/* FORCED WHITE FIELD LABELS (Username, Password, etc.) */
label, 
.stTextInput label, 
.stSelectbox label, 
.stFileUploader label,
div[data-testid="stWidgetLabel"] p {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 16px !important;
}

/* HERO CONTAINER & BOLD WHITE TEXT */
.hero {
    padding: 30px;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.85), rgba(15, 23, 42, 0.95));
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0px 15px 35px rgba(0,0,0,.6);
    margin-bottom: 25px;
    margin-top: 10px;
    text-align: center;
    position: relative;
    z-index: 2;
    animation: fadeInSlide 1.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.hero h1 {
    font-size: 48px;
    font-weight: 900 !important;
    color: #ffffff !important;
    margin-bottom: 10px;
    letter-spacing: 1.5px;
}

.hero h3 {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 22px;
}

.hero p {
    color: #cbd5e1 !important;
    font-weight: 600 !important;
    font-size: 15px;
}

/* ALL FILL-IN INPUT BARS -> LIGHT BROWN COLORFILL & GREY PLACEHOLDERS */
div[data-baseweb="input"] > div, 
input, 
textarea, 
.stSelectbox > div > div {
    background-color: #d7ccc8 !important;
    color: #1a0f0d !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    border: 1px solid #a1887f !important;
}

/* Grey Placeholders styling */
input::placeholder {
    color: #757575 !important;
    font-style: italic;
    font-weight: 500 !important;
}

/* ANIMATED SIGN IN / REGISTER PANE LANDING EFFECT */
div[data-testid="stForm"], 
.stTabs {
    animation: fadeInSlide 1.2s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeInSlide {
    0% {
        opacity: 0;
        transform: translateY(40px) scale(0.96);
    }
    100% {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

.stButton>button {
    background: linear-gradient(90deg, #0284c7, #0891b2);
    color: white;
    font-weight: bold;
    border-radius: 12px;
    height: 48px;
    border: none;
}

.stButton>button:hover {
    transform: scale(1.02);
    background: #0369a1;
}

/* CAPTCHA BOX STYLING */
.captcha-box {
    background: rgba(15, 23, 42, 0.9);
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #0284c7;
    margin-bottom: 15px;
}
</style>

<!-- ANIMATED BACKGROUND ELEMENTS -->
<div class="sky-container">
    <div class="cloud cloud-1"></div>
    <div class="cloud cloud-2"></div>
    <div class="cloud cloud-3"></div>
</div>
""", unsafe_allow_html=True)

# ---------------- SESSION-BASED DATABASE ENGINE ----------------
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

if "users_db" not in st.session_state:
    st.session_state.users_db = {}

if "active_sessions" not in st.session_state:
    st.session_state.active_sessions = {}

if "logs_db" not in st.session_state:
    st.session_state.logs_db = []

def add_user(username, email, password, role="User"):
    if username in st.session_state.users_db:
        return False
    st.session_state.users_db[username] = {
        "email": email,
        "password_hash": make_hashes(password),
        "role": role,
        "created_at": str(datetime.now())
    }
    return True

def login_user(username, password):
    user = st.session_state.users_db.get(username)
    if user and check_hashes(password, user["password_hash"]):
        st.session_state.active_sessions[username] = str(datetime.now())
        return user
    return None

def log_action(user, action):
    st.session_state.logs_db.append({
        "user": user,
        "action": action,
        "timestamp": str(datetime.now())
    })

# ---------------- RECAPTCHA HUMAN VERIFICATION ENGINE ----------------
def bus_recaptcha_widget(key_prefix="auth"):
    st.markdown('<div class="captcha-box">', unsafe_allow_html=True)
    st.write("🤖 **reCAPTCHA: Verify you are human**")
    st.caption("Select the image below that contains a **Bus**:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("📷 Option A")
        st.markdown("🚗 *Car*")
    with col2:
        st.write("📷 Option B")
        st.markdown("🚌 *Bus*")
    with col3:
        st.write("📷 Option C")
        st.markdown("🚲 *Bicycle*")
        
    choice = st.radio("Which image shows a Bus?", ["Select Option...", "Option A (Car)", "Option B (Bus)", "Option C (Bicycle)"], key=f"{key_prefix}_captcha_choice")
    st.markdown('</div>', unsafe_allow_html=True)
    
    return choice == "Option B (Bus)"

# ---------------- SESSION STATE INITIALIZATION ----------------
if 'authenticated' not in st.session_state:
    st.session_state["authenticated"] = False
if 'user_name' not in st.session_state:
    st.session_state["user_name"] = ""
if 'user_email' not in st.session_state:
    st.session_state["user_email"] = ""
if 'role' not in st.session_state:
    st.session_state["role"] = None
if 'current_data' not in st.session_state:
    st.session_state["current_data"] = None
if 'formula_logs' not in st.session_state:
    st.session_state["formula_logs"] = []
if 'auth_mode' not in st.session_state:
    st.session_state['auth_mode'] = 'User Portal'
if 'selected_auth_tab' not in st.session_state:
    st.session_state['selected_auth_tab'] = 0

# Check forced logout by Admin
if st.session_state["authenticated"] and st.session_state["user_name"] in st.session_state.get("forced_logouts", []):
    st.session_state["authenticated"] = False
    st.session_state["forced_logouts"].remove(st.session_state["user_name"])
    st.warning("⚠️ You have been logged out by the System Administrator.")
    st.rerun()

# ---------------- MAIN APP LOGO & LANDING HEADER ----------------
st.markdown(get_logo_html(260), unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>DACRE ANALYSIS</h1>
    <h3>Enterprise AI Spreadsheet & Data Analytics Platform</h3>
    <p>Upload • Clean • Analyse • Visualize • Automate • Export</p>
</div>
""", unsafe_allow_html=True)

# ---------------- AUTHENTICATION & ADMIN PORTAL ----------------
if not st.session_state["authenticated"]:
    
    auth_portal_choice = st.radio("Select Portal:", ["👤 User Access", "🛡️ Admin Portal"], horizontal=True)
    
    # ================= USER PORTAL =================
    if auth_portal_choice == "👤 User Access":
        
        auth_tab1, auth_tab2 = st.tabs(["🔒 Sign In", "📝 Register"])
        
        # --- LOGIN TAB ---
        with auth_tab1:
            st.subheader("User Login")
            login_user_input = st.text_input("Username", placeholder="uchechukwudavid", key="login_user")
            login_pass_input = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pass")
            
            is_human = bus_recaptcha_widget("login")
            
            if st.button("Sign In"):
                if not is_human:
                    st.error("❌ Human verification failed! Please select the picture with the Bus.")
                elif login_user_input not in st.session_state.users_db:
                    st.error("⚠️ Account has not been created. Please sign up!")
                else:
                    user_data = login_user(login_user_input, login_pass_input)
                    if user_data:
                        st.session_state["authenticated"] = True
                        st.session_state["user_name"] = login_user_input
                        st.session_state["user_email"] = user_data["email"]
                        st.session_state["role"] = user_data["role"]
                        log_action(login_user_input, "User Logged In")
                        st.success(f"Welcome back, {login_user_input}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid Password. Please check your credentials.")

        # --- REGISTER TAB ---
        with auth_tab2:
            st.subheader("Create New User Account")
            reg_user = st.text_input("Username", placeholder="uchechukwudavid", key="reg_user")
            reg_email = st.text_input("Email Address", placeholder="david@example.com", key="reg_email")
            reg_pass = st.text_input("New Password", type="password", placeholder="Create a strong password", key="reg_pass")
            
            is_human_reg = bus_recaptcha_widget("register")
            
            if st.button("Register Account"):
                if not is_human_reg:
                    st.error("❌ Human verification failed! Please select the picture with the Bus.")
                elif reg_user in st.session_state.users_db:
                    st.warning("⚠️ This account has already been added! Redirecting to Sign In...")
                    time.sleep(2)
                    st.rerun()
                elif reg_user and reg_pass and reg_email:
                    if add_user(reg_user, reg_email, reg_pass, role="User"):
                        st.success("🎉 Account created successfully! Please sign in now.")
                        log_action(reg_user, "Account Created")
                    else:
                        st.error("Username already exists.")
                else:
                    st.warning("Please fill out all required fields.")

    # ================= ISOLATED ADMIN PORTAL =================
    else:
        st.subheader("🛡️ Dedicated Admin Security Gateway")
        st.info("Authorized System Administrators Only.")
        
        admin_passkey = st.text_input("Enter Admin Passkey", type="password", placeholder="Enter secret key", key="admin_key")
        is_human_admin = bus_recaptcha_widget("admin")
        
        if st.button("Unlock Admin Control Panel"):
            if not is_human_admin:
                st.error("❌ Human verification failed! Select the Bus image.")
            elif admin_passkey == ADMIN_SECRET_KEY:
                st.session_state["authenticated"] = True
                st.session_state["user_name"] = "System Administrator"
                st.session_state["user_email"] = "admin@dacre.ai"
                st.session_state["role"] = "Admin"
                log_action("Admin", "Admin Panel Unlocked")
                st.success("Access Granted! Loading Enterprise Admin Panel...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Incorrect Admin Secret Passkey.")

# ---------------- MAIN APPLICATION INTERFACE (LOGGED IN) ----------------
else:
    with st.sidebar:
        st.markdown(get_logo_html(180), unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(f"## 👋 Welcome, {st.session_state['user_name']}")
        st.caption(f"Role: **{st.session_state['role']}**")

        st.markdown("---")

        nav_options = [
            "🏠 Dashboard",
            "📊 Embedded Sheet & Formula Board",
            "📂 File Vault to Workflow Engine",
            "📥 Add New Files to Vault"
        ]
        
        if st.session_state["role"] == "Admin":
            nav_options.append("🛡️ Master Admin Control Center")

        menu = st.selectbox("Navigation", nav_options)

        st.markdown("---")

        if st.button("🚪 Logout", use_container_width=True):
            if st.session_state["user_name"] in st.session_state.get("active_sessions", {}):
                del st.session_state.active_sessions[st.session_state["user_name"]]
            st.session_state["authenticated"] = False
            st.rerun()

    # ==========================================================
    # NAVIGATION ROUTING
    # ==========================================================

    if menu == "🏠 Dashboard":
        st.title("📊 Executive Dashboard")

        c1, c2, c3, c4 = st.columns(4)

        total_rows = 0
        total_columns = 0

        if st.session_state.get("current_data") is not None and isinstance(st.session_state["current_data"], pd.DataFrame):
            total_rows = len(st.session_state["current_data"])
            total_columns = len(st.session_state["current_data"].columns)

        with c1:
            st.metric("Rows", total_rows)
        with c2:
            st.metric("Columns", total_columns)
        with c3:
            st.metric("Formula Logs", len(st.session_state["formula_logs"]))
        with c4:
            st.metric("Status", "Ready")

        st.write("")

        if st.session_state.get("current_data") is not None and isinstance(st.session_state["current_data"], pd.DataFrame):
            df = st.session_state["current_data"]
            numeric = df.select_dtypes(include="number")
            if len(numeric.columns) > 0:
                chart = px.histogram(numeric, x=numeric.columns[0], template="plotly_dark", title="Distribution")
                st.plotly_chart(chart, use_container_width=True)
                st.write("### Numeric Summary")
                st.dataframe(numeric.describe(), use_container_width=True)
            else:
                st.info("No numeric columns available yet.")
        else:
            st.info("Upload a dataset to begin analysis.")

    elif menu == "📊 Embedded Sheet & Formula Board":
        st.title("📊 Embedded Sheet & Formula Board")
        if st.session_state["current_data"] is None:
            st.info("No data active. Upload or load a file from 'Add New Files to Vault'.")
        else:
            edited_df = st.data_editor(st.session_state["current_data"], num_rows="dynamic", use_container_width=True)
            st.session_state["current_data"] = edited_df

    elif menu == "📂 File Vault to Workflow Engine":
        st.title("📂 File Vault & Workflow Engine")
        st.write("Manage active workspace data files and automated workflow rules.")

    elif menu == "📥 Add New Files to Vault":
        st.title("📥 Upload New Data to Vault")
        uploaded_file = st.file_uploader("Choose CSV or Excel File", type=["csv", "xlsx", "xls"])
        if uploaded_file:
            try:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                st.session_state["current_data"] = df
                log_action(st.session_state["user_name"], f"Uploaded File: {uploaded_file.name}")
                st.success(f"Loaded '{uploaded_file.name}' with {len(df)} rows into active workspace!")
            except Exception as e:
                st.error(f"Failed to process file: {e}")

    # ================= MASTER ADMIN CONTROL CENTER =================
    elif menu == "🛡️ Master Admin Control Center":
        st.title("🛡️ Master Admin Control Center")
        st.caption("Full Administrative & System Supervision Interface")
        
        st.markdown("### ℹ️ App Functionality & Architecture")
        st.info("""
        **DACRE ANALYSIS** is an enterprise AI-powered spreadsheet cleaning, analytics, and workflow automation platform. 
        It allows users to upload datasets, perform real-time data cleaning, run formula logs, generate distribution charts, and export results.
        """)

        st.markdown("---")
        
        # --- ADMIN METRICS ---
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Registered Users", len(st.session_state.users_db))
        with m2:
            st.metric("Active Sessions", len(st.session_state.active_sessions))
        with m3:
            st.metric("Total Audit Logs", len(st.session_state.logs_db))

        st.markdown("---")

        # --- USER MANAGEMENT & FORCE LOGOUT ---
        st.subheader("👥 Registered User Management & Remote Logout Controls")
        
        if len(st.session_state.users_db) == 0:
            st.info("No users registered yet.")
        else:
            user_table = []
            for u, d in st.session_state.users_db.items():
                user_table.append({
                    "Username": u,
                    "Email": d["email"],
                    "Role": d["role"],
                    "Registered At": d["created_at"],
                    "Status": "Online 🟢" if u in st.session_state.active_sessions else "Offline ⚪"
                })
            
            st.dataframe(pd.DataFrame(user_table), use_container_width=True)

            st.write("#### 🚨 Force Disconnect / Logout Any User")
            user_to_kick = st.selectbox("Select User to Terminate Session:", ["None"] + list(st.session_state.users_db.keys()))
            
            if st.button("🔴 Terminate Selected User Session") and user_to_kick != "None":
                if "forced_logouts" not in st.session_state:
                    st.session_state["forced_logouts"] = []
                st.session_state["forced_logouts"].append(user_to_kick)
                if user_to_kick in st.session_state.active_sessions:
                    del st.session_state.active_sessions[user_to_kick]
                log_action("Admin", f"Force logged out user: {user_to_kick}")
                st.success(f"User '{user_to_kick}' has been forcefully logged out.")
                st.rerun()

        st.markdown("---")
        
        # --- AUDIT LOGS ---
        st.subheader("📜 System Audit & Activity Logs")
        st.dataframe(pd.DataFrame(st.session_state.logs_db), use_container_width=True)
