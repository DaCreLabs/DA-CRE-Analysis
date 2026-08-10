import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import time
from datetime import datetime
from PIL import Image
import os
import base64

# =============================================================================
# 1. APP CONFIG & LOGO
# =============================================================================
APP_NAME = "Dacre Analysis Engine"
MASTER_FULL_NAME = "David Emenike"
MASTER_PASSKEY = "theWORDofGOD@111"
LOGO_PATH = "logo.png"

logo_image = None
if os.path.exists(LOGO_PATH):
    try:
        logo_image = Image.open(LOGO_PATH)
    except Exception:
        logo_image = None

st.set_page_config(
    page_title=f"{APP_NAME} | Autonomous DI Platform",
    page_icon=logo_image if logo_image is not None else "📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force permanent favicon
if logo_image is not None and os.path.exists(LOGO_PATH):
    try:
        with open(LOGO_PATH, "rb") as f:
            encoded_logo = base64.b64encode(f.read()).decode("utf-8")
        favicon_js = f"""
        <script>
            function lockFavicon() {{
                var link = parent.document.querySelector("link[rel*='icon']") || parent.document.createElement('link');
                link.type = 'image/png';
                link.rel = 'shortcut icon';
                link.href = 'data:image/png;base64,{encoded_logo}';
                parent.document.getElementsByTagName('head')[0].appendChild(link);
            }}
            lockFavicon();
            setInterval(lockFavicon, 1500);
        </script>
        """
        components.html(favicon_js, height=0, width=0)
    except Exception:
        pass

# =============================================================================
# 2. PREMIUM DARK UI THEME
# =============================================================================
st.markdown("""
<style>
/* ========== GLOBAL ========== */
* {
    font-weight: 700 !important;
    -webkit-font-smoothing: antialiased;
}

html, body, [class*="st-"], p, span, div, label, h1, h2, h3, h4, h5, h6,
input, button, select, textarea, table, th, td {
    color: #f1f5f9 !important;
}

.stApp {
    background: radial-gradient(ellipse at top, #0f172a 0%, #020617 70%) !important;
}

/* ========== SIDEBAR ========== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617 0%, #0f172a 100%) !important;
    border-right: 1px solid #1e293b !important;
}

[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* ========== HERO TITLE ========== */
.hero-title {
    background: linear-gradient(90deg, #38bdf8, #22d3ee, #4ade80, #38bdf8);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.7rem;
    font-weight: 900 !important;
    letter-spacing: -0.5px;
    margin-bottom: 0.2rem;
    animation: gradientMove 5s linear infinite;
}

@keyframes gradientMove {
    to { background-position: 300% center; }
}

.hero-subtitle {
    color: #94a3b8 !important;
    font-size: 1.05rem;
    font-weight: 500 !important;
    margin-bottom: 1.5rem;
}

/* ========== CARDS ========== */
.metric-card {
    background: linear-gradient(145deg, #0f172a, #1e293b);
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    text-align: center;
}

.metric-value {
    font-size: 1.8rem;
    font-weight: 900 !important;
    background: linear-gradient(90deg, #38bdf8, #4ade80);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.metric-label {
    color: #94a3b8 !important;
    font-size: 0.85rem;
    font-weight: 600 !important;
    margin-top: 0.3rem;
}

/* ========== INPUTS & BUTTONS ========== */
.stTextInput input, .stNumberInput input, .stSelectbox > div > div {
    background-color: #0f172a !important;
    color: #f8fafc !important;
    border: 1.5px solid #334155 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.25) !important;
}

label, [data-testid="stWidgetLabel"] p {
    color: #94a3b8 !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

.stButton > button {
    background: linear-gradient(135deg, #0284c7, #0369a1) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.4rem !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.4) !important;
    transition: all 0.25s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(56, 189, 248, 0.5) !important;
    background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
}

/* ========== NAV RADIO ========== */
div[role="radiogroup"] label {
    background: #0f172a !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
    padding: 0.5rem 1rem !important;
    margin-right: 0.4rem !important;
}

div[role="radiogroup"] label[data-checked="true"] {
    background: linear-gradient(135deg, #0c4a6e, #0369a1) !important;
    border-color: #38bdf8 !important;
}

/* ========== PRESENTATION CARD ========== */
.presentation-card {
    background: linear-gradient(145deg, #0f172a, #1e293b);
    border: 1px solid #38bdf8;
    border-radius: 18px;
    padding: 2.2rem;
    min-height: 320px;
    box-shadow: 0 0 40px rgba(56, 189, 248, 0.15);
    animation: fadeUp 0.5s ease;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ========== SUCCESS / ERROR ========== */
.stSuccess {
    background: rgba(16, 185, 129, 0.15) !important;
    border: 1px solid #10b981 !important;
    border-radius: 10px !important;
}

.stError {
    background: rgba(239, 68, 68, 0.15) !important;
    border: 1px solid #ef4444 !important;
    border-radius: 10px !important;
}

.stInfo {
    background: rgba(56, 189, 248, 0.12) !important;
    border: 1px solid #38bdf8 !important;
    border-radius: 10px !important;
}

hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, #334155, transparent) !important;
    margin: 1.5rem 0 !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 3. SPEECH ENGINE
# =============================================================================
def speak_now(text: str):
    clean = text.replace("'", "\\'").replace("\n", " ")
    js = f"""
    <script>
        (function() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance('{clean}');
                msg.rate = 1.12;
                msg.pitch = 1.0;
                msg.volume = 1.0;
                window.parent.isDiSpeaking = true;
                msg.onend = function() {{ window.parent.isDiSpeaking = false; }};
                window.speechSynthesis.speak(msg);
            }}
        }})();
    </script>
    """
    components.html(js, height=0, width=0)

# =============================================================================
# 4. SESSION STATE
# =============================================================================
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

if not st.session_state.logged_in_user and not st.session_state.has_greeted_on_load:
    st.session_state.last_di_speech = "Good day user! How are you doing today? Please sign in or sign up for us to start work."
    st.session_state.has_greeted_on_load = True

if st.session_state.last_di_speech:
    speak_now(st.session_state.last_di_speech)
    st.session_state.last_di_speech = None

# =============================================================================
# 5. HELPERS
# =============================================================================
def get_current_df() -> pd.DataFrame:
    user = st.session_state.logged_in_user or "default"
    if user not in st.session_state.user_datasets:
        st.session_state.user_datasets[user] = st.session_state.user_datasets["default"].copy()
    return st.session_state.user_datasets[user]

def save_current_df(df: pd.DataFrame):
    user = st.session_state.logged_in_user or "default"
    st.session_state.user_datasets[user] = df.copy()

def process_verbal_interaction(speech_input: str) -> str:
    q = speech_input.lower().strip()

    if any(k in q for k in ["sign up", "where do i sign up", "take me to sign up"]):
        st.session_state.auth_mode = "📝 Sign Up"
        return "I have opened the Sign Up portal. Please enter your username, password and full name."

    if any(k in q for k in ["sign in", "login", "take me to sign in"]):
        st.session_state.auth_mode = "🔑 Sign In"
        return "Directing you to the Sign In portal. Please enter your credentials."

    if any(k in q for k in ["hello", "hi", "how are you"]):
        user = st.session_state.logged_in_user or "user"
        return f"Hello {user}! I am doing great and listening. What should we work on next?"

    if any(k in q for k in ["dashboard", "workflow"]):
        st.session_state.current_nav_page = "📊 Workflow Dashboard"
        return "Switched to Workflow Dashboard. What dataset operations shall we run?"

    if any(k in q for k in ["preview", "print"]):
        st.session_state.current_nav_page = "📋 Data Preview & Print"
        return "Opened Data Preview. Would you like to download CSV or print the report?"

    if any(k in q for k in ["presentation", "slide", "analytics"]):
        st.session_state.current_nav_page = "📈 Customize Data & Analytics"
        return "Presentation and Analytics hub is ready. Shall I start the presentation?"

    if any(k in q for k in ["who are you", "master"]):
        return f"I am your Dacre Assistant operating for Master {MASTER_FULL_NAME}. How can I assist you?"

    return f"I heard: {speech_input}. How would you like me to process this?"

# =============================================================================
# 6. SIDEBAR
# =============================================================================
with st.sidebar:
    if logo_image is not None:
        st.image(logo_image, use_container_width=True)
    else:
        st.markdown("### 🔷 DACRE")

    st.markdown(f"### **{APP_NAME}**")
    st.caption("Autonomous Data Intelligence Platform")
    st.markdown("---")

    if st.session_state.logged_in_user:
        st.success(f"**● Online**  \n{st.session_state.logged_in_user}")
        st.caption(f"Role: {st.session_state.db_users.get(st.session_state.logged_in_user, {}).get('role', 'user').title()}")
        if st.button("Log Out", use_container_width=True):
            st.session_state.logged_in_user = None
            st.session_state.is_master_authenticated = False
            st.session_state.has_greeted_on_load = False
            st.session_state.last_di_speech = "Logged out successfully. Have a great day!"
            st.rerun()
    else:
        st.info("Not signed in")

    st.markdown("---")
    st.markdown("**Voice Mode**")
    st.caption("🟢 Continuous listening active")

# =============================================================================
# 7. MAIN HEADER
# =============================================================================
st.markdown('<div class="hero-title">DACRE AUTONOMOUS DATA ENGINE</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Data Today, Smarter Tomorrows • Get Data → Clean → Analyze → Visualize → AI Insights → Export</div>', unsafe_allow_html=True)

# =============================================================================
# 8. VOICE INTERACTION BAR
# =============================================================================
components.html("""
<div style="background:linear-gradient(90deg,rgba(15,23,42,0.95),rgba(15,23,42,0.8));border:1.5px solid #22d3ee;border-radius:12px;padding:0.9rem 1.3rem;display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
    <span style="color:#22d3ee;font-weight:800;font-size:1.05rem;">🎙️ DI Voice Interaction Active</span>
    <span style="color:#4ade80;font-weight:700;">🟢 Hearing You Live...</span>
</div>
<script>
window.parent.isDiSpeaking = window.parent.isDiSpeaking || false;
window.addEventListener('DOMContentLoaded', () => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        recognition.onresult = (event) => {
            if (window.parent.isDiSpeaking) return;
            const transcript = event.results[event.results.length - 1][0].transcript.trim();
            if (!transcript) return;
            const inputs = window.parent.document.querySelectorAll('input[type="text"]');
            if (inputs.length > 0) {
                inputs[0].value = transcript;
                inputs[0].dispatchEvent(new Event('input', { bubbles: true }));
                setTimeout(() => {
                    const btns = window.parent.document.querySelectorAll('button');
                    for (let b of btns) {
                        if (b.innerText.includes("Respond") || b.innerText.includes("Execute")) {
                            b.click(); break;
                        }
                    }
                }, 120);
            }
        };
        recognition.onend = () => { try { recognition.start(); } catch(e) {} };
        try { recognition.start(); } catch(e) {}
    }
});
</script>
""", height=70)

c1, c2 = st.columns([5, 1])
with c1:
    user_speech_val = st.text_input(
        "Command / Voice Input",
        key="live_voice_bar",
        placeholder="Speak or type a command for Di..."
    )
with c2:
    st.write("")
    st.write("")
    if st.button("⚡ Execute", use_container_width=True):
        if user_speech_val:
            reply = process_verbal_interaction(user_speech_val)
            st.session_state.last_di_speech = reply
            st.rerun()

# =============================================================================
# 9. AUTHENTICATION
# =============================================================================
if not st.session_state.logged_in_user:
    st.markdown("---")
    st.markdown("### 🔐 Access Portal")

    modes = ["🔑 Sign In", "📝 Sign Up"]
    st.session_state.auth_mode = st.radio(
        "Choose mode",
        modes,
        index=modes.index(st.session_state.auth_mode),
        horizontal=True,
        label_visibility="collapsed"
    )

    if st.session_state.auth_mode == "🔑 Sign In":
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("#### Sign In")
            u_name = st.text_input("Username", key="login_username")
            u_pass = st.text_input("Password", type="password", key="login_password")
            if st.button("Sign In →", use_container_width=True, type="primary"):
                if u_name in st.session_state.db_users and st.session_state.db_users[u_name]["password"] == u_pass:
                    st.session_state.logged_in_user = u_name
                    st.session_state.last_di_speech = f"Welcome back {u_name}! What task would you like to execute today?"
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")
    else:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("#### Create Account")
            new_u = st.text_input("Choose Username", key="reg_username")
            new_p = st.text_input("Choose Password", type="password", key="reg_password")
            new_full = st.text_input("Full Name", key="reg_fullname")
            if st.button("Create Account →", use_container_width=True, type="primary"):
                if new_u and new_p:
                    st.session_state.db_users[new_u] = {
                        "password": new_p,
                        "full_name": new_full or new_u,
                        "role": "user"
                    }
                    st.session_state.logged_in_user = new_u
                    st.session_state.last_di_speech = f"Account created successfully! Welcome {new_u}."
                    st.rerun()
                else:
                    st.warning("Username and password are required.")

# =============================================================================
# 10. MAIN WORKSPACE
# =============================================================================
else:
    pages = [
        "📊 Workflow Dashboard",
        "📋 Data Preview & Print",
        "📈 Customize Data & Analytics",
        "🛡️ Master Admin Portal"
    ]
    st.session_state.current_nav_page = st.radio(
        "Navigation",
        pages,
        index=pages.index(st.session_state.current_nav_page),
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown("---")
    current_df = get_current_df()

    # ------------------------------------------------------------------
    # 📊 WORKFLOW DASHBOARD
    # ------------------------------------------------------------------
    if st.session_state.current_nav_page == "📊 Workflow Dashboard":
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(current_df)}</div>
                <div class="metric-label">Total Records</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            num_cols = len(current_df.select_dtypes(include=[np.number]).columns)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{num_cols}</div>
                <div class="metric-label">Numeric Columns</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{current_df.shape[1]}</div>
                <div class="metric-label">Total Columns</div>
            </div>
            """, unsafe_allow_html=True)
        with m4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{st.session_state.logged_in_user[:8]}</div>
                <div class="metric-label">Active User</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📂 Import Data")
        uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith(".csv"):
                    imported_df = pd.read_csv(uploaded_file)
                else:
                    imported_df = pd.read_excel(uploaded_file)
                save_current_df(imported_df)
                st.session_state.last_di_speech = f"File {uploaded_file.name} imported successfully!"
                st.success(f"✅ **{uploaded_file.name}** imported and synchronized.")
                st.rerun()
            except Exception as e:
                st.error(f"Error loading file: {e}")

        st.markdown("---")
        st.markdown("### 🛠️ Data Tools")

        t1, t2, t3, t4 = st.columns(4)
        with t1:
            if st.button("🧹 Remove Duplicates", use_container_width=True):
                before = len(current_df)
                cleaned = current_df.drop_duplicates()
                save_current_df(cleaned)
                st.session_state.last_di_speech = f"Removed {before - len(cleaned)} duplicates."
                st.rerun()
        with t2:
            target_col = st.selectbox("Sort by column", current_df.columns.tolist(), key="sort_col")
        with t3:
            if st.button("🔤 Sort A → Z", use_container_width=True):
                save_current_df(current_df.sort_values(by=target_col, ascending=True))
                st.rerun()
        with t4:
            if st.button("🔠 Sort Z → A", use_container_width=True):
                save_current_df(current_df.sort_values(by=target_col, ascending=False))
                st.rerun()

        st.markdown("---")
        st.markdown("### ✏️ Live Data Editor")
        edited_df = st.data_editor(current_df, num_rows="dynamic", use_container_width=True, height=380)
        if st.button("💾 Save Changes", use_container_width=True, type="primary"):
            save_current_df(edited_df)
            st.session_state.last_di_speech = "Grid modifications saved successfully."
            st.success("Changes saved!")

    # ------------------------------------------------------------------
    # 📋 DATA PREVIEW & PRINT
    # ------------------------------------------------------------------
    elif st.session_state.current_nav_page == "📋 Data Preview & Print":
        st.markdown("### 📋 Data Preview")
        st.dataframe(current_df, use_container_width=True, height=420)

        st.markdown("<br>", unsafe_allow_html=True)
        p1, p2, p3 = st.columns(3)
        with p1:
            csv_data = current_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Download CSV",
                data=csv_data,
                file_name=f"dacre_export_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        with p2:
            if st.button("🖨️ Print Report", use_container_width=True):
                components.html("<script>window.print();</script>", height=0)
        with p3:
            st.metric("Rows", len(current_df))

    # ------------------------------------------------------------------
    # 📈 ANALYTICS & PRESENTATION
    # ------------------------------------------------------------------
    elif st.session_state.current_nav_page == "📈 Customize Data & Analytics":
        st.markdown("### 📈 Analytics & Presentation Engine")

        tab1, tab2, tab3 = st.tabs(["📊 Report", "🎨 Charts", "🎬 Presentation"])

        with tab1:
            st.markdown("#### Statistical Summary")
            if st.button("🚀 Generate Full Report", use_container_width=True, type="primary"):
                num_df = current_df.select_dtypes(include=[np.number])
                st.write(f"**Total records:** {len(current_df)}")
                if not num_df.empty:
                    st.dataframe(num_df.describe().round(2), use_container_width=True)
                else:
                    st.info("No numeric columns found for statistical summary.")
                speak_now(f"Analysis complete. Dataset contains {len(current_df)} records.")

        with tab2:
            st.markdown("#### Dynamic Charts")
            chart_type = st.selectbox("Chart Type", ["Bar Chart", "Line Chart", "Area Chart"])
            cols = current_df.columns.tolist()
            x_var = st.selectbox("X Axis", cols, index=0)
            numeric_cols = current_df.select_dtypes(include=[np.number]).columns.tolist()

            if numeric_cols:
                y_var = st.selectbox("Y Axis", numeric_cols, index=0)
                if st.button("Render Chart", use_container_width=True, type="primary"):
                    chart_df = current_df.set_index(x_var)[y_var]
                    if chart_type == "Bar Chart":
                        st.bar_chart(chart_df, use_container_width=True)
                    elif chart_type == "Line Chart":
                        st.line_chart(chart_df, use_container_width=True)
                    else:
                        st.area_chart(chart_df, use_container_width=True)
            else:
                st.warning("No numeric columns available for charting.")

        with tab3:
            st.markdown("#### Dark Mode Presentation")
            if st.button("▶️ Launch Presentation", use_container_width=True, type="primary"):
                slides = [
                    {
                        "title": "Slide 1 — Executive Overview",
                        "body": f"Current dataset holds <strong>{len(current_df)}</strong> records ready for analysis.",
                        "speech": f"Welcome {st.session_state.logged_in_user}. This is your executive overview."
                    },
                    {
                        "title": "Slide 2 — Stock & Sales Dynamics",
                        "body": "Reviewing inventory stability and sales performance across categories.",
                        "speech": "Slide two highlights inventory and sales distribution."
                    },
                    {
                        "title": "Slide 3 — Strategic Recommendations",
                        "body": "Prioritize restocking low-inventory items and focus on high-revenue products.",
                        "speech": "Slide three presents strategic recommendations. Any questions?"
                    }
                ]
                for s in slides:
                    st.markdown(f"""
                    <div class="presentation-card">
                        <h2 style="color:#38bdf8; margin-bottom:0.8rem;">{s['title']}</h2>
                        <hr style="border:none; height:1px; background:#334155;">
                        <p style="font-size:1.25rem; line-height:1.6; margin-top:1.5rem;">{s['body']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    speak_now(s["speech"])
                    time.sleep(3.8)

    # ------------------------------------------------------------------
    # 🛡️ MASTER ADMIN
    # ------------------------------------------------------------------
    elif st.session_state.current_nav_page == "🛡️ Master Admin Portal":
        st.markdown("### 🛡️ Master Admin Portal")

        if not st.session_state.is_master_authenticated:
            st.info("This area is restricted. Enter the master passkey to continue.")
            passkey = st.text_input("Master Passkey", type="password")
            if st.button("Authenticate", use_container_width=True, type="primary"):
                if passkey == MASTER_PASSKEY:
                    st.session_state.is_master_authenticated = True
                    st.session_state.last_di_speech = f"Master {MASTER_FULL_NAME} authorized."
                    st.success(f"Welcome, Master {MASTER_FULL_NAME}")
                    st.rerun()
                else:
                    st.error("Invalid passkey.")
        else:
            st.success(f"👑 **Verified Master:** {MASTER_FULL_NAME}")
            st.markdown("#### Registered Users")
            st.json(st.session_state.db_users)
