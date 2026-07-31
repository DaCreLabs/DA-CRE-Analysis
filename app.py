import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import time
from datetime import datetime
from PIL import Image

# -----------------------------------------------------------------------------
# 1. APP CONFIGURATION & FAVICON LOGO SETUP
# -----------------------------------------------------------------------------
APP_NAME = "Dacre Analysis Engine"
MASTER_FULL_NAME = "David Emenike"
MASTER_PASSKEY = "theWORDofGOD@111"
LOGO_PATH = "ChatGPT Image Jul 29, 2026, 02_27_41 PM.png"

try:
    logo_img = Image.open(LOGO_PATH)
    st.set_page_config(
        page_title=f"{APP_NAME} | Autonomous DI Platform",
        page_icon=logo_img,
        layout="wide",
        initial_sidebar_state="expanded"
    )
except Exception:
    st.set_page_config(
        page_title=f"{APP_NAME} | Autonomous DI Platform",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# -----------------------------------------------------------------------------
# 2. ULTRA-BOLD HIGH VISIBILITY THEME
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    /* Force ABSOLUTELY ALL TEXT to be Ultra-Bold and Sharp White/Blue */
    * {
        font-weight: 900 !important;
        -webkit-font-smoothing: antialiased;
    }
    
    html, body, [class*="st-"], p, span, div, label, h1, h2, h3, h4, h5, h6, input, button, select, textarea, table, th, td {
        font-weight: 900 !important;
        color: #ffffff !important;
    }

    /* Global Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #0b1329 0%, #101d36 50%, #1a2942 100%) !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #090e1a 0%, #111a2e 100%) !important;
        border-right: 2.5px solid #38bdf8 !important;
    }

    [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #f8fafc !important;
        font-weight: 900 !important;
    }

    /* Hero Header Title */
    .hero-title {
        background: linear-gradient(90deg, #38bdf8 0%, #f59e0b 50%, #60a5fa 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.6rem;
        font-weight: 900 !important;
        letter-spacing: 1.2px;
        margin-bottom: 0.5rem;
        animation: shine 4s linear infinite;
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    /* Input Fields */
    .stTextInput input, .stNumberInput input, .stSelectbox div {
        background-color: #1e293b !important;
        color: #ffffff !important;
        font-weight: 900 !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 8px !important;
    }

    /* Form Labels High Visibility */
    label, [data-testid="stWidgetLabel"] p {
        font-size: 1.1rem !important;
        font-weight: 900 !important;
        color: #38bdf8 !important;
    }

    /* High Visibility Glowing Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #0284c7 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: 900 !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.4) !important;
        transition: all 0.3s ease !important;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(56, 189, 248, 0.8) !important;
    }

    /* Dark Theme Card strictly for Presentation Slides */
    .presentation-card {
        background: rgba(15, 23, 42, 0.95) !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 16px !important;
        padding: 35px !important;
        min-height: 400px !important;
        box-shadow: 0 0 30px rgba(56, 189, 248, 0.3) !important;
        animation: fadeIn 0.6s ease-in-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. FAST DIRECT SPEECH SYNTHESIS ENGINE
# -----------------------------------------------------------------------------
def speak_now(text: str):
    """Executes immediate browser TTS and notifies speech receiver when done."""
    clean_text = text.replace("'", "\\'").replace("\n", " ")
    js_code = f"""
    <script>
        (function() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance('{clean_text}');
                msg.rate = 1.15;
                msg.pitch = 1.0;
                msg.volume = 1.0;
                
                // Let the recognition system know when Di is talking
                window.parent.isDiSpeaking = true;
                
                msg.onend = function() {{
                    window.parent.isDiSpeaking = false;
                }};
                
                window.speechSynthesis.speak(msg);
            }}
        }})();
    </script>
    """
    components.html(js_code, height=0, width=0)

# -----------------------------------------------------------------------------
# 4. INITIALIZE SESSION STATES
# -----------------------------------------------------------------------------
if "db_users" not in st.session_state:
    st.session_state.db_users = {
        "david": {"password": "123", "full_name": MASTER_FULL_NAME, "role": "master"}
    }

if "user_datasets" not in st.session_state:
    default_df = pd.DataFrame([
        {"Product ID": "PRD-101", "Name": "Neural Processor Core", "Category": "Hardware", "Status": "In Stock", "Qty": 85, "Cost": 1200, "Sales": 450},
        {"Product ID": "PRD-102", "Name": "DI Memory Module", "Category": "Storage", "Status": "In Stock", "Qty": 140, "Cost": 350, "Sales": 920},
        {"Product ID": "PRD-103", "Name": "SkyNet Gateway Unit", "Category": "Networking", "Status": "Low Stock", "Qty": 6, "Cost": 2100, "Sales": 110},
        {"Product ID": "PRD-104", "Name": "Quantum Bus Interface", "Category": "Hardware", "Status": "In Stock", "Qty": 50, "Cost": 850, "Sales": 380},
        {"Product ID": "PRD-105", "Name": "Cryo Cooling Array", "Category": "Infrastructure", "Status": "Maintenance", "Qty": 2, "Cost": 4500, "Sales": 40},
    ])
    st.session_state.user_datasets = {"default": default_df}

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if "is_master_authenticated" not in st.session_state:
    st.session_state.is_master_authenticated = False

if "last_di_speech" not in st.session_state:
    st.session_state.last_di_speech = None

if "has_greeted_on_load" not in st.session_state:
    st.session_state.has_greeted_on_load = False

if "current_nav_page" not in st.session_state:
    st.session_state.current_nav_page = "📊 Workflow Dashboard"

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "🔑 Sign In"

# Trigger startup greeting immediately on load
if not st.session_state.logged_in_user and not st.session_state.has_greeted_on_load:
    st.session_state.last_di_speech = "Good day user! How are you doing today? Please sign in or sign up for us to start work."
    st.session_state.has_greeted_on_load = True

# Execute speech immediately when queued
if st.session_state.last_di_speech:
    speak_now(st.session_state.last_di_speech)
    st.session_state.last_di_speech = None

def get_current_df():
    u = st.session_state.logged_in_user or "default"
    if u not in st.session_state.user_datasets:
        st.session_state.user_datasets[u] = st.session_state.user_datasets["default"].copy()
    return st.session_state.user_datasets[u]

def save_current_df(df):
    u = st.session_state.logged_in_user or "default"
    st.session_state.user_datasets[u] = df.copy()

# -----------------------------------------------------------------------------
# 5. HUMAN-LIKE FAST VERBAL ROUTER
# -----------------------------------------------------------------------------
def process_verbal_interaction(speech_input: str):
    """Processes spoken inputs, routes screens, and prepares spoken responses."""
    q = speech_input.lower().strip()
    
    # Navigation Commands
    if "where do i sign up" in q or "where is sign up" in q or "take me to sign up" in q or "sign up" in q:
        st.session_state.auth_mode = "📝 Sign Up"
        return "I am directing you right now. I have opened the Sign Up portal. Please enter your desired username, password, and full name to register."
    
    elif "where do i sign in" in q or "take me to sign in" in q or "sign in" in q or "login" in q:
        st.session_state.auth_mode = "🔑 Sign In"
        return "Directing you to the Sign In portal. Please enter your credentials to log in."

    elif "hello" in q or "hi" in q or "how are you" in q:
        user_ref = st.session_state.logged_in_user if st.session_state.logged_in_user else "user"
        return f"Hello {user_ref}! I am doing great and listening. What should we work on next?"
    elif "dashboard" in q or "workflow" in q:
        st.session_state.current_nav_page = "📊 Workflow Dashboard"
        return "Switched to Workflow Dashboard instantly. What dataset operations shall we run?"
    elif "preview" in q or "print" in q:
        st.session_state.current_nav_page = "📋 Data Preview & Print"
        return "Opened Data Preview. Do you want to download clean CSV or print out reports?"
    elif "presentation" in q or "slide" in q:
        st.session_state.current_nav_page = "📈 Customize Data & Analytics"
        return "Presentation Hub ready. Would you like me to start the presentation?"
    elif "who are you" in q or "master" in q:
        return f"I am your Dacre Assistant operating for Master {MASTER_FULL_NAME}. How can I assist you?"
    else:
        return f"I heard you say: {speech_input}. How would you like me to process this?"

# -----------------------------------------------------------------------------
# 6. HEADER & SIDEBAR LOGO
# -----------------------------------------------------------------------------
st.markdown('<div class="hero-title">DACRE AUTONOMOUS DATA ENGINE</div>', unsafe_allow_html=True)

with st.sidebar:
    try:
        st.image(LOGO_PATH, use_container_width=True)
    except Exception:
        pass

    st.markdown(f"### **{APP_NAME}**")
    st.caption("**Bold Voice Dialogue Mode Active**")
    st.markdown("---")

    if st.session_state.logged_in_user:
        st.success(f"**Active User: {st.session_state.logged_in_user}**")
        if st.button("Log Out Session", use_container_width=True):
            st.session_state.logged_in_user = None
            st.session_state.is_master_authenticated = False
            st.session_state.has_greeted_on_load = False
            st.session_state.last_di_speech = "Logged out successfully. Have a great day!"
            st.rerun()

# -----------------------------------------------------------------------------
# CONTINUOUS SPEECH LISTENER & FAST RESPONDER
# -----------------------------------------------------------------------------
speech_receiver_code = """
<div style="background: rgba(15, 23, 42, 0.9); border: 2.5px solid #38bdf8; padding: 12px; border-radius: 10px; margin-bottom: 12px;">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="color:#38bdf8; font-weight:900; font-size:1.15rem;">🎙️ DI Voice Interaction active</span>
        <span style="color:#10b981; font-weight:900; font-size:1.15rem;" id="mic-status">🟢 Hearing You Live...</span>
    </div>
</div>

<script>
window.parent.isDiSpeaking = window.parent.isDiSpeaking || false;

window.addEventListener('DOMContentLoaded', (event) => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onresult = (event) => {
            // Ignore speech recognition while Di is speaking back to user
            if (window.parent.isDiSpeaking) return;

            const transcript = event.results[event.results.length - 1][0].transcript.trim();
            if (!transcript) return;

            const inputs = window.parent.document.querySelectorAll('input[type="text"]');
            if (inputs.length > 0) {
                inputs[0].value = transcript;
                inputs[0].dispatchEvent(new Event('input', { bubbles: true }));
                
                // Immediately trigger response action
                setTimeout(() => {
                    const btns = window.parent.document.querySelectorAll('button');
                    for (let b of btns) {
                        if (b.innerText.includes("Respond") || b.innerText.includes("Execute") || b.innerText.includes("Ask")) {
                            b.click();
                            break;
                        }
                    }
                }, 150);
            }
        };

        recognition.onend = () => { 
            // Continuously restart listening immediately
            try { recognition.start(); } catch(e) {} 
        };

        try { recognition.start(); } catch(e) {}
    }
});
</script>
"""
components.html(speech_receiver_code, height=65)

# Input Command Bar
c_input, c_btn = st.columns([5, 1])
with c_input:
    user_speech_val = st.text_input("Voice Input Command:", key="live_voice_bar", placeholder="Speak verbally to talk directly with Di...")
with c_btn:
    st.write(" ")
    st.write(" ")
    if st.button("⚡ Respond / Execute", use_container_width=True):
        if user_speech_val:
            verbal_reply = process_verbal_interaction(user_speech_val)
            st.session_state.last_di_speech = verbal_reply
            st.rerun()

# -----------------------------------------------------------------------------
# 7. AUTHENTICATION PORTAL (ADDRESSES USERNAME ON SIGN UP)
# -----------------------------------------------------------------------------
if not st.session_state.logged_in_user:
    st.markdown("---")
    modes = ["🔑 Sign In", "📝 Sign Up"]
    st.session_state.auth_mode = st.radio("Access Portal", modes, index=modes.index(st.session_state.auth_mode), horizontal=True)

    if st.session_state.auth_mode == "🔑 Sign In":
        st.subheader("🔑 Sign In Portal")
        c1, c2 = st.columns(2)
        with c1:
            u_name = st.text_input("Username", key="login_username")
            u_pass = st.text_input("Password", type="password", key="login_password")
            if st.button("Sign In", use_container_width=True):
                if u_name in st.session_state.db_users and st.session_state.db_users[u_name]["password"] == u_pass:
                    st.session_state.logged_in_user = u_name
                    st.session_state.last_di_speech = f"Welcome back {u_name}! What task would you like to execute today?"
                    st.rerun()
                else:
                    st.error("Invalid Credentials.")

    else:
        st.subheader("📝 Sign Up Portal")
        c1, c2 = st.columns(2)
        with c1:
            new_u = st.text_input("Choose Username", key="reg_username")
            new_p = st.text_input("Choose Password", type="password", key="reg_password")
            new_full = st.text_input("Full Name", key="reg_fullname")
            if st.button("Create Account", use_container_width=True):
                if new_u and new_p:
                    st.session_state.db_users[new_u] = {"password": new_p, "full_name": new_full, "role": "user"}
                    st.session_state.logged_in_user = new_u
                    st.session_state.last_di_speech = f"Account created successfully! Welcome {new_u}. How can I assist your work today?"
                    st.rerun()

# -----------------------------------------------------------------------------
# 8. MAIN WORKSPACE ENGINE
# -----------------------------------------------------------------------------
else:
    pages = ["📊 Workflow Dashboard", "📋 Data Preview & Print", "📈 Customize Data & Analytics", "🛡️ Master Admin Portal"]
    st.session_state.current_nav_page = st.radio("Navigation Hub", pages, index=pages.index(st.session_state.current_nav_page), horizontal=True)
    st.markdown("---")

    current_df = get_current_df()

    # TAB 1: WORKFLOW DASHBOARD
    if st.session_state.current_nav_page == "📊 Workflow Dashboard":
        st.subheader("📂 Collect Local Data File")
        uploaded_file = st.file_uploader("Collect Data Bar (CSV or Excel)", type=["csv", "xlsx"])

        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith(".csv"):
                    imported_df = pd.read_csv(uploaded_file)
                else:
                    imported_df = pd.read_excel(uploaded_file)
                save_current_df(imported_df)
                st.session_state.last_di_speech = f"File {uploaded_file.name} imported successfully! What visualization or calculation do you want to perform?"
                st.success("File imported and synchronized across Workflow and Preview!")
                st.rerun()
            except Exception as e:
                st.error(f"Error loading file: {e}")

        st.markdown("---")
        st.subheader("📊 Interactive Data Grid Workflow")

        t_col1, t_col2, t_col3, t_col4 = st.columns(4)
        with t_col1:
            if st.button("🧹 Remove Duplicates", use_container_width=True):
                df_clean = current_df.drop_duplicates()
                save_current_df(df_clean)
                st.session_state.last_di_speech = "Duplicates removed instantly. What next?"
                st.rerun()
        with t_col2:
            target_col = st.selectbox("Select Sort Target", current_df.columns)
        with t_col3:
            if st.button("🔤 Sort A-Z", use_container_width=True):
                df_sorted = current_df.sort_values(by=target_col, ascending=True)
                save_current_df(df_sorted)
                st.rerun()
        with t_col4:
            if st.button("🔠 Sort Z-A", use_container_width=True):
                df_sorted = current_df.sort_values(by=target_col, ascending=False)
                save_current_df(df_sorted)
                st.rerun()

        st.markdown("---")
        st.write("**Direct Data Grid Editor:**")
        edited_df = st.data_editor(current_df, num_rows="dynamic", use_container_width=True)
        if st.button("💾 Save Grid Edits", use_container_width=True):
            save_current_df(edited_df)
            st.session_state.last_di_speech = "Grid modifications saved."
            st.success("Workflow saved!")

    # TAB 2: DATA PREVIEW & PRINT
    elif st.session_state.current_nav_page == "📋 Data Preview & Print":
        st.subheader("📋 Synchronized Read-Only Data Preview")
        st.dataframe(current_df, use_container_width=True)

        p_col1, p_col2 = st.columns(2)
        with p_col1:
            csv_data = current_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Clean CSV File",
                data=csv_data,
                file_name=f"dacre_export_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        with p_col2:
            if st.button("🖨️ Print Data Report", use_container_width=True):
                components.html("<script>window.print();</script>", height=0)

    # TAB 3: CUSTOMIZE DATA & ANALYTICS
    elif st.session_state.current_nav_page == "📈 Customize Data & Analytics":
        st.subheader("📈 Business Analyst Reports & Presentation Engine")

        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["📊 Data Report", "🎨 Dynamic Charts", "🎬 Do Presentation (Dark Mode)"])

        with sub_tab1:
            if st.button("🚀 Generate Data Report", use_container_width=True):
                num_df = current_df.select_dtypes(include=[np.number])
                st.write(f"**Total Record Volume:** {len(current_df)}")
                if not num_df.empty:
                    st.dataframe(num_df.describe(), use_container_width=True)
                
                resp = f"Analysis generated. Total dataset items: {len(current_df)}. Would you like to launch the presentation slides?"
                st.info(resp)
                speak_now(resp)

        with sub_tab2:
            chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Line Chart", "Area Chart"])
            c_cols = current_df.columns.tolist()
            x_var = st.selectbox("X-Axis Parameter", c_cols, index=0)
            y_var = st.selectbox("Y-Axis Parameter", current_df.select_dtypes(include=[np.number]).columns.tolist(), index=0)

            if st.button("Render Chart", use_container_width=True):
                chart_df = current_df.set_index(x_var)[y_var]
                if chart_type == "Bar Chart":
                    st.bar_chart(chart_df)
                elif chart_type == "Line Chart":
                    st.line_chart(chart_df)
                elif chart_type == "Area Chart":
                    st.area_chart(chart_df)

        with sub_tab3:
            st.markdown("#### 🎬 Dedicated Dark Theme Dynamic Presentation Engine")
            if st.button("▶️ Launch Presentation", use_container_width=True):
                slides = [
                    {"title": "Slide 1: Executive Overview", "body": f"Master dataset contains {len(current_df)} record items.", "speech": f"Welcome {st.session_state.logged_in_user} to your executive presentation. What metric shall we focus on?"},
                    {"title": "Slide 2: Stock Dynamics", "body": "Analyzing stock stability and sales output across categories.", "speech": "Slide two presents inventory stability and sales distribution."},
                    {"title": "Slide 3: Strategic Recommendations", "body": "Replenish low stock items and prioritize top revenue generators.", "speech": "Slide three details strategic restock priorities. Shall I answer any questions on this data?"}
                ]

                for slide in slides:
                    st.markdown(f"""
                        <div class="presentation-card">
                            <h2 style="color:#38bdf8;">{slide['title']}</h2>
                            <hr style="border-color:#38bdf8;">
                            <p style="font-size:1.3rem; color:#ffffff; font-weight:900; margin-top:20px;">{slide['body']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    speak_now(slide['speech'])
                    time.sleep(4)

    # TAB 4: MASTER ADMIN PORTAL
    elif st.session_state.current_nav_page == "🛡️ Master Admin Portal":
        st.subheader("🛡️ Master Admin Security Portal")
        
        if not st.session_state.is_master_authenticated:
            passkey_in = st.text_input("Enter Passkey:", type="password")
            if st.button("Authenticate Master", use_container_width=True):
                if passkey_in == MASTER_PASSKEY:
                    st.session_state.is_master_authenticated = True
                    st.session_state.last_di_speech = f"Master {MASTER_FULL_NAME} authorized. All core directives operational."
                    st.success(f"Authenticated Master: {MASTER_FULL_NAME}")
                    st.rerun()
                else:
                    st.error("Invalid Security Passkey.")
        else:
            st.success(f"👑 Verified Sovereign Master: **{MASTER_FULL_NAME}**")
            st.json(st.session_state.db_users)
