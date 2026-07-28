import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sqlite3
import hashlib
import json
import time
from PIL import Image
import os
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="DA-CRE Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DATABASE SETUP (SQLite) ---
DB_FILE = "dacre_platform.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Users Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            middle_name TEXT,
            email TEXT UNIQUE,
            password_hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # File Vault Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS file_vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            filename TEXT,
            file_type TEXT,
            file_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- PASSWORD HASHING ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- AUDIO ASSISTANT ENGINE (JavaScript SpeechSynthesis) ---
def trigger_audio_guide(text_to_speak):
    if st.session_state.get('audio_guide_enabled', False):
        js_code = f"""
        <script>
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance("{text_to_speak}");
                msg.rate = 1.0;
                msg.pitch = 1.0;
                window.speechSynthesis.speak(msg);
            }}
        </script>
        """
        components.html(js_code, height=0, width=0)

# --- SESSION STATE INITIALIZATION ---
if 'loading_complete' not in st.session_state:
    st.session_state['loading_complete'] = False
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user_email' not in st.session_state:
    st.session_state['user_email'] = None
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = ""
if 'active_file_name' not in st.session_state:
    st.session_state['active_file_name'] = None
if 'current_data' not in st.session_state:
    st.session_state['current_data'] = None
if 'audio_guide_enabled' not in st.session_state:
    st.session_state['audio_guide_enabled'] = True

# --- CUSTOM CSS WITH FLOATING/COLOR-SHIFTING LOGO ---
st.markdown("""
    <style>
    .stApp {
        background: #080d16;
        color: #f1f5f9;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Floating & Color-Shifting Animated Logo */
    @keyframes floatAndColorShift {
        0% {
            transform: translateY(0px);
            color: #00f2fe;
            filter: drop-shadow(0 0 15px rgba(0, 242, 254, 0.4));
        }
        33% {
            transform: translateY(-12px);
            color: #38bdf8;
            filter: drop-shadow(0 0 25px rgba(56, 189, 248, 0.7));
        }
        66% {
            transform: translateY(-6px);
            color: #818cf8;
            filter: drop-shadow(0 0 20px rgba(129, 140, 248, 0.6));
        }
        100% {
            transform: translateY(0px);
            color: #00f2fe;
            filter: drop-shadow(0 0 15px rgba(0, 242, 254, 0.4));
        }
    }

    .dacre-animated-logo {
        font-size: 3.8rem;
        font-weight: 900;
        letter-spacing: 5px;
        animation: floatAndColorShift 4s ease-in-out infinite;
        text-align: center;
    }

    .logo-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 70vh;
    }

    .glass-card {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }

    .my-data-pill {
        background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%);
        color: #ffffff;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9rem;
    }

    .my-data-pill-empty {
        background: #1e293b;
        color: #64748b;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)


# --- 1. ANIMATED HOVERING LOADING SCREEN ---
if not st.session_state['loading_complete']:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
            <div class="logo-container">
                <div class="dacre-animated-logo">⚡ DACRE ANALYSIS</div>
                <div style="color: #64748b; letter-spacing: 3px; margin-top: 15px;">INITIALIZING ENTERPRISE ENGINE...</div>
            </div>
        """, unsafe_allow_html=True)
    
    time.sleep(3)
    st.session_state['loading_complete'] = True
    placeholder.empty()
    st.rerun()


