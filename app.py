import streamlit as st
import streamlit.components.v1 as components
import random

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & LOGO INITIALIZATION
# -----------------------------------------------------------------------------
APP_NAME = "DA-CRE-Analysis"

# ⬇️ UPDATED TO THE CLEAN REPO IMAGE PATH ⬇️
LOGO_PATH = "IMG_20260729_135217.jpg"

try:
    st.set_page_config(
        page_title=f"{APP_NAME} // Cybernetic Intelligence Grid",
        page_icon=LOGO_PATH,
        layout="wide",
        initial_sidebar_state="expanded"
    )
except Exception:
    st.set_page_config(
        page_title=f"{APP_NAME} // Cybernetic Intelligence Grid",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# -----------------------------------------------------------------------------
# 2. ULTRA-NEXT-GEN SYSTEM STYLING (HTML/CSS ENGINE)
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    .stApp {
        background: radial-gradient(circle at 50% 0%, #0a1128 0%, #040814 70%, #010206 100%);
        color: #e2e8f0;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Neon Cyber Matrix Card */
    .cyber-card {
        background: rgba(6, 11, 25, 0.65);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(0, 242, 254, 0.15);
        border-radius: 24px;
        padding: 32px;
        margin-bottom: 24px;
        box-shadow: 0 0 40px rgba(0, 242, 254, 0.05), inset 0 0 20px rgba(0, 242, 254, 0.02);
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .cyber-card:hover {
        border-color: rgba(0, 242, 254, 0.3);
        box-shadow: 0 0 50px rgba(0, 242, 254, 0.1), inset 0 0 30px rgba(0, 242, 254, 0.05);
    }
    
    /* Admin Matrix Shield Card */
    .admin-card {
        background: rgba(15, 6, 25, 0.7);
        backdrop-filter: blur(24px);
        border: 1px solid rgba(167, 139, 250, 0.25);
        border-radius: 24px;
        padding: 32px;
        box-shadow: 0 0 40px rgba(167, 139, 250, 0.08);
    }
    
    /* Out-Of-The-Box Experimental Typography */
    .cyber-title {
        font-family: 'Space Grotesk', sans-serif;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 40%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -2px;
        line-height: 1.1;
        margin-bottom: 8px;
    }
    .cyber-subtitle {
        color: #94a3b8;
        font-size: 1.15rem;
        font-weight: 300;
        margin-bottom: 40px;
        letter-spacing: 0.5px;
    }
    
    /* Interactive Cybernetic Inputs & Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        color: #020617 !important;
        border: none;
        border-radius: 12px;
        padding: 12px 30px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: 0 8px 20px rgba(0, 242, 254, 0.25);
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 28px rgba(0, 242, 254, 0.45);
    }
    
    /* Custom Data Metrics */
    .metric-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #00f2fe;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. VERBAL AUDIO SYNTHESIS PIPELINE
# -----------------------------------------------------------------------------
def execute_voice_output(text: str):
    """Generates localized speech synthesis arrays dynamically across the browser context."""
    escaped_text = text.replace("'", "\\'").replace("\n", " ")
    speech_component = f"""
    <script>
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel(); 
            var voiceUtterance = new SpeechSynthesisUtterance('{escaped_text}');
            voiceUtterance.rate = 1.05;
            voiceUtterance.pitch = 0.95;
            voiceUtterance.volume = 1.0;
            window.speechSynthesis.speak(voiceUtterance);
        }}
    </script>
    """
    components.html(speech_component, height=0, width=0)

# -----------------------------------------------------------------------------
# 4. DISTRIBUTED HIVE DATA ARCHITECTURE
# -----------------------------------------------------------------------------
if "users" not in st.session_state:
    st.session_state.users = {
        "david": {"password": "123", "role": "admin", "di_name": "DI-MasterPrime"}
    }

if "enrolled_dis" not in st.session_state:
    st.session_state.enrolled_dis = [
        {"user": "david", "di_id": "DI-000", "di_name": "DI-MasterPrime", "status": "Active", "type": "Quantum Executive Core"}
    ]

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if "last_spoken_phrase" not in st.session_state:
    st.session_state.last_spoken_phrase = None

if "captcha_v1" not in st.session_state:
    st.session_state.captcha_v1 = random.randint(2, 9)
    st.session_state.captcha_v2 = random.randint(2, 9)

# Trigger verbal audio queues upon session transitions
if st.session_state.last_spoken_phrase:
    execute_voice_output(st.session_state.last_spoken_phrase)
    st.session_state.last_spoken_phrase = None

# -----------------------------------------------------------------------------
# 5. SIDEBAR ENVIRONMENT
# -----------------------------------------------------------------------------
with st.sidebar:
    # Explicit Logo Rendering Core
    try:
        st.image(LOGO_PATH, use_container_width=True)
    except Exception:
        st.error("System Notification: Logo asset file unreadable or missing from repo directory.")

    st.markdown(f"### **{APP_NAME}**")
    st.caption("Autonomous DI Grid Network")
    st.markdown("---")

    if st.session_state.logged_in_user:
        st.write(f"System Operator: :cyan[**{st.session_state.logged_in_user.upper()}**]")
        if st.button("Terminate Session", use_container_width=True):
            st.session_state.logged_in_user = None
            st.rerun()
    else:
        st.info("🔒 Secure Firewall Active. Authentication Required.")

# -----------------------------------------------------------------------------
# 6. APP MAIN PORTAL VIEW
# -----------------------------------------------------------------------------
if not st.session_state.logged_in_user:
    st.markdown(f'<div class="cyber-title">{APP_NAME}</div>', unsafe_allow_html=True)
    st.markdown('<div class="cyber-subtitle">Integrated Interface Engine for Advanced Exploratory Analytics & Core Intelligence Deployments.</div>', unsafe_allow_html=True)

    tab_login, tab_registration = st.tabs(["🔒 SECURE GATEWAY", "🧬 CONSTRUCT DIGITAL INTELLIGENCE"])

    with tab_login:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.subheader("Operator Login Verification")
        input_user = st.text_input("Operator Username Identifier", key="login_uid")
        input_pass = st.text_input("Cryptographic Security Key", type="password", key="login_pkey")
        
        if st.button("Initialize Authentication"):
            if input_user in st.session_state.users and st.session_state.users[input_user]["password"] == input_pass:
                st.session_state.logged_in_user = input_user
                if input_user == "david":
                    st.session_state.last_spoken_phrase = "Welcome back, Master David. Omni Admin Access granted. Your network systems are online."
                else:
                    st.session_state.last_spoken_phrase = f"Access authorized. Welcome to the neural matrix, {input_user}."
                st.rerun()
            else:
                st.error("Authentication rejected: Invalid identity token mapping.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_registration:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.subheader("Provision New Identity Space")
        reg_user = st.text_input("Register Unique Operator Username", key="reg_uid")
        reg_pass = st.text_input("Establish System Passcode String", type="password", key="reg_pkey")
        desired_di = st.text_input("Designate Digital Intelligence Identifier Token (DI Name)", value=f"DI-Nexus-{random.randint(1000, 9999)}")

        st.markdown("🌐 **Cryptographic Handshake Architecture (reCAPTCHA Verification)**")
        expected_sum = st.session_state.captcha_v1 + st.session_state.captcha_v2
        user_sum = st.number_input(f"Compute Verification Hex Matrix: {st.session_state.captcha_v1} + {st.session_state.captcha_v2} =", step=1, value=0)

        if st.button("Execute Core Compilation"):
            if user_sum != expected_sum:
                st.error("Handshake Failed: Cryptographic mathematical resolution mismatch.")
            elif not reg_user or not reg_pass:
                st.warning("Action Deferred: Registration fields cannot contain null matrix data.")
            elif reg_user in st.session_state.users:
                st.error("Identity Collision: Operator identifier sequence already structurally cataloged.")
            else:
                # Add user to memory matrix
                st.session_state.users[reg_user] = {"password": reg_pass, "role": "user", "di_name": desired_di}
                # Create corresponding Intelligence Node automatically
                st.session_state.enrolled_dis.append({
