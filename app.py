import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import time
from datetime import datetime
from PIL import Image

# -----------------------------------------------------------------------------
# 1. APP CONFIGURATION & LOGO SETUP
# -----------------------------------------------------------------------------
APP_NAME = "Dacre Analysis Engine"
MASTER_FULL_NAME = "David Emenike"
MASTER_PASSKEY = "theWORDofGOD@111"
LOGO_PATH = "ChatGPT Image Jul 29, 2026, 02_27_41 PM.png"

# Load Logo for Favicon Icon
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
# 2. STYLING: STANDARD UI/UX FOR MAIN APP; DARK THEME ONLY FOR PRESENTATION
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    /* Dark Theme restricted EXCLUSIVELY to Presentation Slide Cards */
    .presentation-dark-card {
        background: radial-gradient(ellipse at bottom, #090d16 0%, #020408 100%) !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 14px !important;
        padding: 30px !important;
        min-height: 400px !important;
        color: #ffffff !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.25) !important;
    }
    
    .presentation-dark-card h2 {
        color: #38bdf8 !important;
    }
    
    .presentation-dark-card p {
        color: #f0f9ff !important;
        font-size: 1.25rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. FAST DIRECT SPEECH SYNTHESIS ENGINE
# -----------------------------------------------------------------------------
def speak_direct_response(text: str):
    """Answers user queries directly via speech without recording voice data."""
    clean_text = text.replace("'", "\\'").replace("\n", " ")
    js_code = f"""
    <script>
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance('{clean_text}');
            msg.rate = 1.15;
            msg.pitch = 1.0;
            window.speechSynthesis.speak(msg);
        }}
    </script>
    """
    components.html(js_code, height=0, width=0)

# -----------------------------------------------------------------------------
# 4. STATE PERSISTENCE INITIALIZATION
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

if "last_direct_speech" not in st.session_state:
    st.session_state.last_direct_speech = None

if "current_nav_page" not in st.session_state:
    st.session_state.current_nav_page = "📊 Workflow Dashboard"

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "🔑 Sign In"

# Trigger direct spoken response if pending
if st.session_state.last_direct_speech:
    speak_direct_response(st.session_state.last_direct_speech)
    st.session_state.last_direct_speech = None

def get_current_df():
    u = st.session_state.logged_in_user or "default"
    if u not in st.session_state.user_datasets:
        st.session_state.user_datasets[u] = st.session_state.user_datasets["default"].copy()
    return st.session_state.user_datasets[u]

def save_current_df(df):
    u = st.session_state.logged_in_user or "default"
    st.session_state.user_datasets[u] = df.copy()

# -----------------------------------------------------------------------------
# 5. DI DIRECT ANSWER & SHARP QUESTION ENGINE (NO RECORDING)
# -----------------------------------------------------------------------------
def respond_directly_and_ask(user_query: str):
    """Processes query instantly and asks sharp clarifying follow-ups without recording session logs."""
    q = user_query.lower().strip()
    
    if "hello" in q or "hi" in q:
        return "Hello! I am ready. Would you like me to process your dataset, switch pages, or generate a visual report right now?"
    elif "dashboard" in q or "workflow" in q:
        st.session_state.current_nav_page = "📊 Workflow Dashboard"
        return "Opened Workflow Dashboard immediately. What specific data row or column do you want to analyze next?"
    elif "preview" in q or "print" in q:
        st.session_state.current_nav_page = "📋 Data Preview & Print"
        return "Switched to Data Preview. Shall I generate a downloadable CSV file or trigger document print?"
    elif "presentation" in q or "slide" in q:
        st.session_state.current_nav_page = "📈 Customize Data & Analytics"
        return "Presentation engine ready in Dark Theme mode. Would you like to launch the automated speech slides now?"
    elif "who are you" in q or "master" in q:
        return f"I am the Dacre Autonomous DI Assistant working for {MASTER_FULL_NAME}. What command shall I execute for you now?"
    else:
        return f"Direct Answer: Processing command '{user_query}'. Which analytical transformation should I execute next?"

# -----------------------------------------------------------------------------
# 6. HEADER & SIDEBAR WITH LOGO
# -----------------------------------------------------------------------------
st.title("DACRE AUTONOMOUS DATA ENGINE")

with st.sidebar:
    # Render Logo Image directly in Sidebar
    try:
        st.image(LOGO_PATH, use_container_width=True)
    except Exception:
        st.info("Logo File: Ensure file exists as named in your repo.")

    st.markdown(f"### **{APP_NAME}**")
    st.caption("Sharp Direct-Response Speech Engine")
    st.markdown("---")

    if st.session_state.logged_in_user:
        st.success(f"Active User: **{st.session_state.logged_in_user}**")
        if st.button("Log Out", use_container_width=True):
            st.session_state.logged_in_user = None
            st.session_state.is_master_authenticated = False
            st.session_state.last_direct_speech = "Logged out successfully."
            st.rerun()

# Instant Mic Auto-Listener Widget (Translates speech to quick action without saving speech logs)
mic_widget_html = """
<div style="padding: 6px 0px; margin-bottom: 10px;">
    <span style="font-weight:bold; color:#0284c7;">🎙️ DI Direct Speech Active (Instant Query Answer Mode)</span>
</div>

<script>
window.addEventListener('DOMContentLoaded', (event) => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onresult = (event) => {
            const transcript = event.results[event.results.length - 1][0].transcript.trim();
            const inputElements = window.parent.document.querySelectorAll('input[type="text"]');
            if (inputElements.length > 0) {
                inputElements[0].value = transcript;
                inputElements[0].dispatchEvent(new Event('input', { bubbles: true }));
            }
        };

        recognition.onend = () => { recognition.start(); };
        recognition.start();
    }
});
</script>
"""
components.html(mic_widget_html, height=40)

# Quick Action Command Line
col_cmd, col_act = st.columns([5, 1])
with col_cmd:
    voice_query = st.text_input("Ask DI Question or Command:", key="voice_stream_input", placeholder="Speak or type query...")
with col_act:
    st.write(" ")
    st.write(" ")
    if st.button("⚡ Ask / Execute", use_container_width=True):
        if voice_query:
            answer = respond_directly_and_ask(voice_query)
            st.session_state.last_direct_speech = answer
            st.rerun()

# -----------------------------------------------------------------------------
# 7. AUTHENTICATION PORTAL
# -----------------------------------------------------------------------------
if not st.session_state.logged_in_user:
    st.markdown("---")
    st.session_state.auth_mode = st.radio("Access Portal", ["🔑 Sign In", "📝 Sign Up"], horizontal=True)

    if st.session_state.auth_mode == "🔑 Sign In":
        c1, c2 = st.columns(2)
        with c1:
            u_name = st.text_input("Username", key="login_username")
            u_pass = st.text_input("Password", type="password", key="login_password")
            if st.button("Sign In", use_container_width=True):
                if u_name in st.session_state.db_users and st.session_state.db_users[u_name]["password"] == u_pass:
                    st.session_state.logged_in_user = u_name
                    st.session_state.last_direct_speech = f"Sign in successful. Welcome {u_name}! What data task would you like to perform now?"
                    st.rerun()
                else:
                    st.error("Invalid Credentials.")

    else:
        c1, c2 = st.columns(2)
        with c1:
            new_u = st.text_input("Choose Username", key="reg_username")
            new_p = st.text_input("Choose Password", type="password", key="reg_password")
            new_full = st.text_input("Full Name", key="reg_fullname")
            if st.button("Create Account", use_container_width=True):
                if new_u and new_p:
                    st.session_state.db_users[new_u] = {"password": new_p, "full_name": new_full, "role": "user"}
                    st.session_state.logged_in_user = new_u
                    st.session_state.last_direct_speech = f"Account created! Welcome {new_u}. How may I assist your analysis?"
                    st.rerun()

# -----------------------------------------------------------------------------
# 8. MAIN WORKSPACE
# -----------------------------------------------------------------------------
else:
    pages = ["📊 Workflow Dashboard", "📋 Data Preview & Print", "📈 Customize Data & Analytics", "🛡️ Master Admin Portal"]
    st.session_state.current_nav_page = st.radio("Navigation Hub", pages, index=pages.index(st.session_state.current_nav_page), horizontal=True)
    st.markdown("---")

    current_df = get_current_df()

    # -------------------------------------------------------------------------
    # TAB 1: WORKFLOW DASHBOARD
    # -------------------------------------------------------------------------
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
                st.session_state.last_direct_speech = f"Data collected successfully from {uploaded_file.name}. What chart or calculation do you want to build with this dataset?"
                st.success("File imported and synchronized!")
                st.rerun()
            except Exception as e:
                st.error(f"Error loading file: {e}")

        st.markdown("---")
        st.subheader("📊 Interactive Data Workflow")

        t_col1, t_col2, t_col3, t_col4 = st.columns(4)
        with t_col1:
            if st.button("🧹 Remove Duplicates", use_container_width=True):
                df_clean = current_df.drop_duplicates()
                save_current_df(df_clean)
                st.session_state.last_direct_speech = "Duplicates removed instantly. What next?"
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
        st.write("Editable Data Grid:")
        edited_df = st.data_editor(current_df, num_rows="dynamic", use_container_width=True)
        if st.button("💾 Save Grid Edits", use_container_width=True):
            save_current_df(edited_df)
            st.session_state.last_direct_speech = "Edits saved successfully!"
            st.success("Workflow saved!")

    # -------------------------------------------------------------------------
    # TAB 2: DATA PREVIEW & PRINT
    # -------------------------------------------------------------------------
    elif st.session_state.current_nav_page == "📋 Data Preview & Print":
        st.subheader("📋 Synchronized Data Preview")
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

    # -------------------------------------------------------------------------
    # TAB 3: CUSTOMIZE DATA & ANALYTICS (PRESENTATION IS DARK THEME)
    # -------------------------------------------------------------------------
    elif st.session_state.current_nav_page == "📈 Customize Data & Analytics":
        st.subheader("📈 Analytics & Presentation Hub")

        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["📊 Data Report", "🎨 Dynamic Charts", "🎬 Do Presentation (Dark Mode)"])

        with sub_tab1:
            if st.button("🚀 Generate Analyst Summary", use_container_width=True):
                num_df = current_df.select_dtypes(include=[np.number])
                st.write(f"**Total Records:** {len(current_df)}")
                if not num_df.empty:
                    st.dataframe(num_df.describe(), use_container_width=True)
                
                resp = f"Dataset analysis complete. Total record volume is {len(current_df)} rows. Would you like me to export this to PDF or generate visual charts?"
                st.info(resp)
                speak_direct_response(resp)

        with sub_tab2:
            chart_type = st.selectbox("Chart Type", ["Bar Chart", "Line Chart", "Area Chart"])
            c_cols = current_df.columns.tolist()
            x_var = st.selectbox("X-Axis", c_cols, index=0)
            y_var = st.selectbox("Y-Axis", current_df.select_dtypes(include=[np.number]).columns.tolist(), index=0)

            if st.button("Render Chart", use_container_width=True):
                chart_df = current_df.set_index(x_var)[y_var]
                if chart_type == "Bar Chart":
                    st.bar_chart(chart_df)
                elif chart_type == "Line Chart":
                    st.line_chart(chart_df)
                elif chart_type == "Area Chart":
                    st.area_chart(chart_df)

        # Presentation Mode (Restricted Dark Theme)
        with sub_tab3:
            st.markdown("#### 🎬 Dark Theme Dynamic Presentation Engine")
            if st.button("▶️ Launch Presentation", use_container_width=True):
                slides = [
                    {"title": "Slide 1: Executive Overview", "body": f"Master data preview contains {len(current_df)} items.", "speech": "Welcome to the executive data presentation. What specific metric would you like to highlight?"},
                    {"title": "Slide 2: Inventory & Operations", "body": "Evaluating stock metrics and supply efficiency.", "speech": "Slide two shows your operational stock dynamics. Shall we adjust inventory parameters?"},
                    {"title": "Slide 3: Strategic Recommendations", "body": "Prioritize high sales volume drivers and replenish low inventory.", "speech": "Slide three details strategic recommendations. Ready for further questions?"}
                ]

                for slide in slides:
                    st.markdown(f"""
                        <div class="presentation-dark-card">
                            <h2>{slide['title']}</h2>
                            <hr style="border-color:#38bdf8;">
                            <p>{slide['body']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    speak_direct_response(slide['speech'])
                    time.sleep(4)

    # -------------------------------------------------------------------------
    # TAB 4: MASTER ADMIN PORTAL
    # -------------------------------------------------------------------------
    elif st.session_state.current_nav_page == "🛡️ Master Admin Portal":
        st.subheader("🛡️ Master Admin Security Portal")
        
        if not st.session_state.is_master_authenticated:
            passkey_in = st.text_input("Enter Passkey:", type="password")
            if st.button("Authenticate", use_container_width=True):
                if passkey_in == MASTER_PASSKEY:
                    st.session_state.is_master_authenticated = True
                    st.session_state.last_direct_speech = f"Master {MASTER_FULL_NAME} authenticated! What admin task shall we execute?"
                    st.success(f"Authenticated Master: {MASTER_FULL_NAME}")
                    st.rerun()
                else:
                    st.error("Invalid Passkey.")
        else:
            st.success(f"👑 Verified Sovereign Master: **{MASTER_FULL_NAME}**")
            st.json(st.session_state.db_users)
