import streamlit as st
import streamlit.components.v1 as components
import random
import pandas as pd
import time
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & LOGO SETUP
# -----------------------------------------------------------------------------
APP_NAME = "dacre-analysis"

# ⬇️ CHANGED TO YOUR ACTUAL GITHUB LOGO FILE FOR PERFECT RESOLUTION ⬇️
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
# 2. CUSTOM STYLING (BROWN & LIGHT BLUE SIDEBAR + 5 SEC HOVER LOADER EFFECT)
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    /* Canvas Base Background */
    .stApp {
        background: radial-gradient(ellipse at bottom, #0f172a 0%, #020617 100%) !important;
    }

    /* Floating Background Effect */
    @keyframes floatSky {
        0% { background-position: 0 0; }
        50% { background-position: 100px -100px; }
        100% { background-position: 0 0; }
    }
    
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

    /* Brown & Soft Light Blue Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #3D2314 0%, #22120A 100%) !important;
        border-right: 2px solid #38bdf8 !important;
    }

    [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #E0F2FE !important; /* Soft Light Blue */
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

    /* 5-Second Glowing Hover Loader CSS */
    .hover-loader-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 15px;
        margin-bottom: 20px;
    }

    .hover-loader {
        width: 60px;
        height: 60px;
        border: 4px solid rgba(56, 189, 248, 0.2);
        border-top: 4px solid #38bdf8;
        border-radius: 50%;
        animation: spin 1s linear infinite, glowPulse 5s ease-in-out infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    @keyframes glowPulse {
        0% { box-shadow: 0 0 5px #38bdf8; }
        50% { box-shadow: 0 0 25px #818cf8, 0 0 40px #38bdf8; }
        100% { box-shadow: 0 0 5px #38bdf8; }
    }

    /* Input Contrast Rules */
    label, p, h1, h2, h3, h4, h5, h6, [data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
    }

    .stTextInput input, .stNumberInput input, .stSelectbox div {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    .stButton>button {
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%) !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3) !important;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5) !important;
    }

    div[data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-weight: bold !important;
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
# 4. INITIALIZE SYSTEM DATA & STATE (WITH SELF-HEALING SCHEMAS)
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
        {"Product ID": "PRD-101", "Name": "Neural Processor Core", "Category": "Hardware", "Status": "In Stock", "Qty": 45, "Cost": 1200},
        {"Product ID": "PRD-102", "Name": "DI Memory Module", "Category": "Storage", "Status": "In Stock", "Qty": 120, "Cost": 350},
        {"Product ID": "PRD-103", "Name": "SkyNet Gateway Unit", "Category": "Networking", "Status": "Low Stock", "Qty": 8, "Cost": 2100},
        {"Product ID": "PRD-104", "Name": "Quantum Bus Interface", "Category": "Hardware", "Status": "In Stock", "Qty": 30, "Cost": 850},
        {"Product ID": "PRD-105", "Name": "Cryo Cooling Array", "Category": "Infrastructure", "Status": "Maintenance", "Qty": 3, "Cost": 4500},
    ]

for item in st.session_state.products:
    if "Cost" not in item:
        item["Cost"] = 500

if "audit_logs" not in st.session_state:
    st.session_state.audit_logs = [
        {"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "User": "System", "Field Changed": "Initialization", "Old Value": "None", "New Value": "Online"}
    ]

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if "last_spoken_phrase" not in st.session_state:
    st.session_state.last_spoken_phrase = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "show_verification_gate" not in st.session_state:
    st.session_state.show_verification_gate = False

if "failed_reason" not in st.session_state:
    st.session_state.failed_reason = ""

if "captcha_quiz_options" not in st.session_state:
    st.session_state.captcha_quiz_options = ["Quantum Server Matrix", "Nebular System Cluster", "Bot Automation Footprint", "Organic Human Operator Pro"]
    st.session_state.captcha_quiz_correct = "Organic Human Operator Pro"

if "initial_loaded" not in st.session_state:
    st.session_state.initial_loaded = False

if "captcha_num1" not in st.session_state:
    st.session_state.captcha_num1 = random.randint(1, 9)
    st.session_state.captcha_num2 = random.randint(1, 9)

if st.session_state.last_spoken_phrase:
    speak_text(st.session_state.last_spoken_phrase)
    st.session_state.last_spoken_phrase = None

# -----------------------------------------------------------------------------
# 5. 5-SECOND HOVER LOADER EFFECT EXECUTION BLOCK
# -----------------------------------------------------------------------------
if not st.session_state.initial_loaded:
    loader_placeholder = st.empty()
    with loader_placeholder.container():
        st.markdown("""
            <div class="hover-loader-container">
                <div class="hover-loader"></div>
            </div>
            <p style="text-align:center; font-family:'Space Grotesk'; font-weight:600;">Synchronizing Cybernetic Architecture Grid...</p>
        """, unsafe_allow_html=True)
        time.sleep(5)
    loader_placeholder.empty()
    st.session_state.initial_loaded = True
    st.rerun()

# -----------------------------------------------------------------------------
# 6. SIDEBAR SYSTEM ASSIGNMENTS
# -----------------------------------------------------------------------------
with st.sidebar:
    try:
        st.image(LOGO_PATH, use_container_width=True)
    except Exception:
        st.markdown("<div style='border:1px dashed rgba(255,255,255,0.2); padding:10px; text-align:center;'>🖼️ Brand Image Syncing...</div>", unsafe_allow_html=True)

    st.markdown(f"### **{APP_NAME}**")
    st.caption("Sky Engine v3.5 • High Visibility Core")
    st.markdown("---")

    if st.session_state.logged_in_user:
        st.success(f"Authenticated: **{st.session_state.logged_in_user.upper()}**")
        if st.button("Log Out Node System", use_container_width=True):
            st.session_state.logged_in_user = None
            st.rerun()
    else:
        st.info("🔒 Secure Firewall Matrix Online")

# -----------------------------------------------------------------------------
# FULL SCREEN RECAPTCHA BLOCKS FOR RE-SIGNUPS AND ERRORS
# -----------------------------------------------------------------------------
