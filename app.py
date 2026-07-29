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

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="DACRE ANALYSIS",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

ADMIN_SECRET_KEY = "theWORDofGOD"

# ---------------- LOGO ENGINE (EXACT GITHUB FILE MATCH) ----------------
PRIMARY_LOGO_FILENAME = "ChatGPT Image Jul 29, 2026, 02_27_41 PM.png"
RAW_GITHUB_LOGO_URL = "https://raw.githubusercontent.com/DaCreLabs/DA-CRE-Analysis/main/ChatGPT%20Image%20Jul%2029%2C%202026%2C%2002_27_41%20PM.png"

def get_logo_html(width=250):
    # Check 1: Local repository file
    if os.path.exists(PRIMARY_LOGO_FILENAME):
        try:
            with open(PRIMARY_LOGO_FILENAME, "rb") as img_file:
                b64 = base64.b64encode(img_file.read()).decode()
                return f'<div style="text-align:center;"><img src="data:image/png;base64,{b64}" style="max-width:{width}px; border-radius:12px; box-shadow:0 8px 20px rgba(0,0,0,0.5);"></div>'
        except Exception:
            pass

    # Check 2: Direct Raw GitHub CDN
    return f'<div style="text-align:center;"><img src="{RAW_GITHUB_LOGO_URL}" style="max-width:{width}px; border-radius:12px; box-shadow:0 8px 20px rgba(0,0,0,0.5);"></div>'

# ---------------- THEME ----------------
st.markdown("""
<style>
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

.stApp {
    background: linear-gradient(135deg, #07111f, #0f172a, #111827);
    color: white;
}

.hero {
    padding: 25px;
    border-radius: 18px;
    background: linear-gradient(135deg, #0284c7, #0f766e);
    box-shadow: 0px 15px 35px rgba(0,0,0,.45);
    margin-bottom: 20px;
    margin-top: 15px;
    text-align: center;
}

.hero h1 {
    font-size: 45px;
    font-weight: 900;
    color: white;
}

.hero h3 {
    color: #dbeafe;
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
</style>
""", unsafe_allow_html=True)

# ---------------- FAIL-PROOF SESSION-BASED DATABASE ENGINE ----------------
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "admin": {
            "email": "admin@dacre.ai",
            "password_hash": make_hashes(ADMIN_SECRET_KEY),
            "role": "Admin",
            "created_at": str(datetime.now())
        }
    }

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
        return user
    return None

def log_action(user, action):
    st.session_state.logs_db.append({
        "user": user,
        "action": action,
        "timestamp": str(datetime.now())
    })

# ---------------- HELPER FUNCTIONS ----------------
def trigger_audio_guide(text):
    st.info(f"🔊 **AI Voice Guide:** \"{text}\"")

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

# ---------------- LANDING HEADER & LOGO ----------------
st.markdown(get_logo_html(300), unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🚀 DACRE ANALYSIS</h1>
    <h3>Enterprise AI Spreadsheet & Data Analytics Platform</h3>
    <p>Upload • Clean • Analyse • Visualize • Automate • Export</p>
</div>
""", unsafe_allow_html=True)

# ---------------- AUTHENTICATION SCREEN ----------------
if not st.session_state["authenticated"]:
    auth_tab1, auth_tab2 = st.tabs(["🔒 Login", "📝 Register"])
    
    with auth_tab1:
        st.subheader("Account Login")
        login_user_input = st.text_input("Username", key="login_user")
        login_pass_input = st.text_input("Password", type="password", key="login_pass")
        if st.button("Sign In"):
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
                st.error("Invalid Username or Password.")

    with auth_tab2:
        st.subheader("Create New Account")
        reg_user = st.text_input("New Username", key="reg_user")
        reg_email = st.text_input("Email Address", key="reg_email")
        reg_pass = st.text_input("New Password", type="password", key="reg_pass")
        reg_secret = st.text_input("Admin Secret Key (Optional for Admin Role)", type="password", key="reg_secret")
        
        if st.button("Register"):
            if reg_user and reg_pass and reg_email:
                role = "Admin" if reg_secret == ADMIN_SECRET_KEY else "User"
                if add_user(reg_user, reg_email, reg_pass, role):
                    st.success("Account created successfully! Please log in.")
                    log_action(reg_user, f"Account Created ({role})")
                else:
                    st.error("Username already exists.")
            else:
                st.warning("Please fill out all required fields.")

# ---------------- MAIN APPLICATION INTERFACE ----------------
else:
    # ==========================================================
    # PREMIUM ENTERPRISE SIDEBAR
    # ==========================================================
    with st.sidebar:
        st.markdown(get_logo_html(180), unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("## 👋 Welcome")
        st.success(st.session_state["user_name"])
        st.caption(st.session_state["user_email"])

        st.markdown("---")

        menu = st.selectbox(
            "Navigation",
            [
                "🏠 Dashboard",
                "📊 Embedded Sheet & Formula Board",
                "📂 File Vault to Workflow Engine",
                "📥 Add New Files to Vault",
                "🛡️ Admin Control Panel",
            ],
        )

        st.markdown("---")

        st.info("DACRE ANALYSIS\nEnterprise Edition")

        if st.button("🚪 Logout", use_container_width=True):
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

        st.write("---")
        st.subheader("🎙 Nigerian AI Audio Guide")
        trigger_audio_guide("Welcome to Dacre Analysis. Upload your spreadsheet to begin powerful analysis. Use the File Vault to manage your files, then explore charts and formulas from the dashboard.")

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

    elif menu == "🛡️ Admin Control Panel":
        st.title("🛡️ Admin Control Panel")
        if st.session_state["role"] != "Admin":
            st.error("Access Restricted: Admin privileges required.")
        else:
            st.subheader("User Directory")
            users_list = []
            for u, d in st.session_state.users_db.items():
                users_list.append({"username": u, "email": d["email"], "role": d["role"], "created_at": d["created_at"]})
            st.dataframe(pd.DataFrame(users_list), use_container_width=True)

            st.subheader("Audit Logs")
            st.dataframe(pd.DataFrame(st.session_state.logs_db), use_container_width=True)
