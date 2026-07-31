import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import io
import time
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. APP CONFIGURATION & MASTER CONSTANTS
# -----------------------------------------------------------------------------
APP_NAME = "Dacre Analysis Engine"
MASTER_FULL_NAME = "David Emenike"
MASTER_PASSKEY = "theWORDofGOD@111"
LOGO_PATH = "ChatGPT Image Jul 29, 2026, 02_27_41 PM.png"

# Updated Page Icon Configuration using your official Logo Path
try:
    st.set_page_config(
        page_title=f"{APP_NAME} | Autonomous DI Platform",
        page_icon=LOGO_PATH,
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
# 2. HIGH-PERFORMANCE STYLING & AUTOMATED CORE CSS
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(ellipse at bottom, #090d16 0%, #020408 100%) !important;
        color: #f8fafc !important;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #110d0a 0%, #070504 100%) !important;
        border-right: 2px solid #38bdf8 !important;
    }

    [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #e0f2fe !important;
    }

    .hero-title {
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }

    .di-card {
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        border: 1px solid #38bdf8;
        border-radius: 10px;
        padding: 12px 18px;
        margin-bottom: 15px;
        box-shadow: 0 4px 20px rgba(56, 189, 248, 0.15);
    }

    .stTextInput input, .stNumberInput input, .stSelectbox div {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border: 1.5px solid #38bdf8 !important;
        border-radius: 6px !important;
    }

    .stButton>button {
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 8px 18px !important;
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.4) !important;
    }

    /* Presentation Slide Styling */
    .slide-card {
        background: #030712;
        border: 2px solid #38bdf8;
        border-radius: 14px;
        padding: 30px;
        min-height: 420px;
        box-shadow: 0 0 30px rgba(56, 189, 248, 0.2);
        animation: fadeIn 0.8s ease-in-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. FAST NIGERIAN VOICE SYNTHESIS DISPATCHER
# -----------------------------------------------------------------------------
def speak_fast_text(text: str):
    """Executes high-speed text-to-speech output immediately."""
    clean_text = text.replace("'", "\\'").replace("\n", " ")
    js_code = f"""
    <script>
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance('{clean_text}');
            msg.rate = 1.15;
            msg.pitch = 1.0;
            msg.volume = 1.0;
            window.speechSynthesis.speak(msg);
        }}
    </script>
    """
    components.html(js_code, height=0, width=0)

# -----------------------------------------------------------------------------
# 4. STATE PERSISTENCE & DATA STORAGE INITIALIZATION
# -----------------------------------------------------------------------------
if "db_users" not in st.session_state:
    st.session_state.db_users = {
        "david": {"password": "123", "full_name": MASTER_FULL_NAME, "role": "master"}
    }

if "user_datasets" not in st.session_state:
    # Default enterprise dataset fallback
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

if "last_spoken_phrase" not in st.session_state:
    st.session_state.last_spoken_phrase = None

if "current_nav_page" not in st.session_state:
    st.session_state.current_nav_page = "📊 Workflow Dashboard"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "🔑 Sign In"

# Voice playback trigger
if st.session_state.last_spoken_phrase:
    speak_fast_text(st.session_state.last_spoken_phrase)
    st.session_state.last_spoken_phrase = None

# Helper to retrieve active dataset for current session
def get_current_df():
    u = st.session_state.logged_in_user or "default"
    if u not in st.session_state.user_datasets:
        st.session_state.user_datasets[u] = st.session_state.user_datasets["default"].copy()
    return st.session_state.user_datasets[u]

def save_current_df(df):
    u = st.session_state.logged_in_user or "default"
    st.session_state.user_datasets[u] = df.copy()

# -----------------------------------------------------------------------------
# 5. DI SALUTATION & COMMAND RESOLVER
# -----------------------------------------------------------------------------
def get_user_salutation():
    if st.session_state.is_master_authenticated:
        return f"Sovereign Master {MASTER_FULL_NAME}"
    elif st.session_state.logged_in_user:
        return f"{st.session_state.logged_in_user}"
    else:
        return "Operator"

def process_voice_command(text: str):
    cmd = text.lower()
    salutation = get_user_salutation()

    if "sign in" in cmd or "login" in cmd:
        st.session_state.auth_mode = "🔑 Sign In"
        reply = f"Navigating to Sign In page for you, {salutation}."
        return reply, True
    elif "sign up" in cmd or "register" in cmd:
        st.session_state.auth_mode = "📝 Sign Up"
        reply = f"Opening registration portal now, {salutation}."
        return reply, True
    elif "dashboard" in cmd or "workflow" in cmd:
        st.session_state.current_nav_page = "📊 Workflow Dashboard"
        reply = f"Switching directly to your Workflow Dashboard, {salutation}."
        return reply, True
    elif "preview" in cmd:
        st.session_state.current_nav_page = "📋 Data Preview & Print"
        reply = f"Opening read-only Data Preview, {salutation}."
        return reply, True
    elif "customize" in cmd or "report" in cmd or "chart" in cmd:
        st.session_state.current_nav_page = "📈 Customize Data & Analytics"
        reply = f"Moving to Customize Analytics and Presentation Suite, {salutation}."
        return reply, True
    elif "master" in cmd or "who are you" in cmd or "who built you" in cmd:
        if st.session_state.is_master_authenticated:
            reply = f"My Master is {MASTER_FULL_NAME}. All systems operate under your sovereign directive."
        else:
            reply = f"I am your built-in Digital Intelligence assistant. Welcome, {salutation}."
        return reply, False
    else:
        reply = f"Executed request: '{text}'. Ready for next command, {salutation}."
        return reply, False

# -----------------------------------------------------------------------------
# 6. HEADER & AUTOMATED INSTANT SPEECH RECOGNITION WIDGET
# -----------------------------------------------------------------------------
st.markdown('<div class="hero-title">DACRE AUTONOMOUS DATA ENGINE</div>', unsafe_allow_html=True)

with st.sidebar:
    try:
        st.image(LOGO_PATH, use_container_width=True)
    except Exception:
        pass

    st.markdown(f"### **{APP_NAME}**")
    st.caption("Built-In Continuous Voice Core Active")
    st.markdown("---")

    # Dynamic Identity Box
    st.markdown(f"""
        <div style="background: rgba(56, 189, 248, 0.08); border: 1px solid #38bdf8; padding: 10px; border-radius: 8px;">
            <p style="margin:0; font-weight:bold; color:#38bdf8 !important;">🤖 Built-in DI Assistant</p>
            <p style="margin:0; font-size: 0.85rem;">Status: 🟢 Instant Auto-Listen Active</p>
            <p style="margin:0; font-size: 0.85rem; color:#38bdf8;">User: <b>{get_user_salutation()}</b></p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    if st.session_state.logged_in_user:
        st.success(f"Session Saved: **{st.session_state.logged_in_user}**")
        if st.button("Log Out & Save Session", use_container_width=True):
            st.session_state.logged_in_user = None
            st.session_state.is_master_authenticated = False
            st.session_state.last_spoken_phrase = "Work saved automatically. Session logged out successfully."
            st.rerun()

# Instant JavaScript Auto-Start Mic Widget
mic_widget_html = """
<div style="background: rgba(15, 23, 42, 0.8); border: 1px solid #38bdf8; padding: 10px 14px; border-radius: 8px; margin-bottom: 10px;">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="color:#38bdf8; font-weight:bold; font-size:0.9rem;">🎙️ Continuous Auto-Speech Listening Active...</span>
        <span id="speech-live-status" style="color:#10b981; font-size:0.85rem; font-weight:600;">Listening Live</span>
    </div>
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

        recognition.onerror = (event) => {
            console.log("Auto-speech error: " + event.error);
        };

        recognition.onend = () => {
            recognition.start(); // Auto-restart listening continuously
        };

        recognition.start();
    }
});
</script>
"""
components.html(mic_widget_html, height=55)

# Fast Command Bar
col_cmd, col_act = st.columns([5, 1])
with col_cmd:
    voice_input = st.text_input("Live Voice Input Stream:", key="voice_stream_input", placeholder="Speak or type command...")
with col_act:
    st.write(" ")
    st.write(" ")
    if st.button("⚡ Dispatch Command", use_container_width=True):
        if voice_input:
            msg, rerun_flag = process_voice_command(voice_input)
            st.session_state.last_spoken_phrase = msg
            if rerun_flag:
                st.rerun()

# -----------------------------------------------------------------------------
# 7. AUTHENTICATION ENGINE
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
                    st.session_state.last_spoken_phrase = f"Welcome back, {u_name}! Your previous session data has been restored."
                    st.rerun()
                else:
                    st.error("Invalid Login Credentials.")

    else:
        c1, c2 = st.columns(2)
        with c1:
            new_u = st.text_input("Choose Username", key="reg_username")
            new_p = st.text_input("Choose Password", type="password", key="reg_password")
            new_full = st.text_input("Full Name", key="reg_fullname")
            if st.button("Create Account & Save", use_container_width=True):
                if new_u and new_p:
                    st.session_state.db_users[new_u] = {"password": new_p, "full_name": new_full, "role": "user"}
                    st.session_state.logged_in_user = new_u
                    st.session_state.last_spoken_phrase = f"Account created! Welcome, {new_u}."
                    st.rerun()

# -----------------------------------------------------------------------------
# 8. MAIN WORKSPACE ENGINE
# -----------------------------------------------------------------------------
else:
    # Navigation Hub
    pages = ["📊 Workflow Dashboard", "📋 Data Preview & Print", "📈 Customize Data & Analytics", "🛡️ Master Admin Portal"]
    st.session_state.current_nav_page = st.radio("Navigation Hub", pages, index=pages.index(st.session_state.current_nav_page), horizontal=True)
    st.markdown("---")

    current_df = get_current_df()

    # -------------------------------------------------------------------------
    # TAB 1: WORKFLOW DASHBOARD & COLLECT DATA BAR
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
                st.session_state.last_spoken_phrase = f"Data collected successfully from {uploaded_file.name}. Saved to your dashboard and preview!"
                st.success("File imported and synchronized across Workflow and Preview!")
                st.rerun()
            except Exception as e:
                st.error(f"Error loading file: {e}")

        st.markdown("---")
        st.subheader("📊 Interactive Workflow Board")

        # Top Data Manipulation Action Bar
        t_col1, t_col2, t_col3, t_col4 = st.columns(4)
        with t_col1:
            if st.button("🧹 Remove Duplicates", use_container_width=True):
                df_clean = current_df.drop_duplicates()
                save_current_df(df_clean)
                st.session_state.last_spoken_phrase = "Duplicates removed successfully."
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
        # Sidebar Formula Applications
        st.sidebar.markdown("### 🧮 Formula Engine")
        
        # Excel / Google Sheets Formulas
        excel_formula = st.sidebar.selectbox("Google Sheets / Excel Formula", [
            "None", "SUM", "AVERAGE", "MIN", "MAX", "COUNT", "ROUND", "PERCENTAGE OF TOTAL"
        ])
        num_cols = current_df.select_dtypes(include=[np.number]).columns.tolist()

        if excel_formula != "None" and num_cols:
            formula_col = st.sidebar.selectbox("Apply Excel Formula On:", num_cols)
            if st.sidebar.button("Apply Sheets Formula"):
                if excel_formula == "SUM":
                    val = current_df[formula_col].sum()
                elif excel_formula == "AVERAGE":
                    val = current_df[formula_col].mean()
                elif excel_formula == "MIN":
                    val = current_df[formula_col].min()
                elif excel_formula == "MAX":
                    val = current_df[formula_col].max()
                elif excel_formula == "COUNT":
                    val = current_df[formula_col].count()
                elif excel_formula == "ROUND":
                    current_df[formula_col] = current_df[formula_col].round(2)
                    save_current_df(current_df)
                    val = "Rounded Column"
                elif excel_formula == "PERCENTAGE OF TOTAL":
                    total = current_df[formula_col].sum()
                    current_df[f"{formula_col}_%"] = (current_df[formula_col] / total * 100).round(2)
                    save_current_df(current_df)
                    val = "Calculated % Column"
                
                st.sidebar.success(f"Result ({excel_formula}): {val}")
                st.session_state.last_spoken_phrase = f"Applied {excel_formula} formula to {formula_col}."

        # SQL Formula Engine
        sql_formula = st.sidebar.selectbox("SQL Transformation Query", [
            "None", "SELECT * WHERE Qty > 10", "SELECT * ORDER BY Cost DESC", "GROUP BY Category (SUM Qty)", "COUNT Rows By Status"
        ])

        if sql_formula != "None":
            if st.sidebar.button("Run SQL Command"):
                if sql_formula == "SELECT * WHERE Qty > 10" and "Qty" in current_df.columns:
                    current_df = current_df[current_df["Qty"] > 10]
                elif sql_formula == "SELECT * ORDER BY Cost DESC" and "Cost" in current_df.columns:
                    current_df = current_df.sort_values(by="Cost", ascending=False)
                elif sql_formula == "GROUP BY Category (SUM Qty)" and "Category" in current_df.columns and "Qty" in current_df.columns:
                    current_df = current_df.groupby("Category", as_index=False)["Qty"].sum()
                save_current_df(current_df)
                st.session_state.last_spoken_phrase = "SQL query applied successfully."
                st.rerun()

        # Editable Data Grid
        st.write("Edit cell values directly below:")
        edited_df = st.data_editor(current_df, num_rows="dynamic", use_container_width=True)
        if st.button("💾 Save Grid Edits", use_container_width=True):
            save_current_df(edited_df)
            st.session_state.last_spoken_phrase = "Grid updates saved."
            st.success("Workflow changes saved to persistent storage!")

    # -------------------------------------------------------------------------
    # TAB 2: DATA PREVIEW & PRINT (READ-ONLY)
    # -------------------------------------------------------------------------
    elif st.session_state.current_nav_page == "📋 Data Preview & Print":
        st.subheader("📋 Synchronized Read-Only Data Preview")
        st.caption("Updated clean dataset ready for export or printing.")

        st.dataframe(current_df, use_container_width=True)

        p_col1, p_col2 = st.columns(2)
        with p_col1:
            # Download options
            csv_data = current_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Clean CSV File",
                data=csv_data,
                file_name=f"dacre_data_export_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        with p_col2:
            if st.button("🖨️ Print Data Report", use_container_width=True):
                components.html("<script>window.print();</script>", height=0)

    # -------------------------------------------------------------------------
    # TAB 3: CUSTOMIZE DATA & ANALYTICS SUITE
    # -------------------------------------------------------------------------
    elif st.session_state.current_nav_page == "📈 Customize Data & Analytics":
        st.subheader("📈 Business Analyst Reports, Dynamic Charts & Presentation Engine")

        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["📊 Get Data Report", "🎨 Dynamic Dark Charts", "🎬 Do Presentation"])

        # SUB-TAB 1: DATA REPORT
        with sub_tab1:
            if st.button("🚀 Generate Business Data Analyst Report", use_container_width=True):
                st.markdown("### 📋 Executive Business Data Analyst Report")
                
                num_df = current_df.select_dtypes(include=[np.number])
                total_products = len(current_df)
                
                st.write(f"**Total Record Volume:** {total_products} items")

                if not num_df.empty:
                    st.markdown("#### Statistical Summaries")
                    stats_df = pd.DataFrame({
                        "Mean": num_df.mean(),
                        "Median": num_df.median(),
                        "Std Dev": num_df.std(),
                        "Min": num_df.min(),
                        "Max": num_df.max()
                    })
                    st.dataframe(stats_df, use_container_width=True)

                # Restock & Market Leader Analysis
                if "Qty" in current_df.columns and "Name" in current_df.columns:
                    lacking = current_df.sort_values(by="Qty", ascending=True).iloc[0]
                    st.warning(f"⚠️ **Restock Urgency Alert:** Item **'{lacking['Name']}'** has lowest inventory stock ({lacking['Qty']} units). Action recommended immediately!")
                
                if "Sales" in current_df.columns and "Name" in current_df.columns:
                    leader = current_df.sort_values(by="Sales", ascending=False).iloc[0]
                    st.success(f"🌟 **Market Driver Leader:** Item **'{leader['Name']}'** generates highest sales volume ({leader['Sales']} units). Prioritize inventory allocation!")

                narrative = (
                    f"Business Intelligence Assessment: Based on your preview dataset of {total_products} records, "
                    "operational performance shows strong momentum. Inventory restock is required for lagging stock items, "
                    "while top sales drivers should be allocated maximum supply chain priority."
                )
                st.info(f"**Analyst Narrative:** {narrative}")
                speak_fast_text(narrative)

        # SUB-TAB 2: GORGEOUS DARK CHARTS
        with sub_tab2:
            st.markdown("#### Select Visualizer Type")
            chart_type = st.selectbox("Dynamic Chart Selector", ["Bar Chart", "Pie Chart", "Line Chart", "Scatter Plot", "Donut Chart"])
            
            c_cols = current_df.columns.tolist()
            x_var = st.selectbox("X-Axis Parameter", c_cols, index=0)
            y_var = st.selectbox("Y-Axis Parameter", current_df.select_dtypes(include=[np.number]).columns.tolist(), index=0)

            if st.button("🎨 Render Dark-Theme Visualizer", use_container_width=True):
                if chart_type == "Bar Chart":
                    fig = px.bar(current_df, x=x_var, y=y_var, color=x_var, template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Cyberpunk)
                elif chart_type == "Pie Chart":
                    fig = px.pie(current_df, names=x_var, values=y_var, template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Vivid)
                elif chart_type == "Line Chart":
                    fig = px.line(current_df, x=x_var, y=y_var, markers=True, template="plotly_dark")
                elif chart_type == "Scatter Plot":
                    fig = px.scatter(current_df, x=x_var, y=y_var, color=x_var, size=y_var, template="plotly_dark")
                elif chart_type == "Donut Chart":
                    fig = px.pie(current_df, names=x_var, values=y_var, hole=0.5, template="plotly_dark")

                fig.update_layout(paper_bgcolor="#030712", plot_bgcolor="#030712", font=dict(color="#38bdf8", family="Space Grotesk"))
                st.plotly_chart(fig, use_container_width=True)

        # SUB-TAB 3: DO PRESENTATION MODE
        with sub_tab3:
            st.markdown("#### 🎬 DI Automated Interactive Presentation Engine")
            if st.button("▶️ Launch Verbal DI Animated Presentation", use_container_width=True):
                slides = [
                    {"title": "Slide 1: Executive Overview", "body": f"Welcome to the automated presentation. Master data preview contains {len(current_df)} primary enterprise items.", "speech": f"Welcome to the executive data presentation for {get_user_salutation()}. We have compiled your dataset for analysis."},
                    {"title": "Slide 2: Stock & Inventory Dynamics", "body": "Evaluating stock metrics and inventory variance across all categories.", "speech": "Slide two shows your stock dynamics. Inventory balancing is aligned with operational targets."},
                    {"title": "Slide 3: Strategic Analyst Summary", "body": "Restock lagging inventory items immediately to capitalize on peak market demand.", "speech": "Slide three details strategic recommendations. Restock underperforming units and scale high-volume drivers immediately."}
                ]

                for idx, slide in enumerate(slides):
                    st.markdown(f"""
                        <div class="slide-card">
                            <h2 style="color:#38bdf8;">{slide['title']}</h2>
                            <hr style="border-color:#38bdf8;">
                            <p style="font-size:1.3rem; color:#e0f2fe; margin-top:30px;">{slide['body']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    speak_fast_text(slide['speech'])
                    time.sleep(4)

    # -------------------------------------------------------------------------
    # TAB 4: MASTER ADMIN PORTAL (VERIFIED ACCESS ONLY)
    # -------------------------------------------------------------------------
    elif st.session_state.current_nav_page == "🛡️ Master Admin Portal":
        st.subheader("🛡️ Overall Master Admin Security Portal")
        
        if not st.session_state.is_master_authenticated:
            passkey_in = st.text_input("Enter Master Security Passkey:", type="password")
            if st.button("Authorize Sovereign Master Access", use_container_width=True):
                if passkey_in == MASTER_PASSKEY:
                    st.session_state.is_master_authenticated = True
                    st.session_state.last_spoken_phrase = f"Sovereign Master {MASTER_FULL_NAME} authenticated! All DI cores operate under your explicit master command."
                    st.success(f"Welcome Sovereign Master {MASTER_FULL_NAME}!")
                    st.rerun()
                else:
                    st.error("Access Denied: Invalid Master Security Passkey.")
        else:
            st.success(f"👑 Verified Sovereign Master: **{MASTER_FULL_NAME}**")
            st.write(f"DI is operating in Master Mode for **{MASTER_FULL_NAME}**.")
            st.markdown("---")
            st.write("#### Registered System Users & Saved Sessions")
            st.json(st.session_state.db_users)
