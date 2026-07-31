import streamlit as st
import streamlit.components.v1 as components
import random

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & LOGO SETUP
# -----------------------------------------------------------------------------
APP_NAME = "dacre-analysis"

# ⬇️ UPDATED TO MATCH YOUR GITHUB FILENAME ⬇️
LOGO_PATH = "ChatGPT Image Jul 29, 2026, 02_27_41 PM.png" 

# Set Page Config with Logo as Page Icon
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
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# -----------------------------------------------------------------------------
# 2. CUSTOM UI & GLASSMORPHIC STYLING
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #111827 50%, #030712 100%);
        color: #f3f4f6;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    .glass-card {
        background: rgba(17, 24, 39, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
    }
    .hero-title {
        background: linear-gradient(90deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .hero-subtitle {
        color: #9ca3af;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .stButton>button {
        background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
        color: #ffffff;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px 0 rgba(79, 70, 229, 0.39);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(79, 70, 229, 0.55);
    }
    .recaptcha-box {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 8px;
        padding: 12px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. VOICE SYNTHESIS HELPER
# -----------------------------------------------------------------------------
def speak_text(text: str):
    clean_text = text.replace("'", "\\'").replace("\n", " ")
    js_code = f"""
    <script>
        var msg = new SpeechSynthesisUtterance('{clean_text}');
        msg.rate = 1.0;
        msg.pitch = 1.0;
        msg.volume = 1.0;
        window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js_code, height=0, width=0)

# -----------------------------------------------------------------------------
# 4. INITIALIZE SESSION STATE
# -----------------------------------------------------------------------------
if "users" not in st.session_state:
    st.session_state.users = {
        "david": {"password": "123", "role": "admin", "di_name": "DI-MasterPrime"}
    }

if "enrolled_dis" not in st.session_state:
    st.session_state.enrolled_dis = [
        {"user": "david", "di_id": "DI-000", "di_name": "DI-MasterPrime", "status": "Active", "type": "Master Executive"}
    ]

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "captcha_num1" not in st.session_state:
    st.session_state.captcha_num1 = random.randint(1, 9)
    st.session_state.captcha_num2 = random.randint(1, 9)

# -----------------------------------------------------------------------------
# 5. SIDEBAR: LOGO DISPLAY & BRANDING
# -----------------------------------------------------------------------------
with st.sidebar:
    # Render Logo Image in Sidebar
    try:
        st.image(LOGO_PATH, use_container_width=True)
    except Exception:
        st.info("🖼️ Place your logo file in your GitHub repository to display your logo here.")

    st.markdown(f"### ⚡ **{APP_NAME}**")
    st.caption("Autonomous DI Network Core")
    st.markdown("---")

    if st.session_state.logged_in_user:
        st.success(f"User: **{st.session_state.logged_in_user}**")
        if st.button("Sign Out"):
            st.session_state.logged_in_user = None
            st.session_state.messages = []
            st.rerun()
    else:
        st.info("🔒 Authentication Required")

# -----------------------------------------------------------------------------
# 6. AUTHENTICATION & RECAPTCHA
# -----------------------------------------------------------------------------
if not st.session_state.logged_in_user:
    st.markdown(f'<div class="hero-title">{APP_NAME} Portal</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Sign in or register to deploy your personal Digital Intelligence.</div>', unsafe_allow_html=True)

    tab_signin, tab_signup = st.tabs(["🔑 Sign In", "📝 Sign Up & Create DI"])

    with tab_signin:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Account Login")
        login_user = st.text_input("Username", key="l_user")
        login_pass = st.text_input("Password", type="password", key="l_pass")
        
        if st.button("Sign In"):
            if login_user in st.session_state.users and st.session_state.users[login_user]["password"] == login_pass:
                st.session_state.logged_in_user = login_user
                st.success("Authenticated successfully!")
                st.rerun()
            else:
                st.error("Invalid username or password.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_signup:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Create Account & Auto-Enroll DI")
        new_user = st.text_input("New Username", key="s_user")
        new_pass = st.text_input("New Password", type="password", key="s_pass")
        custom_di_name = st.text_input("Name Your Digital Intelligence (DI)", value=f"DI-{random.randint(100, 999)}")

        st.markdown('<div class="recaptcha-box">', unsafe_allow_html=True)
        st.markdown("🤖 **Security Check (reCAPTCHA)**")
        captcha_ans = st.number_input(
            f"Solve: {st.session_state.captcha_num1} + {st.session_state.captcha_num2} =", 
            step=1, value=0
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Create Account"):
            expected = st.session_state.captcha_num1 + st.session_state.captcha_num2
            if captcha_ans != expected:
                st.error("❌ reCAPTCHA check failed.")
            elif not new_user or not new_pass:
                st.warning("Please fill out all fields.")
            elif new_user in st.session_state.users:
                st.error("Username already registered.")
            else{
                st.session_state.users[new_user] = {
                    "password": new_pass, 
                    "role": "user", 
                    "di_name": custom_di_name
                }
                st.session_state.enrolled_dis.append({
                    "user": new_user,
                    "di_id": f"DI-{len(st.session_state.enrolled_dis):03d}",
                    "di_name": custom_di_name,
                    "status": "Active",
                    "type": "Standard Intelligence"
                })
                
                st.success(f"Account created! **{custom_di_name}** enrolled successfully.")
                st.session_state.logged_in_user = new_user
                st.rerun()
