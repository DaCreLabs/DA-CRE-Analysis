import hashlib
import io
import json
import os
import re
import sqlite3
import urllib.parse
import urllib.request

try:
    import speech_recognition as sr
except Exception:
    sr = None

from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

# =============================================================================
# DACRE ANALYSIS ENGINE
# DI = DAVID'S INTELLIGENCE
# Enhanced build: landing page + natural DI chat + voice + company admin portal
# + audit/notifications + optional online knowledge.
# Existing analytics, formulas, charts, vault and exports are retained.
# =============================================================================

APP_NAME = "DACRE Analysis"
DI_NAME = "DI — David's Intelligence"
MASTER_USERNAME = "david"
MASTER_FULL_NAME = "David Emenike"
MASTER_PASSKEY = os.getenv("DACRE_MASTER_PASSKEY", "theWORDofGOD@111")

BASE_DIR = Path(__file__).resolve().parent
LOGO_CANDIDATES = [
    "ChatGPT Image Jul 29, 2026, 02_27_41 PM.png",
    "dacre_logo.png",
    "logo.png",
]
LOGO_PATH = next((BASE_DIR / x for x in LOGO_CANDIDATES if (BASE_DIR / x).exists()), BASE_DIR / LOGO_CANDIDATES[0])
FAVICON_PATH = BASE_DIR / ".dacre_favicon.png"
DB_PATH = BASE_DIR / "dacre_platform.db"

# =============================================================================
# BRAND / FAVICON
# =============================================================================

