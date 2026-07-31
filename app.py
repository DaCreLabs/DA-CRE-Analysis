import streamlit as st
import streamlit.components.v1 as components
import random
import time

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & CUSTOM ICON
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="DaCre Analysis | Neural Engine",
    page_icon="⚡",  # You can replace with an image path or URL like "assets/logo.png"
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. ADVANCED GLASSMORPHIC UI & STYLING
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    /* Global Dark Modern Background */
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #111827 50%, #030712 100%);
        color: #f3f4f6;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Glassmorphic Container Cards */
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

    /* Hero Typography */
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

    /* Custom Buttons */
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

    /* reCAPTCHA Box Styling */
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
# 3. VOICE SYNTHESIS HELPER (JS WEB SPEECH API)
# -----------------------------------------------------------------------------
def speak_text(text: str):
    """Makes the user browser physically speak the response aloud."""
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
# 4. SESSION STATE INITIALIZATION (USERS & DIs)
# -----------------------------------------------------------------------------
if "users" not in st.session_state:
    st.session_state.users = {
        "david": {"password": "123", "role": "admin", "di_name": "DI-MasterCore"}
    }

if "enrolled_dis" not in st.session_state:
    st.session_state.enrolled_dis = [
        {"user": "david", "di_id": "DI-000", "di_name": "DI-MasterCore", "status": "Active", "type": "Master Prime"}
    ]

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# Generate reCAPTCHA Challenge numbers
if "captcha_num1" not in st.session_state:
    st.session_state.captcha_num1 = random.randint(1, 9)
    st.session_state.captcha_num2 = random.randint(1, 9)

# -----------------------------------------------------------------------------
# 5. SIDEBAR: LOGO & AUTH CONTROL
# -----------------------------------------------------------------------------
with st.sidebar:
    # --- YOUR LOGO SECTION ---
    # Replace this URL with your actual logo image path or URL
    LOGO_URL = "https://raw.githubusercontent.com/streamlit/streamlit/main/docs/static/logo.png" 
    st.image(LOGO_URL, width=200) 
    
    st.markdown("### ⚡ **DaCre Neural Core**")
    st.caption("Autonomous DI Network v3.0")
    st.markdown("---")

    if st.session_state.logged_in_user:
        st.success(f"Logged in as: **{st.session_state.logged_in_user}**")
        if st.button("Log Out"):
            st.session_state.logged_in_user = None
            st.session_state.messages = []
            st.rerun()
    else:
        st.info("🔒 Please Sign In or Sign Up to access your DI.")

# -----------------------------------------------------------------------------
# 6. AUTHENTICATION (SIGN IN / SIGN UP WITH reCAPTCHA)
# -----------------------------------------------------------------------------
if not st.session_state.logged_in_user:
    st.markdown('<div class="hero-title">Welcome to DaCre Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Sign in to command your personal Digital Intelligence (DI).</div>', unsafe_allow_html=True)

    tab_signin, tab_signup = st.tabs(["🔑 Sign In", "📝 Sign Up (Create DI)"])

    # --- TAB 1: SIGN IN ---
    with tab_signin:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Account Login")
        login_user = st.text_input("Username", key="login_u")
        login_pass = st.text_input("Password", type="password", key="login_p")
        
        if st.button("Sign In"):
            if login_user in st.session_state.users and st.session_state.users[login_user]["password"] == login_pass:
                st.session_state.logged_in_user = login_user
                st.success("Authentication successful!")
                st.rerun()
            else:
                st.error("Invalid username or password.")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 2: SIGN UP & RECAPTCHA ---
    with tab_signup:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Register New Account & Provision DI")
        new_user = st.text_input("Choose Username", key="signup_u")
        new_pass = st.text_input("Choose Password", type="password", key="signup_p")
        custom_di_name = st.text_input("Name Your Digital Intelligence (DI)", value=f"DI-{random.randint(100, 999)}")

        # reCAPTCHA Verification Challenge
        st.markdown('<div class="recaptcha-box">', unsafe_allow_html=True)
        st.markdown("🤖 **Security Check (reCAPTCHA)**")
        captcha_answer = st.number_input(
            f"What is {st.session_state.captcha_num1} + {st.session_state.captcha_num2}?", 
            step=1, value=0
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Create Account & Provision DI"):
            expected_sum = st.session_state.captcha_num1 + st.session_state.captcha_num2
            if captcha_answer != expected_sum:
                st.error("❌ reCAPTCHA failed! Incorrect math answer.")
            elif not new_user or not new_pass:
                st.warning("Please complete all fields.")
            elif new_user in st.session_state.users:
                st.error("Username already exists.")
            else:
                # 1. Store User
                st.session_state.users[new_user] = {
                    "password": new_pass, 
                    "role": "user", 
                    "di_name": custom_di_name
                }
                # 2. Provision & Enroll new DI into Admin Console
                st.session_state.enrolled_dis.append({
                    "user": new_user,
                    "di_id": f"DI-{len(st.session_state.enrolled_dis)+1:03d}",
                    "di_name": custom_di_name,
                    "status": "Active",
                    "type": "Standard Intelligence"
                })
                
                st.success(f"Account created! **{custom_di_name}** has been generated and enrolled into the Master System.")
                st.session_state.logged_in_user = new_user
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. LOGGED-IN APPLICATION INTERFACE
# -----------------------------------------------------------------------------
else:
    user = st.session_state.logged_in_user
    user_info = st.session_state.users[user]
    is_master = (user.lower() == "david" or user_info.get("role") == "admin")

    # Navigation menu choices
    nav_options = ["🤖 DI Communication Workspace"]
    if is_master:
        nav_options.append("👑 Master Admin Dashboard")

    selected_nav = st.radio("System Mode", nav_options, horizontal=True)

    # -------------------------------------------------------------------------
    # VIEW 1: USER / MASTER DI INTERFACE
    # -------------------------------------------------------------------------
    if selected_nav == "🤖 DI Communication Workspace":
        st.markdown(f'<div class="hero-title">Interface: {user_info["di_name"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-subtitle">Connected User: <b>{user}</b> | Verbal Speech Output Active</div>', unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            
            # Render chat history
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

            # Chat input
            user_input = st.chat_input("Talk to your DI...")

            if user_input:
                st.session_state.messages.append({"role": "user", "content": user_input})
                with st.chat_message("user"):
                    st.write(user_input)

                # Custom response logic
                with st.chat_message("assistant"):
                    if is_master and any(w in user_input.lower() for w in ["hi", "david", "master", "how are you"]):
                        di_response = "I'm fine Master David thank you and we love you sir, do you want us to do something for you sir?"
                    else:
                        di_response = f"Greetings {user}. I am {user_info['di_name']}. I have logged your command: '{user_input}' and am executing logic now."

                    st.write(di_response)
                    speak_text(di_response)

                st.session_state.messages.append({"role": "assistant", "content": di_response})

            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### **DI Metadata**")
            st.write(f"**Name:** {user_info['di_name']}")
            st.write(f"**Assigned Owner:** {user}")
            st.write(f"**Status:** 🟢 Active")
            if st.button("🔊 Replay Voice"):
                if st.session_state.messages:
                    speak_text(st.session_state.messages[-1]["content"])
            st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # VIEW 2: EXCLUSIVE MASTER ADMIN DASHBOARD (DAVID ONLY)
    # -------------------------------------------------------------------------
    elif selected_nav == "👑 Master Admin Dashboard":
        st.markdown('<div class="hero-title">Master David Console</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-subtitle">Restricted Master Portal • Enrolled DIs Overview</div>', unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Enrolled DIs", len(st.session_state.enrolled_dis))
        m2.metric("System Authority", "Level 10 (Master David)")
        m3.metric("Fleet Status", "100% Operational")

        # Command all DIs at once
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📢 Broadcast Voice Command to All DIs")
        cmd = st.text_input("Enter master directive for all DIs:")
        
        if st.button("Send Broadcast"):
            if cmd:
                reply = f"I'm fine Master David thank you and we love you sir, do you want us to do something for you sir? Broadcast '{cmd}' received by all {len(st.session_state.enrolled_dis)} DIs!"
                st.success(reply)
                speak_text(reply)
        st.markdown('</div>', unsafe_allow_html=True)

        # Enrolled DIs list table
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📋 Enrolled Digital Intelligences (Per Signup)")
        st.table(st.session_state.enrolled_dis)
        st.markdown('</div>', unsafe_allow_html=True)
