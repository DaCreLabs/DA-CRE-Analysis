import io
import streamlit as st
from gtts import gTTS

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="DACRE Analysis Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. SESSION STATE INITIALIZATION ---
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"
if "di_history" not in st.session_state:
    st.session_state.di_history = []
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = "Admin"

# --- 3. DI (DAVID'S INTELLIGENCE) CORE BRAIN ---
def generate_di_response(user_input):
    query = user_input.lower()
    
    # Master recognition trigger
    if any(w in query for w in ["master", "creator", "owner", "who made you", "who built you"]):
        response = "My master is Mr. Uchechukwu David Emenike, the sole admin of the DACRE Analysis app."
        nav = None
    elif "dashboard" in query or "home" in query:
        response = "Navigating to the main Dashboard."
        nav = "Dashboard"
    else:
        response = f"Order received: '{user_input}'. DI is executing."
        nav = None
        
    return response, nav

def speak_text(text):
    tts = gTTS(text=text, lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

# --- 4. SIDEBAR LOGO & DI ASSISTANT ---
with st.sidebar:
    st.title("📊 DACRE Analysis")
    st.caption("Commercial Real Estate Analytics Engine")
    st.markdown("---")
    
    st.subheader("🤖 DI (David's Intelligence)")
    user_query = st.text_input("Talk to DI:", placeholder="Enter command for DI...", key="di_input")
    
    col_send, col_clear = st.columns(2)
    with col_send:
        submit_btn = st.button("Send to DI", use_container_width=True)
    with col_clear:
        if st.button("Clear History", use_container_width=True):
            st.session_state.di_history = []
            st.rerun()

    if submit_btn and user_query:
        di_reply, nav_target = generate_di_response(user_query)
        if nav_target:
            st.session_state.current_page = nav_target
            
        st.session_state.di_history.append({"user": user_query, "di": di_reply})
        
        audio_fp = speak_text(di_reply)
        st.audio(audio_fp, format="audio/mp3", autoplay=True)
        
    if st.session_state.di_history:
        st.markdown("### DI Logs")
        for chat in reversed(st.session_state.di_history):
            st.write(f"🗣️ **Admin:** {chat['user']}")
            st.write(f"🤖 **DI:** {chat['di']}")
            st.markdown("---")

# --- 5. MAIN DASHBOARD CONTENT ---
st.title("📊 DACRE Analysis Platform")

# Dashboard Metrics
st.header("Main Dashboard")
m1, m2, m3, m4 = st.columns(4)
m1.metric("DI Core", "Online")
m2.metric("System Health", "100%")
m3.metric("User Status", st.session_state.logged_in_user)
m4.metric("Version", "v1.0")

st.markdown("---")

# Real Estate Calculator
st.subheader("💡 Commercial Real Estate Calculator")
c1, c2 = st.columns(2)

with c1:
    purchase_price = st.number_input("Purchase Price ($)", value=1000000, step=50000)
    gross_income = st.number_input("Gross Annual Income ($)", value=120000, step=5000)
with c2:
    operating_expenses = st.number_input("Operating Expenses ($)", value=40000, step=2000)
    noi = gross_income - operating_expenses
    st.metric("Net Operating Income (NOI)", f"${noi:,.2f}")

if purchase_price > 0:
    cap_rate = (noi / purchase_price) * 100
    st.metric("Cap Rate", f"{cap_rate:.2f}%")
