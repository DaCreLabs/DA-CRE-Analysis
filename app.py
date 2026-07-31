import streamlit as st
import streamlit.components.v1 as components
import random
import pandas as pd
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & LOGO SETUP
# -----------------------------------------------------------------------------
APP_NAME = "dacre-analysis"
LOGO_PATH = "ChatGPT Image Jul 29, 2026, 02_27_41 PM.png"

try:
    st.set_page_config(
        page_title=f"{APP_NAME} | Neural Core",
        page_icon=LOGO_PATH,
        layout="wide",
        initial_sidebar_state="expanded"
    )
except Exception:
    st.set_page_config(
        page_title=f"{APP_NAME} | Neural Core",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# -----------------------------------------------------------------------------
# 2. SKY ANIMATION BACKGROUND & HIGH-VISIBILITY FORM STYLING
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    /* Floating Celestial Sky Background */
    .stApp {
        background: radial-gradient(ellipse at bottom, #0f172a 0%, #020617 100%) !important;
    }

    @keyframes floatSky {
        0% { background-position: 0 0; }
        50% { background-position: 100px -100px; }
        100% { background-position: 0 0; }
    }
    
    /* Background element index layer pushed backward to protect visibility elements */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: url('https://user-images.githubusercontent.com/2673119/31048080-86532e74-a612-11e7-8250-9343be34a781.png') repeat;
        opacity: 0.15;
        pointer-events: none;
        animation: floatSky 75s infinite linear;
        z-index: -1 !important;
    }

    .hero-title {
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    /* Force Form Elements & Labels to be 100% Visible with Clear Formatting */
    label, p, h1, h2, h3, h4, h5, h6, [data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
    }

    /* High Visibility Form Input Fields with Clean Contrast Dark Slate */
    .stTextInput input, .stNumberInput input, .stSelectbox div {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    .stButton>button {
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%) !important;
        color: #ffffff !important;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: bold !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        width: 100%;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3) !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5) !important;
    }
    
    .intercept-box {
        background-color: #1e293b !important;
        border: 2px solid #ff3366 !important;
        border-radius: 12px;
        padding: 24px;
        margin: 15px 0;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. VOICE SYNTHESIS HELPER
# -----------------------------------------------------------------------------
def speak_text(text: str):
    """Triggers browser native text-to-speech engine."""
    clean_text = text.replace("'", "\\'").replace("\n", " ")
    js_code = f"""
    <script>
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance('{clean_text}');
            msg.rate = 1.0;
            msg.pitch = 1.0;
            msg.volume = 1.0;
            window.speechSynthesis.speak(msg);
        }}
    </script>
    """
    components.html(js_code, height=0, width=0)

# -----------------------------------------------------------------------------
# 4. INITIALIZE SYSTEM DATA & STATE
# -----------------------------------------------------------------------------
if "users" not in st.session_state:
    st.session_state.users = {
        "david": {"password": "123", "role": "master", "di_name": "DI-MasterPrime"}
    }

if "enrolled_dis" not in st.session_state:
    st.session_state.enrolled_dis = [
        {"user": "david", "di_id": "DI-000", "di_name": "DI-MasterPrime", "status": "Active", "type": "Master Prime"}
    ]

if "products" not in st.session_state:
    st.session_state.products = [
        {"Product ID": "PRD-101", "Name": "Neural Processor Core", "Category": "Hardware", "Status": "In Stock", "Qty": 45},
        {"Product ID": "PRD-102", "Name": "DI Memory Module", "Category": "Storage", "Status": "In Stock", "Qty": 120},
        {"Product ID": "PRD-103", "Name": "SkyNet Gateway Unit", "Category": "Networking", "Status": "Low Stock", "Qty": 8},
    ]

if "audit_logs" not in st.session_state:
    st.session_state.audit_logs = [
        {"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "User": "System", "Field Changed": "Initialization", "Old Value": "None", "New Value": "Online"}
    ]

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if "last_spoken_phrase" not in st.session_state:
    st.session_state.last_spoken_phrase = None

if "show_fullscreen_captcha" not in st.session_state:
    st.session_state.show_fullscreen_captcha = False

if "captcha_quiz_options" not in st.session_state:
    st.session_state.captcha_quiz_options = []
    st.session_state.captcha_quiz_correct = ""

if "captcha_num1" not in st.session_state:
    st.session_state.captcha_num1 = random.randint(1, 9)
    st.session_state.captcha_num2 = random.randint(1, 9)

# Trigger audio streams
if st.session_state.last_spoken_phrase:
    speak_text(st.session_state.last_spoken_phrase)
    st.session_state.last_spoken_phrase = None

# -----------------------------------------------------------------------------
# 5. SIDEBAR BRANDING & AUTHENTICATION
# -----------------------------------------------------------------------------
with st.sidebar:
    try:
        st.image(LOGO_PATH, use_container_width=True)
    except Exception:
        st.markdown("<div style='border:1px dashed rgba(255,255,255,0.2); padding:10px; text-align:center;'>🖼️ Brand Image Syncing...</div>", unsafe_allow_html=True)

    st.markdown(f"### **{APP_NAME}**")
    st.caption("Sky Engine v3.5 • Neural Core")
    st.markdown("---")

    if st.session_state.logged_in_user:
        st.success(f"Authenticated: **{st.session_state.logged_in_user.upper()}**")
        if st.button("Log Out"):
            st.session_state.logged_in_user = None
            st.rerun()
    else:
        st.info("🔒 Secure Firewall Matrix Online")

# -----------------------------------------------------------------------------
# FULL-SCREEN INTERCEPT WINDOW FOR DUPLICATED ACCOUNT COLLISIONS
# -----------------------------------------------------------------------------
if st.session_state.show_fullscreen_captcha:
    st.markdown("""
        <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="stRadio"] { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
    
    st.error("🚨 SECURITY OVERRIDE TRIGGERED: IDENTITY CONFLICT ENCOUNTERED")
    st.markdown("### This account has already been added. Please sign in!")
    st.write(f"Verification Parameter Checklist request matching category: **{st.session_state.captcha_quiz_correct.upper()}**")
    
    user_selected_ans = st.radio("Select verified response token:", st.session_state.captcha_quiz_options)
    
    if st.button("Authorize Gate Entry Clearance Re-route Link", use_container_width=True):
        if user_selected_ans == st.session_state.captcha_quiz_correct:
            st.session_state.show_fullscreen_captcha = False
            st.rerun()
        else:
            st.error("Verification parameters mismatched. Re-indexing tracking challenges.")
            st.session_state.captcha_quiz_options = random.sample(["Quantum Server Matrix", "Nebular System Cluster", "Bot Automation Footprint", "Organic Human Operator Pro"], 4)
            st.session_state.captcha_quiz_correct = "Organic Human Operator Pro"
            st.rerun()

# -----------------------------------------------------------------------------
# 6. SIGN IN / SIGN UP PORTAL LAYER DEFINITION
# -----------------------------------------------------------------------------
elif not st.session_state.logged_in_user:
    st.markdown(f'<div class="hero-title">{APP_NAME} Portal</div>', unsafe_allow_html=True)
    st.write("Sign in or register an account to deploy your Digital Intelligence.")
    st.markdown("---")

    auth_action = st.radio("Select Portal Action", ["🔑 Sign In", "📝 Sign Up"], horizontal=True)

    if auth_action == "🔑 Sign In":
        st.subheader("Account Login")
        login_user = st.text_input("Username", placeholder="Enter your operator username...", key="l_user")
        login_pass = st.text_input("Password", placeholder="Enter your cryptographic code...", type="password", key="l_pass")
        
        if st.button("Sign In"):
            if login_user in st.session_state.users and st.session_state.users[login_user]["password"] == login_pass:
                st.session_state.logged_in_user = login_user
                if st.session_state.users[login_user]["role"] == "master":
