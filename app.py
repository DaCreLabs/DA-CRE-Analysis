import streamlit as st
import streamlit.components.v1 as components
import random
import pandas as pd
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & LOGO SETUP
# -----------------------------------------------------------------------------
APP_NAME = "dacre-analysis"
LOGO_PATH = "david_profile.png"

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
    
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: url('https://user-images.githubusercontent.com/2673119/31048080-86532e74-a612-11e7-8250-9343be34a781.png') repeat;
        opacity: 0.15;
        pointer-events: none;
        animation: floatSky 75s infinite linear;
        z-index: 0 !important;
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

    /* Force Form Elements & Labels to be 100% Visible */
    label, p, h1, h2, h3, h4, h5, h6, [data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
    }

    /* High Visibility Form Input Fields */
    .stTextInput input, .stNumberInput input {
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
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5) !important;
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

if "messages" not in st.session_state:
    st.session_state.messages = []

if "show_fullscreen_captcha" not in st.session_state:
    st.session_state.show_fullscreen_captcha = False

if "captcha_quiz_options" not in st.session_state:
    st.session_state.captcha_quiz_options = ["Quantum Server Matrix", "Nebular System Cluster", "Bot Automation Footprint", "Organic Human Operator Pro"]
    st.session_state.captcha_quiz_correct = "Organic Human Operator Pro"

if "captcha_num1" not in st.session_state:
    st.session_state.captcha_num1 = random.randint(1, 9)
    st.session_state.captcha_num2 = random.randint(1, 9)

