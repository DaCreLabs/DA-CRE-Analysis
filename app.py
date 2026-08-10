import hashlib
import hmac
import io
import json
import os
import re
import sqlite3
import datetime
from pathlib import Path

import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

# =============================================================================
# 1. APPLICATION & BRAND CONFIGURATION
# =============================================================================
APP_NAME = "Dacre Data Studio & SQL Lab"
DI_NAME = "DI — David's Intelligence"
MASTER_USERNAME = "david"
MASTER_FULL_NAME = "David Emenike"

def get_master_passkey():
    env_value = os.getenv("DACRE_MASTER_PASSKEY")
    if env_value:
        return env_value
    try:
        secret_value = st.secrets.get("DACRE_MASTER_PASSKEY")
        if secret_value:
            return str(secret_value)
    except Exception:
        pass
    return "theWORDofGOD@111"

MASTER_PASSKEY = get_master_passkey()

BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "logo.png"
ALT_LOGO_PATH = BASE_DIR / "dacre_logo.png"
FAVICON_PATH = BASE_DIR / ".dacre_favicon.png"
DB_PATH = BASE_DIR / "dacre_platform.db"

# Dynamic Favicon and Page Icon Preparation Engine
def prepare_favicon():
    target_logo = LOGO_PATH if LOGO_PATH.exists() else (ALT_LOGO_PATH if ALT_LOGO_PATH.exists() else None)
    if not target_logo:
        return None
    try:
        source = Image.open(target_logo).convert("RGBA")
        width, height = source.size
        top = int(height * 0.08)
        bottom = int(height * 0.64)
        crop = source.crop((0, top, width, bottom))
        side = min(crop.size)
        left = max(0, (crop.width - side) // 2)
        crop_top = max(0, (crop.height - side) // 2)
        crop = crop.crop((left, crop_top, left + side, crop_top + side))
        crop.thumbnail((128, 128), Image.Resampling.LANCZOS)
        crop.save(FAVICON_PATH, format="PNG", optimize=True)
        return str(FAVICON_PATH)
    except Exception:
        return str(target_logo)

FAVICON = prepare_favicon()

st.set_page_config(
    page_title=f"{APP_NAME} | {DI_NAME}",
    page_icon=FAVICON if FAVICON else "📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# 2. HIGH-END AURORA THEME & ANIMATED DACRE LOADER CSS
# =============================================================================
CUSTOM_CSS = """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
    :root {
        --dacre-cyan: #18b7ff;
        --dacre-gold: #ffc107;
        --dacre-mint: #00dc96;
        --dacre-ink: #050914;
        --dacre-line: rgba(24,183,255,.22);
        --dacre-text: #ffffff;
        --dacre-muted: #c7d8ea;
    }

    /* Global Canvas Styling */
    .stApp {
        background:
            radial-gradient(1100px 600px at 12% -6%, rgba(24,183,255,.16), transparent 60%),
            radial-gradient(900px 520px at 92% 8%, rgba(255,193,7,.10), transparent 58%),
            radial-gradient(800px 700px at 50% 120%, rgba(0,220,150,.08), transparent 60%),
            linear-gradient(135deg, #050914, #091322 55%, #050914);
        background-attachment: fixed;
        color: var(--dacre-text);
        font-family: 'Inter', system-ui, sans-serif;
    }

    /* Animated Sheen Background */
    .stApp::before {
        content: "";
        position: fixed;
        inset: -40%;
        pointer-events: none;
        background:
            conic-gradient(from 0deg at 50% 50%,
                rgba(24,183,255,.05), transparent 25%,
                rgba(255,193,7,.04) 45%, transparent 70%,
                rgba(0,220,150,.04) 85%, transparent 100%);
        animation: dacreSpin 48s linear infinite;
        z-index: 0;
    }
    @keyframes dacreSpin { to { transform: rotate(360deg); } }
    .main .block-container { position: relative; z-index: 1; padding-top: 2rem; max-width: 1500px; }

    /* Streamlit Default Spinner Override with Floating Dacre Animated Logo */
    [data-testid="stAppLoading"], div.stSpinner {
        background-color: #050914 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    [data-testid="stAppLoading"] svg, div.stSpinner > div > svg, .stSpinner svg {
        display: none !important;
        visibility: hidden !important;
    }
    [data-testid="stAppLoading"] > div, div.stSpinner > div {
        background-image: url('logo.png'), url('dacre_logo.png'), url('app/static/logo.png') !important;
        background-size: contain !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        width: 130px !important;
        height: 130px !important;
        border: none !important;
        border-radius: 50% !important;
        animation: dacreHover 2s ease-in-out infinite !important;
    }
    @keyframes dacreHover {
        0% { transform: translateY(0px) scale(1); filter: drop-shadow(0 6px 15px rgba(24,183,255,0.4)); }
        50% { transform: translateY(-14px) scale(1.08); filter: drop-shadow(0 20px 25px rgba(24,183,255,0.8)); }
        100% { transform: translateY(0px) scale(1); filter: drop-shadow(0 6px 15px rgba(24,183,255,0.4)); }
    }

    /* Sharp White Text Formatting */
    html, body, .stApp, .stApp p, .stApp li, .stApp span, .stApp label,
    .stMarkdown, .stMarkdown p, .stMarkdown li,
    [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label,
    .stRadio label, .stCheckbox label, .stSelectbox label, .stTextInput label,
    .stTextArea label, .stFileUploader label, .stDateInput label {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        font-family: 'Sora', 'Inter', sans-serif !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
    }
    .stApp h3 {
        margin-top: 1.4rem;
        padding-left: 12px;
        border-left: 4px solid var(--dacre-cyan);
        text-shadow: 0 0 18px rgba(24,183,255,.35);
    }
    .stApp code, .stApp kbd, .stCode {
        font-family: 'JetBrains Mono', monospace !important;
        color: #7fe3ff !important;
        background: rgba(24,183,255,.10) !important;
        border: 1px solid rgba(24,183,255,.25);
        border-radius: 6px;
        font-weight: 600 !important;
    }

    /* Sidebar Navigation */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #07101d 0%, #060d18 55%, #050914 100%);
        border-right: 1px solid var(--dacre-line);
        box-shadow: 24px 0 60px -40px rgba(24,183,255,.55);
    }
    [data-testid="stSidebar"] * { color: #ffffff !important; }

    /* Glowing Custom Cards */
    .dacre-hero {
        position: relative;
        padding: 24px 30px;
        border-radius: 20px;
        border: 1px solid rgba(24,183,255,.35);
        background: linear-gradient(135deg, rgba(6,16,31,.94), rgba(10,28,47,.86));
        box-shadow: 0 24px 60px -28px rgba(0,0,0,.9);
        backdrop-filter: blur(10px);
        margin-bottom: 22px;
        overflow: hidden;
    }
    .dacre-hero::after {
        content: "";
        position: absolute;
        left: 0; right: 0; top: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--dacre-cyan), var(--dacre-mint), var(--dacre-gold), var(--dacre-cyan));
        background-size: 300% 100%;
        animation: dacreFlow 9s linear infinite;
    }
    @keyframes dacreFlow { to { background-position: 300% 0; } }

    /* High Visibility Input Controls */
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background: rgba(6,16,31,.92) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: 1.5px solid rgba(24,183,255,.35) !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--dacre-cyan) !important;
        box-shadow: 0 0 18px rgba(24,183,255,.3) !important;
    }

    /* Interactive Action Buttons */
    div.stButton > button, div.stFormSubmitButton > button, div.stDownloadButton > button {
        border-radius: 12px;
        border: 1px solid rgba(24,183,255,.45);
        background: linear-gradient(135deg, #0a2540, #0d3860);
        color: #ffffff !important;
        font-weight: 800 !important;
        padding: 10px 18px;
        transition: all .22s ease;
    }
    div.stButton > button:hover, div.stFormSubmitButton > button:hover, div.stDownloadButton > button:hover {
        border-color: var(--dacre-cyan);
        background: linear-gradient(135deg, #0d3860, #12508c);
        box-shadow: 0 0 20px rgba(24,183,255,.45);
        transform: translateY(-1px);
    }

    /* Metric Badges */
    [data-testid="stMetric"] {
        padding: 14px 18px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,.10);
        background: linear-gradient(145deg, rgba(255,255,255,.05), rgba(255,255,255,.015));
    }
    #MainMenu, footer { visibility: hidden; }
    </style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# =============================================================================
# 3. SECURE PERSISTENT DATABASE LAYER (PBKDF2-HMAC-SHA256)
# =============================================================================
PBKDF2_ITERATIONS = 100_000
PBKDF2_ALGORITHM = "sha256"

def get_db_connection():
    con = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=30)
    con.execute("PRAGMA foreign_keys = ON")
    con.execute("PRAGMA journal_mode = WAL")
    return con

def hash_password(password: str, salt: str = None) -> tuple:
    if not salt:
        salt = os.urandom(16).hex()
    pwd_hash = hashlib.pbkdf2_hmac(
        PBKDF2_ALGORITHM,
        password.encode("utf-8"),
        salt.encode("utf-8"),
        PBKDF2_ITERATIONS
    ).hex()
    return pwd_hash, salt

def init_db():
    with get_db_connection() as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'User',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                action TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Provision Master Admin
        cur.execute("SELECT * FROM users WHERE username = ?", (MASTER_USERNAME,))
        if not cur.fetchone():
            pwd_hash, salt = hash_password("admin123")
            cur.execute(
                "INSERT INTO users (username, password_hash, salt, full_name, role) VALUES (?, ?, ?, ?, ?)",
                (MASTER_USERNAME, pwd_hash, salt, MASTER_FULL_NAME, "Admin")
            )
        con.commit()

init_db()

def verify_credentials(username: str, password: str):
    with get_db_connection() as con:
        cur = con.cursor()
        cur.execute("SELECT password_hash, salt, full_name, role FROM users WHERE username = ?", (username,))
        record = cur.fetchone()
        if record:
            stored_hash, salt, full_name, role = record
            computed_hash, _ = hash_password(password, salt)
            if hmac.compare_digest(computed_hash, stored_hash):
                return True, full_name, role
    return False, None, None

def log_activity(username: str, action: str):
    with get_db_connection() as con:
        cur = con.cursor()
        cur.execute("INSERT INTO logs (username, action) VALUES (?, ?)", (username, action))
        con.commit()

# =============================================================================
# 4. DATA ENGINE, CLEANING & SQL LAB FORMULAS
# =============================================================================
SHEET_FORMULAS = [
    "UPPER", "LOWER", "TRIM", "ROUND", "SUM", "AVERAGE", "COUNT", "MAX", "MIN"
]

def clean_data(df: pd.DataFrame, drop_dups=False, fill_numeric=False, strip_str=False) -> pd.DataFrame:
    cleaned_df = df.copy()
    if drop_dups:
        cleaned_df = cleaned_df.drop_duplicates()
    if strip_str:
        str_cols = cleaned_df.select_dtypes(include=['object']).columns
        for col in str_cols:
            cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
    if fill_numeric:
        num_cols = cleaned_df.select_dtypes(include=['number']).columns
        cleaned_df[num_cols] = cleaned_df[num_cols].fillna(cleaned_df[num_cols].median())
    return cleaned_df

def execute_sql_query(df: pd.DataFrame, query: str) -> pd.DataFrame:
    if df is None or df.empty:
        raise ValueError("No active dataset loaded to query.")
    conn = sqlite3.connect(":memory:")
    try:
        df.to_sql("df", conn, index=False, if_exists="replace")
        result = pd.read_sql_query(query, conn)
        return result
    finally:
        conn.close()

def apply_simple_formula(df: pd.DataFrame, column: str, formula: str) -> pd.Series:
    formula_upper = formula.strip().upper()
    if formula_upper == "UPPER":
        return df[column].astype(str).str.upper()
    elif formula_upper == "LOWER":
        return df[column].astype(str).str.lower()
    elif formula_upper == "TRIM":
        return df[column].astype(str).str.strip()
    elif formula_upper == "ROUND" and pd.api.types.is_numeric_dtype(df[column]):
        return df[column].round(2)
    elif formula_upper in ["SUM", "AVERAGE", "COUNT", "MAX", "MIN"] and pd.api.types.is_numeric_dtype(df[column]):
        if formula_upper == "SUM":
            return pd.Series([df[column].sum()] * len(df))
        elif formula_upper == "AVERAGE":
            return pd.Series([df[column].mean()] * len(df))
        elif formula_upper == "COUNT":
            return pd.Series([df[column].count()] * len(df))
        elif formula_upper == "MAX":
            return pd.Series([df[column].max()] * len(df))
        elif formula_upper == "MIN":
            return pd.Series([df[column].min()] * len(df))
    return df[column]

# =============================================================================
# 5. SESSION INITIALIZATION
# =============================================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "full_name" not in st.session_state:
    st.session_state.full_name = None
if "role" not in st.session_state:
    st.session_state.role = None
if "active_df" not in st.session_state:
    # Default initial dataset
    st.session_state.active_df = pd.DataFrame([
        {"Product ID": "PRD-101", "Name": "Neural Core", "Category": "Hardware", "Qty": 85, "Cost": 1200, "Sales": 450},
        {"Product ID": "PRD-102", "Name": "DI Memory Block", "Category": "Storage", "Qty": 140, "Cost": 350, "Sales": 920},
        {"Product ID": "PRD-103", "Name": "SkyNet Gateway", "Category": "Networking", "Qty": 6, "Cost": 2100, "Sales": 110},
        {"Product ID": "PRD-104", "Name": "Quantum Bus", "Category": "Hardware", "Qty": 50, "Cost": 850, "Sales": 380},
    ])

# =============================================================================
# 6. AUTHENTICATION PORTAL
# =============================================================================
if not st.session_state.authenticated:
    st.markdown(f"""
        <div class="dacre-hero">
            <h1>⚡ {APP_NAME}</h1>
            <p>Unified Enterprise Analytics, SQL Workbench & Formula Automation Studio</p>
        </div>
    """, unsafe_allow_html=True)

    auth_tab1, auth_tab2 = st.tabs(["🔑 Sign In", "📝 Create Account"])

    with auth_tab1:
        st.subheader("Sign In")
        with st.form("login_form"):
            user_input = st.text_input("Username")
            pass_input = st.text_input("Password", type="password")
            submit = st.form_submit_button("Authenticate")

            if submit:
                valid, full_name, role = verify_credentials(user_input, pass_input)
                if valid:
                    st.session_state.authenticated = True
                    st.session_state.username = user_input
                    st.session_state.full_name = full_name
                    st.session_state.role = role
                    log_activity(user_input, "User Login Successful")
                    st.success(f"Welcome back, {full_name}!")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password.")

    with auth_tab2:
        st.subheader("Register Account")
        with st.form("register_form"):
            reg_u = st.text_input("Choose Username")
            reg_f = st.text_input("Full Name")
            reg_p = st.text_input("Choose Password", type="password")
            reg_submit = st.form_submit_button("Register Account")

            if reg_submit:
                if reg_u and reg_f and reg_p:
                    try:
                        pwd_hash, salt = hash_password(reg_p)
                        with get_db_connection() as con:
                            cur = con.cursor()
                            cur.execute(
                                "INSERT INTO users (username, password_hash, salt, full_name, role) VALUES (?, ?, ?, ?, ?)",
                                (reg_u, pwd_hash, salt, reg_f, "User")
                            )
                            con.commit()
                        st.session_state.authenticated = True
                        st.session_state.username = reg_u
                        st.session_state.full_name = reg_f
                        st.session_state.role = "User"
                        log_activity(reg_u, "User Registration Successful")
                        st.success("Account registered successfully!")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("Username already taken. Please pick another.")
                else:
                    st.warning("Please fill in all registration fields.")
    st.stop()

# =============================================================================
# 7. MAIN APPLICATION WORKSPACE
# =============================================================================
# Header Hero
st.markdown(f"""
    <div class="dacre-hero">
        <h1>{APP_NAME}</h1>
        <p>Active Analyst: <strong>{st.session_state.full_name}</strong> ({st.session_state.role}) | Engine Status: 🟢 Online</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    target_logo = LOGO_PATH if LOGO_PATH.exists() else (ALT_LOGO_PATH if ALT_LOGO_PATH.exists() else None)
    if target_logo:
        st.image(str(target_logo), use_container_width=True)
    else:
        st.markdown("### ⚡ DACRE DATA STUDIO")

    st.markdown(f"**User:** `{st.session_state.username}`")
    st.markdown(f"**Role:** `{st.session_state.role}`")

    if st.button("Log Out", use_container_width=True):
        log_activity(st.session_state.username, "User Logged Out")
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.role = None
        st.rerun()

    st.markdown("---")
    st.subheader("📂 Data Import")
    uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                st.session_state.active_df = pd.read_csv(uploaded_file)
            else:
                st.session_state.active_df = pd.read_excel(uploaded_file)
            log_activity(st.session_state.username, f"Uploaded Dataset: {uploaded_file.name}")
            st.success(f"Loaded: {uploaded_file.name}")
        except Exception as e:
            st.error(f"Error loading file: {e}")

# Application Navigation Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Data Workspace", 
    "💻 SQL Lab", 
    "🧮 Formula Engine", 
    "📈 Visualizations",
    "🛡️ Admin & Audit Logs"
])

# -----------------------------------------------------------------------------
# TAB 1: DATA WORKSPACE
# -----------------------------------------------------------------------------
with tab1:
    st.header("Data Cleaning & Inspection Pipeline")
    if st.session_state.active_df is not None:
        df = st.session_state.active_df
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Rows", df.shape[0])
        c2.metric("Total Columns", df.shape[1])
        c3.metric("Duplicate Rows", df.duplicated().sum())

        st.markdown("### Cleaning Controls")
        cl1, cl2, cl3 = st.columns(3)
        drop_dups = cl1.checkbox("Remove Duplicates")
        fill_num = cl2.checkbox("Fill Missing Numeric (Median)")
        strip_str = cl3.checkbox("Trim String Whitespace")

        if st.button("Apply Cleaning Pipeline"):
            st.session_state.active_df = clean_data(df, drop_dups, fill_num, strip_str)
            log_activity(st.session_state.username, "Executed Data Cleaning")
            st.success("Dataset cleaned successfully!")
            st.rerun()

        st.markdown("### Interactive Dataset Inspection")
        edited_df = st.data_editor(st.session_state.active_df, use_container_width=True, num_rows="dynamic")
        if st.button("💾 Commit Grid Changes"):
            st.session_state.active_df = edited_df
            st.success("Grid changes committed to memory!")
    else:
        st.info("Upload a dataset from the sidebar to begin.")

# -----------------------------------------------------------------------------
# TAB 2: SQL LAB WORKBENCH
# -----------------------------------------------------------------------------
with tab2:
    st.header("SQL Query Workbench")
    st.markdown("Run standard SQL queries against your active dataset. The target table is named **`df`**.")
    if st.session_state.active_df is not None:
        default_query = "SELECT * FROM df LIMIT 10;"
        query_input = st.text_area("SQL Query Input", value=default_query, height=120)

        if st.button("Run SQL Query"):
            try:
                res = execute_sql_query(st.session_state.active_df, query_input)
                log_activity(st.session_state.username, f"Executed SQL: {query_input[:30]}...")
                st.markdown(f"**Query Results:** ({len(res)} rows returned)")
                st.dataframe(res, use_container_width=True)
            except Exception as e:
                st.error(f"SQL Execution Error: {e}")
    else:
        st.info("Upload a dataset to run SQL queries.")

# -----------------------------------------------------------------------------
# TAB 3: FORMULA ENGINE
# -----------------------------------------------------------------------------
with tab3:
    st.header("Spreadsheet Formula Engine")
    if st.session_state.active_df is not None:
        df = st.session_state.active_df
        st.markdown("Select a target column and choose a formula function to compute new values.")

        f1, f2, f3 = st.columns(3)
        target_col = f1.selectbox("Target Column", df.columns)
        formula_choice = f2.selectbox("Formula Function", SHEET_FORMULAS)
        new_col_name = f3.text_input("Output Column Name", value=f"{target_col}_{formula_choice.lower()}")

        if st.button("Apply Formula"):
            try:
                st.session_state.active_df[new_col_name] = apply_simple_formula(df, target_col, formula_choice)
                log_activity(st.session_state.username, f"Applied Formula {formula_choice} on {target_col}")
                st.success(f"Column '{new_col_name}' created successfully!")
                st.dataframe(st.session_state.active_df.head(20), use_container_width=True)
            except Exception as e:
                st.error(f"Formula Error: {e}")
    else:
        st.info("Upload a dataset to use the Formula Engine.")

# -----------------------------------------------------------------------------
# TAB 4: VISUALIZATIONS
# -----------------------------------------------------------------------------
with tab4:
    st.header("Plotly Dynamic Visualizations")
    if st.session_state.active_df is not None:
        df = st.session_state.active_df

        v1, v2, v3 = st.columns(3)
        chart_type = v1.selectbox("Chart Type", ["Bar", "Line", "Scatter", "Histogram"])
        x_col = v2.selectbox("X-Axis Parameter", df.columns)
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        y_col = v3.selectbox("Y-Axis Parameter", num_cols if num_cols else df.columns)

        if st.button("Generate Chart"):
            if chart_type == "Bar":
                fig = px.bar(df, x=x_col, y=y_col, template="plotly_dark", color_discrete_sequence=["#18b7ff"])
            elif chart_type == "Line":
                fig = px.line(df, x=x_col, y=y_col, template="plotly_dark", color_discrete_sequence=["#00dc96"])
            elif chart_type == "Scatter":
                fig = px.scatter(df, x=x_col, y=y_col, template="plotly_dark", color_discrete_sequence=["#ffc107"])
            elif chart_type == "Histogram":
                fig = px.histogram(df, x=x_col, template="plotly_dark", color_discrete_sequence=["#18b7ff"])

            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Upload a dataset to generate visual plots.")

# -----------------------------------------------------------------------------
# TAB 5: ADMIN & AUDIT LOGS
# -----------------------------------------------------------------------------
with tab5:
    st.header("🛡️ Master Security & Audit Logs")
    if st.session_state.role == "Admin":
        st.subheader("Registered System Users")
        with get_db_connection() as con:
            users_df = pd.read_sql_query("SELECT id, username, full_name, role, created_at FROM users", con)
            st.dataframe(users_df, use_container_width=True)

        st.subheader("Security Audit Activity Logs")
        with get_db_connection() as con:
            logs_df = pd.read_sql_query("SELECT * FROM logs ORDER BY timestamp DESC LIMIT 50", con)
            st.dataframe(logs_df, use_container_width=True)
    else:
        st.warning("Master Admin credentials required to view full audit logs.")
