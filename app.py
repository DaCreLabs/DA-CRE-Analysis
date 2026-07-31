import streamlit as st
import streamlit.components.v1 as components
import random
import pandas as pd
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. PAGE INITIALIZATION & CONFIGURATION
# -----------------------------------------------------------------------------
APP_NAME = "DA-CRE-Analysis"

# ⬇️ CHOOSE THE EXACT RENAMED LOGO DIRECTORY AS THE HOOK ⬇️
LOGO_PATH = "my_logo.png"

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
    
    /* Premium Glassmorphic Cards with High Contrast Visibility Borders */
    .sky-card {
        background: rgba(13, 22, 47, 0.9) !important;
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 2px solid rgba(0, 242, 254, 0.4) !important;
        border-radius: 20px;
        padding: 35px;
        margin-top: 15px;
        margin-bottom: 24px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7), inset 0 0 20px rgba(0, 242, 254, 0.05);
    }
    
    /* Absolute Force Global Text Colors for Clear Legibility */
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown div {
        color: #ffffff !important;
    }
    
    .sidebar-text {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    .sub-text {
        color: #e2e8f0 !important;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    /* Stunning Kinetic Title */
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
    
    /* Enhanced Input Layout Structure */
    .stTextInput>div>div>input {
        background-color: #0b1120 !important;
        color: #ffffff !important;
        border: 2px solid rgba(0, 242, 254, 0.3) !important;
        border-radius: 12px !important;
        padding: 10px !important;
        font-size: 1.05rem !important;
    }
    
    /* Custom Interactive Navigation Elements */
    .stTabs [data-baseweb="tab"] {
        color: #cbd5e1 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #00f2fe !important;
        border-bottom-color: #00f2fe !important;
    }
    
    /* Kinetic Action Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #00f2fe 0%, #3b82f6 100%) !important;
        color: #020617 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 32px !important;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
        box-shadow: 0 8px 25px rgba(0, 242, 254, 0.3) !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 14px 35px rgba(0, 242, 254, 0.5) !important;
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
# 4. MEMORY STORAGE (SESSION STATE ENGINE)
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
# 5. SIDEBAR BRANDING
# -----------------------------------------------------------------------------
with st.sidebar:
    try:
        st.image(LOGO_PATH, use_container_width=True)
    except Exception:
        st.markdown("<div style='border:1px dashed rgba(255,255,255,0.2); padding:10px; text-align:center;'>🖼️ Waiting for my_logo.png file sync...</div>", unsafe_allow_html=True)

    st.markdown(f"<h2>{APP_NAME}</h2>", unsafe_allow_html=True)
    st.markdown("<p class='sidebar-text'>Starfall Cybernetic Mesh</p>", unsafe_allow_html=True)
    st.markdown("---")

    if st.session_state.logged_in_user:
        st.write(f"Active Session: :cyan[**{st.session_state.logged_in_user.upper()}**]")
        if st.button("Disconnect Platform", use_container_width=True):
            st.session_state.logged_in_user = None
            st.rerun()
    else:
        st.markdown("<div style='background:rgba(0,242,254,0.1); border:1px solid #00f2fe; padding:10px; border-radius:8px; text-align:center;'>🔒 Security Firewall Active</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# INTERCEPT MODAL: FULLSCREEN SECURITY CAPTCHA OVERTAKE
# -----------------------------------------------------------------------------
if st.session_state.show_fullscreen_captcha:
    st.markdown("""
        <style>
        [data-testid="stSidebar"] { display: none !important; }
        .stTabs { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: #ff3366 !important; font-size: 3rem;'>🚨 SYSTEM SECURITY TAKEOVER</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem;'>This account has already been added. Solve the challenge to return to the sign-in hub.</p>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    _, col_c2, _ = st.columns([1, 2, 1])
    with col_c2:
        st.markdown('<div class="sky-card" style="border: 2px solid #ff3366 !important;">', unsafe_allow_html=True)
        st.subheader("🛡️ CAPTCHA Verification Matrix Challenge")
        st.write(f"**Question:** Select the item matching classification: **{st.session_state.captcha_quiz_correct.upper()}**")
        
        user_selected_ans = st.radio("Available Signatures:", st.session_state.captcha_quiz_options)
        
        if st.button("Submit Cryptographic Resolution Verification"):
            if user_selected_ans == st.session_state.captcha_quiz_correct:
                st.session_state.show_fullscreen_captcha = False
                st.rerun()
            else:
