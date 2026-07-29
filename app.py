import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import hashlib
import time
import io
import json
import base64
import os
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

# DO NOT CHANGE THIS
ADMIN_SECRET_KEY = "theWORDofGOD"

# ---------------- THEME ----------------
st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

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
    text-align: center;
}

.hero h1 {
    font-size: 50px;
    font-weight: 900;
    color: white;
}

.hero h3 {
    color: #dbeafe;
}

.metric-card {
    background: #111827;
    padding: 18px;
    border-radius: 15px;
    border: 1px solid #38bdf8;
    box-shadow: 0 0 18px rgba(56,189,248,.2);
}

.logo {
    display: flex;
    justify-content: center;
    margin-top: 10px;
    margin-bottom: 15px;
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

input {
    font-weight: bold !important;
}

[data-baseweb="select"] {
    font-weight: bold !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOGO ENGINE ----------------
# Fallback online logo or local file detection
def get_logo_html(width=180):
    if os.path.exists("dacre_logo.png"):
        try:
            with open("dacre_logo.png", "rb") as img:
                b64 = base64.b64encode(img.read()).decode()
                return f'<img src="data:image/png;base64,{b64}" width="{width}">'
        except Exception:
            pass
    return f'<h1 style="color:#38bdf8; font-weight:900;">📊 DACRE</h1>'

# ---------------- SAFE DATABASE ENGINE ----------------
DB_FILE = "dacre_platform.db"

def get_db_connection():
    return sqlite3.connect(DB_FILE, timeout=10)

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        email TEXT,
                        password_hash TEXT,
                        role TEXT,
                        created_at TEXT
                    )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS system_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user TEXT,
                        action TEXT,
                        timestamp TEXT
                    )''')
        conn.commit()
    except Exception:
        # Re-create database if corrupted schema exists
        conn.close()
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        email TEXT,
                        password_hash TEXT,
                        role TEXT,
                        created_at TEXT
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS system_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user TEXT,
                        action TEXT,
                        timestamp TEXT
                    )''')
        conn.commit()
    finally:
        conn.close()

init_db()

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

def add_user(username, email, password, role="User"):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users(username, email, password_hash, role, created_at) VALUES (?,?,?,?,?)",
                  (username, email, make_hashes(password), role, str(datetime.now())))
        conn.commit()
        success = True
    except Exception:
        success = False
    finally:
        conn.close()
    return success

def login_user(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT email, password_hash, role FROM users WHERE username=?", (username,))
    data = c.fetchone()
    conn.close()
    if data and check_hashes(password, data[1]):
        return {"email": data[0] if data[0] else f"{username}@dacre.ai", "role": data[2]}
    return None

def log_action(user, action):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO system_logs(user, action, timestamp) VALUES (?,?,?)",
                  (user, action, str(datetime.now())))
        conn.commit()
        conn.close()
    except Exception:
        pass

def ensure_admin_exists():
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username='admin'")
        if not c.fetchone():
            c.execute("INSERT INTO users(username, email, password_hash, role, created_at) VALUES (?,?,?,?,?)",
                      ("admin", "admin@dacre.ai", make_hashes(ADMIN_SECRET_KEY), "Admin", str(datetime.now())))
            conn.commit()
        conn.close()
    except Exception:
        pass

ensure_admin_exists()

# ---------------- HELPER FUNCTIONS ----------------
def trigger_audio_guide(text):
    st.info(f"🔊 **AI Voice Guide:** \"{text}\"")

def sync_to_database_workflow():
    pass

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

# ---------------- LANDING HEADER ----------------
st.markdown(f'<div class="logo">{get_logo_html(220)}</div>', unsafe_allow_html=True)

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
        st.markdown(f'<div style="text-align:center;">{get_logo_html(160)}</div>', unsafe_allow_html=True)

        st.markdown("---")

        st.markdown(f"## 👋 Welcome")

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
            sync_to_database_workflow()
            st.session_state["authenticated"] = False
            st.rerun()

    # ==========================================================
    # NAVIGATION ROUTING
    # ==========================================================

    # --- HOME DASHBOARD ---
    if menu == "🏠 Dashboard":
        st.title("📊 Executive Dashboard")

        c1, c2, c3, c4 = st.columns(4)

        total_rows = 0
        total_columns = 0

        if (
            st.session_state.get("current_data") is not None
            and isinstance(st.session_state["current_data"], pd.DataFrame)
        ):
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

        if (
            st.session_state.get("current_data") is not None
            and isinstance(st.session_state["current_data"], pd.DataFrame)
        ):

            df = st.session_state["current_data"]

            numeric = df.select_dtypes(include="number")

            if len(numeric.columns) > 0:

                chart = px.histogram(
                    numeric,
                    x=numeric.columns[0],
                    template="plotly_dark",
                    title="Distribution",
                )

                st.plotly_chart(chart, use_container_width=True)

                st.write("### Numeric Summary")

                st.dataframe(numeric.describe(), use_container_width=True)

            else:

                st.info("No numeric columns available yet.")

        else:

            st.info("Upload a dataset to begin analysis.")

        st.write("---")

        st.subheader("🎙 Nigerian AI Audio Guide")

        trigger_audio_guide(
            "Welcome to Dacre Analysis. Upload your spreadsheet to begin powerful analysis. Use the File Vault to manage your files, then explore charts and formulas from the dashboard."
        )

    # --- EMBEDDED SHEET & FORMULA BOARD ---
    elif menu == "📊 Embedded Sheet & Formula Board":
        st.title("📊 Embedded Sheet & Formula Board")
        if st.session_state["current_data"] is None:
            st.info("No data active. Upload or load a file from 'Add New Files to Vault'.")
        else:
            edited_df = st.data_editor(st.session_state["current_data"], num_rows="dynamic", use_container_width=True)
            st.session_state["current_data"] = edited_df

    # --- FILE VAULT & WORKFLOW ---
    elif menu == "📂 File Vault to Workflow Engine":
        st.title("📂 File Vault & Workflow Engine")
        st.write("Manage active workspace data files and automated workflow rules.")

    # --- ADD NEW FILES TO VAULT ---
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

    # --- ADMIN CONTROL PANEL ---
    elif menu == "🛡️ Admin Control Panel":
        st.title("🛡️ Admin Control Panel")
        if st.session_state["role"] != "Admin":
            st.error("Access Restricted: Admin privileges required.")
        else:
            conn = get_db_connection()
            st.subheader("User Directory")
            users_df = pd.read_sql_query("SELECT id, username, email, role, created_at FROM users", conn)
            st.dataframe(users_df, use_container_width=True)

            st.subheader("Audit Logs")
            logs_df = pd.read_sql_query("SELECT * FROM system_logs ORDER BY timestamp DESC", conn)
            st.dataframe(logs_df, use_container_width=True)
            conn.close()
