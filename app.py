import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import hashlib
import time
import io
import json
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="DA-CRE Workflow Engine",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADMIN SECURITY KEY ---
ADMIN_SECRET_KEY = "theWORDofGOD"

# --- DATABASE SETUP (SQLite Backend) ---
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
        CREATE TABLE IF NOT EXISTS database_workflow (
            user_email TEXT PRIMARY KEY,
            active_filename TEXT,
            raw_extracted_data TEXT,
            processed_data TEXT,
            formula_logs TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- HELPER: ADVANCED DATA CLEANUP ENGINE ---
def arrange_and_clean_data(df):
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

# --- HELPER: FILE READER ---
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

# --- IMPROVED VOICE ENGINE (BROWSER & USER-GESTURE COMPATIBLE) ---
def trigger_audio_guide(text_to_speak):
    st.session_state['last_audio_text'] = text_to_speak
    safe_text = text_to_speak.replace("'", "\\'").replace("\n", " ")
    
    js_code = f"""
    <div style="margin: 10px 0;">
        <button onclick="speakText()" style="
            background-color: #38bdf8; 
            color: #000000; 
            font-weight: bold; 
            padding: 8px 16px; 
            border: none; 
            border-radius: 6px; 
            cursor: pointer;">
            🔊 Play Audio Assistant
        </button>
    </div>
    <script>
        function speakText() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance('{safe_text}');
                msg.rate = 0.9;
                msg.pitch = 1.0;
                
                var voices = window.speechSynthesis.getVoices();
                if (voices.length > 0) {{
                    var selectedVoice = voices.find(v => v.lang.includes('en'));
                    if (selectedVoice) msg.voice = selectedVoice;
                }}
                window.speechSynthesis.speak(msg);
            }} else {{
                alert("Speech synthesis is not supported in this browser.");
            }}
        }}
        // Attempt autoplay
        setTimeout(speakText, 300);
    </script>
    """
    components.html(js_code, height=60)

# --- WORKFLOW DATABASE SYNC ENGINE ---
def sync_to_database_workflow():
    if st.session_state.get('authenticated') and st.session_state.get('user_email'):
        email = st.session_state['user_email']
        fname = st.session_state.get('active_file_name', 'Untitled')
        
        raw_json = ""
        if st.session_state.get('raw_data') is not None and isinstance(st.session_state['raw_data'], pd.DataFrame):
            raw_json = st.session_state['raw_data'].to_json()

        processed_json = ""
        if st.session_state.get('current_data') is not None and isinstance(st.session_state['current_data'], pd.DataFrame):
            processed_json = st.session_state['current_data'].to_json()
            
        logs_json = json.dumps(st.session_state.get('formula_logs', []))
        
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("""
            INSERT INTO database_workflow (user_email, active_filename, raw_extracted_data, processed_data, formula_logs)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_email) DO UPDATE SET
                active_filename = excluded.active_filename,
                raw_extracted_data = excluded.raw_extracted_data,
                processed_data = excluded.processed_data,
                formula_logs = excluded.formula_logs,
                updated_at = CURRENT_TIMESTAMP
        """, (email, fname, raw_json, processed_json, logs_json))
        conn.commit()
        conn.close()

def restore_from_database_workflow(email):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT active_filename, raw_extracted_data, processed_data, formula_logs FROM database_workflow WHERE user_email = ?", (email,))
    row = c.fetchone()
    conn.close()
    
    if row:
        active_f, raw_str, proc_str, logs_str = row
        st.session_state['active_file_name'] = active_f
        
        if proc_str:
            try:
                st.session_state['current_data'] = pd.read_json(io.StringIO(proc_str))
            except Exception:
                st.session_state['current_data'] = None
                
        if raw_str:
            try:
                st.session_state['raw_data'] = pd.read_json(io.StringIO(raw_str))
            except Exception:
                st.session_state['raw_data'] = None

        if logs_str:
            try:
                st.session_state['formula_logs'] = json.loads(logs_str)
            except Exception:
                st.session_state['formula_logs'] = []

# --- INITIAL SESSION STATES ---
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
if 'raw_data' not in st.session_state:
    st.session_state['raw_data'] = None
if 'formula_logs' not in st.session_state:
    st.session_state['formula_logs'] = []
if 'last_audio_text' not in st.session_state:
    st.session_state['last_audio_text'] = None

# --- HIGH-CONTRAST STYLING ---
st.markdown("""
    <style>
    /* Dark Theme Core */
    .stApp { background-color: #0b0f19; color: #f8fafc; font-family: 'Inter', sans-serif; }
    
    /* Input Fields & Dropdowns - High Contrast Bold Text */
    input, textarea, [data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 8px !important;
    }
    
    /* Dropdown Options Text */
    div[role="listbox"] div {
        color: #000000 !important;
        font-weight: 700 !important;
    }
    
    /* Input Labels */
    label, .stMarkdown label {
        color: #38bdf8 !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
    }
    
    /* Buttons Styling */
    .stButton>button {
        background-color: #0284c7 !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        border-radius: 8px !important;
        border: none !important;
    }
    .stButton>button:hover {
        background-color: #0369a1 !important;
    }
    
    /* Character Logo Styling */
    .logo-container {
        text-align: center;
        padding: 10px;
    }
    .logo-img {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        border: 4px solid #38bdf8;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# --- APP FLOW ---
if not st.session_state['loading_complete']:
    time.sleep(1)
    st.session_state['loading_complete'] = True
    st.rerun()

elif not st.session_state['authenticated']:
    # ONLINE CHARACTER LOGO
    st.markdown("""
        <div class="logo-container">
            <img class="logo-img" src="https://img.freepik.com/free-vector/gradient-ai-avatar_23-2150529851.jpg" alt="DA-CRE Logo"/>
            <h1 style='color:#38bdf8; font-weight:900; margin-top:10px;'>DA-CRE WORKFLOW PLATFORM</h1>
        </div>
    """, unsafe_allow_html=True)

    col_c = st.columns([1, 2, 1])[1]
    with col_c:
        tab1, tab2 = st.tabs(["🔒 Sign In", "📝 Sign Up"])
        with tab1:
            l_email = st.text_input("Email", placeholder="Enter your registered email address...", key="l_e")
            l_pass = st.text_input("Password", type="password", placeholder="Enter your account password...", key="l_p")
            if st.button("Log In", use_container_width=True):
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute("SELECT first_name, password_hash FROM users WHERE email = ?", (l_email.strip().lower(),))
                u = c.fetchone()
                conn.close()
                if u and u[1] == hash_password(l_pass):
                    st.session_state['authenticated'] = True
                    st.session_state['user_email'] = l_email.strip().lower()
                    st.session_state['user_name'] = u[0]
                    restore_from_database_workflow(st.session_state['user_email'])
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
        with tab2:
            s_fname = st.text_input("First Name", placeholder="Enter your first name...", key="s_fn")
            s_email = st.text_input("Email", placeholder="Enter your email address...", key="s_e")
            s_pass = st.text_input("Password", type="password", placeholder="Create a strong password...", key="s_p")
            if st.button("Sign Up", use_container_width=True):
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute("INSERT INTO users (first_name, email, password_hash) VALUES (?, ?, ?)", 
                          (s_fname, s_email.strip().lower(), hash_password(s_pass)))
                conn.commit()
                conn.close()
                st.session_state['authenticated'] = True
                st.session_state['user_email'] = s_email.strip().lower()
                st.session_state['user_name'] = s_fname
                st.rerun()

else:
    # --- SIDEBAR NAVIGATION WITH CHARACTER LOGO ---
    st.sidebar.markdown("""
        <div style="text-align:center;">
            <img src="https://img.freepik.com/free-vector/gradient-ai-avatar_23-2150529851.jpg" style="width:80px; height:80px; border-radius:50%; border:3px solid #38bdf8;"/>
        </div>
    """, unsafe_allow_html=True)
    st.sidebar.title(f"👤 {st.session_state['user_name']}")
    
    menu = st.sidebar.selectbox(
        "Workflow Engine Nav",
        [
            "📊 Embedded Sheet & Formula Board",
            "📂 File Vault to Workflow Engine",
            "📥 Add New Files to Vault",
            "🛡️ Admin Control Panel"
        ]
    )

    if st.sidebar.button("Logout"):
        sync_to_database_workflow()
        st.session_state['authenticated'] = False
        st.rerun()

    # --- PRIMARY WORKFLOW PAGE ---
    if menu == "📊 Embedded Sheet & Formula Board":
        st.title("📊 Embedded Sheet & Formula Board")

        if st.session_state.get('last_audio_text'):
            trigger_audio_guide(st.session_state['last_audio_text'])

        if st.session_state['current_data'] is not None and isinstance(st.session_state['current_data'], pd.DataFrame):
            
            # ==========================================
            # 1. READ-ONLY DATA BOARD (DISPLAY ONLY)
            # ==========================================
            st.markdown("### 📋 DATA BOARD (Read-Only Preview & Export)")
            st.caption("Displays changes from the database_workflow below. Use the download button to print or export to your local computer.")

            # READ-ONLY DISPLAY GRID
            st.dataframe(
                st.session_state['current_data'],
                use_container_width=True
            )

            # PERMANENT DOWNLOAD & PRINT BUTTONS
            st.markdown("##### 💾 Download or Print Finalized Work Sheet")
            csv_data = st.session_state['current_data'].to_csv(index=False).encode('utf-8')
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.download_button(
                    label="⬇️ Download Sheet Permanently to Computer (.csv)",
                    data=csv_data,
                    file_name=f"Finalized_{st.session_state['active_file_name'] or 'Sheet'}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with col_d2:
                js_print = """<button onclick="window.print()" style="width:100%; height:42px; background-color:#10b981; color:white; font-weight:bold; border:none; border-radius:8px; cursor:pointer;">🖨️ Print Data Board Sheet</button>"""
                components.html(js_print, height=45)

            st.write("---")

            # ==========================================
            # 2. DATABASE WORKFLOW GRID & CLEANUP ENGINE
            # ==========================================
            st.markdown("### ⚙️ DATABASE WORKFLOW TABLE (Editable Working Area)")
            st.caption("Click column headers/rows to highlight, edit cells directly, or arrange data. All updates instantly sync above.")

            # ENHANCED EDITABLE GRID WITH COLUMN/ROW HIGHLIGHT SELECTION
           selection_mode="multi-column",
                st.session_state['current_data'],
                num_rows="dynamic",
                use_container_width=True,
                selection_mode=["multi-column", "multi-row"],
                key="database_workflow_editor"
            )

            if not edited_df.equals(st.session_state['current_data']):
                st.session_state['current_data'] = edited_df
                sync_to_database_workflow()

            st.write(" ")
            
            # CLEANUP TOOLBAR
            c1, c2, c3, c4 = st.columns(4)
            df = st.session_state['current_data'].copy()

            with c1:
                if st.button("✨ Arrange Data", use_container_width=True):
                    cleaned_df = arrange_and_clean_data(df)
                    st.session_state['current_data'] = cleaned_df
                    sync_to_database_workflow()
                    st.session_state['last_audio_text'] = "Data arranged and formatted successfully on the Data Board."
                    st.success("Data arranged and formatting cleaned!")
                    st.rerun()

            with c2:
                if st.button("🧹 Remove Duplicates", use_container_width=True):
                    no_dup_df = df.drop_duplicates()
                    st.session_state['current_data'] = no_dup_df
                    sync_to_database_workflow()
                    st.session_state['last_audio_text'] = "Duplicate rows removed from workflow data."
                    st.success("Duplicate rows removed!")
                    st.rerun()

            with c3:
                sort_column = st.selectbox("Select Sort Target Column", df.columns, key="sort_col")
                if st.button("🔼 Sort Ascending", use_container_width=True):
                    st.session_state['current_data'] = df.sort_values(by=sort_column, ascending=True)
                    sync_to_database_workflow()
                    st.rerun()

            with c4:
                if st.button("🔽 Sort Descending", use_container_width=True):
                    st.session_state['current_data'] = df.sort_values(by=sort_column, ascending=False)
                    sync_to_database_workflow()
                    st.rerun()

            st.write("---")

            # ==========================================
            # 3. SHEET FORMULAS DROPDOWN ENGINE
            # ==========================================
            st.markdown("### 📐 SHEET FORMULAS (EXCEL & GOOGLE SHEETS DROPDOWN)")
            
            all_formulas = [
                "VLOOKUP", "XLOOKUP", "HLOOKUP", "INDEX / MATCH", "INDIRECT", "OFFSET", "IMPORTRANGE",
                "IF", "IFS", "IFERROR", "IFNA", "AND", "OR", "XOR", "NOT", "SWITCH",
                "SUM", "SUMIF", "SUMIFS", "COUNT", "COUNTA", "COUNTIF", "COUNTIFS", "AVERAGE", "AVERAGEIF", "AVERAGEIFS", "MAX", "MIN", "PRODUCT",
                "CONCATENATE", "TEXTJOIN", "SPLIT", "UPPER", "LOWER", "PROPER", "TRIM", "CLEAN", "LEFT", "RIGHT", "MID", "LEN", "SUBSTITUTE", "REPLACE", "REGEXEXTRACT", "REGEXREPLACE",
                "ARRAYFORMULA", "QUERY", "FILTER", "SORT", "SORTBY", "UNIQUE", "SEQUENCE", "RANDARRAY", "FLATTEN", "TRANSPOSE",
                "TODAY", "NOW", "DATE", "DATEDIF", "YEAR", "MONTH", "DAY", "EDATE", "EOMONTH",
                "LAMBDA", "MAP", "REDUCE", "BYROW", "BYCOL"
            ]

            selected_formula = st.selectbox("🔍 Choose Formula to Apply", all_formulas, key="sheet_formula_dropdown")

            st.markdown(f"**Execute `={selected_formula}()` on Database Workflow:**")
            
            p_col1, p_col2, p_col3 = st.columns(3)

            if selected_formula in ["VLOOKUP", "XLOOKUP"]:
                with p_col1: lookup_key_col = st.selectbox("Search Key Column", df.columns, key="v_key")
                with p_col2: return_target_col = st.selectbox("Return Value Column", df.columns, key="v_ret")
                with p_col3: search_value = st.text_input("Enter Key Value to Search", placeholder="e.g. A26 5G...", key="v_val")
                
                if st.button("OK - Apply Formula", use_container_width=True):
                    matched = df[df[lookup_key_col].astype(str) == str(search_value)]
                    if not matched.empty:
                        res_val = matched[return_target_col].values[0]
                        st.success(f"Result for {selected_formula}('{search_value}'): **{res_val}**")
                        st.session_state['formula_logs'].append(f"{selected_formula}('{search_value}') -> {res_val}")
                        sync_to_database_workflow()
                    else:
                        st.warning("No matching row found in dataset.")

            elif selected_formula == "CONCATENATE":
                with p_col1: c_first = st.selectbox("First Text Column", df.columns, key="c_1")
                with p_col2: c_second = st.selectbox("Second Text Column", df.columns, key="c_2")
                with p_col3: new_c_name = st.text_input("New Result Header", placeholder="Combined_Column_Name", key="c_name")

                if st.button("OK - Apply Formula", use_container_width=True):
                    st.session_state['current_data'][new_c_name] = df[c_first].astype(str) + " " + df[c_second].astype(str)
                    sync_to_database_workflow()
                    st.success(f"Formula evaluated! New column '{new_c_name}' added to DATA BOARD.")
                    st.rerun()

            elif selected_formula in ["SUMIF", "COUNTIF"]:
                with p_col1: cond_c = st.selectbox("Condition Column", df.columns, key="cond_col")
                with p_col2: cond_v = st.text_input("Condition Match Value", placeholder="Enter value to match...", key="cond_val")
                with p_col3: 
                    target_s = st.selectbox("Sum Target Column", df.columns, key="sum_target") if selected_formula == "SUMIF" else None

                if st.button("OK - Apply Formula", use_container_width=True):
                    filtered_rows = df[df[cond_c].astype(str) == str(cond_v)]
                    if selected_formula == "SUMIF":
                        total_sum = pd.to_numeric(filtered_rows[target_s], errors='coerce').sum()
                        st.success(f"{selected_formula} Result: **{total_sum:,.2f}**")
                    else:
                        count_res = len(filtered_rows)
                        st.success(f"{selected_formula} Result: **{count_res} rows matched**")
                    
                    st.session_state['formula_logs'].append(f"{selected_formula}(Condition: {cond_v})")
                    sync_to_database_workflow()

            elif selected_formula in ["UPPER", "LOWER", "TRIM"]:
                with p_col1: target_text_col = st.selectbox("Target Column", df.columns, key="txt_col")
                
                if st.button("OK - Apply Formula", use_container_width=True):
                    if selected_formula == "UPPER":
                        st.session_state['current_data'][target_text_col] = df[target_text_col].astype(str).str.upper()
                    elif selected_formula == "LOWER":
                        st.session_state['current_data'][target_text_col] = df[target_text_col].astype(str).str.lower()
                    elif selected_formula == "TRIM":
                        st.session_state['current_data'][target_text_col] = df[target_text_col].astype(str).str.strip()
                    
                    sync_to_database_workflow()
                    st.success(f"Applied {selected_formula} to column '{target_text_col}' on DATA BOARD!")
                    st.rerun()

            else:
                st.info(f"Formula **`={selected_formula}()`** is ready in the workflow engine.")

        else:
            st.info("No active dataset in the database_workflow. Please select or extract a file from the File Vault menu.")

    # --- WORKFLOW: FILE VAULT TRANSFER ---
    elif menu == "📂 File Vault to Workflow Engine":
        st.title("📂 Database File Vault")
        st.caption("Select files from your vault to automatically extract and push into database_workflow.")

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT filename FROM file_vault WHERE user_email = ?", (st.session_state['user_email'],))
        file_list = c.fetchall()
        conn.close()

        if file_list:
            selected_file = st.selectbox("Select File from Vault:", [f[0] for f in file_list])
            if st.button("Extract Data & Push to Database Workflow 🚀", use_container_width=True):
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute("SELECT file_data FROM file_vault WHERE user_email = ? AND filename = ?", (st.session_state['user_email'], selected_file))
                b_data = c.fetchone()[0]
                conn.close()

                extracted_df = pd.read_json(io.StringIO(b_data))
                st.session_state['raw_data'] = extracted_df.copy()
                st.session_state['current_data'] = extracted_df.copy()
                st.session_state['active_file_name'] = selected_file
                st.session_state['last_audio_text'] = f"Extracted {selected_file} into workflow database."
                
                sync_to_database_workflow()
                st.success(f"Successfully extracted `{selected_file}` into database_workflow table and populated DATA BOARD!")
                st.rerun()
        else:
            st.warning("Your File Vault is currently empty. Upload files in the 'Add New Files to Vault' tab.")

    # --- WORKFLOW: UPLOAD FILES ---
    elif menu == "📥 Add New Files to Vault":
        st.title("📥 Upload New File to Vault")
        uploaded_file = st.file_uploader("Choose Excel or CSV File", type=['xlsx', 'xls', 'csv'])
        if uploaded_file:
            if st.button("Save to File Vault 💾", use_container_width=True):
                df_uploaded = load_file_data(uploaded_file)
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute("INSERT INTO file_vault (user_email, filename, file_type, file_data) VALUES (?, ?, ?, ?)",
                          (st.session_state['user_email'], uploaded_file.name, 'excel', df_uploaded.to_json()))
                conn.commit()
                conn.close()
                st.success(f"Saved `{uploaded_file.name}` to File Vault!")

    # --- WORKFLOW: ADMIN CONTROL PANEL ---
    elif menu == "🛡️ Admin Control Panel":
        st.title("🛡️ Admin Control Panel")
        passkey = st.text_input("Enter Admin Security Passkey", type="password", placeholder="Enter admin lock passkey...")
        if passkey == ADMIN_SECRET_KEY:
            st.success("Admin Access Granted!")
            conn = sqlite3.connect(DB_FILE)
            st.markdown("##### Registered System Users")
            st.dataframe(pd.read_sql_query("SELECT id, first_name, email, created_at FROM users", conn), use_container_width=True)
            st.markdown("##### Database Workflow Records")
            st.dataframe(pd.read_sql_query("SELECT user_email, active_filename, updated_at FROM database_workflow", conn), use_container_width=True)
            conn.close()
        elif passkey:
            st.error("Incorrect Admin Passkey.")
