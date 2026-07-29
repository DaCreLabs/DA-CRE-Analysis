import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sqlite3
import hashlib
import time
import io
import json
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="DA-CRE Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADMIN SECURITY KEY ---
ADMIN_SECRET_KEY = "david2026"  # You can change this admin passcode anytime!

# --- DATABASE SETUP (SQLite) ---
DB_FILE = "dacre_platform.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
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
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            user_email TEXT PRIMARY KEY,
            active_file_name TEXT,
            current_data TEXT,
            calculation_history TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- HELPER: AUTO-CLEAN MESSY DATA ---
def clean_messy_dataframe(df):
    cleaned_df = df.copy()
    for col in cleaned_df.columns:
        if cleaned_df[col].dtype == 'object':
            cleaned_col = (
                cleaned_df[col]
                .astype(str)
                .str.replace(r'[\$,%₦€£]', '', regex=True)
                .str.replace(',', '', regex=False)
                .str.strip()
            )
            numeric_series = pd.to_numeric(cleaned_col, errors='ignore')
            cleaned_df[col] = numeric_series
    return cleaned_df

# --- HELPER: UNIVERSAL FILE READER ---
def load_file_data(uploaded_file):
    filename = uploaded_file.name
    ext = filename.split('.')[-1].lower()
    
    if ext in ['xlsx', 'xls']:
        return pd.read_excel(uploaded_file)
    elif ext == 'csv':
        return pd.read_csv(uploaded_file)
    elif ext == 'tsv':
        return pd.read_csv(uploaded_file, sep='\t')
    elif ext == 'json':
        return pd.read_json(uploaded_file)
    elif ext == 'parquet':
        return pd.read_parquet(uploaded_file)
    else:
        raise ValueError(f"Unsupported file format: .{ext}")

# --- PASSWORD HASHING ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- DAVID'S VOICE PITCH SPEECH ENGINE ---
def trigger_audio_guide(text_to_speak):
    if st.session_state.get('audio_guide_enabled', True):
        safe_text = text_to_speak.replace("'", "\\'").replace("\n", " ")
        js_code = f"""
        <script>
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance('{safe_text}');
                msg.rate = 0.82;  /* Calm, deliberate speech pace matching David's video */
                msg.pitch = 0.78; /* Tuned male voice pitch frequency matching David's pitch */
                
                var voices = window.speechSynthesis.getVoices();
                /* Select male / African / English voice if available */
                var selectedVoice = voices.find(function(v) {{
                    return v.lang.includes('en-NG') || v.name.includes('Male') || v.name.includes('David') || v.lang.includes('en-GB');
                }});
                if (selectedVoice) {{
                    msg.voice = selectedVoice;
                }}
                window.speechSynthesis.speak(msg);
            }}
        </script>
        """
        components.html(js_code, height=0, width=0)

# --- WORK PERSISTENCE: SAVE SESSION TO DB ---
def save_user_session():
    if st.session_state.get('authenticated') and st.session_state.get('user_email'):
        email = st.session_state['user_email']
        fname = st.session_state.get('active_file_name')
        
        data_json = ""
        if st.session_state.get('current_data') is not None and isinstance(st.session_state['current_data'], pd.DataFrame):
            data_json = st.session_state['current_data'].to_json()
            
        history_json = json.dumps(st.session_state.get('calculation_history', []))
        
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("""
            INSERT INTO user_sessions (user_email, active_file_name, current_data, calculation_history)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_email) DO UPDATE SET
                active_file_name = excluded.active_file_name,
                current_data = excluded.current_data,
                calculation_history = excluded.calculation_history,
                updated_at = CURRENT_TIMESTAMP
        """, (email, fname, data_json, history_json))
        conn.commit()
        conn.close()

