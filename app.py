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
    st.session_state.logged_in_user = "Guest User"

# --- 3. DI (DAVID'S INTELLIGENCE) ENGINE ---
def generate_di_response(user_input):
    query = user_input.lower()
    
    # Master recognition trigger
    if any(w in query for w in ["master", "creator", "owner", "who made you", "who built you"]):
        response = "My master is Mr. Uchechukwu David Emenike, the sole admin of the DACRE Analysis app."
        nav = None
        
    # App navigation triggers
    elif "formula" in query or "embedded formula" in query:
        response = "Taking you to the Embedded Formula Board right now."
        nav = "Embedded Formula Board"
    elif "dashboard" in query or "home" in query:
        response = "Navigating back to the main Dashboard."
        nav = "Dashboard"
    elif "how to use" in query or "help" in query:
        response = "Welcome to DACRE Analysis! Use the main dashboard for real estate metrics or the Embedded Formula Board for underlying equations."
        nav = None
    else:
        response = f"I received your query: '{user_input}'. As DI, I'm here to assist you with DACRE Analysis."
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
    # App Logo / Header
    st.title("📊 DACRE Analysis")
    st.caption("Commercial Real Estate Analytics Engine")
    st.markdown("---")
    
    # DI Section Header
    st.subheader("🤖 DI (David's Intelligence)")
    
    # DI Chat Input Box
    user_query = st.text_input("Talk to DI:", placeholder="Ask DI or tell it where to navigate...", key="di_input")
    
    col_send, col_clear = st.columns(2)
    with col_send:
        submit_btn = st.button("Send to DI", use_container_width=True)
    with col_clear:
        if st.button("Clear History", use_container_width=True):
            st.session_state.di_history = []
            st.rerun()

    # Process DI Interaction
    if submit_btn and user_query:
        di_reply, nav_target = generate_di_response(user_query)
        
        # Auto Navigation Command from DI
        if nav_target:
            st.session_state.current_page = nav_target
            
        st.session_state.di_history.append({"user": user_query, "di": di_reply})
        
        # Generate and play DI voice
        audio_fp = speak_text(di_reply)
        st.audio(audio_fp, format="audio/mp3", autoplay=True)
        
    # Display DI Conversation History
    if st.session_state.di_history:
        st.markdown("### Conversation")
        for chat in reversed(st.session_state.di_history):
            st.write(f"🗣️ **You:** {chat['user']}")
            st.write(f"🤖 **DI:** {chat['di']}")
            st.markdown("---")

# --- 5. MAIN NAVIGATION BAR ---
st.title("📊 DACRE Analysis Platform")

# Top Navigation Selector
selected_page = st.radio(
    "Select View:", 
    ["Dashboard", "Embedded Formula Board"], 
    index=0 if st.session_state.current_page == "Dashboard" else 1,
    horizontal=True
)

st.session_state.current_page = selected_page

# --- 6. PAGE 1: MAIN DASHBOARD ---
if st.session_state.current_page == "Dashboard":
    st.header("Commercial Real Estate Dashboard")
    st.info("Welcome back. Use DI in the sidebar to ask questions or execute navigation commands.")
    
    # Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Active DI Instance", "Online")
    m2.metric("System Health", "100%")
    m3.metric("Current User", st.session_state.logged_in_user)
    m4.metric("Platform Version", "v1.0")

    st.markdown("---")
    
    # Analysis Calculator Inputs
    st.subheader("💡 Property Investment Calculator")
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
        st.metric("Calculated Capitalization Rate", f"{cap_rate:.2f}%")

# --- 7. PAGE 2: EMBEDDED FORMULA BOARD ---
elif st.session_state.current_page == "Embedded Formula Board":
    st.header("Embedded Formula Board")
    st.write("Reference list of core commercial real estate equations used across the DACRE Analysis platform.")
    
    st.markdown("---")
    
    st.subheader("1. Capitalization Rate (Cap Rate)")
    st.latex(r"Cap\ Rate = \frac{Net\ Operating\ Income\ (NOI)}{Current\ Market\ Value}")
    
    st.subheader("2. Cash-on-Cash Return")
    st.latex(r"Cash\ on\ Cash\ Return = \frac{Annual\ Pre-Tax\ Cash\ Flow}{Total\ Cash\ Invested}")
    
    st.subheader("3. Debt Service Coverage Ratio (DSCR)")
    st.latex(r"DSCR = \frac{Net\ Operating\ Income\ (NOI)}{Total\ Debt\ Service}")
    
    st.subheader("4. Gross Rent Multiplier (GRM)")
    st.latex(r"GRM = \frac{Property\ Price}{Gross\ Annual\ Rent}")