# --- 2. AUTHENTICATION (LOGIN & SIGN-UP WITH DATABASE CHECK) ---
elif not st.session_state['authenticated']:
    
    st.markdown("""
        <div style="padding: 1rem 0 1.5rem 0; text-align: center;">
            <div class="dacre-animated-logo" style="font-size: 2.5rem;">⚡ DA-CRE PLATFORM</div>
            <p style="color: #94a3b8; font-size: 1.1rem;">Commercial Real Estate Data & Advanced Analytics Hub</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.1], gap="large")

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if os.path.exists("david_profile.png"):
            img = Image.open("david_profile.png")
            st.image(img, use_container_width=True)
        else:
            st.info("📷 Profile photo (david_profile.png)")

        st.markdown("""
            <div style="text-align: center; margin-top: 15px; padding: 12px; background: rgba(56, 189, 248, 0.1); border-radius: 12px; border: 1px solid rgba(56, 189, 248, 0.3);">
                <h4 style="color: #38bdf8; margin: 0;">Welcome to DA-CRE! 👉</h4>
                <p style="color: #cbd5e1; margin: 5px 0 0 0; font-size: 0.9rem;">Sign in or create a new account on the right to access your database vault.</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        tab_login, tab_signup = st.tabs(["🔒 Log In", "📝 Create Account"])

        # TAB 1: LOG IN
        with tab_login:
            st.subheader("Welcome Back")
            login_email = st.text_input("Email Address", key="login_email")
            login_pass = st.text_input("Password", type="password", key="login_pass")

            if st.button("Log In 🚀", use_container_width=True, type="primary"):
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute("SELECT first_name, middle_name, password_hash FROM users WHERE email = ?", (login_email.strip().lower(),))
                user = c.fetchone()
                conn.close()

                if user and user[2] == hash_password(login_pass):
                    st.session_state['authenticated'] = True
                    st.session_state['user_email'] = login_email.strip().lower()
                    st.session_state['user_name'] = f"{user[0]} {user[1]}".strip()
                    st.success("Log in successful!")
                    trigger_audio_guide("Welcome back! Loading your workspace.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password.")
                    trigger_audio_guide("Invalid credentials entered. Please try again.")

        # TAB 2: SIGN UP
        with tab_signup:
            st.subheader("Create Account")
            fname = st.text_input("First Name", key="su_fname")
            mname = st.text_input("Middle Name (Optional)", key="su_mname")
            su_email = st.text_input("Email Address", key="su_email")
            su_pass = st.text_input("Password", type="password", key="su_pass")

            if st.button("Complete Sign Up 🎯", use_container_width=True):
                if not fname or not su_email or not su_pass:
                    st.warning("Please fill in all required fields.")
                elif "@" not in su_email:
                    st.error("Invalid email address format.")
                else:
                    # Database Duplicate Check
                    conn = sqlite3.connect(DB_FILE)
                    c = conn.cursor()
                    c.execute("SELECT id FROM users WHERE email = ?", (su_email.strip().lower(),))
                    existing_user = c.fetchone()

                    if existing_user:
                        st.error("⚠️ This account has already been added. Please log in!")
                        trigger_audio_guide("This account already exists. Please switch to the log in tab.")
                        conn.close()
                    else:
                        c.execute(
                            "INSERT INTO users (first_name, middle_name, email, password_hash) VALUES (?, ?, ?, ?)",
                            (fname.strip(), mname.strip(), su_email.strip().lower(), hash_password(su_pass))
                        )
                        conn.commit()
                        conn.close()

                        st.session_state['authenticated'] = True
                        st.session_state['user_email'] = su_email.strip().lower()
                        st.session_state['user_name'] = f"{fname} {mname}".strip()
                        st.success("Account created successfully!")
                        trigger_audio_guide("Account successfully created. Opening your workspace.")
                        time.sleep(1)
                        st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


# --- 3. MAIN WORKSPACE DASHBOARD ---
else:
    # TOP HEADER & ACTIVE DATA BADGE
    col_n1, col_n2, col_n3 = st.columns([2, 1, 1])
    with col_n1:
        st.markdown("### ⚡ DA-CRE Analysis Workspace")
    with col_n2:
        # Audio Toggle
        audio_on = st.toggle("🔊 Audio Guide", value=st.session_state['audio_guide_enabled'])
        if audio_on != st.session_state['audio_guide_enabled']:
            st.session_state['audio_guide_enabled'] = audio_on
            if audio_on:
                trigger_audio_guide("Audio guide enabled.")
    with col_n3:
        if st.session_state['active_file_name']:
            st.markdown(f'<div class="my-data-pill">📂 MY DATA: {st.session_state["active_file_name"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="my-data-pill-empty">📂 MY DATA: Empty</div>', unsafe_allow_html=True)

    st.write("---")

    # SIDEBAR PLATFORM NAVIGATION
    st.sidebar.title(f"👤 {st.session_state.get('user_name', 'User')}")
    
    action_choice = st.sidebar.selectbox(
        "Platform Action",
        [
            "📊 Embedded Sheet & Formula Board",
            "📂 Database File Vault",
            "📥 Add New Files to Database",
            "🌐 Web Scraper Engine",
            "📈 Visualizations & Graphs",
            "🚀 Export Data"
        ]
    )

    if st.sidebar.button("🔒 Logout", use_container_width=True):
        st.session_state['authenticated'] = False
        st.session_state['loading_complete'] = True
        st.rerun()

    # SECTION 1: EMBEDDED SHEET & FORMULA BOARD
    if action_choice == "📊 Embedded Sheet & Formula Board":
        st.subheader("📊 Interactive DA-CRE Sheet Editor")
        
        if st.session_state['current_data'] is not None and isinstance(st.session_state['current_data'], pd.DataFrame):
            df = st.session_state['current_data'].copy()

            # TOOLBAR OPTIONS
            st.markdown("##### 🛠️ Quick Action Toolbar")
            tb1, tb2, tb3, tb4 = st.columns(4)
            
            with tb1:
                if st.button("🧹 Remove Duplicates", use_container_width=True):
                    st.session_state['current_data'] = df.drop_duplicates()
                    trigger_audio_guide("Duplicate rows removed from active sheet.")
                    st.success("Duplicates purged!")
                    st.rerun()
            with tb2:
                sort_col = st.selectbox("Sort Column", df.columns, key="sort_col_sb")
                if st.button("Sort (A-Z / Min-Max)", use_container_width=True):
                    st.session_state['current_data'] = df.sort_values(by=sort_col)
                    trigger_audio_guide(f"Data sorted by column {sort_col}")
                    st.rerun()
            with tb3:
                if st.button("Sort (Z-A / Max-Min)", use_container_width=True):
                    st.session_state['current_data'] = df.sort_values(by=sort_col, ascending=False)
                    trigger_audio_guide(f"Data sorted in reverse order by {sort_col}")
                    st.rerun()
            with tb4:
                if st.button("Drop Missing Rows", use_container_width=True):
                    st.session_state['current_data'] = df.dropna()
                    trigger_audio_guide("Missing values removed.")
                    st.rerun()

            st.write("---")

            # FORMULA BOARD ENGINE
            st.markdown("##### 🧮 Formula Board (Excel, Google Sheets, SQL, Python)")
            
            f_cat = st.selectbox("Formula Engine Family", ["Excel / Google Sheets Formulas", "SQL Engine", "Python / Pandas Code"])
            
            if f_cat == "Excel / Google Sheets Formulas":
                excel_formula = st.selectbox("Select Formula", ["SUM (Total of column)", "AVERAGE (Mean of column)", "COUNT (Row count)", "PROFIT MARGIN (Custom Calc)"])
                num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                
                if num_cols:
                    target_c = st.selectbox("Apply to Column", num_cols)
                    if st.button("Execute Formula"):
                        if "SUM" in excel_formula:
                            res = df[target_c].sum()
                            st.info(f"Result = SUM({target_c}): **{res}**")
                            trigger_audio_guide(f"The sum of {target_c} is {res}")
                        elif "AVERAGE" in excel_formula:
                            res = df[target_c].mean()
                            st.info(f"Result = AVERAGE({target_c}): **{res:.2f}**")
                            trigger_audio_guide(f"The average of {target_c} is {res:.2f}")
                        elif "COUNT" in excel_formula:
                            res = df[target_c].count()
                            st.info(f"Result = COUNT({target_c}): **{res}**")
                            trigger_audio_guide(f"Total count is {res}")
                else:
                    st.warning("No numeric columns available for this formula.")

            elif f_cat == "SQL Engine":
                sql_q = st.text_input("Enter SQL Query (Table Name: `df`)", f"SELECT * FROM df LIMIT 10")
                if st.button("Run SQL Query"):
                    try:
                        import sqlite3
                        temp_conn = sqlite3.connect(":memory:")
                        df.to_sql("df", temp_conn, index=False)
                        sql_res = pd.read_sql_query(sql_q, temp_conn)
                        st.dataframe(sql_res)
                        trigger_audio_guide("SQL Query executed successfully.")
                    except Exception as e:
                        st.error(f"SQL Error: {e}")

            elif f_cat == "Python / Pandas Code":
                py_code = st.text_area("Write Python Expression (e.g., `df.describe()`)", "df.describe()")
                if st.button("Run Python Code"):
                    try:
                        py_res = eval(py_code)
                        st.write(py_res)
                        trigger_audio_guide("Python execution complete.")
                    except Exception as e:
                        st.error(f"Python Execution Error: {e}")

            st.write("---")
            st.markdown("##### 📝 Live Data Grid Editor")
            edited_df = st.data_editor(st.session_state['current_data'], num_rows="dynamic", use_container_width=True)
            st.session_state['current_data'] = edited_df

        else:
            st.info("No active dataset loaded in MY DATA. Open or upload a file into your database vault first.")
            if st.button("How do I load data?"):
                trigger_audio_guide("To load data, go to Add New Files to Database in the sidebar.")

    # SECTION 2: DATABASE FILE VAULT
    elif action_choice == "📂 Database File Vault":
        st.subheader("📂 Persistent Database Vault")
        
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT filename, created_at FROM file_vault WHERE user_email = ?", (st.session_state['user_email'],))
        db_files = c.fetchall()
        conn.close()

        if db_files:
            file_names = [f[0] for f in db_files]
            selected_f = st.selectbox("Choose a saved file from your database:", file_names)
            
            if st.button("Open File into Active MY DATA Workspace 🚀"):
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute("SELECT file_data FROM file_vault WHERE user_email = ? AND filename = ?", (st.session_state['user_email'], selected_f))
                blob = c.fetchone()[0]
                conn.close()
                
                df_loaded = pd.read_json(blob)
                st.session_state['current_data'] = df_loaded
                st.session_state['active_file_name'] = selected_f
                st.success(f"'{selected_f}' loaded from Database!")
                trigger_audio_guide(f"Opened file {selected_f} from your persistent database vault.")
                st.rerun()
        else:
            st.info("Your database vault is empty. Upload files in the 'Add New Files' menu.")

    # SECTION 3: ADD NEW FILES TO DATABASE
    elif action_choice == "📥 Add New Files to Database":
        st.subheader("📥 Save Files into Database Vault")
        
        uploaded_files = st.file_uploader("Select CSV or Excel files to store in database", accept_multiple_files=True)
        
        if uploaded_files:
            for file in uploaded_files:
                ext = file.name.split('.')[-1].lower()
                try:
                    df = pd.read_csv(file) if ext == 'csv' else pd.read_excel(file)
                    json_data = df.to_json()
                    
                    conn = sqlite3.connect(DB_FILE)
                    c = conn.cursor()
                    c.execute(
                        "INSERT INTO file_vault (user_email, filename, file_type, file_data) VALUES (?, ?, ?, ?)",
                        (st.session_state['user_email'], file.name, ext, json_data)
                    )
                    conn.commit()
                    conn.close()
                    
                    st.success(f"Saved '{file.name}' permanently into Database Vault!")
                    trigger_audio_guide(f"File {file.name} saved into your database vault.")
                except Exception as e:
                    st.error(f"Error saving {file.name}: {e}")

    # SECTION 4: WEB SCRAPER ENGINE
    elif action_choice == "🌐 Web Scraper Engine":
        st.subheader("🌐 Scrape Data Tables from Web")
        url_in = st.text_input("Enter URL:", "https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue")
        
        if st.button("Extract Data Tables"):
            if url_in:
                try:
                    tables = pd.read_html(url_in)
                    st.success(f"Extracted {len(tables)} tables!")
                    trigger_audio_guide(f"Successfully extracted {len(tables)} tables from the website.")
                    
                    for i, df in enumerate(tables):
                        with st.expander(f"Table #{i+1} ({df.shape[0]} rows x {df.shape[1]} cols)"):
                            st.dataframe(df)
                            fname = f"Web_Table_{i+1}.csv"
                            if st.button(f"Save Table #{i+1} to Database Vault"):
                                conn = sqlite3.connect(DB_FILE)
                                c = conn.cursor()
                                c.execute(
                                    "INSERT INTO file_vault (user_email, filename, file_type, file_data) VALUES (?, ?, ?, ?)",
                                    (st.session_state['user_email'], fname, 'csv', df.to_json())
                                )
                                conn.commit()
                                conn.close()
                                
                                st.session_state['current_data'] = df
                                st.session_state['active_file_name'] = fname
                                st.success(f"Saved {fname} to database!")
                                trigger_audio_guide(f"Saved web table {i+1} to database vault.")
                                st.rerun()
                except Exception as e:
                    st.error(f"Scraper error: {e}")

    # SECTION 5: VISUALIZATIONS & GRAPHS
    elif action_choice == "📈 Visualizations & Graphs":
        st.subheader("📈 Interactive Data Charts")
        if st.session_state['current_data'] is not None and isinstance(st.session_state['current_data'], pd.DataFrame):
            df = st.session_state['current_data']
            num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            all_cols = df.columns.tolist()
            
            if num_cols and len(all_cols) >= 2:
                x_a = st.selectbox("X-Axis", all_cols)
                y_a = st.selectbox("Y-Axis", num_cols)
                style = st.radio("Chart Type", ["Bar", "Line", "Scatter"])
                
                if style == "Bar":
                    fig = px.bar(df, x=x_a, y=y_a, template="plotly_dark")
                elif style == "Line":
                    fig = px.line(df, x=x_a, y=y_a, template="plotly_dark")
                else:
                    fig = px.scatter(df, x=x_a, y=y_a, template="plotly_dark")
                
                st.plotly_chart(fig, use_container_width=True)
                trigger_audio_guide(f"Generated {style} chart for {x_a} and {y_a}")
            else:
                st.warning("Numeric columns required for plotting.")
        else:
            st.info("No active dataset loaded in MY DATA.")

    # SECTION 6: EXPORT DATA
    elif action_choice == "🚀 Export Data":
        st.subheader("🚀 Export Workspace Data")
        if st.session_state['current_data'] is not None and isinstance(st.session_state['current_data'], pd.DataFrame):
            df = st.session_state['current_data']
            
            col_e1, col_e2 = st.columns(2)
            with col_e1:
                st.markdown("#### 🟢 Google Apps")
                st.link_button("Open Google Sheets 🟢", "https://sheets.new", use_container_width=True)
                st.link_button("Open Google Docs 📄", "https://docs.new", use_container_width=True)
                st.link_button("Open Google Slides 📊", "https://slides.new", use_container_width=True)

            with col_e2:
                st.markdown("#### 🔵 Local Export")
                csv_b = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV / Excel File 📥",
                    data=csv_b,
                    file_name=f"DA_CRE_{st.session_state['active_file_name']}",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.info("No active dataset in MY DATA to export.")