# --- WORK PERSISTENCE: RESTORE SESSION FROM DB ---
def restore_user_session(email):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT active_file_name, current_data, calculation_history FROM user_sessions WHERE user_email = ?", (email,))
    row = c.fetchone()
    conn.close()
    
    if row:
        active_f, data_str, hist_str = row
        st.session_state['active_file_name'] = active_f
        if data_str:
            try:
                st.session_state['current_data'] = pd.read_json(io.StringIO(data_str))
            except Exception:
                st.session_state['current_data'] = None
        else:
            st.session_state['current_data'] = None
            
        if hist_str:
            try:
                st.session_state['calculation_history'] = json.loads(hist_str)
            except Exception:
                st.session_state['calculation_history'] = []
        else:
            st.session_state['calculation_history'] = []

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
if 'calculation_history' not in st.session_state:
    st.session_state['calculation_history'] = []
if 'show_verification' not in st.session_state:
    st.session_state['show_verification'] = False

# --- CUSTOM UI STYLING (LIGHT BLUE, BLACK, YELLOW-GREEN, HOVERING CLOUDS) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #060913;
        color: #e2e8f0;
        font-family: 'Inter', -apple-system, sans-serif;
    }

    @keyframes floatClouds {
        0% { transform: translateY(0px) scale(1); opacity: 0.25; }
        50% { transform: translateY(-25px) scale(1.08); opacity: 0.45; }
        100% { transform: translateY(0px) scale(1); opacity: 0.25; }
    }

    .cloud-bg-container {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        pointer-events: none; z-index: 0; overflow: hidden;
    }

    .cloud-1 {
        position: absolute; top: 8%; left: 10%; width: 450px; height: 250px;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.35) 0%, rgba(6, 9, 19, 0) 70%);
        border-radius: 50%; filter: blur(50px); animation: floatClouds 9s ease-in-out infinite;
    }

    .cloud-2 {
        position: absolute; bottom: 12%; right: 8%; width: 550px; height: 300px;
        background: radial-gradient(circle, rgba(14, 165, 233, 0.3) 0%, rgba(6, 9, 19, 0) 70%);
        border-radius: 50%; filter: blur(60px); animation: floatClouds 12s ease-in-out infinite reverse;
    }

    .black-card {
        background: #000000; border: 2px solid #38bdf8; border-radius: 16px;
        padding: 2.2rem; box-shadow: 0 10px 30px rgba(56, 189, 248, 0.15);
        position: relative; z-index: 1;
    }

    .yg-text { color: #a3e635; font-weight: 800; }
    .yg-badge { background-color: #a3e635; color: #000000; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 0.85rem; }

    .stButton>button {
        background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%);
        color: #000000; font-weight: 700; border: none; border-radius: 10px; transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover { background: #a3e635; color: #000000; transform: translateY(-2px); }
    </style>
""", unsafe_allow_html=True)


# --- 1. INITIAL LOADING SCREEN ---
if not st.session_state['loading_complete']:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
            <div style="display:flex; flex-direction:column; justify-content:center; align-items:center; height:75vh;">
                <h1 style="color:#38bdf8; font-size: 3.5rem; letter-spacing:4px;">⚡ DA-CRE PLATFORM</h1>
                <p style="color:#a3e635; font-size: 1.2rem; letter-spacing:2px; margin-top:10px;">INITIALIZING SYSTEM & DAVID'S VOICE ENGINE...</p>
            </div>
        """, unsafe_allow_html=True)
    
    time.sleep(2)
    st.session_state['loading_complete'] = True
    placeholder.empty()
    st.rerun()


# --- 2. AUTHENTICATION (LOGIN & SIGN-UP) ---
elif not st.session_state['authenticated']:
    
    st.markdown("""
        <div style="text-align: center; margin-top: 2rem; margin-bottom: 2rem;">
            <h1 style="color: #38bdf8; font-size: 3rem; margin-bottom: 0px;">⚡ DA-CRE PLATFORM</h1>
            <p style="color: #a3e635; font-size: 1.1rem; font-weight: 600;">Commercial Real Estate Analytics & Data Suite</p>
        </div>
    """, unsafe_allow_html=True)

    col_center = st.columns([1, 2.2, 1])[1]

    with col_center:
        st.markdown('<div class="black-card">', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔒 Sign In", "📝 Sign Up"])

        # TAB 1: SIGN IN
        with tab1:
            st.markdown("<h3 class='yg-text'>Welcome Back, Sign In</h3>", unsafe_allow_html=True)
            login_email = st.text_input("Email Address", key="login_email")
            login_pass = st.text_input("Password", type="password", key="login_pass")

            if st.button("Log In Now 🚀", use_container_width=True):
                if not login_email or not login_pass:
                    st.warning("Please enter your email and password.")
                    trigger_audio_guide("Hello there. Please enter your email address and password to sign in.")
                else:
                    conn = sqlite3.connect(DB_FILE)
                    c = conn.cursor()
                    c.execute("SELECT first_name, middle_name, password_hash FROM users WHERE email = ?", (login_email.strip().lower(),))
                    user = c.fetchone()
                    conn.close()

                    if user and user[2] == hash_password(login_pass):
                        st.session_state['authenticated'] = True
                        st.session_state['user_email'] = login_email.strip().lower()
                        st.session_state['user_name'] = f"{user[0]} {user[1]}".strip()
                        
                        restore_user_session(st.session_state['user_email'])
                        
                        st.success("Log in successful!")
                        trigger_audio_guide(f"Welcome back {user[0]}! I have restored your previous work session so you can continue where you stopped.")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")
                        trigger_audio_guide("The credentials you entered do not match our system. Please try again.")

        # TAB 2: SIGN UP WITH DUPLICATE HUMAN VERIFICATION
        with tab2:
            st.markdown("<h3 class='yg-text'>Create New Account</h3>", unsafe_allow_html=True)
            fname = st.text_input("First Name", key="su_fname")
            mname = st.text_input("Middle Name (Optional)", key="su_mname")
            su_email = st.text_input("Email Address", key="su_email")
            su_pass = st.text_input("Password", type="password", key="su_pass")

            if st.session_state['show_verification']:
                st.warning("⚠️ This email is already registered in our database.")
                verify_human = st.checkbox("Verify your identity: Check box to confirm you are human")
                
                if verify_human:
                    st.success("✅ Verified Human!")
                    trigger_audio_guide("Identity verified! The details you entered have already been added to our database. I am redirecting you back to sign in.")
                    time.sleep(2.5)
                    st.session_state['show_verification'] = False
                    st.rerun()

            else:
                if st.button("Complete Sign Up 🎯", use_container_width=True):
                    if not fname or not su_email or not su_pass:
                        st.warning("Please fill in all required fields.")
                        trigger_audio_guide("Please fill in all required fields before clicking sign up.")
                    elif "@" not in su_email:
                        st.error("Invalid email address format.")
                        trigger_audio_guide("The email address format is invalid. Please check and try again.")
                    else:
                        conn = sqlite3.connect(DB_FILE)
                        c = conn.cursor()
                        c.execute("SELECT id FROM users WHERE email = ?", (su_email.strip().lower(),))
                        existing_user = c.fetchone()

                        if existing_user:
                            st.session_state['show_verification'] = True
                            trigger_audio_guide("It looks like this account already exists. Please check the verification box to prove you are human.")
                            conn.close()
                            st.rerun()
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
                            trigger_audio_guide(f"Welcome {fname}! Your account has been created. Opening your workspace now.")
                            time.sleep(1)
                            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


# --- 3. MAIN WORKSPACE DASHBOARD ---
else:
    # Floating Blue Cloud Animation Container
    st.markdown("""
        <div class="cloud-bg-container">
            <div class="cloud-1"></div>
            <div class="cloud-2"></div>
        </div>
    """, unsafe_allow_html=True)

    col_n1, col_n2, col_n3 = st.columns([2, 1.2, 1.2])
    with col_n1:
        st.markdown("### ⚡ DA-CRE Analysis Workspace")
    with col_n2:
        audio_on = st.toggle("🔊 Voice Guide", value=st.session_state['audio_guide_enabled'])
        if audio_on != st.session_state['audio_guide_enabled']:
            st.session_state['audio_guide_enabled'] = audio_on
            if audio_on:
                trigger_audio_guide("Voice guide activated. I will explain actions as you navigate through the app.")
    with col_n3:
        if st.session_state['active_file_name']:
            st.markdown(f'<span class="yg-badge">📂 MY DATA: {st.session_state["active_file_name"]}</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span style="color:#64748b; font-weight:bold;">📂 MY DATA: Empty</span>', unsafe_allow_html=True)

    st.write("---")

    st.sidebar.title(f"👤 {st.session_state.get('user_name', 'User')}")
    
    action_choice = st.sidebar.selectbox(
        "Platform Action",
        [
            "📊 Embedded Sheet & Formula Board",
            "📂 Database File Vault",
            "📥 Add New Files to Database",
            "🌐 Web Scraper Engine",
            "📈 Visualizations & Graphs",
            "🚀 Export Data",
            "🛡️ Admin Control Panel"
        ]
    )

    if st.sidebar.button("🔒 Logout & Auto-Save", use_container_width=True):
        save_user_session()
        trigger_audio_guide("Your session data has been saved automatically. Goodbye!")
        time.sleep(1)
        st.session_state['authenticated'] = False
        st.rerun()

    # SECTION 1: EMBEDDED SHEET & FORMULA BOARD
    if action_choice == "📊 Embedded Sheet & Formula Board":
        st.subheader("📊 Interactive DA-CRE Sheet Editor")
        
        if st.session_state['current_data'] is not None and isinstance(st.session_state['current_data'], pd.DataFrame):
            df = st.session_state['current_data'].copy()

            # TOOLBAR WITH ARRANGE DATA
            st.markdown("##### 🛠️ Quick Action Toolbar")
            tb0, tb1, tb2, tb3 = st.columns(4)
            
            with tb0:
                if st.button("✨ Arrange Messy Data", use_container_width=True):
                    cleaned = clean_messy_dataframe(df)
                    st.session_state['current_data'] = cleaned
                    save_user_session()
                    st.success("Messy data arranged! Currency symbols, commas, and text numbers converted into numbers.")
                    trigger_audio_guide("Messy data arranged! Currency symbols and formatting have been cleaned and your numbers are ready for formula calculations.")
                    st.rerun()

            with tb1:
                if st.button("🧹 Remove Duplicates", use_container_width=True):
                    st.session_state['current_data'] = df.drop_duplicates()
                    save_user_session()
                    trigger_audio_guide("Duplicate rows removed from your active sheet.")
                    st.success("Duplicates purged!")
                    st.rerun()
            with tb2:
                sort_col = st.selectbox("Sort Column", df.columns, key="sort_col_sb")
                if st.button("Sort (A-Z / Min-Max)", use_container_width=True):
                    st.session_state['current_data'] = df.sort_values(by=sort_col)
                    save_user_session()
                    trigger_audio_guide(f"Data sorted in ascending order by column {sort_col}.")
                    st.rerun()
            with tb3:
                if st.button("Sort (Z-A / Max-Min)", use_container_width=True):
                    st.session_state['current_data'] = df.sort_values(by=sort_col, ascending=False)
                    save_user_session()
                    trigger_audio_guide(f"Data sorted in descending order by column {sort_col}.")
                    st.rerun()

            st.write("---")

            # FORMULA BOARD ENGINE
            st.markdown("##### 🧮 Formula Board (Excel, Google Sheets, SQL, Python)")
            f_cat = st.selectbox("Formula Engine Family", ["Excel / Google Sheets Formulas", "SQL Engine", "Python / Pandas Code"])
            
            if f_cat == "Excel / Google Sheets Formulas":
                excel_formula = st.selectbox("Select Formula", ["SUM (Total of column)", "AVERAGE (Mean of column)", "COUNT (Row count)"])
                all_cols = df.columns.tolist()
                
                target_c = st.selectbox("Select Target Column", all_cols)
                
                if st.button("Execute Formula 🚀"):
                    series = pd.to_numeric(
                        df[target_c].astype(str).str.replace(r'[\$,%₦€£,]', '', regex=True).str.strip(),
                        errors='coerce'
                    )
                    
                    if "SUM" in excel_formula:
                        res = series.sum()
                        msg = f"SUM({target_c}) = {res:,.2f}"
                        st.info(f"Result: **{msg}**")
                        st.session_state['calculation_history'].append(msg)
                        save_user_session()
                        trigger_audio_guide(f"The total sum for column {target_c} is {res:,.2f}. The result is saved in your calculation workspace.")
                    elif "AVERAGE" in excel_formula:
                        res = series.mean()
                        msg = f"AVERAGE({target_c}) = {res:,.2f}"
                        st.info(f"Result: **{msg}**")
                        st.session_state['calculation_history'].append(msg)
                        save_user_session()
                        trigger_audio_guide(f"The average mean value for column {target_c} is {res:,.2f}.")
                    elif "COUNT" in excel_formula:
                        res = series.count()
                        msg = f"COUNT({target_c}) = {res}"
                        st.info(f"Result: **{msg}**")
                        st.session_state['calculation_history'].append(msg)
                        save_user_session()
                        trigger_audio_guide(f"Total row count for column {target_c} is {res}.")

            elif f_cat == "SQL Engine":
                sql_q = st.text_input("Enter SQL Query (Table Name: `df`)", f"SELECT * FROM df LIMIT 10")
                if st.button("Run SQL Query"):
                    try:
                        temp_conn = sqlite3.connect(":memory:")
                        df.to_sql("df", temp_conn, index=False)
                        sql_res = pd.read_sql_query(sql_q, temp_conn)
                        st.dataframe(sql_res)
                        st.session_state['calculation_history'].append(f"SQL Executed: `{sql_q}`")
                        save_user_session()
                        trigger_audio_guide("SQL query executed successfully.")
                    except Exception as e:
                        st.error(f"SQL Error: {e}")

            elif f_cat == "Python / Pandas Code":
                py_code = st.text_area("Write Python Expression (e.g., `df.describe()`)", "df.describe()")
                if st.button("Run Python Code"):
                    try:
                        py_res = eval(py_code)
                        st.write(py_res)
                        st.session_state['calculation_history'].append(f"Python Executed: `{py_code}`")
                        save_user_session()
                        trigger_audio_guide("Python expression executed successfully.")
                    except Exception as e:
                        st.error(f"Python Execution Error: {e}")

            # AUTOMATIC CALCULATION WORKSPACE & AUDIT LOG
            if st.session_state['calculation_history']:
                st.write("---")
                st.markdown("##### 📋 Live Calculation & Formula Workspace")
                for item in reversed(st.session_state['calculation_history']):
                    st.code(item, language="markdown")

            st.write("---")
            st.markdown("##### 📝 Live Data Grid Editor")
            edited_df = st.data_editor(st.session_state['current_data'], num_rows="dynamic", use_container_width=True)
            if not edited_df.equals(st.session_state['current_data']):
                st.session_state['current_data'] = edited_df
                save_user_session()

        else:
            st.info("No active dataset loaded in MY DATA. Open or upload a file into your database vault first.")
            trigger_audio_guide("Your active workspace is empty right now. Go to the Database Vault or Add New Files menu to load your data.")

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
                
                df_loaded = pd.read_json(io.StringIO(blob))
                st.session_state['current_data'] = df_loaded
                st.session_state['active_file_name'] = selected_f
                save_user_session()
                
                st.success(f"'{selected_f}' loaded from Database!")
                trigger_audio_guide(f"Loaded file {selected_f} into your active workspace.")
                st.rerun()
        else:
            st.info("Your database vault is empty. Upload files in the 'Add New Files' menu.")

    # SECTION 3: ADD NEW FILES TO DATABASE
    elif action_choice == "📥 Add New Files to Database":
        st.subheader("📥 Save Files into Database Vault")
        
        uploaded_files = st.file_uploader(
            "Select files to store in database (.xlsx, .xls, .csv, .tsv, .json, .parquet)", 
            type=['xlsx', 'xls', 'csv', 'tsv', 'json', 'parquet'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            for file in uploaded_files:
                ext = file.name.split('.')[-1].lower()
                try:
                    df = load_file_data(file)
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
                    trigger_audio_guide(f"File {file.name} saved permanently into your database vault.")
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
                    trigger_audio_guide(f"Extracted {len(tables)} tables from website.")
                    
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
                                save_user_session()
                                st.success(f"Saved {fname} to database!")
                                trigger_audio_guide(f"Saved web table {i+1} directly into database vault.")
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
                trigger_audio_guide(f"Generated {style} chart for {x_a} and {y_a}.")
            else:
                st.warning("Numeric columns required for plotting. Click 'Arrange Messy Data' in the Embedded Sheet toolbar first.")
        else:
            st.info("No active dataset loaded in MY DATA.")

    # SECTION 6: EXPORT DATA
    elif action_choice == "🚀 Export Data":
        st.subheader("🚀 Export Workspace Data")
        if st.session_state['current_data'] is not None and isinstance(st.session_state['current_data'], pd.DataFrame):
            df = st.session_state['current_data']
            
            col_e1, col_e2 = st.columns(2)
            with col_e1:
                st.markdown("#### 🟢 Google Apps Integration")
                st.link_button("Open Google Sheets 🟢", "https://sheets.new", use_container_width=True)
                st.link_button("Open Google Docs 📄", "https://docs.new", use_container_width=True)
            with col_e2:
                st.markdown("#### 🔵 Local Export")
                csv_b = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV File 📥",
                    data=csv_b,
                    file_name=f"DA_CRE_{st.session_state['active_file_name'] or 'Export.csv'}",
                    mime="text/csv",
                    use_container_width=True
                )
                trigger_audio_guide("Download your clean dataset as a CSV file.")
        else:
            st.info("No active dataset in MY DATA to export.")

    # SECTION 7: ADMIN CONTROL PANEL (DATABASE ACCESS)
    elif action_choice == "🛡️ Admin Control Panel":
        st.subheader("🛡️ Database Admin Panel")
        
        passkey_input = st.text_input("Enter Admin Security Passkey:", type="password")
        
        if passkey_input == ADMIN_SECRET_KEY:
            st.success("🔓 Access Granted: Connected to SQLite Backend!")
            trigger_audio_guide("Admin access granted. Showing registered user database and system statistics.")
            
            conn = sqlite3.connect(DB_FILE)
            
            # Registered Users Table
            st.markdown("#### 👥 Registered Users List")
            users_df = pd.read_sql_query("SELECT id, first_name, middle_name, email, created_at FROM users", conn)
            st.dataframe(users_df, use_container_width=True)
            st.info(f"Total Registered Users: **{len(users_df)}**")

            st.write("---")

            # Stored Files Table
            st.markdown("#### 📂 Vault File Inventory")
            files_df = pd.read_sql_query("SELECT id, user_email, filename, file_type, created_at FROM file_vault", conn)
            st.dataframe(files_df, use_container_width=True)

            st.write("---")

            # Saved Sessions Table
            st.markdown("#### 💾 Active Work Sessions")
            sessions_df = pd.read_sql_query("SELECT user_email, active_file_name, updated_at FROM user_sessions", conn)
            st.dataframe(sessions_df, use_container_width=True)
            
            conn.close()
        
        elif passkey_input != "":
            st.error("❌ Invalid Admin Passkey.")
            trigger_audio_guide("Invalid admin passkey entered.")
