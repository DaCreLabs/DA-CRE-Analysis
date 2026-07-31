import io
import streamlit as st
from gtts import gTTS

# Page Configuration
st.set_page_config(
    page_title="DACRE Analysis with DI",
    page_icon="🤖",
    layout="wide"
)

# Initialize Session States
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"
if "di_history" not in st.session_state:
    st.session_state.di_history = []
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = "Guest User"

# --- DI KNOWLEDGE BASE & CORE BRAIN ---
DI_SYSTEM_PROMPT = """
You are DI (David's Intelligence), the built-in AI assistant for the DACRE Analysis platform.
Your master and sole creator is Mr. Uchechukwu David Emenike, the sole admin of DACRE Analysis.

Rules:
1. If asked about your creator, master, or owner, respond: 
   "My master is Mr. Uchechukwu David Emenike, the sole admin of the DACRE Analysis app."
2. You assist users with real estate analysis, embedded formulas, and site navigation.
"""

def generate_di_response(user_input):
    """Processes user queries and returns DI's response with navigation triggers."""
    query = user_input.lower()
    
    # Master recognition trigger
    if any(w in query for w in ["master", "creator", "owner", "who made you", "who built you"]):
        response = "My master is Mr. Uchechukwu David Emenike, the sole admin of the DACRE Analysis app."
        nav = None
        
    # Navigation triggers
    elif "formula" in query or "embedded formula" in query:
        response = "Taking you to the Embedded Formula Board right now."
        nav = "Embedded Formula Board"
    elif "dashboard" in query or "home" in query:
        response = "Navigating back to the main Dashboard."
        nav = "Dashboard"
    elif "how to use" in query or "help" in query:
        response = "Welcome to DACRE Analysis! You can analyze commercial real estate data on the Dashboard or view core calculations on the Embedded Formula Board."
        nav = None
    else:
        response = f"I received your request: '{user_input}'. As DI, I'm here to assist you with DACRE Analysis."
        nav = None
        
    return response, nav

def speak_text(text):
    """Generates audio for DI's voice output."""
    tts = gTTS(text=text, lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

# --- SIDEBAR: DI (DAVID'S INTELLIGENCE) ---
with st.sidebar:
    st.title("🤖 DI (David's Intelligence)")
    st.caption("Powered by David's Intelligence Engine")
    st.markdown("---")
    
    # DI Chat Input
    user_query = st.text_input("Talk to DI:", placeholder="Ask DI anything or tell it where to take you...")
    
    col_send, col_clear = st.columns(2)
    with col_send:
        submit_btn = st.button("Send to DI", use_container_width=True)
    with col_clear:
        if st.button("Clear History", use_container_width=True):
            st.session_state.di_history = []
            st.rerun()

    if submit_btn and user_query:
        di_reply, nav_target = generate_di_response(user_query)
        
        # If DI orders a navigation action
        if nav_target:
            st.session_state.current_page = nav_target
            
        # Store chat
        st.session_state.di_history.append({"user": user_query, "di": di_reply})
        
        # Audio Playback (DI Speaking)
        audio_fp = speak_text(di_reply)
        st.audio(audio_fp, format="audio/mp3", autoplay=True)
        
    # Display Chat History
    st.markdown("### Conversation with DI")
    for chat in reversed(st.session_state.di_history):
        st.write(f"🗣️ **You:** {chat['user']}")
        st.write(f"🤖 **DI:** {chat['di']}")
        st.markdown("---")

# --- MAIN APP NAVIGATION & CONTENT ---
st.title("📊 DACRE Analysis Platform")

# Top Navigation Tabs
nav_selection = st.radio(
    "Navigation", 
    ["Dashboard", "Embedded Formula Board"], 
    index=0 if st.session_state.current_page == "Dashboard" else 1,
    horizontal=True
)

st.session_state.current_page = nav_selection

# --- PAGE 1: DASHBOARD ---
if st.session_state.current_page == "Dashboard":
    st.header("Main Dashboard")
    st.info("Welcome to the main analytics suite. Ask DI on the sidebar to guide you or take you to other boards.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Active DI Instances", "1 Online")
    col2.metric("System Status", "Operational")
    col3.metric("Current User", st.session_state.logged_in_user)

# --- PAGE 2: EMBEDDED FORMULA BOARD ---
elif st.session_state.current_page == "Embedded Formula Board":
    st.header("Embedded Formula Board")
    st.success("You are now on the Embedded Formula Board.")
    
    st.subheader("Commercial Real Estate Formulas")
    st.latex(r"Cap\ Rate = \frac{Net\ Operating\ Income\ (NOI)}{Current\ Market\ Value}")
    st.latex(r"Cash\ on\ Cash\ Return = \frac{Annual\ Pre-Tax\ Cash\ Flow}{Total\ Cash\ Invested}")