# Voice output trigger
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
        st.title("⚡ Logo")

    st.markdown(f"### **{APP_NAME}**")
    st.caption("Sky Engine v3.5 • Neural Core")
    st.markdown("---")

    if st.session_state.logged_in_user:
        st.success(f"Authenticated: **{st.session_state.logged_in_user.upper()}**")
        if st.button("Log Out"):
            st.session_state.logged_in_user = None
            st.session_state.messages = []
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
# 6. SIGN IN / SIGN UP PORTAL
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
                    st.session_state.last_spoken_phrase = "Welcome back, Master David. All sovereign admin control channels are operational."
                else:
                    st.session_state.last_spoken_phrase = f"Welcome back, operator {login_user}."
                st.success("Welcome back!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    else:
        st.subheader("Create Account")
        new_user = st.text_input("Choose Username", key="s_user")
        new_pass = st.text_input("Choose Password", type="password", key="s_pass")
        custom_di_name = st.text_input("Name Your DI Entity", value=f"DI-{random.randint(100, 999)}")

        st.markdown("---")
        st.write("🤖 **Security Check (reCAPTCHA)**")
        captcha_ans = st.number_input(
            f"Solve: {st.session_state.captcha_num1} + {st.session_state.captcha_num2} =", 
            step=1, value=0
        )

        if st.button("Create Account"):
            expected = st.session_state.captcha_num1 + st.session_state.captcha_num2
            if captcha_ans != expected:
                st.error("❌ reCAPTCHA check failed. Incorrect answer.")
            elif not new_user or not new_pass:
                st.warning("Please complete all fields.")
            elif new_user in st.session_state.users:
                st.session_state.show_fullscreen_captcha = True
                st.rerun()
            else:
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
                
                st.session_state.audit_logs.append({
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "User": new_user,
                    "Field Changed": "User Account Created",
                    "Old Value": "None",
                    "New Value": f"Enrolled {custom_di_name}"
                })

                st.session_state.last_spoken_phrase = f"Account created successfully. Welcome aboard, operator {new_user}."
                st.session_state.logged_in_user = new_user
                st.rerun()

# -----------------------------------------------------------------------------
# 7. LOGGED-IN SYSTEM WORKSPACE & ADMIN CONTROLS
# -----------------------------------------------------------------------------
else:
    user = st.session_state.logged_in_user
    user_info = st.session_state.users[user]
    is_master = (user.lower() == "david" or user_info.get("role") == "master")

    nav_tabs = ["🤖 DI Communication Console", "🛡️ User/Org Admin Portal"]
    if is_master:
        nav_tabs.append("👑 Master Executive Portal")

    selected_mode = st.radio("System Mode", nav_tabs, horizontal=True)
    st.markdown("---")

    # TAB 1: CONSOLE
    if selected_mode == "🤖 DI Communication Console":
        st.markdown(f'<div class="hero-title">{user_info["di_name"]} Core</div>', unsafe_allow_html=True)
        st.write(f"Connected User: **{user}** | Voice Engine Online")

        c1, c2 = st.columns([3, 1])

        with c1:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

            user_input = st.chat_input("Command your DI...")

            if user_input:
                st.session_state.messages.append({"role": "user", "content": user_input})
                with st.chat_message("user"):
                    st.write(user_input)

                with st.chat_message("assistant"):
                    if is_master and any(w in user_input.lower() for w in ["hi", "david", "master", "how are you"]):
                        response_text = "I'm fine Master David thank you and we love you sir, do you want us to do something for you sir?"
                    else:
                        response_text = f"Greetings {user}. I am {user_info['di_name']}. Request '{user_input}' received and processed."

                    st.write(response_text)
                    speak_text(response_text)

                st.session_state.messages.append({"role": "assistant", "content": response_text})

        with c2:
            st.markdown("#### **DI Status**")
            st.write(f"**Entity:** {user_info['di_name']}")
            st.write(f"**Assigned User:** {user}")
            st.write(f"**Status:** 🟢 Operational")
            if st.button("🔊 Replay Voice"):
                if st.session_state.messages:
                    speak_text(st.session_state.messages[-1]["content"])

    # TAB 2: ADMIN ACCESS
    elif selected_mode == "🛡️ User/Org Admin Portal":
        st.markdown('<div class="hero-title">Organization Admin Access</div>', unsafe_allow_html=True)
        st.write("Manage products, modify data fields, and view audit trails.")

        admin_passkey = st.text_input("Enter Admin Passkey", type="password")

        if admin_passkey == "admin123" or is_master:
            st.success("🔓 Admin Passkey Verified.")

            st.subheader("📦 Products & Resource Data")
            st.dataframe(pd.DataFrame(st.session_state.products), use_container_width=True)

            st.markdown("---")
            st.subheader("✏️ Make Status & Field Changes")

            col_a, col_b = st.columns(2)
            with col_a:
                selected_prod = st.selectbox("Select Product to Update", [p["Name"] for p in st.session_state.products])
            with col_b:
                new_status = st.selectbox("Select New Status", ["In Stock", "Low Stock", "Out of Stock", "Maintenance"])

            if st.button("Update Data Status"):
                for p in st.session_state.products:
                    if p["Name"] == selected_prod:
                        old_val = p["Status"]
                        p["Status"] = new_status
                        
                        st.session_state.audit_logs.append({
                            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "User": user,
                            "Field Changed": f"{selected_prod} Status",
                            "Old Value": old_val,
                            "New Value": new_status
                        })
                        st.success(f"Updated {selected_prod} status to '{new_status}'!")
                        st.rerun()

            st.markdown("---")
            st.subheader("📜 Data Change Audit Logs")
            st.dataframe(pd.DataFrame(st.session_state.audit_logs), use_container_width=True)

        else:
            st.info("🔑 Passkey required to unlock admin functions. Default passkey: `admin123`")

    # TAB 3: MASTER PORTAL
    elif selected_mode == "👑 Master Executive Portal" and is_master:
        st.markdown('<div class="hero-title">Master Executive Portal</div>', unsafe_allow_html=True)
        st.write("Full Authority Portal • Enrolled Fleet Overview")

        m1, m2, m3 = st.columns(3)
        m1.metric("Enrolled DIs", len(st.session_state.enrolled_dis))
        m2.metric("Master Level", "10 (David)")
        m3.metric("Fleet Status", "100% Operational")

        st.markdown("---")
        st.subheader("📢 Broadcast Voice Command to All DIs")
        broadcast_cmd = st.text_input("Issue global command:")

        if st.button("Execute Broadcast"):
            if broadcast_cmd:
                reply = f"I'm fine Master David thank you and we love you sir, do you want us to do something for you sir? Broadcast '{broadcast_cmd}' dispatched!"
                st.success(reply)
                speak_text(reply)

        st.markdown("---")
        st.subheader("📋 Enrolled DI Registry")
        st.dataframe(pd.DataFrame(st.session_state.enrolled_dis), use_container_width=True)