def prepare_favicon():
    if not LOGO_PATH.exists():
        return None
    try:
        source = Image.open(LOGO_PATH).convert("RGBA")
        width, height = source.size
        top = int(height * 0.08)
        bottom = int(height * 0.64)
        crop = source.crop((0, top, width, bottom))
        side = min(crop.size)
        left = (crop.width - side) // 2
        crop_top = max(0, (crop.height - side) // 2)
        crop = crop.crop((left, crop_top, left + side, crop_top + side))
        crop.thumbnail((128, 128), Image.Resampling.LANCZOS)
        crop.save(FAVICON_PATH, format="PNG", optimize=True)
        return str(FAVICON_PATH)
    except Exception:
        return str(LOGO_PATH)

FAVICON = prepare_favicon()

st.set_page_config(
    page_title=f"{APP_NAME} | {DI_NAME}",
    page_icon=FAVICON if FAVICON else "📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# DATABASE
# =============================================================================

def db():
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con


def hash_password(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def init_db():
    con = db()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            owner_username TEXT NOT NULL,
            admin_password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            company_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            email_password TEXT,
            password_hash TEXT NOT NULL,
            passkey_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            login_count INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            last_login TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            company_name TEXT NOT NULL,
            filename TEXT NOT NULL,
            file_type TEXT NOT NULL,
            file_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            company_name TEXT NOT NULL,
            project_name TEXT NOT NULL,
            active_filename TEXT,
            raw_json TEXT,
            processed_json TEXT,
            formula_logs TEXT,
            chart_config TEXT,
            updated_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            company_name TEXT NOT NULL,
            action TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS emails_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient_email TEXT NOT NULL,
            recipient_name TEXT NOT NULL,
            company_name TEXT NOT NULL,
            subject TEXT NOT NULL,
            body TEXT NOT NULL,
            sender_email TEXT,
            status TEXT NOT NULL,
            sent_at TEXT NOT NULL
        )
    """)

    # New additions; IF NOT EXISTS keeps existing databases intact.
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            target_username TEXT,
            event_type TEXT NOT NULL,
            message TEXT NOT NULL,
            is_read INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            company_name TEXT NOT NULL,
            sender TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    con.commit()
    con.close()


init_db()


def ensure_master():
    con = db()
    cur = con.cursor()
    cur.execute("SELECT id FROM users WHERE username = ?", (MASTER_USERNAME,))
    if not cur.fetchone():
        now = datetime.now().isoformat(timespec="seconds")
        cur.execute("""
            INSERT INTO users
            (first_name, last_name, username, company_name, email, email_password,
             password_hash, passkey_hash, role, login_count, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "David", "Emenike", MASTER_USERNAME, "DACRE MASTER", "master@dacre.local", "",
            hash_password(MASTER_PASSKEY), hash_password(MASTER_PASSKEY), "master", 0, now,
        ))
        con.commit()
    con.close()


ensure_master()


def log_activity(username, company, action, notify_admin=True):
    now = datetime.now().isoformat(timespec="seconds")
    con = db()
    con.execute(
        "INSERT INTO activity(username, company_name, action, created_at) VALUES (?, ?, ?, ?)",
        (username, company, action, now),
    )
    if notify_admin and company and company.upper() != "DACRE MASTER":
        con.execute(
            "INSERT INTO notifications(company_name, target_username, event_type, message, created_at) VALUES (?, ?, ?, ?, ?)",
            (company, None, "activity", f"{username}: {action}", now),
        )
    con.commit()
    con.close()


def notify_company_admin(company, message, event_type="system"):
    con = db()
    now = datetime.now().isoformat(timespec="seconds")
    con.execute(
        "INSERT INTO notifications(company_name, target_username, event_type, message, created_at) VALUES (?, ?, ?, ?, ?)",
        (company, None, event_type, message, now),
    )
    con.commit()
    con.close()

# =============================================================================
# EMAIL / ADMIN DI MAIL SOURCE
# =============================================================================

def send_di_welcome_email(first_name, last_name, company_name, email, email_password=""):
    full_name = f"{first_name} {last_name}".strip()
    subject = f"Welcome to DACRE Analysis — DI is now active for {company_name}!"
    body = (
        f"Hello {first_name},\n\n"
        "Welcome to DACRE Analysis. I am DI (David's Intelligence), your business and data intelligence copilot.\n\n"
        f"Your workspace for {company_name} is now active. You can upload datasets, clean and analyse them, build charts, "
        "export results and chat with DI about your workspace.\n\n"
        "Warm regards,\nDI — David's Intelligence\nDACRE Analysis Platform"
    )

    status = "Logged & Dispatched (SMTP if configured; otherwise simulated)"
    smtp_host = os.getenv("DACRE_SMTP_HOST", "")
    smtp_port = int(os.getenv("DACRE_SMTP_PORT", "587"))
    smtp_user = os.getenv("DACRE_SMTP_USER", "")
    smtp_pass = os.getenv("DACRE_SMTP_PASSWORD", "")
    sender = os.getenv("DACRE_SMTP_FROM", smtp_user or "di-system@dacre.local")

    if smtp_host and smtp_user and smtp_pass:
        try:
            msg = MIMEMultipart()
            msg["From"] = sender
            msg["To"] = email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain", "utf-8"))
            with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.sendmail(sender, [email], msg.as_string())
            status = "Sent via configured SMTP"
        except Exception as exc:
            status = f"SMTP failed; logged only: {type(exc).__name__}"

    con = db()
    con.execute("""
        INSERT INTO emails_log
        (recipient_email, recipient_name, company_name, subject, body, sender_email, status, sent_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        email, full_name, company_name, subject, body, sender, status,
        datetime.now().isoformat(timespec="seconds"),
    ))
    con.commit()
    con.close()

# =============================================================================
# AUTHENTICATION
# =============================================================================

def authenticate(company_name, full_name, passkey):
    con = db()
    company_clean = company_name.strip().lower()
    full_name_clean = full_name.strip().lower()
    pass_hash = hash_password(passkey.strip())

    if (company_clean == "dacre master" or full_name_clean == "david emenike") and passkey == MASTER_PASSKEY:
        row = con.execute(
            "SELECT first_name,last_name,username,company_name,email,role FROM users WHERE username=?",
            (MASTER_USERNAME,),
        ).fetchone()
        con.close()
        if row:
            return dict(row)

    rows = con.execute("""
        SELECT first_name,last_name,username,company_name,email,passkey_hash,role
        FROM users
        WHERE lower(company_name)=? AND passkey_hash=?
    """, (company_clean, pass_hash)).fetchall()

    matched = None
    for r in rows:
        user_fullname = f"{r['first_name']} {r['last_name']}".strip().lower()
        if user_fullname == full_name_clean or r["first_name"].lower() in full_name_clean or not full_name_clean:
            matched = r
            break
    if not matched and rows:
        matched = rows[0]
    if not matched:
        con.close()
        return None

    now = datetime.now().isoformat(timespec="seconds")
    con.execute("UPDATE users SET login_count=login_count+1,last_login=? WHERE username=?", (now, matched["username"]))
    con.commit()
    con.close()
    log_activity(matched["username"], matched["company_name"], "Signed in", notify_admin=matched["role"] != "master")
    return {
        "first_name": matched["first_name"], "last_name": matched["last_name"], "username": matched["username"],
        "company": matched["company_name"], "email": matched["email"], "role": matched["role"],
    }


def create_account(first, last, company, email, email_password, passkey):
    company_clean = company.strip()
    email_clean = email.strip().lower()
    passkey_clean = passkey.strip()
    if not company_clean or not email_clean or not passkey_clean:
        return False, "Please fill in Company Name, Email Address, and Account Passkey.", None

    if "@" not in email_clean or "." not in email_clean.split("@")[-1]:
        return False, "Please enter a valid email address.", None

    email_prefix = email_clean.split("@")[0].replace(".", " ").replace("_", " ").title()
    first_clean = first.strip() if first and first.strip() else (email_prefix.split()[0] if email_prefix else "User")
    last_clean = last.strip() if last and last.strip() else (" ".join(email_prefix.split()[1:]) if len(email_prefix.split()) > 1 else "Member")
    username_clean = email_clean

    if username_clean == MASTER_USERNAME:
        return False, "That username/email is reserved for the Master account.", None

    con = db()
    try:
        now = datetime.now().isoformat(timespec="seconds")
        cur = con.cursor()
        company_row = cur.execute("SELECT name FROM companies WHERE lower(name)=lower(?)", (company_clean,)).fetchone()

        if company_row:
            # Existing company: creator becomes a normal user unless an admin explicitly grants admin rights.
            role = "user"
        else:
            cur.execute("INSERT INTO companies(name,owner_username,admin_password_hash,created_at) VALUES (?,?,?,?)",
                        (company_clean, username_clean, hash_password(passkey_clean), now))
            role = "company_admin"

        cur.execute("""
            INSERT INTO users
            (first_name,last_name,username,company_name,email,email_password,password_hash,passkey_hash,role,login_count,created_at,last_login)
            VALUES (?,?,?,?,?,?,?,?,?,1,?,?)
        """, (
            first_clean, last_clean, username_clean, company_clean, email_clean, email_password.strip(),
            hash_password(passkey_clean), hash_password(passkey_clean), role, now, now,
        ))
        con.commit()

        send_di_welcome_email(first_clean, last_clean, company_clean, email_clean, email_password.strip())
        log_activity(username_clean, company_clean, "Created account & signed in", notify_admin=(role == "user"))
        if role == "company_admin":
            notify_company_admin(company_clean, f"New organization created by {first_clean} {last_clean}. You are the organization admin.", "new_company")

        return True, "Account created successfully!", {
            "first_name": first_clean, "last_name": last_clean, "username": username_clean,
            "company": company_clean, "email": email_clean, "role": role,
        }
    except sqlite3.IntegrityError:
        return False, "An account with this email address is already registered.", None
    finally:
        con.close()

# =============================================================================
# DATA ENGINE
# =============================================================================

SUPPORTED_EXTENSIONS = ["csv", "xlsx", "xls", "tsv", "json"]


def load_dataframe(uploaded_file):
    extension = uploaded_file.name.rsplit(".", 1)[-1].lower()
    if extension == "csv":
        return pd.read_csv(uploaded_file)
    if extension == "tsv":
        return pd.read_csv(uploaded_file, sep="\t")
    if extension in ("xlsx", "xls"):
        return pd.read_excel(uploaded_file)
    if extension == "json":
        return pd.read_json(uploaded_file)
    raise ValueError(f"Unsupported file type: .{extension}")


def clean_dataframe(df):
    out = df.copy()
    out.columns = [re.sub(r"\s+", " ", str(c).strip()) if str(c).strip() else f"Column_{i+1}" for i,c in enumerate(out.columns)]
    out = out.dropna(axis=0, how="all").dropna(axis=1, how="all")
    for column in out.columns:
        if out[column].dtype == "object":
            series = out[column].astype(str).replace({"nan": ""}).str.strip()
            numeric_candidate = series.str.replace(r"[\$€£₦,%]", "", regex=True).str.replace(",", "", regex=False)
            numeric = pd.to_numeric(numeric_candidate, errors="coerce")
            if numeric.notna().mean() >= 0.80 and series.ne("").any():
                out[column] = numeric
            else:
                out[column] = series
    return out.drop_duplicates().reset_index(drop=True)


def dataframe_to_json(df):
    return "" if df is None else df.to_json(orient="split", date_format="iso")


def dataframe_from_json(value):
    if not value:
        return None
    try:
        return pd.read_json(io.StringIO(value), orient="split")
    except Exception:
        return None


def save_file(user, uploaded_file, df):
    con = db()
    con.execute("INSERT INTO files(username,company_name,filename,file_type,file_json,created_at) VALUES(?,?,?,?,?,?)",
                (user["username"], user["company"], uploaded_file.name, uploaded_file.name.rsplit(".",1)[-1].lower(), dataframe_to_json(df), datetime.now().isoformat(timespec="seconds")))
    con.commit(); con.close()
    log_activity(user["username"], user["company"], f"Saved file: {uploaded_file.name}")


def get_files(user):
    con = db(); rows = con.execute("SELECT filename,file_type,created_at,file_json FROM files WHERE company_name=? ORDER BY id DESC", (user["company"],)).fetchall(); con.close(); return rows


def save_project(user, raw_df, processed_df, filename, logs, chart_config=None):
    con = db()
    existing = con.execute("SELECT id FROM projects WHERE username=? AND company_name=?", (user["username"], user["company"])).fetchone()
    payload = (user["username"], user["company"], "Main Workspace", filename or "", dataframe_to_json(raw_df), dataframe_to_json(processed_df), json.dumps(logs), json.dumps(chart_config or {}), datetime.now().isoformat(timespec="seconds"))
    if existing:
        con.execute("""UPDATE projects SET project_name=?,active_filename=?,raw_json=?,processed_json=?,formula_logs=?,chart_config=?,updated_at=? WHERE id=?""", (*payload[2:], existing["id"]))
    else:
        con.execute("""INSERT INTO projects(username,company_name,project_name,active_filename,raw_json,processed_json,formula_logs,chart_config,updated_at) VALUES(?,?,?,?,?,?,?,?,?)""", payload)
    con.commit(); con.close()


def restore_project(user):
    con = db(); row = con.execute("SELECT active_filename,raw_json,processed_json,formula_logs,chart_config FROM projects WHERE username=? AND company_name=? ORDER BY id DESC LIMIT 1", (user["username"],user["company"])).fetchone(); con.close()
    if not row: return None
    try: logs = json.loads(row["formula_logs"]) if row["formula_logs"] else []
    except Exception: logs = []
    try: chart = json.loads(row["chart_config"]) if row["chart_config"] else {}
    except Exception: chart = {}
    return {"filename":row["active_filename"],"raw":dataframe_from_json(row["raw_json"]),"processed":dataframe_from_json(row["processed_json"]),"logs":logs,"chart":chart}


def make_excel(processed_df, chart_df=None):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        processed_df.to_excel(writer, sheet_name="Processed Data", index=False)
        if chart_df is not None:
            chart_df.to_excel(writer, sheet_name="Dynamic Chart", index=False)
    output.seek(0); return output.getvalue()

# =============================================================================
# FORMULA ENGINE
# =============================================================================

SHEET_FORMULAS = ["SUM","AVERAGE","COUNT","COUNTA","MAX","MIN","CONCATENATE","UPPER","LOWER","TRIM"]


def apply_formula(df, formula, options):
    formula = formula.upper()
    if formula == "SUM": return pd.to_numeric(df[options["column"]], errors="coerce").sum()
    if formula == "AVERAGE": return pd.to_numeric(df[options["column"]], errors="coerce").mean()
    if formula == "COUNT": return int(pd.to_numeric(df[options["column"]], errors="coerce").count())
    if formula == "COUNTA": return int(df[options["column"]].notna().sum())
    if formula == "MAX": return pd.to_numeric(df[options["column"]], errors="coerce").max()
    if formula == "MIN": return pd.to_numeric(df[options["column"]], errors="coerce").min()
    if formula == "CONCATENATE":
        result = df[options["first"]].astype(str) + options.get("separator", " ") + df[options["second"]].astype(str)
        return "column", options["new_column"], result
    if formula in ("UPPER","LOWER","TRIM"):
        series = df[options["column"]].astype(str)
        result = series.str.upper() if formula == "UPPER" else series.str.lower() if formula == "LOWER" else series.str.strip()
        return "column", options["column"], result
    return None

# =============================================================================
# DI KNOWLEDGE + ONLINE KNOWLEDGE
# =============================================================================

APP_KNOWLEDGE = """
DACRE Analysis is a business and data analysis workspace. Users can upload CSV, Excel, TSV and JSON files; clean datasets; remove empty rows/columns and duplicates; inspect rows and columns; run formulas such as SUM, AVERAGE, COUNT, COUNTA, MAX, MIN, CONCATENATE, UPPER, LOWER and TRIM; build bar, line and area charts; save workspace state; use a File Vault; and export processed data as CSV or Excel.
DI means David's Intelligence. DI is the assistant inside DACRE Analysis. Each organization has its own workspace. The first person who creates a new organization becomes that organization's company admin. Later users joining an existing organization are regular users unless an admin grants them admin rights. Company admins can inspect users, account creation, sign-ins, file activity and changes for their organization. The master account can see system-wide activity.
""".strip()


def online_lookup(query, max_results=5):
    """Small dependency-free DuckDuckGo HTML lookup. It is optional and fails safely."""
    try:
        url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote_plus(query)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 DACRE-DI/1.0"})
        with urllib.request.urlopen(req, timeout=8) as response:
            html = response.read().decode("utf-8", errors="ignore")
        items = re.findall(r'<a rel="nofollow" class="result__a" href="([^"]+)"[^>]*>(.*?)</a>', html, flags=re.I|re.S)
        results = []
        for href, title in items[:max_results]:
            clean_title = re.sub(r"<.*?>", "", title).strip()
            clean_href = urllib.parse.unquote(href)
            results.append((clean_title, clean_href))
        return results
    except Exception:
        return []


def build_di_context(user, df):
    context = [APP_KNOWLEDGE, f"Current organization: {user['company']}. Current user: {user['first_name']} {user['last_name']}. Role: {user['role']}."]
    if df is not None:
        context.append(f"Active dataset has {len(df):,} rows and {len(df.columns):,} columns.")
        context.append("Columns: " + ", ".join(map(str, df.columns)))
    return "\n".join(context)


def di_reply(message, user, df, allow_online=True):
    text = message.strip()
    low = text.lower()
    if not text:
        return "I am ready. Tell me what you want me to do."

    name = "Master David" if user["role"] == "master" else user["first_name"]

    greetings = ["hello", "hi", "good morning", "good afternoon", "good evening", "good day"]
    if any(p in low for p in greetings) and len(low.split()) <= 6:
        return f"Good day {name}. DI is online. Tell me the business or data problem you want us to solve, and I will guide you step by step."

    if "what can you do" in low or "what can di do" in low:
        return "I can work with your DACRE workspace, explain your data, count and inspect rows/columns, detect duplicates, help with formulas and charts, explain the app, and—when online lookup is available—bring in current public knowledge. I can also help you think through business decisions in a clear, professional way."
    if "how many rows" in low or "row count" in low:
        return "There is no active dataset yet." if df is None else f"The active dataset contains {len(df):,} rows."
    if "how many columns" in low or "column count" in low:
        return "There is no active dataset yet." if df is None else f"The active dataset contains {len(df.columns):,} columns."
    if "duplicate" in low:
        return "There is no active dataset yet." if df is None else f"The current dataset has {int(df.duplicated().sum()):,} duplicate rows."
    if "columns" in low and df is not None:
        return "The current columns are: " + ", ".join(map(str, df.columns))
    if "missing" in low or "empty" in low:
        if df is None: return "There is no active dataset yet."
        missing = df.isna().sum().sort_values(ascending=False)
        top = missing[missing > 0].head(8)
        if top.empty: return "I checked the active dataset: I do not see missing values in the current columns."
        return "The columns with the most missing values are: " + "; ".join(f"{c}: {int(v)}" for c,v in top.items())
    if "describe" in low or "summary" in low or "overview" in low:
        if df is None: return "There is no active dataset yet. Upload a dataset and I can summarise it."
        return f"Dataset overview: {len(df):,} rows, {len(df.columns):,} columns. Numeric columns: {len(df.select_dtypes(include='number').columns)}. Duplicate rows: {int(df.duplicated().sum()):,}."

    # Explain the app from built-in knowledge without pretending to know private data.
    if any(k in low for k in ["dacre", "file vault", "formula lab", "export center", "admin portal", "workspace"]):
        return "DACRE Analysis is your business/data workspace. You can upload and clean data, run formulas, create charts, save project state, use the File Vault, export CSV/Excel, and use the DI assistant. Your organization has its own user and activity records, while admins have a separate management view."

    # Optional current/public web lookup. DI does not claim the web result is a fact until it has retrieved it.
    if allow_online and any(k in low for k in ["latest", "today", "current", "news", "price", "market", "who is", "what is", "how does", "recent"]):
        results = online_lookup(text)
        if results:
            lines = ["I checked current public web results for that question. Here are the strongest matches I found:"]
            for title, href in results:
                lines.append(f"• {title} — {href}")
            lines.append("\nIf you want, ask me to interpret these results for your business context.")
            return "\n".join(lines)

    return (
        f"I understand the request: {text}\n\n"
        "I can handle questions about this DACRE workspace and the active dataset directly. For a question outside the app, "
        "I can try a current public-web lookup when online access is available. Give me the goal and I will approach it like a business intelligence copilot."
    )



def load_chat_history(user, limit=40):
    con = db()
    rows = con.execute(
        "SELECT sender, message FROM chat_history WHERE username=? AND company_name=? ORDER BY id DESC LIMIT ?",
        (user["username"], user["company"], limit),
    ).fetchall()
    con.close()
    return [{"sender": r["sender"], "text": r["message"]} for r in reversed(rows)]


def transcribe_audio(audio_value):
    """Transcribe a browser recording when SpeechRecognition is installed."""
    if sr is None:
        return None, "Voice transcription package is not installed. Add SpeechRecognition to requirements.txt."
    try:
        recognizer = sr.Recognizer()
        raw = audio_value.getvalue()
        with sr.AudioFile(io.BytesIO(raw)) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language="en-NG")
        return text, None
    except sr.UnknownValueError:
        return None, "DI could not clearly understand that recording. Please speak a little slower and try again."
    except sr.RequestError:
        return None, "Voice transcription service is temporarily unavailable. You can still use text chat."
    except Exception as exc:
        return None, f"Voice transcription could not be completed: {type(exc).__name__}."

# =============================================================================
# VOICE
# =============================================================================

def speak(text):
    safe = json.dumps(text)
    components.html(f"""
    <script>
    (function() {{
      const text = {safe};
      if (!('speechSynthesis' in window)) return;
      const speak = () => {{
        const u = new SpeechSynthesisUtterance(text);
        u.lang = 'en-NG';
        u.rate = 0.90;
        u.pitch = 0.72;
        const voices = window.speechSynthesis.getVoices();
        const preferred = voices.find(v => /en-NG/i.test(v.lang)) || voices.find(v => /Nigeria|English.*Male|Male/i.test(v.name + ' ' + v.lang));
        if (preferred) u.voice = preferred;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(u);
      }};
      if (window.speechSynthesis.getVoices().length) speak();
      else window.speechSynthesis.onvoiceschanged = speak;
    }})();
    </script>
    """, height=0)

# =============================================================================
# STYLING
# =============================================================================

st.markdown("""
<style>
:root{--dacre-cyan:#18b7ff;--dacre-mint:#00dc96;--dacre-gold:#f4b942;--dacre-line:rgba(24,183,255,.25)}
.stApp{background:radial-gradient(circle at 10% 10%,rgba(24,183,255,.14),transparent 32%),radial-gradient(circle at 90% 20%,rgba(244,185,66,.10),transparent 28%),linear-gradient(135deg,#050914,#091322 55%,#050914);color:#fff}
.stApp::before{content:"";position:fixed;inset:-40%;pointer-events:none;background:conic-gradient(from 0deg at 50% 50%,rgba(24,183,255,.05),transparent 25%,rgba(255,193,7,.04) 45%,transparent 70%,rgba(0,220,150,.04) 85%,transparent 100%);animation:dacreSpin 48s linear infinite;z-index:0}
@keyframes dacreSpin{to{transform:rotate(360deg)}}
.main .block-container{position:relative;z-index:1;padding-top:2rem;max-width:1500px}
html,body,.stApp,.stApp p,.stApp li,.stApp span,.stApp label,.stMarkdown,.stMarkdown p,.stMarkdown li,[data-testid="stWidgetLabel"] p,[data-testid="stWidgetLabel"] label,.stRadio label,.stCheckbox label,.stSelectbox label,.stTextInput label,.stTextArea label,.stFileUploader label{color:#fff!important;font-weight:700!important}
.stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp h5,.stApp h6{font-family:'Inter','Segoe UI',sans-serif!important;color:#fff!important;font-weight:800!important;letter-spacing:-.02em}
.stApp h3{margin-top:1.2rem;padding-left:12px;border-left:4px solid var(--dacre-cyan);text-shadow:0 0 18px rgba(24,183,255,.35)}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#07101d 0%,#060d18 55%,#050914 100%);border-right:1px solid var(--dacre-line);box-shadow:24px 0 60px -40px rgba(24,183,255,.55)}
[data-testid="stSidebar"] *{color:#fff!important}
.dacre-hero{position:relative;padding:28px 30px;border-radius:22px;border:1px solid rgba(24,183,255,.35);background:linear-gradient(135deg,rgba(6,16,31,.94),rgba(10,28,47,.86));box-shadow:0 24px 60px -28px rgba(0,0,0,.9);backdrop-filter:blur(10px);margin-bottom:22px;overflow:hidden}
.dacre-hero:after{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(90deg,var(--dacre-cyan),var(--dacre-mint),var(--dacre-gold),var(--dacre-cyan));background-size:300% 100%;animation:dacreFlow 9s linear infinite}
@keyframes dacreFlow{to{background-position:300% 0}}
.dacre-title{font-size:clamp(2.2rem,5vw,4.2rem);font-weight:900;letter-spacing:-.04em;color:#fff}
.dacre-sub{font-size:1.08rem;color:#9edcff!important;font-weight:700}
.feature-card{padding:18px;border:1px solid rgba(255,255,255,.12);border-radius:16px;background:rgba(255,255,255,.045);min-height:145px}
.chat-card{padding:16px 18px;border-radius:18px;border:1px solid rgba(24,183,255,.25);background:rgba(4,12,24,.72);margin:8px 0}
.stTextInput input,.stTextArea textarea,.stNumberInput input{background:rgba(6,16,31,.92)!important;color:#fff!important;font-weight:700!important;border:1.5px solid rgba(24,183,255,.35)!important;border-radius:12px!important;padding:10px 14px!important}
.stTextInput input::placeholder,.stTextArea textarea::placeholder{color:#9aa4b2!important;font-weight:500!important}
div.stButton>button,div.stFormSubmitButton>button,div.stDownloadButton>button{border-radius:12px;border:1px solid rgba(24,183,255,.45);background:linear-gradient(135deg,#0a2540,#0d3860);color:#fff!important;font-weight:800!important;padding:10px 18px;transition:all .22s ease}
div.stButton>button:hover,div.stFormSubmitButton>button:hover,div.stDownloadButton>button:hover{border-color:var(--dacre-cyan);background:linear-gradient(135deg,#0d3860,#12508c);box-shadow:0 0 20px rgba(24,183,255,.45);transform:translateY(-1px)}
[data-testid="stMetric"]{padding:14px 18px;border-radius:16px;border:1px solid rgba(255,255,255,.10);background:linear-gradient(145deg,rgba(255,255,255,.05),rgba(255,255,255,.015))}
#MainMenu,footer{visibility:hidden}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SESSION STATE
# =============================================================================

for key, default in {
    "user": None, "raw_df": None, "processed_df": None, "active_filename": "",
    "formula_logs": [], "chart_config": {}, "chat_history": [], "landing_mode": "home",
    "last_speech": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# =============================================================================
# LANDING + AUTHENTICATION
# =============================================================================

def landing_page():
    top1, top2, top3 = st.columns([4,1,1])
    with top1:
        st.markdown("### **DACRE Analysis**")
    with top2:
        if st.button("🔐 Login", use_container_width=True):
            st.session_state.landing_mode = "login"
            st.rerun()
    with top3:
        if st.button("✨ Sign Up", use_container_width=True):
            st.session_state.landing_mode = "signup"
            st.rerun()

    if st.session_state.landing_mode in ("login","signup"):
        c1,c2,c3=st.columns([1,2,1])
        with c2:
            if st.button("← Back to DACRE Introduction"):
                st.session_state.landing_mode="home"; st.rerun()
            tab_login,tab_signup=st.tabs(["🔒 Sign In","📝 Sign Up"])
            with tab_login:
                st.markdown("### Access your workspace")
                login_company=st.text_input("Company / Organization Name",placeholder="e.g. Edubridge Consultant Limited",key="lin_comp")
                login_fullname=st.text_input("Full Name",placeholder="e.g. David Emenike",key="lin_fn")
                login_passkey=st.text_input("Account Passkey",type="password",placeholder="Enter your account passkey",key="lin_pk")
                if st.button("Sign In & Restore Workspace",use_container_width=True):
                    auth=authenticate(login_company,login_fullname,login_passkey)
                    if auth:
                        st.session_state.user=auth
                        project=restore_project(auth)
                        if project:
                            st.session_state.active_filename=project["filename"] or ""
                            st.session_state.raw_df=project["raw"]
                            st.session_state.processed_df=project["processed"]
                            st.session_state.formula_logs=project["logs"]
                            st.session_state.chart_config=project["chart"]
                        st.toast(f"Welcome back, {auth['first_name']}!",icon="🚀")
                        st.rerun()
                    else: st.error("Invalid credentials. Please verify your Company Name, Full Name, and Passkey.")
            with tab_signup:
                st.markdown("### Create a DACRE account")
                s_first=st.text_input("First Name",placeholder="e.g. David",key="su_first")
                s_last=st.text_input("Last Name",placeholder="e.g. Emenike",key="su_last")
                s_company=st.text_input("Company / Organization Name",placeholder="e.g. Edubridge Consultant Limited",key="su_comp")
                s_email=st.text_input("Email Address",placeholder="e.g. name@example.com",key="su_email")
                s_email_pass=st.text_input("Email Password (optional)",type="password",placeholder="Optional — SMTP credentials are safer",key="su_epass")
                s_passkey=st.text_input("Create Account Passkey",type="password",placeholder="Create your account passkey",key="su_passkey")
                if st.button("Create DACRE Account",use_container_width=True):
                    success,msg,created=create_account(s_first,s_last,s_company,s_email,s_email_pass,s_passkey)
                    if success:
                        st.session_state.user=created
                        st.toast(f"Welcome to DACRE, {created['first_name']}!",icon="✨")
                        st.rerun()
                    else: st.error(msg)
        return

    if LOGO_PATH.exists():
        left,mid,right=st.columns([1,2,1])
        with mid: st.image(str(LOGO_PATH),use_container_width=True)

    st.markdown("""
    <div class="dacre-hero">
      <div class="dacre-title">Turn business data into decisions.</div>
      <div class="dacre-sub">DACRE Analysis combines data cleaning, analysis, visualisation, workspace memory and DI — David's Intelligence — in one business intelligence workspace.</div>
    </div>
    """,unsafe_allow_html=True)

    st.markdown("### Meet DI — your business intelligence copilot")
    st.write("DI is designed to communicate naturally with users, understand the DACRE workspace, explain data in plain business language, and help users move from a question to an actionable answer.")

    cols=st.columns(4)
    cards=[("📊","Analyse","Upload CSV, Excel, TSV or JSON data and inspect it quickly."),("🧹","Clean","Clean headers, empty rows/columns, numeric fields and duplicates."),("📈","Visualise","Build bar, line and area charts from your active dataset."),("🤖","Talk to DI","Chat with DI about your data, your workspace or a wider business question.")]
    for c,(icon,title,desc) in zip(cols,cards):
        with c: st.markdown(f'<div class="feature-card"><h3>{icon} {title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)

    st.markdown("### Built for organizations")
    st.write("Each organization gets its own workspace. The first account that creates a new organization becomes that organization's admin. Organization admins can monitor users, account creation, sign-ins and workspace changes for their organization. The master portal remains separate.")

    a,b=st.columns(2)
    with a:
        if st.button("🚀 Start with DACRE",use_container_width=True): st.session_state.landing_mode="signup"; st.rerun()
    with b:
        if st.button("🔐 I already have an account",use_container_width=True): st.session_state.landing_mode="login"; st.rerun()


if st.session_state.user is None:
    landing_page()
    st.stop()

# Restore persistent DI conversation memory for this account.
if not st.session_state.chat_history:
    st.session_state.chat_history = load_chat_history(st.session_state.user, limit=40)

# =============================================================================
# MAIN APP
# =============================================================================

user=st.session_state.user

head_col1,head_col2=st.columns([3,1])
with head_col1:
    st.markdown(f"""<div class="dacre-hero"><div class="dacre-title">{APP_NAME}</div><div class="dacre-sub">{DI_NAME} · Active Organization: {user['company']}</div><p><b>User:</b> {user['first_name']} {user['last_name']} &nbsp; <b>Role:</b> {user['role'].upper()}</p></div>""",unsafe_allow_html=True)
with head_col2:
    if st.button("🚪 Sign Out",use_container_width=True):
        log_activity(user["username"],user["company"],"Signed out",notify_admin=user["role"] not in ("master","company_admin"))
        st.session_state.user=None
        st.rerun()

with st.sidebar:
    if LOGO_PATH.exists(): st.image(str(LOGO_PATH),use_container_width=True)
    st.markdown(f"### **{user['first_name']}'s Workspace**")
    st.caption(f"{user['company']} · {user['role']}")
    navigation=["🏠 DI Home","📊 Workspace & Data","⚙️ Formula Lab","📈 Add Dynamics (Charts)","📁 File Vault","📥 Export Center"]
    if user["role"] in ("company_admin","master"):
        navigation.append("🛡️ Organization Admin Portal")
    if user["role"]=="master": navigation.append("👑 Overall Admin DI Portal")
    selected_page=st.radio("Navigation",navigation)

# =============================================================================
# DI HOME / CHAT
# =============================================================================

if selected_page=="🏠 DI Home":
    st.header("🤖 Chat with DI")
    st.markdown("<div class='dacre-hero'><div class='dacre-title' style='font-size:2.2rem'>Talk to DI like a business partner.</div><div class='dacre-sub'>Ask about your data, DACRE, your workflow, or a public/current question. DI will use the active workspace when it can and can attempt an online lookup for current topics.</div></div>",unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.info("Try: “DI, how many rows are in my dataset?”, “Explain my data”, “What can DACRE do?”, or “What is the latest market news?”")

    for msg in st.session_state.chat_history[-30:]:
        role=msg["sender"]
        st.markdown(f"<div class='chat-card'><b>{'DI' if role=='DI' else role}</b><br>{msg['text']}</div>",unsafe_allow_html=True)

    with st.form("di_chat_form",clear_on_submit=True):
        chat_text=st.text_input("Chat with DI",placeholder="Chat with DI — ask me anything about your data or business...",label_visibility="collapsed")
        c1,c2=st.columns([5,1])
        with c1: send=st.form_submit_button("Send to DI",use_container_width=True)
        with c2: speak_back=st.form_submit_button("🔊 Reply aloud",use_container_width=True)
    if send or speak_back:
        if chat_text.strip():
            st.session_state.chat_history.append({"sender":user["first_name"],"text":chat_text.strip()})
            reply=di_reply(chat_text,user,st.session_state.processed_df,allow_online=True)
            st.session_state.chat_history.append({"sender":"DI","text":reply})
            con=db(); now=datetime.now().isoformat(timespec="seconds")
            con.execute("INSERT INTO chat_history(username,company_name,sender,message,created_at) VALUES(?,?,?,?,?)",(user["username"],user["company"],user["first_name"],chat_text.strip(),now))
            con.execute("INSERT INTO chat_history(username,company_name,sender,message,created_at) VALUES(?,?,?,?,?)",(user["username"],user["company"],"DI",reply,now)); con.commit(); con.close()
            if speak_back: speak(reply)
            st.rerun()

    st.markdown("### 🎙️ Voice input")
    st.caption("Your browser/Streamlit version must support audio input. For automatic speech-to-text, configure an external transcription service such as an OpenAI-compatible API; without one, the recording can still be captured but cannot be reliably transcribed inside Python.")
    try:
        audio_value=st.audio_input("Speak to DI")
        if audio_value:
            st.audio(audio_value)
            if st.button("🎙️ Send recording to DI", use_container_width=True):
                spoken_text, voice_error = transcribe_audio(audio_value)
                if spoken_text:
                    st.session_state.chat_history.append({"sender":user["first_name"],"text":spoken_text})
                    reply=di_reply(spoken_text,user,st.session_state.processed_df,allow_online=True)
                    st.session_state.chat_history.append({"sender":"DI","text":reply})
                    con=db(); now=datetime.now().isoformat(timespec="seconds")
                    con.execute("INSERT INTO chat_history(username,company_name,sender,message,created_at) VALUES(?,?,?,?,?)",(user["username"],user["company"],user["first_name"],spoken_text,now))
                    con.execute("INSERT INTO chat_history(username,company_name,sender,message,created_at) VALUES(?,?,?,?,?)",(user["username"],user["company"],"DI",reply,now)); con.commit(); con.close()
                    speak(reply)
                    st.success(f"You said: {spoken_text}")
                    st.rerun()
                elif voice_error:
                    st.warning(voice_error)
    except Exception:
        st.info("Voice recording is not available in this Streamlit runtime yet. Text chat and browser speech output remain available.")

# =============================================================================
# PAGE 1 WORKSPACE
# =============================================================================
elif selected_page=="📊 Workspace & Data":
    st.header("Workspace & Data Engine")
    file_upload=st.file_uploader("Upload dataset (CSV, Excel, TSV, JSON)",type=SUPPORTED_EXTENSIONS)
    if file_upload is not None and st.button("Import & Load Dataset"):
        try:
            df_raw=load_dataframe(file_upload)
            st.session_state.raw_df=df_raw
            st.session_state.processed_df=clean_dataframe(df_raw)
            st.session_state.active_filename=file_upload.name
            save_file(user,file_upload,st.session_state.processed_df)
            save_project(user,st.session_state.raw_df,st.session_state.processed_df,st.session_state.active_filename,st.session_state.formula_logs,st.session_state.chart_config)
            st.success(f"Loaded '{file_upload.name}' successfully!")
            st.rerun()
        except Exception as exc: st.error(f"Could not load the dataset: {exc}")

    if st.session_state.processed_df is not None:
        df=st.session_state.processed_df
        st.subheader(f"Active File: {st.session_state.active_filename}")
        m1,m2,m3=st.columns(3)
        m1.metric("Total Rows",f"{len(df):,}")
        m2.metric("Total Columns",len(df.columns))
        m3.metric("Duplicates Removed",int(st.session_state.raw_df.duplicated().sum()) if st.session_state.raw_df is not None else 0)
        st.dataframe(df,use_container_width=True)
        if st.button("💾 Save Project State to DI"):
            save_project(user,st.session_state.raw_df,df,st.session_state.active_filename,st.session_state.formula_logs,st.session_state.chart_config)
            log_activity(user["username"],user["company"],"Saved project state")
            st.toast("Project saved.",icon="💾")
    else: st.info("No active dataset. Upload a file or restore a saved project by signing in again.")

# =============================================================================
# PAGE 2 FORMULA LAB
# =============================================================================
elif selected_page=="⚙️ Formula Lab":
    st.header("Formula Lab")
    df=st.session_state.processed_df
    if df is None: st.warning("Please upload or open a dataset first.")
    else:
        formula=st.selectbox("Formula Operation",SHEET_FORMULAS)
        cols=list(df.columns)
        if formula in ["SUM","AVERAGE","COUNT","COUNTA","MAX","MIN","UPPER","LOWER","TRIM"]:
            target_col=st.selectbox("Target Column",cols)
            if st.button("Run Formula"):
                res=apply_formula(df,formula,{"column":target_col})
                if isinstance(res,tuple) and res[0]=="column":
                    df[res[1]]=res[2]; st.session_state.processed_df=df
                    st.session_state.formula_logs.append(f"Applied {formula} on {target_col}")
                    log_activity(user["username"],user["company"],f"Ran formula {formula} on {target_col}")
                    st.success(f"Applied {formula} on '{target_col}'!")
                else:
                    st.markdown(f"### Result: `{res}`")
                    st.session_state.formula_logs.append(f"{formula}({target_col}) = {res}")
        elif formula=="CONCATENATE":
            first=st.selectbox("First Column",cols); second=st.selectbox("Second Column",cols,index=min(1,len(cols)-1)); new_col=st.text_input("New Column Name",value="Combined"); sep=st.text_input("Separator",value=" ")
            if st.button("Run CONCATENATE"):
                df[new_col]=df[first].astype(str)+sep+df[second].astype(str); st.session_state.processed_df=df; log_activity(user["username"],user["company"],f"Created concatenated column {new_col}"); st.success(f"Created '{new_col}'.")

# =============================================================================
# PAGE 3 CHARTS
# =============================================================================
elif selected_page=="📈 Add Dynamics (Charts)":
    st.header("Add Dynamics — Chart Builder")
    df=st.session_state.processed_df
    if df is None: st.warning("Please upload or open a dataset first.")
    else:
        chart_type=st.selectbox("Chart Type",["Bar Chart","Line Chart","Area Chart"]); cols=list(df.columns); num_cols=df.select_dtypes(include=["number"]).columns.tolist(); x_col=st.selectbox("X-Axis (Category Column)",cols); y_col=st.selectbox("Y-Axis (Numeric Values)",num_cols if num_cols else cols)
        if st.button("Generate Dynamic Chart"):
            st.session_state.chart_config={"type":chart_type,"x":x_col,"y":y_col}; log_activity(user["username"],user["company"],f"Created {chart_type}: {x_col} vs {y_col}"); st.success("Chart attached to workspace!")
        if st.session_state.chart_config:
            cfg=st.session_state.chart_config; chart_data=df[[cfg["x"],cfg["y"]]].dropna().set_index(cfg["x"])
            if cfg["type"]=="Bar Chart": st.bar_chart(chart_data)
            elif cfg["type"]=="Line Chart": st.line_chart(chart_data)
            else: st.area_chart(chart_data)

# =============================================================================
# PAGE 4 FILE VAULT
# =============================================================================
elif selected_page=="📁 File Vault":
    st.header("Organization File Vault")
    saved_files=get_files(user)
    if not saved_files: st.info("No files stored in vault for your organization.")
    else:
        for fname,ftype,created,fjson in saved_files:
            col_a,col_b=st.columns([3,1]); col_a.markdown(f"**{fname}** (`.{ftype}`) — Saved on: {created}")
            if col_b.button(f"Load '{fname}'",key=f"btn_{fname}_{created}"):
                restored_df=dataframe_from_json(fjson); st.session_state.processed_df=restored_df; st.session_state.raw_df=restored_df; st.session_state.active_filename=fname; log_activity(user["username"],user["company"],f"Loaded file from vault: {fname}"); st.success(f"Loaded {fname} from Vault!"); st.rerun()

# =============================================================================
# PAGE 5 EXPORT
# =============================================================================
elif selected_page=="📥 Export Center":
    st.header("Export Center")
    df=st.session_state.processed_df
    if df is None: st.warning("No data available to export.")
    else:
        csv_data=df.to_csv(index=False).encode("utf-8"); excel_data=make_excel(df)
        st.download_button("📥 Download CSV Dataset",data=csv_data,file_name=f"{st.session_state.active_filename or 'dacre'}_processed.csv",mime="text/csv")
        st.download_button("📥 Download Excel Workbook (.xlsx)",data=excel_data,file_name=f"{st.session_state.active_filename or 'dacre'}_workbook.xlsx",mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        log_activity(user["username"],user["company"],"Opened Export Center")

# =============================================================================
# ORGANIZATION ADMIN PORTAL
# =============================================================================
elif selected_page=="🛡️ Organization Admin Portal" and user["role"] in ("company_admin","master"):
    st.header("🛡️ Organization Admin Portal")
    if user["role"]=="master":
        st.success("Master access confirmed. You can inspect all organizations.")
        target_company=st.selectbox("Organization",pd.read_sql_query("SELECT name FROM companies ORDER BY name",db())["name"].tolist())
    else:
        target_company=user["company"]
        st.success(f"Admin access confirmed for {target_company}.")

    con=db()
    tabs=st.tabs(["👥 People & Accounts","📜 Changes & Activity","🔔 DI Messages"])
    with tabs[0]:
        users_df=pd.read_sql_query("SELECT id,first_name,last_name,username,email,role,login_count,created_at,last_login FROM users WHERE company_name=? ORDER BY id DESC",con,params=(target_company,))
        st.dataframe(users_df,use_container_width=True)
        st.metric("Accounts in organization",len(users_df))

        if user["role"]=="company_admin":
            st.markdown("### Grant or remove admin access")
            usernames=users_df[users_df["role"]!="company_admin"]["username"].tolist()
            if usernames:
                selected_user=st.selectbox("User",usernames)
                action=st.selectbox("Action",["Grant company admin","Revoke company admin"])
                if st.button("Apply account role change"):
                    new_role="company_admin" if action.startswith("Grant") else "user"
                    con.execute("UPDATE users SET role=? WHERE username=? AND company_name=?",(new_role,selected_user,target_company)); con.commit()
                    notify_company_admin(target_company,f"Admin role changed for {selected_user}: {new_role}.","role_change")
                    log_activity(user["username"],target_company,f"Changed role for {selected_user} to {new_role}",notify_admin=False)
                    st.success("Role updated."); st.rerun()
    with tabs[1]:
        activity_df=pd.read_sql_query("SELECT id,username,action,created_at FROM activity WHERE company_name=? ORDER BY id DESC",con,params=(target_company,))
        st.dataframe(activity_df,use_container_width=True)
    with tabs[2]:
        notes_df=pd.read_sql_query("SELECT id,event_type,message,is_read,created_at FROM notifications WHERE company_name=? ORDER BY id DESC",con,params=(target_company,))
        st.dataframe(notes_df,use_container_width=True)
        if not notes_df.empty and st.button("Mark DI messages as read"):
            con.execute("UPDATE notifications SET is_read=1 WHERE company_name=?",(target_company,)); con.commit(); st.rerun()
    con.close()

# =============================================================================
# MASTER ADMIN PORTAL
# =============================================================================
elif selected_page=="👑 Overall Admin DI Portal" and user["role"]=="master":
    st.header("👑 Overall Admin DI Portal")
    st.success("Good day Master David. DI recognises this as the overall master administration account.")
    con=db()
    adm1,adm2,adm3,adm4=st.tabs(["👥 Users","🏢 Organizations","✉️ Mail Source","📜 System Activity"])
    with adm1:
        users_df=pd.read_sql_query("SELECT id,first_name,last_name,company_name,email,role,login_count,created_at,last_login FROM users ORDER BY id DESC",con); st.dataframe(users_df,use_container_width=True); st.metric("Registered accounts",len(users_df))
    with adm2:
        companies_df=pd.read_sql_query("SELECT id,name,owner_username,created_at FROM companies ORDER BY id DESC",con); st.dataframe(companies_df,use_container_width=True); st.metric("Organizations",len(companies_df))
    with adm3:
        mails_df=pd.read_sql_query("SELECT id,recipient_name,recipient_email,company_name,subject,sender_email,status,sent_at,body FROM emails_log ORDER BY id DESC",con); st.dataframe(mails_df,use_container_width=True)
    with adm4:
        activity_df=pd.read_sql_query("SELECT * FROM activity ORDER BY id DESC",con); st.dataframe(activity_df,use_container_width=True)
    con.close()

# =============================================================================
# PERSISTENT DI DOCK
# =============================================================================

st.markdown("---")
with st.expander("🤖 Chat with DI — quick assistant",expanded=False):
    for msg in st.session_state.chat_history[-10:]: st.write(f"**{msg['sender']}**: {msg['text']}")
    with st.form("quick_di_form",clear_on_submit=True):
        q=st.text_input("Chat with DI",placeholder="Chat with DI — ask a question...",label_visibility="collapsed")
        send=st.form_submit_button("Send")
    if send and q.strip():
        st.session_state.chat_history.append({"sender":user["first_name"],"text":q.strip()})
        reply=di_reply(q,user,st.session_state.processed_df,allow_online=True)
        st.session_state.chat_history.append({"sender":"DI","text":reply})
        st.session_state.last_speech=reply
        st.rerun()

if st.session_state.last_speech:
    speech=st.session_state.last_speech
    st.session_state.last_speech=None
    speak(speech)
