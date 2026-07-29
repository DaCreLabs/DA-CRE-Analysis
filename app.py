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
import streamlit.components.v1 as components

# ==========================================================
# DACRE ANALYSIS 2026 PROFESSIONAL EDITION
# ==========================================================

APP_NAME = "DACRE ANALYSIS"
APP_VERSION = "Enterprise 2026"

APP_LOGO_PATH = "dacre_logo.png"

# ---------------- LOGO ENGINE ----------------
def get_base64_logo(path):
    if os.path.exists(path):
        with open(path, "rb") as img:
            return "data:image/png;base64," + base64.b64encode(img.read()).decode()
    return None

logo_b64 = get_base64_logo(APP_LOGO_PATH)

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

# ---------------- LANDING HEADER ----------------

if logo_b64:
    st.markdown(f"""
    <div class="logo">
        <img src="{logo_b64}" width="180">
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🚀 DACRE ANALYSIS</h1>
    <h3>Enterprise AI Spreadsheet & Data Analytics Platform</h3>
    <p>Upload • Clean • Analyse • Visualize • Automate • Export</p>
</div>
""", unsafe_allow_html=True)

# ---------------- DATABASE ENGINE ----------------
DB_FILE = "dacre_platform.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
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
    conn.close()

init_db()

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

def add_user(username, password, role="User"):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users(username, password_hash, role, created_at) VALUES (?,?,?,?)",
                  (username, make_hashes(password), role, str(datetime.now())))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

def login_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT password_hash, role FROM users WHERE username=?", (username,))
    data = c.fetchone()
    conn.close()
    if data and check_hashes(password, data[0]):
        return data[1]
    return None

def log_action(user, action):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO system_logs(user, action, timestamp) VALUES (?,?,?)",
              (user, action, str(datetime.now())))
    conn.commit()
    conn.close()

# Ensure default admin exists
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
c.execute("SELECT * FROM users WHERE username='admin'")
if not c.fetchone():
    add_user("admin", ADMIN_SECRET_KEY, role="Admin")
conn.close()

# ---------------- SESSION STATE ----------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'role' not in st.session_state:
    st.session_state.role = None
if 'df' not in st.session_state:
    st.session_state.df = None

# ---------------- AUTHENTICATION UI ----------------
if not st.session_state.logged_in:
    auth_tab1, auth_tab2 = st.tabs(["🔒 Login", "📝 Register"])
    
    with auth_tab1:
        st.subheader("Account Login")
        login_user_input = st.text_input("Username", key="login_user")
        login_pass_input = st.text_input("Password", type="password", key="login_pass")
        if st.button("Sign In"):
            role = login_user(login_user_input, login_pass_input)
            if role:
                st.session_state.logged_in = True
                st.session_state.user = login_user_input
                st.session_state.role = role
                log_action(login_user_input, "User Logged In")
                st.success(f"Welcome back, {login_user_input}!")
                st.rerun()
            else:
                st.error("Invalid Username or Password.")

    with auth_tab2:
        st.subheader("Create New Account")
        reg_user = st.text_input("New Username", key="reg_user")
        reg_pass = st.text_input("New Password", type="password", key="reg_pass")
        reg_secret = st.text_input("Admin Secret Key (Optional for Admin Role)", type="password", key="reg_secret")
        
        if st.button("Register"):
            if reg_user and reg_pass:
                role = "Admin" if reg_secret == ADMIN_SECRET_KEY else "User"
                if add_user(reg_user, reg_pass, role):
                    st.success("Account created successfully! Please log in.")
                    log_action(reg_user, f"Account Created ({role})")
                else:
                    st.error("Username already exists.")
            else:
                st.warning("Please provide both username and password.")

