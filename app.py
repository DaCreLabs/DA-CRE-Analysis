import streamlit as st
import streamlit.components.v1 as components
import random
import pandas as pd
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. PAGE INITIALIZATION & CONFIGURATION
# -----------------------------------------------------------------------------
APP_NAME = "DA-CRE-Analysis"
LOGO_PATH = "ChatGPT Image Jul 29, 2026, 02_27_41 PM.png"

try:
    st.set_page_config(
        page_title=f"{APP_NAME} | Analytics Core",
        page_icon=LOGO_PATH,
        layout="wide",
        initial_sidebar_state="expanded"
    )
except Exception:
    st.set_page_config(
        page_title=f"{APP_NAME} | Analytics Core",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# -----------------------------------------------------------------------------
# 2. PREMIUM LIGHT BLUE & INDIGO BRAND UI ENGINE
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    .stApp {
        background: linear-gradient(135deg, #f4f7fe 0%, #e0e8f9 100%);
        color: #1e293b !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .brand-card {
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-top: 5px solid #3b82f6 !important;
        border-radius: 16px !important;
        padding: 28px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.04);
        transition: all 0.3s ease;
    }
    .brand-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 16px 35px rgba(59, 130, 246, 0.09);
        border-top-color: #4f46e5 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #1e1b4b !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
    }
    p, label, span {
        color: #334155 !important;
        font-weight: 500 !important;
    }
    
    .brand-title {
        background: linear-gradient(135deg, #3b82f6 0%, #4f46e5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -1.5px;
        margin-bottom: 6px;
    }
    
    .stTextInput>div>div>input {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 10px !important;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 28px !important;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700 !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.25) !important;
        transition: all 0.2s ease !important;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #64748b !important;
        font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #4f46e5 !important;
        border-bottom-color: #4f46e5 !important;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. VERBAL AUDIO VOICE SYSTEM
# -----------------------------------------------------------------------------
def execute_voice_output(text: str):
    escaped_text = text.replace("'", "\\'").replace("\n", " ")
    speech_component = f"""
    <script>
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel(); 
            var voiceUtterance = new SpeechSynthesisUtterance('{escaped_text}');
            voiceUtterance.rate = 1.05;
            voiceUtterance.volume = 1.0;
            window.speechSynthesis.speak(voiceUtterance);
        }}
    </script>
    """
    components.html(speech_component, height=0, width=0)

# -----------------------------------------------------------------------------
# 4. DATA ENGINE REPOSITORIES
# -----------------------------------------------------------------------------
if "users" not in st.session_state:
    st.session_state.users = {
        "david": {"password": "123", "role": "admin", "di_name": "DI-MasterPrime"}
    }

if "enrolled_dis" not in st.session_state:
    st.session_state.enrolled_dis = [
        {"user": "david", "di_id": "DI-000", "di_name": "DI-MasterPrime", "status": "Active", "type": "Quantum Core"}
    ]

if "products_db" not in st.session_state:
    st.session_state.products_db = [
        {"Product ID": "P-101", "Product Name": "Neural Network Node", "Category": "Hardware", "Status": "Operational", "Assigned Field": "Quantum Computing"},
        {"Product ID": "P-102", "Product Name": "Starfall Analytics Suite", "Category": "Software", "Status": "Optimization", "Assigned Field": "Data Processing"},
        {"Product ID": "P-103", "Product Name": "Sovereign Link Matrix", "Category": "Network", "Status": "Deploying", "Assigned Field": "Security"}
    ]

if "audit_logs" not in st.session_state:
    st.session_state.audit_logs = [
        {"Timestamp": "2026-07-31 12:00:00", "User": "System", "Action": "Initialized Hive Environment", "Details": "All system parameters optimal."}
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

if st.session_state.last_spoken_phrase:
    execute_voice_output(st.session_state.last_spoken_phrase)
    st.session_state.last_spoken_phrase = None

# -----------------------------------------------------------------------------
# 5. SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    try:
        st.image(LOGO_PATH, use_container_width=True)
    except Exception:
        st.info("ℹ️ Secure logo link placeholder active.")

    st.title(APP_NAME)
    st.markdown("<p style='color:#64748b;'>Data Today, Smarter Tomorrows</p>", unsafe_allow_html=True)
    st.markdown("---")

    if st.session_state.logged_in_user:
        st.success(f"Operator: **{st.session_state.logged_in_user.upper()}**")
        if st.button("Close Active Session", use_container_width=True):
            st.session_state.logged_in_user = None
            st.rerun()
    else:
        st.info("🔒 Identity Verification Protocol Online")

# -----------------------------------------------------------------------------
# SECURITY INTERCEPT POPUP
# -----------------------------------------------------------------------------
if st.session_state.show_fullscreen_captcha:
    st.warning("🚨 SECURITY LOG: IDENTITY CONFLICT DETECTED")
    st.markdown("### This account has already been added. Please sign in!")
    st.write(f"To continue, confirm classification matching parameter: **{st.session_state.captcha_quiz_correct}**")
    
    user_selected_ans = st.radio("Select verified response signature:", st.session_state.captcha_quiz_options)
    
    if st.button("Submit Verification Check", use_container_width=True):
        if user_selected_ans == st.session_state.captcha_quiz_correct:
            st.session_state.show_fullscreen_captcha = False
            st.rerun()
        else:
            st.error("Verification mismatch. Re-syncing anti-bot token challenges.")
            st.session_state.captcha_quiz_options = random.sample(["Quantum Server", "Cyber Grid Node", "System Bot Core", "Human Operator Asset"], 4)
            st.session_state.captcha_quiz_correct = "Human Operator Asset"
            st.rerun()

# -----------------------------------------------------------------------------
# 6. ENTRANCE GATEWAY INTERFACE
# -----------------------------------------------------------------------------
elif not st.session_state.logged_in_user:
    st.markdown(f'<div class="brand-title">{APP_NAME} Hub</div>', unsafe_allow_html=True)
    st.write("Deploy deep metrics telemetry, query analytics pipelines, and connect seamlessly to operational intelligence frameworks.")
    
    tab_login, tab_registration = st.tabs(["🔑 CORE SYSTEM ACCESS", "📝 INITIALIZE NEW CORE PROFILE"])
    
    with tab_login:
        st.markdown('<div class="brand-card">', unsafe_allow_html=True)
        st.subheader("Sign In Verification")
        input_user = st.text_input("Account Identifier Token", placeholder="Enter username sequence...", key="login_uid")
        input_pass = st.text_input("Security Key Verification String", placeholder="Enter account passkey code...", type="password", key="login_pkey")
        
        if st.button("Authorize Connection Link", use_container_width=True):
            if input_user in st.session_state.users and st.session_state.users[input_user]["password"] == input_pass:
                st.session_state.logged_in_user = input_user
                if st.session_state.users[input_user]["role"] == "admin":
                    st.session_state.last_spoken_phrase = f"Welcome back, Master {input_user}. Full executive administrative controls are now completely unlocked."
                else:
                    st.session_state.last_spoken_phrase = f"Connection successful. Operator dashboard online for user {input_user}."
                st.rerun()
            else:
