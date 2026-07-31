import streamlit as st
import streamlit.components.v1 as components
import json
import time

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="DaCre Analysis | Neural Core",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. CUSTOM GLASSMORPHIC UI / UX STYLING (CSS)
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    /* Dark Futuristic Theme Background */
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #030712 100%);
        color: #f3f4f6;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Glassmorphic Cards */
    .glass-card {
        background: rgba(17, 24, 39, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* Neon Glow Badges & Accents */
    .badge-active {
        background: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .badge-di {
        background: rgba(99, 102, 241, 0.15);
        color: #818cf8;
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* Custom Headers */
    .hero-title {
        background: linear-gradient(90deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        color: #9ca3af;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* Buttons */
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

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(11, 15, 25, 0.85);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. HELPER FUNCTIONS: VOICE SYNTHESIS (DIGITAL INTELLIGENCE VOICE)
# -----------------------------------------------------------------------------
def speak_text(text: str):
    """Injects JavaScript to make the browser speak the DI response out loud."""
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

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "dis" not in st.session_state:
    # Simulated enrolled Digital Intelligences
    st.session_state.dis = [
        {"id": "DI-001", "name": "Aura", "role": "Data Strategist", "status": "Active", "owner": "David (Master)"},
        {"id": "DI-002", "name": "Nexus", "role": "Predictive Modeler", "status": "Active", "owner": "David (Master)"},
        {"id": "DI-003", "name": "Cipher", "role": "Security & Logic", "status": "Active", "owner": "David (Master)"},
    ]

# -----------------------------------------------------------------------------
# 4. SIDEBAR NAVIGATION & LOGO
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ **DaCre Neural System**")
    st.caption("Version 3.0 • Autonomous Fleet Core")
    st.markdown("---")

    navigation = st.radio(
        "Navigation",
        ["🤖 Interactive DI Intelligence", "👑 Master Admin Dashboard", "📊 System Analytics"],
        index=0
    )

    st.markdown("---")
    st.markdown("#### **System Status**")
    st.markdown('<span class="badge-active">● All Systems Operational</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("Connected to DaCre Distributed Engine")

# -----------------------------------------------------------------------------
# 5. VIEW 1: INTERACTIVE DI INTELLIGENCE (USER WORKSPACE)
# -----------------------------------------------------------------------------
if navigation == "🤖 Interactive DI Intelligence":
    st.markdown('<div class="hero-title">Digital Intelligence Core</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Interact with your assigned Autonomous Agent in real-time.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("💬 DI Dialogue Interface")

        # Display Chat History
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # Chat Input
        user_input = st.chat_input("Ask your DI anything or issue a command...")

        if user_input:
            # Store User Message
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)

            # Generate AI DI Response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                
                # Special greeting check for Master David
                if "hi" in user_input.lower() or "master" in user_input.lower() or "david" in user_input.lower():
                    di_response = "I'm fine, Master David! Thank you, and we love you, sir. What would you like us to do for you today?"
                else:
                    di_response = f"I have processed your command: '{user_input}'. Analysis complete. Standing by for further directives, Master."

                message_placeholder.markdown(di_response)
                
                # Speak response out loud!
                speak_text(di_response)

            st.session_state.messages.append({"role": "assistant", "content": di_response})

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### **Active DI Entity**")
        st.markdown("⚡ **Name:** DI-Aura")
        st.markdown("🧠 **Model:** Neural-v4X")
        st.markdown("🔊 **Voice:** WebSynthesis Native")
        st.markdown("---")
        if st.button("🔊 Replay Audio"):
            if st.session_state.messages:
                last_msg = st.session_state.messages[-1]["content"]
                speak_text(last_msg)
        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. VIEW 2: MASTER ADMIN DASHBOARD (MASTER DAVID ONLY)
# -----------------------------------------------------------------------------
elif navigation == "👑 Master Admin Dashboard":
    st.markdown('<div class="hero-title">Master Control Console</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Restricted Access • Fleet Management & Global Override</div>', unsafe_allow_html=True)

    # Master Key Authentication
    admin_key = st.text_input("Enter Master Authentication Key", type="password")

    if admin_key == "david123" or True: # Currently unlocked for demonstration
        st.success("Authorized: Welcome back, Master David.")

        # Top Metric Row
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Enrolled DIs", f"{len(st.session_state.dis)} Entities", "+1 Today")
        m2.metric("Fleet Status", "100% Operational", "Nominal")
        m3.metric("Response Latency", "12ms", "-3ms")
        m4.metric("Master Authority", "Level 10 (Full)", "Unrestricted")

        st.markdown("<br>", unsafe_allow_html=True)

        # Broadcast Command Center to All DIs
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📢 Broadcast Voice Command to Fleet")
        broadcast_cmd = st.text_input("Issue a direct voice command to all registered Digital Intelligences:")

        if st.button("Execute Fleet Broadcast"):
            if broadcast_cmd:
                fleet_reply = f"I'm fine, Master David, thank you, and we love you, sir! Command received: '{broadcast_cmd}'. All DIs are executing your request immediately!"
                st.info(fleet_reply)
                speak_text(fleet_reply)
            else:
                st.warning("Please type a command first, Master David.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Table of Enrolled Digital Intelligences
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🤖 Registered Digital Intelligence Entities")
        st.table(st.session_state.dis)
        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. VIEW 3: SYSTEM ANALYTICS
# -----------------------------------------------------------------------------
elif navigation == "📊 System Analytics":
    st.markdown('<div class="hero-title">Neural Telemetry</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Real-time compute loads and memory utilization.</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📈 Performance Metrics")
    st.line_chart([12, 18, 29, 31, 45, 60, 52, 78, 88, 95])
    st.markdown('</div>', unsafe_allow_html=True)
