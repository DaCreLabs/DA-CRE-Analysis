import streamlit as st
import streamlit.components.v1 as components
import random
import pandas as pd
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. PAGE INITIALIZATION & CONFIGURATION
# -----------------------------------------------------------------------------
APP_NAME = "DA-CRE-Analysis"
LOGO_PATH = "my_logo.png"

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
# 2. VERBAL AUDIO VOICE SYSTEM
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
# 3. SYSTEM STATE STORAGE ENGINE
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
# 4. SIDEBAR LOGO AND NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    try:
        st.image(LOGO_PATH, use_container_width=True)
    except Exception:
        st.info("ℹ️ my_logo.png not found. Upload it to GitHub to show your brand logo here.")

    st.title(APP_NAME)
    st.caption("Cybernetic Mesh Engine")
    st.markdown("---")

    if st.session_state.logged_in_user:
        st.success(f"Active: **{st.session_state.logged_in_user.upper()}**")
        if st.button("Sign Out System", use_container_width=True):
            st.session_state.logged_in_user = None
            st.rerun()
    else:
        st.warning("🔒 Secure Login Required")

# -----------------------------------------------------------------------------
# INTERCEPT TRIGGER MODE: FULLSCREEN CAPTCHA OVERTAKE
# -----------------------------------------------------------------------------
if st.session_state.show_fullscreen_captcha:
    st.error("🚨 SECURITY CLEARANCE INTERCEPT TRIGGERED")
    st.subheader("This account has already been added. Please sign in!")
    st.write(f"Verification Challenge: Select the classification mapping exactly matching: **{st.session_state.captcha_quiz_correct}**")
    
    user_selected_ans = st.radio("Select matching matrix sequence:", st.session_state.captcha_quiz_options)
    
    if st.button("Verify Identity Credentials", use_container_width=True):
        if user_selected_ans == st.session_state.captcha_quiz_correct:
            st.session_state.show_fullscreen_captcha = False
            st.rerun()
        else:
            st.error("Verification failed. Regenerating tracking parameters.")
            st.session_state.captcha_quiz_options = random.sample(["Quantum Server", "Cyber Grid Node", "System Bot Core", "Human Operator Asset"], 4)
            st.session_state.captcha_quiz_correct = "Human Operator Asset"
            st.rerun()

# -----------------------------------------------------------------------------
# 5. ENTRY SECURITY GATEWAY (LOGIN / REGISTRATION PROMPTS)
# -----------------------------------------------------------------------------
elif not st.session_state.logged_in_user:
    st.title(f"Welcome to {APP_NAME}")
    st.write("Access your safe multi-tenant sandbox space and monitor real-time analytical telemetry matrices below.")
    
    tab_login, tab_registration = st.tabs(["🔑 SYSTEM LOG-IN GATEWAY", "📝 REGISTER ACCOUNT NODE"])
    
    with tab_login:
        st.subheader("Operator Identity Gateway Check")
        input_user = st.text_input("Account Username Token", placeholder="Type username reference here...", key="login_uid")
        input_pass = st.text_input("Cryptographic Secure Key", placeholder="Type passkey credentials here...", type="password", key="login_pkey")
        
        if st.button("Establish Verified Interface Access Connection", use_container_width=True):
            if input_user in st.session_state.users and st.session_state.users[input_user]["password"] == input_pass:
                st.session_state.logged_in_user = input_user
                if st.session_state.users[input_user]["role"] == "admin":
                    st.session_state.last_spoken_phrase = f"Welcome back, Master {input_user}. Full executive administrative controls are now completely unlocked."
                else:
                    st.session_state.last_spoken_phrase = f"Connection successful. Operator dashboard online for user {input_user}."
                st.rerun()
            else:
                st.error("Authentication Error: Checked values do not match registered records.")

    with tab_registration:
        st.subheader("Provision New Active Account Node")
        reg_user = st.text_input("Choose Unique Account Username", placeholder="e.g., david_analytics", key="reg_uid")
        reg_pass = st.text_input("Choose Secure Code Password", placeholder="Type security passkey sequence...", type="password", key="reg_pkey")
        desired_di = st.text_input("Name Your Assigned DI Node", placeholder="Choose custom intelligence name...", value=f"DI-Nebula-{random.randint(1000, 9999)}")

        if st.button("Compile Global Node Profile Structure", use_container_width=True):
            if not reg_user or not reg_pass:
                st.warning("Action Cancelled: Empty parameter verification parameters processed.")
            elif reg_user in st.session_state.users:
                st.session_state.last_spoken_phrase = "This account has already been added. Please sign in immediately."
                st.session_state.captcha_quiz_options = random.sample(["Quantum Server", "Cyber Grid Node", "System Bot Core", "Human Operator Asset"], 4)
                st.session_state.captcha_quiz_correct = "Human Operator Asset"
                st.session_state.show_fullscreen_captcha = True
                st.rerun()
            else:
                st.session_state.users[reg_user] = {"password": reg_pass, "role": "user", "di_name": desired_di}
                st.session_state.enrolled_dis.append({
                    "user": reg_user, "di_id": f"DI-{random.randint(100,999)}", "di_name": desired_di, "status": "Active", "type": "Subscriber Node"
                })
                st.session_state.audit_logs.append({
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "User": reg_user, "Action": "Account Creation", "Details": f"New user signed up and created intelligence node: {desired_di}"
                })
                st.session_state.logged_in_user = reg_user
                st.session_state.last_spoken_phrase = f"Registration finalized. Welcome to the tracking interface."
                st.rerun()

# -----------------------------------------------------------------------------
# 6. HIGH-PRIVILEGE EXECUTIVE ADMINISTRATOR CONSOLE
# -----------------------------------------------------------------------------
elif st.session_state.users[st.session_state.logged_in_user]["role"] == "admin":
    st.title("🛡️ Master Control Dashboard")
    st.caption("Global Multi-Tenant Hub Overview")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    col1.metric("Active Subscribed DI Nodes", len(st.session_state.enrolled_dis))
    col2.metric("Total Cataloged Products", len(st.session_state.products_db))
    col3.metric("System Core Status", "OPTIMAL")

    st.markdown("---")
    st.subheader("🔮 Sovereign Hive Mind Vocal Interlink")
