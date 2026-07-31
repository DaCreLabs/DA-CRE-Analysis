import streamlit as st
import streamlit.components.v1 as components
import random
import pandas as pd
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. PAGE INITIALIZATION & CONFIGURATION
# -----------------------------------------------------------------------------
APP_NAME = "DA-CRE-Analysis"
LOGO_PATH = "IMG_20260729_135217.jpg"

try:
    st.set_page_config(
        page_title=f"{APP_NAME} // Starfall Analytics Core",
        page_icon=LOGO_PATH,
        layout="wide",
        initial_sidebar_state="expanded"
    )
except Exception:
    st.set_page_config(
        page_title=f"{APP_NAME} // Starfall Analytics Core",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# -----------------------------------------------------------------------------
# 2. EXPERIMENTAL HOVERING SKY ANIMATION ENGINE & HIGH-CONTRAST TYPOGRAPHY
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    /* Cosmic Animated Background */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #0d1527 0%, #050914 50%, #02040a 100%);
        background-size: 200% 200%;
        animation: starSkyMovement 25s ease infinite alternate;
        color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    @keyframes starSkyMovement {
        0% { background-position: 0% 10%; }
        50% { background-position: 50% 80%; }
        100% { background-position: 100% 10%; }
    }
    
    /* Premium Glassmorphic Cards with Float Actions */
    .sky-card {
        background: rgba(10, 17, 34, 0.75);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 242, 254, 0.18);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 24px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5), inset 0 0 15px rgba(0, 242, 254, 0.03);
        transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .sky-card:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 242, 254, 0.45);
        box-shadow: 0 20px 45px rgba(0, 242, 254, 0.12), inset 0 0 25px rgba(0, 242, 254, 0.05);
    }
    
    /* Super-High Contrast Global Override for Text Visibility */
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: #ffffff !important;
    }
    .sub-text {
        color: #cbd5e1 !important;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    /* Stunning Kinetic Headers */
    .sky-title {
        font-family: 'Space Grotesk', sans-serif;
        background: linear-gradient(135deg, #00f2fe 0%, #3b82f6 50%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.8rem;
        font-weight: 800;
        letter-spacing: -2px;
        line-height: 1.1;
        margin-bottom: 12px;
    }
    
    /* Customized Form Inputs for Legibility */
    .stTextInput>div>div>input {
        background-color: rgba(15, 23, 42, 0.8) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
    }
    
    /* Interactive Cybernetic Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #00f2fe 0%, #3b82f6 100%) !important;
        color: #020617 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 28px !important;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
        box-shadow: 0 8px 20px rgba(0, 242, 254, 0.25) !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 28px rgba(0, 242, 254, 0.45) !important;
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
# 4. MEMORY STORAGE (SESSION STATE)
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

if "captcha_v1" not in st.session_state:
    st.session_state.captcha_v1 = random.randint(2, 9)
    st.session_state.captcha_v2 = random.randint(2, 9)

if st.session_state.last_spoken_phrase:
    execute_voice_output(st.session_state.last_spoken_phrase)
    st.session_state.last_spoken_phrase = None

# -----------------------------------------------------------------------------
# 5. SIDEBAR BRANDING
# -----------------------------------------------------------------------------
with st.sidebar:
    try:
        st.image(LOGO_PATH, use_container_width=True)
    except Exception:
        st.error("System Log: Logo image asset missing from root folder directory.")

    st.markdown(f"### **{APP_NAME}**")
    st.markdown("<p style='color:#cbd5e1 !important;'>Starfall Cybernetic Mesh</p>", unsafe_allow_html=True)
    st.markdown("---")

    if st.session_state.logged_in_user:
        st.write(f"Active Session: :cyan[**{st.session_state.logged_in_user.upper()}**]")
        if st.button("Disconnect Platform", use_container_width=True):
            st.session_state.logged_in_user = None
            st.rerun()
    else:
        st.info("Authentication Gateway Online.")

# -----------------------------------------------------------------------------
# 6. GATEWAY WALL (LOGIN / SIGN UP)
# -----------------------------------------------------------------------------
if not st.session_state.logged_in_user:
    st.markdown(f'<div class="sky-title">{APP_NAME}</div>', unsafe_allow_html=True)
    st.markdown('<p class="sub-text">Welcome to the Starfall Ecosystem. Log in to deploy telemetry analytics and query independent network instances.</p>', unsafe_allow_html=True)

    tab_login, tab_registration = st.tabs(["🔑 UNLOCK CORE PORTAL", "📝 PROVISION SECURITY INDEX"])

    with tab_login:
        st.markdown('<div class="sky-card">', unsafe_allow_html=True)
        st.subheader("Identity Verification Check")
        input_user = st.text_input("Username Reference Token", key="login_uid")
        input_pass = st.text_input("Cryptographic Access Key", type="password", key="login_pkey")
        
        if st.button("Establish Verified Interface Link"):
            if input_user in st.session_state.users and st.session_state.users[input_user]["password"] == input_pass:
                st.session_state.logged_in_user = input_user
                if st.session_state.users[input_user]["role"] == "admin":
                    st.session_state.last_spoken_phrase = f"Welcome back, Master {input_user}. Full executive administrative controls are now completely unlocked."
                else:
                    st.session_state.last_spoken_phrase = f"Connection successful. Operator dashboard online for user {input_user}."
                st.rerun()
            else:
                st.error("Access Denied: Provided token mismatch.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_registration:
        st.markdown('<div class="sky-card">', unsafe_allow_html=True)
        st.subheader("Initialize Brand New System Account")
        reg_user = st.text_input("Choose Operator Username", key="reg_uid")
        reg_pass = st.text_input("Choose System Password", type="password", key="reg_pkey")
        desired_di = st.text_input("Designate System DI Alias Node", value=f"DI-Nebula-{random.randint(1000, 9999)}")

        st.markdown("<p style='font-weight:600;'>Security Matrix Sync Code Check</p>", unsafe_allow_html=True)
        expected_sum = st.session_state.captcha_v1 + st.session_state.captcha_v2
