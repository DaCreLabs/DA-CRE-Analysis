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
# 2. CUSTOM UI: HIGH-CONTRAST TEXT & ANIMATED SKY BACKGROUND
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    /* Animated Sky Background */
    .stApp {
        background: radial-gradient(ellipse at bottom, #1b2735 0%, #090a0f 100%);
        color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Floating Sky/Stars Effect */
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
        opacity: 0.25;
        pointer-events: none;
        animation: floatSky 60s infinite linear;
        z-index: 0;
    }

    /* Glassmorphic Cards with High Contrast */
    .glass-card {
        background: rgba(15, 23, 42, 0.88) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
    }

    /* Force All Main Element Visibility */
    p, label, span, h1, h2, h3, h4, h5, h6, [data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
    }

    /* Input Field Visibility Modifications */
    .stTextInput input, .stNumberInput input, .stSelectbox div {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 2px solid #475569 !important;
        border-radius: 10px !important;
    }

    /* Hero Typography */
    .hero-title {
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.2rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        color: #cbd5e1 !important;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }

    /* Custom Kinetic Command Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #3b82f6 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 28px !important;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4) !important;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6) !important;
    }

    /* Security Takeover Component Card Layout */
    .recaptcha-box {
        background: rgba(30, 41, 59, 0.85);
        border: 2px solid #ff3366;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. VOICE SYNTHESIS HELPER
# -----------------------------------------------------------------------------
def speak_text(text: str):
    """Triggers browser native text-to-speech engine cleanly."""
    clean_text = text.replace("'", "\\'").replace("\n", " ")
    js_code = f"""
    <script>
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance('{clean_text}');
            msg.rate = 1.05;
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

# Dispatch pending verbal triggers
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
        st.markdown("<div style='border:1px dashed rgba(255,255,255,0.2); padding:10px; text-align:center;'>🖼️ Brand Image Sync Active...</div>", unsafe_allow_html=True)

    st.markdown(f"### **{APP_NAME}**")
    st.caption("Sky Engine v3.5 • High Visibility UI")
    st.markdown("---")

    if st.session_state.logged_in_user:
        st.success(f"Authenticated: **{st.session_state.logged_in_user.upper()}**")
        if st.button("Log Out Session", use_container_width=True):
            st.session_state.logged_in_user = None
            st.rerun()
    else:
        st.info("🔒 Secure Firewall Matrix Active")

# -----------------------------------------------------------------------------
# FULL-SCREEN RECAPTCHA TAKEOVER INTERCEPT WINDOW
# -----------------------------------------------------------------------------
if st.session_state.show_fullscreen_captcha:
    st.markdown("""
        <style>
        [data-testid="stSidebar"] { display: none !important; }
        .stTabs { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: #ff3366 !important; font-size: 3rem;'>🚨 SYSTEM SECURITY CAPTCHA INTERCEPT</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #cbd5e1 !important;'>This account has already been added. Complete verification to redirect to login panel.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    _, col_c2, _ = st.columns([1, 2, 1])
    with col_c2:
        st.markdown('<div class="recaptcha-box">', unsafe_allow_html=True)
        st.subheader("🛡️ Multi-Choice Anti-Bot Query Challenge")
        st.write(f"**Verification Parameter Request:** Select the item that represents: **{st.session_state.captcha_quiz_correct.upper()}**")
        
        user_selected_ans = st.radio("Available Signatures:", st.session_state.captcha_quiz_options)
        
        if st.button("Authorize Resolution Core Sync"):
            if user_selected_ans == st.session_state.captcha_quiz_correct:
                st.session_state.show_fullscreen_captcha = False
                st.rerun()
            else:
                st.error("Challenge Rejected. Regenerating target network challenges.")
                st.session_state.captcha_quiz_options = random.sample(["Quantum Server Node", "Space Nebular Loop", "Bot Application Script", "Organic Human Operator Pro"], 4)
                st.session_state.captcha_quiz_correct = "Organic Human Operator Pro"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. SIGN IN / SIGN UP GATEWAYS
