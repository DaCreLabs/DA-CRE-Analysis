import streamlit as st
import streamlit.components.v1 as components
import random
import pandas as pd
import time
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & LOGO SETUP
# -----------------------------------------------------------------------------
APP_NAME = "dacre-analysis"
LOGO_PATH = "ChatGPT Image Jul 29, 2026, 02_27_41 PM.png"

try:
    st.set_page_config(
        page_title=f"{APP_NAME} | Built-In DI System",
        page_icon=LOGO_PATH,
        layout="wide",
        initial_sidebar_state="expanded"
    )
except Exception:
    st.set_page_config(
        page_title=f"{APP_NAME} | Built-In DI System",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# -----------------------------------------------------------------------------
# 2. CUSTOM STYLING & PERMANENT DI WIDGET CSS
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    /* Canvas Base Background */
    .stApp {
        background: radial-gradient(ellipse at bottom, #0f172a 0%, #020617 100%) !important;
    }

    /* Floating Sky Background Effect */
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
        z-index: -1 !important;
    }

    /* Custom Brown & Soft Light Blue Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #3D2314 0%, #22120A 100%) !important;
        border-right: 2px solid #38bdf8 !important;
    }

    [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #E0F2FE !important;
    }

    .hero-title {
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    /* Permanently Active DI Header Card */
    .di-status-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #38bdf8;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.2);
    }

    /* 5-Second Glowing Hover Loader CSS */
    .hover-loader-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 15px;
        margin-bottom: 20px;
    }

    .hover-loader {
        width: 60px;
        height: 60px;
        border: 4px solid rgba(56, 189, 248, 0.2);
        border-top: 4px solid #38bdf8;
        border-radius: 50%;
        animation: spin 1s linear infinite, glowPulse 5s ease-in-out infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    @keyframes glowPulse {
        0% { box-shadow: 0 0 5px #38bdf8; }
        50% { box-shadow: 0 0 25px #818cf8, 0 0 40px #38bdf8; }
        100% { box-shadow: 0 0 5px #38bdf8; }
    }

    /* Input Contrast Rules */
    label, p, h1, h2, h3, h4, h5, h6, [data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
    }

    .stTextInput input, .stNumberInput input, .stSelectbox div {
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
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5) !important;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. NIGERIAN VOICE SYNTHESIS HELPER ENGINE
# -----------------------------------------------------------------------------
def speak_text_nigerian(text: str):
    """Triggers browser text-to-speech with natural speech patterns."""
    clean_text = text.replace("'", "\\'").replace("\n", " ")
    js_code = f"""
    <script>
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance('{clean_text}');
            msg.rate = 0.95;
            msg.pitch = 1.0;
            msg.volume = 1.0;
            window.speechSynthesis.speak(msg);
        }}
    </script>
    """
    components.html(js_code, height=0, width=0)

# -----------------------------------------------------------------------------
# 4. INITIALIZE SYSTEM DATA & NAVIGATION STATE
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
        {"Product ID": "PRD-101", "Name": "Neural Processor Core", "Category": "Hardware", "Status": "In Stock", "Qty": 45, "Cost": 1200},
        {"Product ID": "PRD-102", "Name": "DI Memory Module", "Category": "Storage", "Status": "In Stock", "Qty": 120, "Cost": 350},
        {"Product ID": "PRD-103", "Name": "SkyNet Gateway Unit", "Category": "Networking", "Status": "Low Stock", "Qty": 8, "Cost": 2100},
        {"Product ID": "PRD-104", "Name": "Quantum Bus Interface", "Category": "Hardware", "Status": "In Stock", "Qty": 30, "Cost": 850},
        {"Product ID": "PRD-105", "Name": "Cryo Cooling Array", "Category": "Infrastructure", "Status": "Maintenance", "Qty": 3, "Cost": 4500},
    ]

for item in st.session_state.products:
    if "Cost" not in item:
        item["Cost"] = 500

if "audit_logs" not in st.session_state:
    st.session_state.audit_logs = [
        {"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "User": "System", "Field Changed": "Initialization", "Old Value": "None", "New Value": "Online"}
    ]

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if "last_spoken_phrase" not in st.session_state:
    # IMMEDATE WELCOME & BENEFITS AUDIO SPEECH IN NIGERIAN ACCENT
    welcome_speech = (
        "Welcome to Dacre Analysis! How far now? I am your built-in Digital Intelligence assistant, "
        "and I am always live here to help you. With this app, you can track your full inventory in real-time, "
        "manage user access, analyze system metrics, and control your entire database with voice or text commands. "
        "Just tell me where you want to go, like say take me to sign in or take me to sign up, and I will move your screen immediately!"
    )
    st.session_state.last_spoken_phrase = welcome_speech

if "messages" not in st.session_state:
    st.session_state.messages = []

if "show_verification_gate" not in st.session_state:
    st.session_state.show_verification_gate = False

if "failed_reason" not in st.session_state:
    st.session_state.failed_reason = ""

if "auth_portal_mode" not in st.session_state:
    st.session_state.auth_portal_mode = "🔑 Sign In"

if "current_dashboard_tab" not in st.session_state:
    st.session_state.current_dashboard_tab = "📊 Data Dashboard"

if "initial_loaded" not in st.session_state:
    st.session_state.initial_loaded = False

if "captcha_num1" not in st.session_state:
    st.session_state.captcha_num1 = random.randint(1, 9)
    st.session_state.captcha_num2 = random.randint(1, 9)

if "captcha_quiz_options" not in st.session_state:
    st.session_state.captcha_quiz_options = ["Quantum Server Matrix", "Nebular System Cluster", "Bot Automation Footprint", "Organic Human Operator Pro"]
    st.session_state.captcha_quiz_correct = "Organic Human Operator Pro"

# Execute automatic audio broadcast if pending
if st.session_state.last_spoken_phrase:
    speak_text_nigerian(st.session_state.last_spoken_phrase)
    st.session_state.last_spoken_phrase = None

# -----------------------------------------------------------------------------
# 5. 5-SECOND INITIAL LOAD LOADER
# -----------------------------------------------------------------------------
if not st.session_state.initial_loaded:
    loader_placeholder = st.empty()
    with loader_placeholder.container():
        st.markdown("""
            <div class="hover-loader-container">
                <div class="hover-loader"></div>
            </div>
            <p style="text-align:center; font-family:'Space Grotesk'; font-weight:600; color:#38bdf8;">
                Initializing Built-In DI Cybernetic Voice Core... (5 Seconds)
            </p>
        """, unsafe_allow_html=True)
        time.sleep(5)
    loader_placeholder.empty()
    st.session_state.initial_loaded = True
    st.rerun()

# -----------------------------------------------------------------------------
# 6. SIDEBAR BRANDING & PERMANENT DI STATUS (CANNOT BE DISABLED)
# -----------------------------------------------------------------------------
with st.sidebar:
    try:
        st.image(LOGO_PATH, use_container_width=True)
    except Exception:
        st.markdown("<div style='border:1px dashed rgba(255,255,255,0.2); padding:10px; text-align:center;'>🖼️ Brand Image Active</div>", unsafe_allow_html=True)

    st.markdown(f"### **{APP_NAME}**")
    st.caption("Sky Engine v3.5 • Built-In DI Core Live")
    st.markdown("---")

    # Built-In DI Status Monitor Card
    st.markdown("""
        <div style="background: rgba(56, 189, 248, 0.1); border: 1px solid #38bdf8; padding: 10px; border-radius: 8px;">
            <p style="margin:0; font-weight:bold; color:#38bdf8 !important;">🤖 Built-in DI Engine</p>
            <p style="margin:0; font-size: 0.85rem; color:#E0F2FE !important;">Status: 🟢 Always Active & Listening</p>
            <p style="margin:0; font-size: 0.8rem; color:#94a3b8 !important;">Accent: Nigerian English/Pidgin</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    if st.session_state.logged_in_user:
        st.success(f"Authenticated: **{st.session_state.logged_in_user.upper()}**")
        if st.button("Log Out Node System", use_container_width=True):
            st.session_state.logged_in_user = None
            st.session_state.messages = []
            st.session_state.last_spoken_phrase = "You have logged out successfully. Built-in DI is still active to help you."
            st.rerun()
    else:
        st.info("🔒 Secure Firewall Matrix Online")

# -----------------------------------------------------------------------------
# 7. SCREEN NAVIGATION ENGINE HANDLED BY DI CONTROL
# -----------------------------------------------------------------------------
def process_di_voice_command(user_text: str):
    """Parses user input to automatically navigate screens or answer queries."""
    text_lower = user_text.lower()
    
    # 1. Navigation Commands
    if "sign in" in text_lower or "login" in text_lower or "log in" in text_lower:
        st.session_state.auth_portal_mode = "🔑 Sign In"
        reply = "No wahala! I am taking you directly to the sign in page right now."
        return reply, True

    elif "sign up" in text_lower or "register" in text_lower or "create account" in text_lower:
        st.session_state.auth_portal_mode = "📝 Sign Up"
        reply = "Alright boss! Moving you to the sign up page so you can register your account."
        return reply, True

    elif "dashboard" in text_lower or "data" in text_lower or "analytics" in text_lower:
        st.session_state.current_dashboard_tab = "📊 Data Dashboard"
        reply = "Navigating to your Data Dashboard right now. Here are all your metrics."
        return reply, True

    elif "chat" in text_lower or "console" in text_lower or "di core" in text_lower:
        st.session_state.current_dashboard_tab = "🤖 DI Communication Console"
        reply = "Opening our full DI communication console now."
        return reply, True

    elif "admin" in text_lower or "audit" in text_lower:
        st.session_state.current_dashboard_tab = "🛡️ User/Org Admin Portal"
        reply = "Switching over to the Organization Admin Portal."
        return reply, True

    # 2. Sovereign Greetings
    elif any(w in text_lower for w in ["hi", "david", "master", "how are you"]):
        if st.session_state.logged_in_user and (st.session_state.logged_in_user.lower() == "david"):
            reply = "I'm fine Master David thank you and we love you sir, do you want us to do something for you sir?"
        else:
            reply = "How far my friend! I am active and ready. Ask me any question or tell me which page to move you to!"
        return reply, False

    # 3. General App Knowledge Query
    elif "benefit" in text_lower or "what can you do" in text_lower or "help" in text_lower:
        reply = (
            "Dacre Analysis gives you complete control over your enterprise inventory and data matrix! "
            "You get real-time chart visualizers, security audit logs, and my built-in voice assistance "
            "that moves your screens automatically whenever you command me!"
        )
        return reply, False

    else:
        reply = f"I hear you loud and clear! You said: '{user_text}'. I have processed your request."
        return reply, False

# -----------------------------------------------------------------------------
# 8. PERMANENT TOP-LEVEL DI INTERACTION BAR
# -----------------------------------------------------------------------------
st.markdown('<div class="hero-title">DACRE ANALYSIS & CONTROL CENTER</div>', unsafe_allow_html=True)

with st.container():
    st.markdown("""
        <div class="di-status-card">
            <h4 style="margin:0; color:#38bdf8;">🤖 Built-in DI Screen Navigation & Assistance</h4>
            <p style="margin:5px 0 0 0; font-size:0.9rem; color:#cbd5e1;">
                Speak or type any command (e.g., <i>"Take me to sign in"</i>, <i>"Take me to sign up"</i>, or <i>"Show me data dashboard"</i>) 
                and your built-in DI will automatically move your screen!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        di_direct_cmd = st.text_input("Talk to your Built-in DI (Command or Question):", key="di_top_bar_cmd", placeholder="e.g. Please take me to the sign up page...")
    with col_btn:
        st.write(" ")
        st.write(" ")
        submit_cmd = st.button("🗣️ Issue Command")

    if submit_cmd and di_direct_cmd:
        reply_msg, should_rerun = process_di_voice_command(di_direct_cmd)
        st.session_state.messages.append({"role": "user", "content": di_direct_cmd})
        st.session_state.messages.append({"role": "assistant", "content": reply_msg})
        st.session_state.last_spoken_phrase = reply_msg
        if should_rerun:
            st.rerun()
        else:
            speak_text_nigerian(reply_msg)

# -----------------------------------------------------------------------------
# 9. RECAPTCHA GATEWAY (ONLY TRIGGERED UPON FAILED LOGIN/SIGNUP)
# -----------------------------------------------------------------------------
if st.session_state.show_verification_gate:
    st.markdown("""
        <style>
        [data-testid="stSidebar"] { display: none !important; }
        </style>
    """, unsafe_allow_html=True)

    st.error("🚨 SECURITY VERIFICATION REQUIRED")
    st.markdown(f"### Reason: {st.session_state.failed_reason}")
    st.write("Complete human verification challenge to clear firewall locks:")
    
    expected_ans = st.session_state.captcha_num1 + st.session_state.captcha_num2
    st.markdown(f"Solve math validation: **{st.session_state.captcha_num1} + {st.session_state.captcha_num2} = ?**")
    user_math_ans = st.number_input("Enter Sum Result:", min_value=0, max_value=100, step=1)

    st.write("---")
    st.write(f"Target Token Match: **{st.session_state.captcha_quiz_correct.upper()}**")
    user_selected_ans = st.radio("Select verified response token:", st.session_state.captcha_quiz_options)

    if st.button("Verify & Authorize Gate Clearance", use_container_width=True):
        if user_math_ans == expected_ans and user_selected_ans == st.session_state.captcha_quiz_correct:
            st.session_state.show_verification_gate = False
            st.session_state.failed_reason = ""
            st.session_state.captcha_num1 = random.randint(1, 9)
            st.session_state.captcha_num2 = random.randint(1, 9)
            st.session_state.last_spoken_phrase = "Verification successful! Access has been restored."
            st.success("Verification complete. Access restored.")
            st.rerun()
        else:
            st.error("Verification parameters mismatched. Challenge re-indexed.")
            st.session_state.captcha_num1 = random.randint(1, 9)
            st.session_state.captcha_num2 = random.randint(1, 9)
            st.session_state.captcha_quiz_options = random.sample(["Quantum Server Matrix", "Nebular System Cluster", "Bot Automation Footprint", "Organic Human Operator Pro"], 4)
            st.session_state.captcha_quiz_correct = "Organic Human Operator Pro"
            st.rerun()

# -----------------------------------------------------------------------------
# 10. SIGN IN / SIGN UP PORTAL
# -----------------------------------------------------------------------------
elif not st.session_state.logged_in_user:
    st.markdown("---")
    
    # Controlled dynamically by state or user click
    st.session_state.auth_portal_mode = st.radio(
        "Select Portal Action", 
        ["🔑 Sign In", "📝 Sign Up"], 
        index=0 if st.session_state.auth_portal_mode == "🔑 Sign In" else 1,
        horizontal=True
    )

    if st.session_state.auth_portal_mode == "🔑 Sign In":
        st.subheader("Account Login")
        login_user = st.text_input("Username", placeholder="Enter username...", key="l_user")
        login_pass = st.text_input("Password", placeholder="Enter password...", type="password", key="l_pass")
        
        if st.button("Sign In", use_container_width=True):
            if login_user in st.session_state.users and st.session_state.users[login_user]["password"] == login_pass:
                st.session_state.logged_in_user = login_user
                if st.session_state.users[login_user]["role"] == "master":
                    st.session_state.last_spoken_phrase = "Welcome back, Master David. All sovereign admin control channels are operational."
                else:
                    st.session_state.last_spoken_phrase = f"Welcome back, operator {login_user}! Your system environment is fully online."
                st.success("Welcome back!")
                st.rerun()
            else:
                st.session_state.show_verification_gate = True
                st.session_state.failed_reason = "Invalid credentials provided."
                st.session_state.last_spoken_phrase = "Incorrect login details! Security verification required now."
                st.rerun()

    else:
        st.subheader("Create Account")
        new_user = st.text_input("Choose Username", key="s_user")
        new_pass = st.text_input("Choose Password", type="password", key="s_pass")
        custom_di_name = st.text_input("Name Your Built-in DI Entity", value=f"DI-{random.randint(100, 999)}")

        if st.button("Create Account", use_container_width=True):
            if not new_user or not new_pass:
                st.warning("Please fill out all mandatory fields.")
            elif new_user in st.session_state.users:
                st.session_state.show_verification_gate = True
                st.session_state.failed_reason = f"Username '{new_user}' already exists in system memory."
                st.session_state.last_spoken_phrase = "That username already exists! Please complete verification."
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

                st.session_state.last_spoken_phrase = f"Account created successfully! Welcome aboard operator {new_user}. Your built-in DI {custom_di_name} is active."
                st.session_state.logged_in_user = new_user
                st.rerun()

# -----------------------------------------------------------------------------
# 11. LOGGED-IN MAIN WORKSPACE & DASHBOARD
# -----------------------------------------------------------------------------
else:
    user = st.session_state.logged_in_user
    user_info = st.session_state.users[user]
    is_master = (user.lower() == "david" or user_info.get("role") == "master")

    nav_tabs = ["📊 Data Dashboard", "🤖 DI Communication Console", "🛡️ User/Org Admin Portal"]
    if is_master:
        nav_tabs.append("👑 Master Executive Portal")

    # Sync selection with voice navigation state
    try:
        tab_index = nav_tabs.index(st.session_state.current_dashboard_tab)
    except ValueError:
        tab_index = 0

    st.session_state.current_dashboard_tab = st.radio("System Mode", nav_tabs, index=tab_index, horizontal=True)
    st.markdown("---")

    # TAB 1: DATA DASHBOARD
    if st.session_state.current_dashboard_tab == "📊 Data Dashboard":
        st.subheader("📊 DACRE Data Analytics Board")
        st.write("Real-time operational metrics, resource tracking, and infrastructure allocation.")

        df_products = pd.DataFrame(st.session_state.products)
        if "Cost" not in df_products.columns:
            df_products["Cost"] = 0

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Items Managed", len(df_products))
        m2.metric("Total Units Inventory", int(df_products["Qty"].sum()))
        
        total_val = (df_products['Qty'] * df_products['Cost']).sum()
        m3.metric("System Asset Value", f"${total_val:,}")
        m4.metric("Active System Users", len(st.session_state.users))

        st.markdown("---")

        c_left, c_right = st.columns(2)
        with c_left:
            st.subheader("📦 Inventory Status Breakdown")
            status_counts = df_products["Status"].value_counts()
            st.bar_chart(status_counts)

        with c_right:
            st.subheader("⚙️ Stock Quantities per Product")
            st.line_chart(df_products.set_index("Name")["Qty"])

        st.markdown("---")
        st.subheader("📋 Resource Detail Board")
        st.dataframe(df_products, use_container_width=True)

    # TAB 2: COMMUNICATION CONSOLE
    elif st.session_state.current_dashboard_tab == "🤖 DI Communication Console":
        st.subheader(f"🤖 {user_info['di_name']} Deep Interaction Console")
        st.write(f"Connected User: **{user}** | Built-in Nigerian Audio Core Active")

        c1, c2 = st.columns([3, 1])

        with c1:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

            user_input = st.chat_input("Ask your Built-in DI anything or command a page move...")

            if user_input:
                st.session_state.messages.append({"role": "user", "content": user_input})
                with st.chat_message("user"):
                    st.write(user_input)

                response_text, should_rerun = process_di_voice_command(user_input)

                with st.chat_message("assistant"):
                    st.write(response_text)
                    speak_text_nigerian(response_text)

                st.session_state.messages.append({"role": "assistant", "content": response_text})
                if should_rerun:
                    st.rerun()

        with c2:
            st.markdown("#### **Built-in DI Specs**")
            st.write(f"**Entity Name:** {user_info['di_name']}")
            st.write(f"**Assigned User:** {user}")
            st.write(f"**State:** 🟢 Permanent Built-in")
            if st.button("🔊 Replay Voice Response"):
                if st.session_state.messages:
                    speak_text_nigerian(st.session_state.messages[-1]["content"])

    # TAB 3: ADMIN ACCESS
    elif st.session_state.current_dashboard_tab == "🛡️ User/Org Admin Portal":
        st.subheader("🛡️ Organization Admin Access")
        st.write("Manage inventory, modify properties, and track system logs.")

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
                        st.session_state.last_spoken_phrase = f"Status for {selected_prod} updated successfully to {new_status}!"
                        st.success(f"Updated {selected_prod} status to '{new_status}'!")
                        st.rerun()

            st.markdown("---")
            st.subheader("📜 Data Change Audit Logs")
            st.dataframe(pd.DataFrame(st.session_state.audit_logs), use_container_width=True)

        else:
            st.info("🔑 Passkey required to unlock admin functions. Default passkey: `admin123`")

    # TAB 4: MASTER PORTAL
    elif st.session_state.current_dashboard_tab == "👑 Master Executive Portal" and is_master:
        st.subheader("👑 Master Executive Portal")
        st.write("Full Authority Portal • Sovereign Control Center")

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
                speak_text_nigerian(reply)

        st.markdown("---")
        st.subheader("📋 Enrolled DI Registry")
        st.dataframe(pd.DataFrame(st.session_state.enrolled_dis), use_container_width=True)
