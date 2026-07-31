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
# 2. BALANCED CONTRAST BRAND UI STYLING ENGINE
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    /* Smooth, Flat Deep Space Canvas Background */
    .stApp {
        background-color: #0e1726 !important;
        background-image: none !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Clean Solid Slate Cards for Optimal Contrast Visibility */
    .glass-card {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 16px !important;
        padding: 30px;
        margin-top: 10px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }

    /* Stark White Text for Complete Legibility */
    h1, h2, h3, h4, h5, h6, p, label, span, div, [data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
    }

    /* Clear High-Contrast Sidebar Labels */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }

    /* Dynamic Multi-Color Hero Typography */
    .hero-title {
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .hero-subtitle {
        color: #94a3b8 !important;
        font-size: 1.1rem;
        margin-bottom: 25px;
    }

    /* Solid White Input Fields for Perfect Form Ingestion */
    .stTextInput input, .stNumberInput input, .stSelectbox div {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    
    /* Interactive Navigation Tab Settings */
    .stTabs [data-baseweb="tab"] {
        color: #94a3b8 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #38bdf8 !important;
        border-bottom-color: #38bdf8 !important;
    }

    /* Kinetic Action Command Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #3b82f6 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 28px !important;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700 !important;
        box-shadow: 0 4px 14px rgba(59, 130, 246, 0.3) !important;
        width: 100%;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5) !important;
    }

    /* Security Component Alert Container Box */
    .recaptcha-box {
        background: #1e293b !important;
        border: 2px solid #ff3366 !important;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. VERBAL AUDIO VOICE ENGINE
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

# Execute browser voice triggers
if st.session_state.last_spoken_phrase:
    speak_text(st.session_state.last_spoken_phrase)
    st.session_state.last_spoken_phrase = None

# -----------------------------------------------------------------------------
# 5. SIDEBAR BRANDING & OPERATOR PROTOCOLS
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
        st.write(f"Active Account: :cyan[**{st.session_state.logged_in_user.upper()}**]")
        if st.button("Disconnect Session", use_container_width=True):
            st.session_state.logged_in_user = None
            st.rerun()
    else:
        st.markdown("<div style='background:rgba(56,189,248,0.1); border:1px solid #38bdf8; padding:10px; border-radius:8px; text-align:center; color:#38bdf8 !important; font-weight:600;'>🔒 Secure Firewall Active</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# FULL-SCREEN RECAPTCHA TAKEOVER INTERCEPT LAYOUT
# -----------------------------------------------------------------------------
if st.session_state.show_fullscreen_captcha:
    st.markdown("""
        <style>
        [data-testid="stSidebar"] { display: none !important; }
        .stTabs { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: #ff3366 !important; font-size: 3rem;'>🚨 SYSTEM SECURITY CAPTCHA INTERCEPT</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem;'>This account has already been added. Complete verification to return to entry hub.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    _, col_c2, _ = st.columns()
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

