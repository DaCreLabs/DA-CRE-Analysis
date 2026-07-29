import streamlit as st
import pandas as pd
import numpy as np
import hashlib
import time
import os
import base64
from datetime import datetime
import plotly.express as px

# ==========================================================
# DACRE ANALYSIS 2026 ENTERPRISE EDITION
# ==========================================================

APP_NAME = "DACRE ANALYSIS"
APP_VERSION = "Enterprise 2026"

PRIMARY_LOGO_FILENAME = "ChatGPT Image Jul 29, 2026, 02_27_41 PM.png"
RAW_GITHUB_LOGO_URL = "https://raw.githubusercontent.com/DaCreLabs/DA-CRE-Analysis/main/ChatGPT%20Image%20Jul%2029%2C%202026%2C%2002_27_41%20PM.png"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="DACRE ANALYSIS",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

ADMIN_SECRET_KEY = "theWORDofGOD"

# ---------------- LOGO RENDER ENGINE (WITH FAILSAFE) ----------------
@st.cache_data
def load_logo_b64():
    if os.path.exists(PRIMARY_LOGO_FILENAME):
        try:
            with open(PRIMARY_LOGO_FILENAME, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except Exception:
            return None
    return None

def get_logo_html(width=220):
    b64 = load_logo_b64()
    if b64:
        return f'<div style="text-align:center; margin-bottom:12px;"><img src="data:image/png;base64,{b64}" style="max-width:{width}px; border-radius:12px; box-shadow:0 6px 16px rgba(0,0,0,0.5);"></div>'
    return f'<div style="text-align:center; margin-bottom:12px;"><img src="{RAW_GITHUB_LOGO_URL}" style="max-width:{width}px; border-radius:12px; box-shadow:0 6px 16px rgba(0,0,0,0.5);" onerror="this.onerror=null; this.src=\'https://img.icons8.com/color/180/analytics.png\';"></div>'

# ---------------- INITIAL 5-SECOND HOVER LOADING SPLASH SCREEN ----------------
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
            {get_logo_html(180)}
            <h1 style="color: #ffffff; font-weight: 900; font-size: 45px; font-family: sans-serif; letter-spacing: 2px; margin-top: 15px;">DACRE ANALYSIS</h1>
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

/* DARK ENTERPRISE THEME */
.stApp {
    background: radial-gradient(circle at 50% 20%, #0d1b2a, #0b131f, #050a0f);
    color: #ffffff;
}

/* FORCED WHITE FIELD LABELS */
label, 
.stTextInput label, 
.stSelectbox label, 
.stFileUploader label,
div[data-testid="stWidgetLabel"] p {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 15px !important;
}

/* HERO CONTAINER */
.hero {
    padding: 20px;
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.85), rgba(15, 23, 42, 0.95));
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0px 10px 25px rgba(0,0,0,.5);
    margin-bottom: 20px;
    text-align: center;
}

.hero h1 {
    font-size: 40px;
    font-weight: 900 !important;
    color: #ffffff !important;
    margin-bottom: 5px;
}

.hero h3 {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 18px;
}

/* INPUT BARS - LIGHT BROWN FILL & GREY PLACEHOLDERS */
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

input::placeholder {
    color: #757575 !important;
    font-style: italic;
    font-weight: 500 !important;
}

.stButton>button {
    background: linear-gradient(90deg, #0284c7, #0891b2);
    color: white;
    font-weight: bold;
    border-radius: 10px;
    height: 44px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION DATABASE & STATE MANAGEMENT ----------------
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

if "current_data" not in st.session_state:
    st.session_state["current_data"] = None

if 'authenticated' not in st.session_state:
    st.session_state["authenticated"] = False

if 'user_name' not in st.session_state:
    st.session_state["user_name"] = ""

if 'role' not in st.session_state:
    st.session_state["role"] = None

if 'show_captcha' not in st.session_state:
    st.session_state['show_captcha'] = False

if 'captcha_verified' not in st.session_state:
    st.session_state['captcha_verified'] = False

if 'captcha_reason' not in st.session_state:
    st.session_state['captcha_reason'] = ""

def log_action(user, action):
    st.session_state.logs_db.append({
        "user": user,
        "action": action,
        "timestamp": str(datetime.now())
    })

# ---------------- DYNAMIC ROTATING RECAPTCHA ENGINE (1-MIN ROTATION) ----------------
def get_current_captcha_target():
    minute_bucket = int(time.time() // 60)
    challenges = [
        {"target": "Bus", "correct": "Option B", "a": "🚗 Car", "b": "🚌 Bus", "c": "🐶 Dog"},
        {"target": "Animal (Dog)", "correct": "Option C", "a": "🚲 Bicycle", "b": "🚌 Bus", "c": "🐶 Dog"},
        {"target": "Bicycle", "correct": "Option A", "a": "🚲 Bicycle", "b": "🚗 Car", "c": "🚌 Bus"}
    ]
    return challenges[minute_bucket % len(challenges)]

def trigger_captcha_overlay(reason="Security check required due to invalid input."):
    st.session_state['show_captcha'] = True
    st.session_state['captcha_verified'] = False
    st.session_state['captcha_reason'] = reason

# ---------------- LANDING HEADER ----------------
st.markdown(get_logo_html(220), unsafe_allow_html=True)
st.markdown("""
<div class="hero">
    <h1>DACRE ANALYSIS</h1>
    <h3>Enterprise AI Spreadsheet & Data Analytics Platform</h3>
    <p>Upload • Clean • Analyse • Visualize • Automate • Export</p>
</div>
""", unsafe_allow_html=True)

# ---------------- FULL PAGE CAPTCHA OVERTAKE ----------------
if st.session_state['show_captcha'] and not st.session_state['captcha_verified']:
    challenge = get_current_captcha_target()
    
    st.error(f"🚨 **SECURITY VERIFICATION REQUIRED**: {st.session_state['captcha_reason']}")
    st.markdown("---")
    
    st.subheader(f"🤖 reCAPTCHA: Select the image/option that displays a **{challenge['target']}**")
    st.caption("This challenge rotates automatically every 1 minute.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info(f"**Option A**\n\n{challenge['a']}")
    with c2:
        st.info(f"**Option B**\n\n{challenge['b']}")
    with c3:
        st.info(f"**Option C**\n\n{challenge['c']}")
        
    user_choice = st.radio("Select the correct verification option:", ["Select...", "Option A", "Option B", "Option C"], key="full_captcha_choice")
    
    if st.button("Verify & Continue"):
        if user_choice == challenge['correct']:
            st.session_state['captcha_verified'] = True
            st.session_state['show_captcha'] = False
            st.success("✅ Verification successful! Returning you to authentication...")
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ Verification failed! Please try again.")

# ---------------- AUTHENTICATION & PORTAL SCREEN ----------------
elif not st.session_state["authenticated"]:
    portal_type = st.radio("Select Access Portal:", ["👤 User Access", "🛡️ Isolated Admin Portal"], horizontal=True)
    
    if portal_type == "👤 User Access":
        tab_login, tab_signup = st.tabs(["🔒 Sign In", "📝 Sign Up"])
        
        # --- LOGIN TAB ---
        with tab_login:
            st.subheader("User Login")
            l_user = st.text_input("Username", placeholder="Enter username", key="l_user")
            l_pass = st.text_input("Password", type="password", placeholder="Enter password", key="l_pass")
            
            if st.button("Sign In"):
                if l_user not in st.session_state.users_db:
                    trigger_captcha_overlay("Account has not been created. Please verify you are human before signing up!")
                    st.rerun()
                else:
                    user_record = st.session_state.users_db.get(l_user)
                    if user_record and check_hashes(l_pass, user_record["password_hash"]):
                        st.session_state["authenticated"] = True
                        st.session_state["user_name"] = l_user
                        st.session_state["role"] = user_record["role"]
                        st.session_state.active_sessions[l_user] = str(datetime.now())
                        log_action(l_user, "User Logged In")
                        st.success(f"Welcome back, {l_user}!")
                        st.rerun()
                    else:
                        trigger_captcha_overlay("Incorrect password entered. Please verify you are human.")
                        st.rerun()

        # --- SIGNUP TAB ---
        with tab_signup:
            st.subheader("Create New Account")
            s_user = st.text_input("Username", placeholder="Choose username", key="s_user")
            s_email = st.text_input("Email Address", placeholder="user@example.com", key="s_email")
            s_pass = st.text_input("Password", type="password", placeholder="Create password", key="s_pass")
            
            if st.button("Create Account"):
                if s_user in st.session_state.users_db:
                    trigger_captcha_overlay("This account has already been added! Verify to return to Sign In.")
                    st.rerun()
                elif s_user and s_pass and s_email:
                    st.session_state.users_db[s_user] = {
                        "email": s_email,
                        "password_hash": make_hashes(s_pass),
                        "role": "User",
                        "created_at": str(datetime.now())
                    }
                    log_action(s_user, "Account Created")
                    st.success("🎉 Account created successfully! You can now log in.")
                else:
                    st.warning("Please fill out all required fields.")

    # --- ISOLATED ADMIN PORTAL ---
    else:
        st.subheader("🛡️ Dedicated Admin Control Gateway")
        st.info("System Administrators Only. Input your secret passkey below.")
        
        a_pass = st.text_input("Enter Admin Passkey", type="password", placeholder="Enter secret key", key="a_pass")
        
        if st.button("Unlock Admin Gateway"):
            if a_pass == ADMIN_SECRET_KEY:
                st.session_state["authenticated"] = True
                st.session_state["user_name"] = "System Administrator"
                st.session_state["role"] = "Admin"
                log_action("Admin", "Admin Access Unlocked")
                st.success("Admin access granted! Directing to Master Control Center...")
                time.sleep(1)
                st.rerun()
            else:
                trigger_captcha_overlay("Incorrect Admin Secret Key entered!")
                st.rerun()

# ---------------- MAIN APPLICATION INTERFACE (LOGGED IN) ----------------
else:
    with st.sidebar:
        st.markdown(get_logo_html(160), unsafe_allow_html=True)
        st.markdown(f"### 👋 {st.session_state['user_name']}")
        st.caption(f"Role: **{st.session_state['role']}**")
        st.markdown("---")

        nav_items = [
            "🏠 Dashboard (Pure File View)",
            "📊 Embedded Sheet & Formula Board",
            "📂 File Vault",
        ]
        if st.session_state["role"] == "Admin":
            nav_items.append("🛡️ Master Admin Control")

        menu = st.selectbox("Navigation", nav_items)
        st.markdown("---")

        if st.button("🚪 Logout", use_container_width=True):
            if st.session_state["user_name"] in st.session_state.active_sessions:
                del st.session_state.active_sessions[st.session_state["user_name"]]
            st.session_state["authenticated"] = False
            st.rerun()

    # ==========================================================
    # WORKSPACE PAGES
    # ==========================================================

    # 1. FILE VAULT
    if menu == "📂 File Vault":
        st.title("📂 File Vault")
        st.write("Upload CSV or Excel files here. Loaded files automatically sync across your Workspace Sheet and Dashboard Pure File View.")
        
        uploaded_file = st.file_uploader("Upload Data File", type=["csv", "xlsx", "xls"])
        if uploaded_file:
            try:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                st.session_state["current_data"] = df
                log_action(st.session_state["user_name"], f"Vault File Uploaded: {uploaded_file.name}")
                st.success(f"✅ Loaded '{uploaded_file.name}' ({len(df)} rows) into Active Workspace!")
            except Exception as e:
                st.error(f"Error processing file: {e}")

        if st.session_state["current_data"] is not None:
            st.write("### Currently Vaulted File Preview")
            st.dataframe(st.session_state["current_data"].head(10), use_container_width=True)

    # 2. EMBEDDED SHEET & FORMULA BOARD
    elif menu == "📊 Embedded Sheet & Formula Board":
        st.title("📊 Embedded Sheet & Workflow Engine")
        st.caption("Interactive Google Sheet-Style Workspace with Formula Transformations")

        if st.session_state["current_data"] is None:
            st.info("⚠️ No file in Vault yet. Please go to 'File Vault' and upload a file first.")
        else:
            df = st.session_state["current_data"].copy()

            # --- FORMULA TOOLBAR ---
            st.markdown("### 🧮 Sheet Formulas Engine")
            f_col1, f_col2, f_col3, f_col4 = st.columns([2, 2, 2, 1])
            
            with f_col1:
                selected_formula = st.selectbox(
                    "Sheet Formulas",
                    [
                        "Select Formula...",
                        "CONCATENATE (Combine Columns)",
                        "SUM (Add Numeric Column)",
                        "AVERAGE (Mean Value)",
                        "UPPER (Convert Text to UPPERCASE)",
                        "LOWER (Convert Text to lowercase)",
                        "TRIM (Remove Spaces)",
                        "MULTIPLY (Scale Column by Factor)",
                        "DIVIDE (Divide Column by Factor)"
                    ]
                )

            cols = list(df.columns)
            
            with f_col2:
                target_col1 = st.selectbox("Select Target Column / Primary Column", ["None"] + cols, key="f_col_target1")
            
            with f_col3:
                target_col2 = st.selectbox("Select Secondary Column (if applicable)", ["None"] + cols, key="f_col_target2")

            with f_col4:
                num_factor = st.number_input("Factor / Value", value=1.0, key="num_factor")

            if st.button("⚡ Apply Formula to Worksheet"):
                if selected_formula == "CONCATENATE (Combine Columns)" and target_col1 != "None" and target_col2 != "None":
                    new_col_name = f"{target_col1}_{target_col2}_CONCAT"
                    df[new_col_name] = df[target_col1].astype(str) + " " + df[target_col2].astype(str)
                    st.session_state["current_data"] = df
                    st.success(f"Added concatenated column: '{new_col_name}'!")
                    st.rerun()

                elif selected_formula == "UPPER (Convert Text to UPPERCASE)" and target_col1 != "None":
                    df[target_col1] = df[target_col1].astype(str).str.upper()
                    st.session_state["current_data"] = df
                    st.success(f"Converted '{target_col1}' to UPPERCASE!")
                    st.rerun()

                elif selected_formula == "LOWER (Convert Text to lowercase)" and target_col1 != "None":
                    df[target_col1] = df[target_col1].astype(str).str.lower()
                    st.session_state["current_data"] = df
                    st.success(f"Converted '{target_col1}' to lowercase!")
                    st.rerun()

                elif selected_formula == "TRIM (Remove Spaces)" and target_col1 != "None":
                    df[target_col1] = df[target_col1].astype(str).str.strip()
                    st.session_state["current_data"] = df
                    st.success(f"Trimmed whitespace in '{target_col1}'!")
                    st.rerun()

                elif selected_formula == "SUM (Add Numeric Column)" and target_col1 != "None":
                    total_sum = pd.to_numeric(df[target_col1], errors='coerce').sum()
                    st.info(f"📊 **SUM Result for {target_col1}**: {total_sum}")

                elif selected_formula == "AVERAGE (Mean Value)" and target_col1 != "None":
                    avg_val = pd.to_numeric(df[target_col1], errors='coerce').mean()
                    st.info(f"📊 **AVERAGE Result for {target_col1}**: {avg_val:.2f}")

                elif selected_formula == "MULTIPLY (Scale Column by Factor)" and target_col1 != "None":
                    df[target_col1] = pd.to_numeric(df[target_col1], errors='coerce') * num_factor
                    st.session_state["current_data"] = df
                    st.success(f"Multiplied '{target_col1}' by {num_factor}!")
                    st.rerun()

                elif selected_formula == "DIVIDE (Divide Column by Factor)" and target_col1 != "None" and num_factor != 0:
                    df[target_col1] = pd.to_numeric(df[target_col1], errors='coerce') / num_factor
                    st.session_state["current_data"] = df
                    st.success(f"Divided '{target_col1}' by {num_factor}!")
                    st.rerun()

            st.markdown("---")
            st.write("### 📝 Interactive Google Sheet Editor")
            edited_df = st.data_editor(st.session_state["current_data"], num_rows="dynamic", use_container_width=True)
            st.session_state["current_data"] = edited_df

    # 3. DASHBOARD & PURE FILE READ-ONLY VIEW
    elif menu == "🏠 Dashboard (Pure File View)":
        st.title("🏠 Executive Dashboard & Read-Only Pure File View")
        
        if st.session_state["current_data"] is None:
            st.info("No active dataset. Upload a file in File Vault to view the Pure File View and metrics here.")
        else:
            df = st.session_state["current_data"]
            
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("Total Rows", len(df))
            with c2:
                st.metric("Total Columns", len(df.columns))
            with c3:
                st.metric("Numeric Columns", len(df.select_dtypes(include="number").columns))
            with c4:
                st.metric("Status", "Live Synced")

            st.markdown("---")
            st.subheader("📄 Pure File View (Read-Only)")
            st.caption("Any edits made in the Embedded Sheet dynamically display here. This view is read-only.")

            # Read-Only DataFrame display
            st.dataframe(df, use_container_width=True)

            # EXPORT & PRINT BUTTONS
            exp_col1, exp_col2 = st.columns(2)
            with exp_col1:
                csv_bytes = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Pure File (CSV)",
                    data=csv_bytes,
                    file_name="DACRE_Pure_File_Export.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with exp_col2:
                st.markdown("""
                <button onclick="window.print()" style="
                    width: 100%;
                    height: 44px;
                    background-color: #334155;
                    color: white;
                    font-weight: bold;
                    border-radius: 10px;
                    border: 1px solid #64748b;
                    cursor: pointer;
                ">🖨️ Print Pure File Page</button>
                """, unsafe_allow_html=True)

    # 4. MASTER ADMIN CONTROL
    elif menu == "🛡️ Master Admin Control":
        st.title("🛡️ Master Admin Control Panel")
        st.subheader("System Administration & User Session Governance")
        
        st.markdown("### Users Directory & Active Connections")
        user_list = []
        for u, d in st.session_state.users_db.items():
            user_list.append({
                "Username": u,
                "Email": d["email"],
                "Role": d["role"],
                "Status": "Online 🟢" if u in st.session_state.active_sessions else "Offline ⚪"
            })
        st.dataframe(pd.DataFrame(user_list), use_container_width=True)

        st.subheader("Audit Logs")
        st.dataframe(pd.DataFrame(st.session_state.logs_db), use_container_width=True)