# ---------------- MAIN APPLICATION ----------------
else:
    # Sidebar Navigation
    st.sidebar.markdown(f"### 👤 User: **{st.session_state.user}** ({st.session_state.role})")
    if st.sidebar.button("Logout"):
        log_action(st.session_state.user, "User Logged Out")
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None
        st.session_state.df = None
        st.rerun()

    st.sidebar.divider()
    app_mode = st.sidebar.radio("Navigation", ["📂 Data Workspace", "📈 Analytics & Charts", "⚙️ Admin Portal"])

    # --- DATA WORKSPACE ---
    if app_mode == "📂 Data Workspace":
        st.header("📂 Data Import & Management")
        
        uploaded_file = st.file_uploader("Upload CSV or Excel File", type=["csv", "xlsx", "xls"])
        if uploaded_file:
            try:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                st.session_state.df = df
                log_action(st.session_state.user, f"Uploaded Dataset: {uploaded_file.name}")
                st.success(f"Successfully loaded `{uploaded_file.name}` ({df.shape[0]} rows, {df.shape[1]} columns)")
            except Exception as e:
                st.error(f"Error loading file: {e}")

        if st.session_state.df is not None:
            df = st.session_state.df
            
            # Metrics Overview
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Rows", df.shape[0])
            m2.metric("Columns", df.shape[1])
            m3.metric("Numeric Fields", len(df.select_dtypes(include=np.number).columns))
            m4.metric("Missing Values", df.isnull().sum().sum())
            
            st.divider()
            
            # Data Preview & Editing
            st.subheader("Data Preview")
            edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
            st.session_state.df = edited_df

            # Quick Clean Options
            st.subheader("🧹 Cleaning Tools")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Drop Duplicate Rows"):
                    st.session_state.df = st.session_state.df.drop_duplicates()
                    st.success("Duplicates removed!")
                    st.rerun()
            with c2:
                if st.button("Fill NA with 0"):
                    st.session_state.df = st.session_state.df.fillna(0)
                    st.success("Missing values filled!")
                    st.rerun()

    # --- ANALYTICS & CHARTS ---
    elif app_mode == "📈 Analytics & Charts":
        st.header("📈 Interactive Analytics Engine")
        
        if st.session_state.df is None:
            st.warning("Please upload a dataset in the Data Workspace first.")
        else:
            df = st.session_state.df
            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
            all_cols = df.columns.tolist()

            if not numeric_cols:
                st.error("No numeric columns found in the uploaded dataset for charting.")
            else:
                chart_type = st.selectbox("Select Visual Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram"])
                col1, col2 = st.columns(2)
                
                with col1:
                    x_axis = st.selectbox("X-Axis Field", options=all_cols)
                with col2:
                    y_axis = st.selectbox("Y-Axis Field", options=numeric_cols)

                if chart_type == "Bar Chart":
                    fig = px.bar(df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}", template="plotly_dark")
                elif chart_type == "Line Chart":
                    fig = px.line(df, x=x_axis, y=y_axis, title=f"{y_axis} Trend over {x_axis}", template="plotly_dark")
                elif chart_type == "Scatter Plot":
                    fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}", template="plotly_dark")
                elif chart_type == "Histogram":
                    fig = px.histogram(df, x=y_axis, title=f"Distribution of {y_axis}", template="plotly_dark")

                st.plotly_chart(fig, use_container_width=True)

    # --- ADMIN PORTAL ---
    elif app_mode == "⚙️ Admin Portal":
        st.header("⚙️ Administration & Security Logs")
        if st.session_state.role != "Admin":
            st.error("Access Denied: You must have an Admin role to view this panel.")
        else:
            conn = sqlite3.connect(DB_FILE)
            st.subheader("Registered Users")
            users_df = pd.read_sql_query("SELECT id, username, role, created_at FROM users", conn)
            st.dataframe(users_df, use_container_width=True)

            st.subheader("System Activity Logs")
            logs_df = pd.read_sql_query("SELECT * FROM system_logs ORDER BY timestamp DESC", conn)
            st.dataframe(logs_df, use_container_width=True)
            conn.close()
