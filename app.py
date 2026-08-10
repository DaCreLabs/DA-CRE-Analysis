import hashlib
import io
import json
import os
import re
import smtplib
import sqlite3
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
# =============================================================================

APP_NAME = "DACRE Analysis"
DI_NAME = "DI — David's Intelligence"
MASTER_USERNAME = "david"
MASTER_FULL_NAME = "David Emenike"
MASTER_PASSKEY = os.getenv("DACRE_MASTER_PASSKEY", "theWORDofGOD@111")

BASE_DIR = Path(__file__).resolve().parent
LOGO_FILENAME = "ChatGPT Image Jul 29, 2026, 02_27_41 PM.png"
LOGO_PATH = BASE_DIR / LOGO_FILENAME
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

        # Keep the upper/middle DA emblem area.
        top = int(height * 0.08)
        bottom = int(height * 0.64)
        crop = source.crop((0, top, width, bottom))

        side = min(crop.size)
        left = (crop.width - side) // 2
        crop_top = max(0, (crop.height - side) // 2)
        crop = crop.crop(
            (left, crop_top, left + side, crop_top + side)
        )
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
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def hash_password(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def init_db():
    con = db()
    cur = con.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            owner_username TEXT NOT NULL,
            admin_password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
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
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            company_name TEXT NOT NULL,
            filename TEXT NOT NULL,
            file_type TEXT NOT NULL,
            file_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
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
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            company_name TEXT NOT NULL,
            action TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
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
        """
    )

    con.commit()
    con.close()


init_db()


def ensure_master():
    con = db()
    cur = con.cursor()

    cur.execute(
        "SELECT id FROM users WHERE username = ?",
        (MASTER_USERNAME,),
    )

    if not cur.fetchone():
        now = datetime.now().isoformat(timespec="seconds")
        cur.execute(
            """
            INSERT INTO users
            (
                first_name, last_name, username, company_name, email, email_password,
                password_hash, passkey_hash, role, login_count, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "David",
                "Emenike",
                MASTER_USERNAME,
                "DACRE MASTER",
                "master@dacre.local",
                "",
                hash_password(MASTER_PASSKEY),
                hash_password(MASTER_PASSKEY),
                "master",
                0,
                now,
            ),
        )
        con.commit()

    con.close()


ensure_master()


def log_activity(username, company, action):
    con = db()
    con.execute(
        """
        INSERT INTO activity(username, company_name, action, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            username,
            company,
            action,
            datetime.now().isoformat(timespec="seconds"),
        ),
    )
    con.commit()
    con.close()


# =============================================================================
# EMAIL & ADMIN DI MAIL SOURCE SYSTEM
# =============================================================================
def send_di_welcome_email(first_name, last_name, company_name, email, email_password=""):
    full_name = f"{first_name} {last_name}".strip()
    subject = f"Welcome to DACRE Analysis — DI is now active for {company_name}!"
    body = (
        f"Hello {first_name},\n\n"
        f"Thank you for signing up for DACRE Analysis!\n\n"
        f"I am DI (David's Intelligence), your automated business and data intelligence copilot. "
        f"I am fully configured to empower {company_name} by streaming real-time data analytics, "
        f"optimizing financial models, and providing lightning-fast business insights.\n\n"
        f"Your account details and passkey are securely stored under Overall Admin DI. Whenever you return, "
        f"simply sign in with your Company Name, Account Passkey, and Full Name to restore your exact "
        f"workspace in under 1 second.\n\n"
        f"We are excited to help scale your business!\n\n"
        f"Warm regards,\n"
        f"DI — David's Intelligence\n"
        f"DACRE Analysis Platform"
    )

    status = "Logged & Dispatched (Simulated/SMTP)"

    con = db()
    con.execute(
        """
        INSERT INTO emails_log
        (recipient_email, recipient_name, company_name, subject, body, sender_email, status, sent_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            email,
            full_name,
            company_name,
            subject,
            body,
            "di-system@dacre.ai",
            status,
            datetime.now().isoformat(timespec="seconds"),
        ),
    )
    con.commit()
    con.close()


# =============================================================================
# AUTHENTICATION ENGINE
# =============================================================================
def authenticate(company_name, full_name, passkey):
    con = db()

    # Master login bypass
    if (
        company_name.strip().lower() == "dacre master"
        or full_name.strip().lower() == "david emenike"
    ) and passkey == MASTER_PASSKEY:
        row = con.execute(
            "SELECT first_name, last_name, username, company_name, email, role FROM users WHERE username = ?",
            (MASTER_USERNAME,),
        ).fetchone()
        con.close()
        if row:
            return {
                "first_name": row[0],
                "last_name": row[1],
                "username": row[2],
                "company": row[3],
                "email": row[4],
                "role": row[5],
            }

    pass_hash = hash_password(passkey.strip())
    full_name_clean = full_name.strip().lower()
    company_clean = company_name.strip().lower()

    rows = con.execute(
        """
        SELECT
            first_name,
            last_name,
            username,
            company_name,
            email,
            passkey_hash,
            role
        FROM users
        WHERE lower(company_name) = ? AND passkey_hash = ?
        """,
        (company_clean, pass_hash),
    ).fetchall()

    matched_user = None
    for r in rows:
        user_fullname = f"{r[0]} {r[1]}".strip().lower()
        if user_fullname == full_name_clean or r[0].lower() in full_name_clean or full_name_clean in user_fullname or not full_name_clean:
            matched_user = r
            break

    # If exact passkey and company match but full name was given casually, accept match
    if not matched_user and rows:
        matched_user = rows[0]

    if not matched_user:
        con.close()
        return None

    now = datetime.now().isoformat(timespec="seconds")
    con.execute(
        """
        UPDATE users
        SET login_count = login_count + 1, last_login = ?
        WHERE username = ?
        """,
        (now, matched_user[2]),
    )
    con.commit()
    con.close()

    log_activity(matched_user[2], matched_user[3], "Signed in")

    return {
        "first_name": matched_user[0],
        "last_name": matched_user[1],
        "username": matched_user[2],
        "company": matched_user[3],
        "email": matched_user[4],
        "role": matched_user[6],
    }


def create_account(first, last, company, email, email_password, passkey):
    company_clean = company.strip()
    email_clean = email.strip().lower()
    passkey_clean = passkey.strip()

    # Core requirement validation: Company, Email, and Passkey
    if not company_clean or not email_clean or not passkey_clean:
        return False, "Please fill in Company Name, Email Address, and Account Passkey.", None

    # Derive names if first/last were left blank or scrolled out of view
    email_prefix = email_clean.split("@")[0].replace(".", " ").title()
    first_clean = first.strip() if first and first.strip() else (email_prefix.split()[0] if email_prefix else "User")
    last_clean = last.strip() if last and last.strip() else (" ".join(email_prefix.split()[1:]) if len(email_prefix.split()) > 1 else "Member")

    username_clean = email_clean

    if username_clean == MASTER_USERNAME:
        return False, "That username/email is reserved for the Master account.", None

    con = db()

    try:
        now = datetime.now().isoformat(timespec="seconds")
        cur = con.cursor()

        cur.execute(
            "SELECT id FROM companies WHERE lower(name) = lower(?)",
            (company_clean,),
        )

        if not cur.fetchone():
            cur.execute(
                """
                INSERT INTO companies
                (name, owner_username, admin_password_hash, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    company_clean,
                    username_clean,
                    hash_password(passkey_clean),
                    now,
                ),
            )

        cur.execute(
            """
            INSERT INTO users
            (
                first_name, last_name, username, company_name, email, email_password,
                password_hash, passkey_hash, role, login_count, created_at, last_login
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
            """,
            (
                first_clean,
                last_clean,
                username_clean,
                company_clean,
                email_clean,
                email_password.strip(),
                hash_password(passkey_clean),
                hash_password(passkey_clean),
                "company_admin",
                now,
                now,
            ),
        )

        con.commit()

        send_di_welcome_email(first_clean, last_clean, company_clean, email_clean, email_password.strip())
        log_activity(username_clean, company_clean, "Created account & Auto Logged In")

        user_dict = {
            "first_name": first_clean,
            "last_name": last_clean,
            "username": username_clean,
            "company": company_clean,
            "email": email_clean,
            "role": "company_admin",
        }

        return True, "Account created successfully!", user_dict

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

    out.columns = [
        re.sub(r"\s+", " ", str(column).strip())
        if str(column).strip()
        else f"Column_{index + 1}"
        for index, column in enumerate(out.columns)
    ]

    out = out.dropna(axis=0, how="all")
    out = out.dropna(axis=1, how="all")

    for column in out.columns:
        if out[column].dtype == "object":
            series = (
                out[column]
                .astype(str)
                .replace({"nan": ""})
                .str.strip()
            )

            numeric_candidate = (
                series
                .str.replace(r"[\$€£₦,%]", "", regex=True)
                .str.replace(",", "", regex=False)
            )

            numeric = pd.to_numeric(
                numeric_candidate,
                errors="coerce",
            )

            if numeric.notna().mean() >= 0.80 and series.ne("").any():
                out[column] = numeric
            else:
                out[column] = series

    return out.drop_duplicates().reset_index(drop=True)


def dataframe_to_json(df):
    if df is None:
        return ""
    return df.to_json(
        orient="split",
        date_format="iso",
    )


def dataframe_from_json(value):
    if not value:
        return None

    try:
        return pd.read_json(
            io.StringIO(value),
            orient="split",
        )
    except Exception:
        return None


def save_file(user, uploaded_file, df):
    con = db()

    con.execute(
        """
        INSERT INTO files
        (
            username, company_name, filename, file_type,
            file_json, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user["username"],
            user["company"],
            uploaded_file.name,
            uploaded_file.name.rsplit(".", 1)[-1].lower(),
            dataframe_to_json(df),
            datetime.now().isoformat(timespec="seconds"),
        ),
    )

    con.commit()
    con.close()

    log_activity(
        user["username"],
        user["company"],
        f"Saved file: {uploaded_file.name}",
    )


def get_files(user):
    con = db()

    rows = con.execute(
        """
        SELECT filename, file_type, created_at, file_json
        FROM files
        WHERE company_name = ?
        ORDER BY id DESC
        """,
        (user["company"],),
    ).fetchall()

    con.close()
    return rows


def save_project(
    user,
    raw_df,
    processed_df,
    filename,
    logs,
    chart_config=None,
):
    con = db()

    existing = con.execute(
        """
        SELECT id
        FROM projects
        WHERE username = ? AND company_name = ?
        """,
        (
            user["username"],
            user["company"],
        ),
    ).fetchone()

    payload = (
        user["username"],
        user["company"],
        "Main Workspace",
        filename or "",
        dataframe_to_json(raw_df),
        dataframe_to_json(processed_df),
        json.dumps(logs),
        json.dumps(chart_config or {}),
        datetime.now().isoformat(timespec="seconds"),
    )

    if existing:
        con.execute(
            """
            UPDATE projects
            SET
                project_name = ?,
                active_filename = ?,
                raw_json = ?,
                processed_json = ?,
                formula_logs = ?,
                chart_config = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (
                payload[2],
                payload[3],
                payload[4],
                payload[5],
                payload[6],
                payload[7],
                payload[8],
                existing[0],
            ),
        )
    else:
        con.execute(
            """
            INSERT INTO projects
            (
                username, company_name, project_name, active_filename,
                raw_json, processed_json, formula_logs,
                chart_config, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            payload,
        )

    con.commit()
    con.close()


def restore_project(user):
    con = db()

    row = con.execute(
        """
        SELECT
            active_filename,
            raw_json,
            processed_json,
            formula_logs,
            chart_config
        FROM projects
        WHERE username = ? AND company_name = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (
            user["username"],
            user["company"],
        ),
    ).fetchone()

    con.close()

    if not row:
        return None

    try:
        logs = json.loads(row[3]) if row[3] else []
    except Exception:
        logs = []

    try:
        chart = json.loads(row[4]) if row[4] else {}
    except Exception:
        chart = {}

    return {
        "filename": row[0],
        "raw": dataframe_from_json(row[1]),
        "processed": dataframe_from_json(row[2]),
        "logs": logs,
        "chart": chart,
    }


def make_excel(processed_df, chart_df=None):
    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl",
    ) as writer:
        processed_df.to_excel(
            writer,
            sheet_name="Processed Data",
            index=False,
        )

        if chart_df is not None:
            chart_df.to_excel(
                writer,
                sheet_name="Dynamic Chart",
                index=False,
            )

    output.seek(0)
    return output.getvalue()


# =============================================================================
# FORMULA ENGINE
# =============================================================================
SHEET_FORMULAS = [
    "SUM",
    "AVERAGE",
    "COUNT",
    "COUNTA",
    "MAX",
    "MIN",
    "CONCATENATE",
    "UPPER",
    "LOWER",
    "TRIM",
]


def apply_formula(df, formula, options):
    formula = formula.upper()

    if formula == "SUM":
        return pd.to_numeric(
            df[options["column"]],
            errors="coerce",
        ).sum()

    if formula == "AVERAGE":
        return pd.to_numeric(
            df[options["column"]],
            errors="coerce",
        ).mean()

    if formula == "COUNT":
        return int(
            pd.to_numeric(
                df[options["column"]],
                errors="coerce",
            ).count()
        )

    if formula == "COUNTA":
        return int(
            df[options["column"]].notna().sum()
        )

    if formula == "MAX":
        return pd.to_numeric(
            df[options["column"]],
            errors="coerce",
        ).max()

    if formula == "MIN":
        return pd.to_numeric(
            df[options["column"]],
            errors="coerce",
        ).min()

    if formula == "CONCATENATE":
        first = options["first"]
        second = options["second"]

        result = (
            df[first].astype(str)
            + options.get("separator", " ")
            + df[second].astype(str)
        )

        return (
            "column",
            options["new_column"],
            result,
        )

    if formula in ("UPPER", "LOWER", "TRIM"):
        series = df[options["column"]].astype(str)

        if formula == "UPPER":
            result = series.str.upper()
        elif formula == "LOWER":
            result = series.str.lower()
        else:
            result = series.str.strip()

        return (
            "column",
            options["column"],
            result,
        )

    return None


# =============================================================================
# DI ASSISTANT ENGINE
# =============================================================================
def di_reply(message, user, df):
    text = message.strip()
    low = text.lower()

    if not text:
        return "I am ready. Tell me what you want me to do."

    name = (
        "Master David"
        if user["role"] == "master"
        else user["first_name"]
    )

    if any(
        phrase in low
        for phrase in [
            "hello",
            "hi",
            "good morning",
            "good afternoon",
            "good day",
        ]
    ):
        return (
            f"Good day {name}. DI is online and ready "
            "to work with your data."
        )

    if "how many rows" in low or "row count" in low:
        if df is None:
            return "There is no active dataset yet. Open or upload a file first."
        return f"The active dataset contains {len(df):,} rows."

    if "how many columns" in low or "column count" in low:
        if df is None:
            return "There is no active dataset yet."
        return f"The active dataset contains {len(df.columns):,} columns."

    if "duplicate" in low and df is not None:
        return f"The current dataset has {int(df.duplicated().sum()):,} duplicate rows."

    if "columns" in low and df is not None:
        return "Current columns: " + ", ".join(map(str, df.columns))

    return (
        f"DI received your request: '{text}'. "
        "I am fully monitoring your active workspace."
    )


def speak(text):
    safe_text = json.dumps(text)

    components.html(
        f"""
        <script>
        const message = new SpeechSynthesisUtterance({safe_text});
        message.rate = 0.95;
        message.pitch = 0.85;
        message.lang = "en-NG";

        if (window.speechSynthesis) {{
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(message);
        }}
        </script>
        """,
        height=0,
    )


# =============================================================================
# VISUAL SYSTEM & STYLING (LIGHT GOLD BARS + SOFT GREY PLACEHOLDERS)
# =============================================================================
st.markdown(
    """
    <style>
    :root {
        --blue: #18b7ff;
        --gold: #f4b942;
        --light-gold: #fef8e7;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(24,183,255,.14),
                transparent 32%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(244,185,66,.10),
                transparent 28%
            ),
            linear-gradient(
                135deg,
                #050914,
                #091322 55%,
                #050914
            );
        color: #ffffff;
    }

    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 7rem;
    }

    /* LIGHT GOLD INPUT BARS */
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div,
    .stTextInput input,
    .stTextArea textarea {
        background-color: #fef7e0 !important;
        color: #111111 !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        border: 2px solid #f4b942 !important;
    }

    /* SOFT VISIBLE GREY PLACEHOLDER TEXT */
    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder,
    div[data-baseweb="input"] input::placeholder {
        color: #888888 !important;
        font-weight: 400 !important;
        opacity: 0.85 !important;
        -webkit-text-fill-color: #888888 !important;
    }

    .dacre-hero {
        padding: 24px;
        border: 1px solid rgba(24,183,255,.35);
        border-radius: 24px;
        background:
            linear-gradient(
                135deg,
                rgba(6,16,31,.94),
                rgba(10,28,47,.88)
            );
        box-shadow: 0 18px 60px rgba(0,0,0,.28);
    }

    .dacre-title {
        font-size: 2.7rem;
        font-weight: 900;
        letter-spacing: .8px;
        color: #ffffff !important;
    }

    .dacre-sub {
        color: #9edcff;
        font-size: 1.05rem;
        font-weight: 700;
    }

    .badge {
        display: inline-block;
        padding: 6px 12px;
        margin: 3px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,.15);
        background: rgba(255,255,255,.05);
        color: #ffffff !important;
    }

    .stButton > button {
        border-radius: 12px;
        font-weight: 800;
        min-height: 44px;
        background-color: #f4b942 !important;
        color: #050914 !important;
        border: 1px solid #f4b942 !important;
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #040a14,
                #071423
            );
        border-right: 1px solid rgba(24,183,255,.28);
    }
    
    html, body, .stApp, .stApp p, .stApp li, .stApp span, .stApp label, .stMarkdown, .stMarkdown p, .stMarkdown li,
    [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label, .stRadio label, .stCheckbox label,
    .stSelectbox label, .stTextInput label, .stTextArea label, .stFileUploader label, .stDateInput label {
        color: #ffffff !important; 
        font-weight: 700 !important; 
    }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        font-family: 'Inter', sans-serif !important; 
        color: #ffffff !important; 
        font-weight: 800 !important; 
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================
if "user" not in st.session_state:
    st.session_state.user = None
if "raw_df" not in st.session_state:
    st.session_state.raw_df = None
if "processed_df" not in st.session_state:
    st.session_state.processed_df = None
if "active_filename" not in st.session_state:
    st.session_state.active_filename = ""
if "formula_logs" not in st.session_state:
    st.session_state.formula_logs = []
if "chart_config" not in st.session_state:
    st.session_state.chart_config = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# =============================================================================
# SIGN IN / SIGN UP SCREEN
# =============================================================================
if st.session_state.user is None:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), use_container_width=True)
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <h1 style="margin:0; font-size: 2.4rem; color: #ffffff;">{APP_NAME}</h1>
                <p style="color: #18b7ff; font-size: 1.1rem; margin-top: 4px;">{DI_NAME}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        tab_login, tab_signup = st.tabs(["🔒 Sign In", "📝 Sign Up for DACRE"])

        with tab_login:
            st.markdown("### Access Your Workspace")
            login_company = st.text_input(
                "Company / Organization Name",
                placeholder="e.g., Edubridge Consultant Limited",
                key="lin_comp",
            )
            login_fullname = st.text_input(
                "Full Name (First & Last Name)",
                placeholder="e.g., David Emenike",
                key="lin_fn",
            )
            login_passkey = st.text_input(
                "Account Passkey",
                type="password",
                placeholder="Enter your account passkey",
                key="lin_pk",
            )

            if st.button("Sign In & Restore Workspace", use_container_width=True):
                user_auth = authenticate(login_company, login_fullname, login_passkey)
                if user_auth:
                    st.session_state.user = user_auth
                    st.toast(f"Welcome back, {user_auth['first_name']}! Restoring previous state...", icon="🚀")
                    
                    project = restore_project(user_auth)
                    if project:
                        st.session_state.active_filename = project["filename"]
                        st.session_state.raw_df = project["raw"]
                        st.session_state.processed_df = project["processed"]
                        st.session_state.formula_logs = project["logs"]
                        st.session_state.chart_config = project["chart"]

                    st.rerun()
                else:
                    st.error("Invalid credentials. Please verify your Company Name, Full Name, and Passkey.")

        with tab_signup:
            st.markdown("### Create New DACRE Account")
            s_first = st.text_input(
                "First Name",
                placeholder="e.g., David",
                key="su_first",
            )
            s_last = st.text_input(
                "Last Name",
                placeholder="e.g., Emenike",
                key="su_last",
            )
            s_company = st.text_input(
                "Company / Organization Name",
                placeholder="e.g., Edubridge Consultant Limited",
                key="su_comp",
            )
            s_email = st.text_input(
                "Email Address",
                placeholder="e.g., uchechukwudavid@proton.mail",
                key="su_email",
            )
            s_email_pass = st.text_input(
                "Email Password",
                type="password",
                placeholder="Enter your email password for DI sync",
                key="su_epass",
            )
            s_passkey = st.text_input(
                "Account Passkey",
                type="password",
                placeholder="Create your account passkey",
                key="su_passkey",
            )

            if st.button("Sign Up for DACRE", use_container_width=True):
                success, msg, created_user = create_account(
                    s_first, s_last, s_company, s_email, s_email_pass, s_passkey
                )
                if success:
                    st.session_state.user = created_user
                    st.toast("Account created! DI is taking you straight into your workspace...", icon="✨")
                    st.rerun()
                else:
                    st.error(msg)
    st.stop()


# =============================================================================
# MAIN APPLICATION INTERFACE
# =============================================================================
user = st.session_state.user

head_col1, head_col2 = st.columns([3, 1])
with head_col1:
    st.markdown(
        f"""
        <div class="dacre-hero">
            <div class="dacre-title">{APP_NAME}</div>
            <div class="dacre-sub">{DI_NAME} | Active Organization: <span style="color:#f4b942;">{user['company']}</span></div>
            <div style="margin-top:8px;">
                <span class="badge">User: {user['first_name']} {user['last_name']}</span>
                <span class="badge">Role: {user['role'].upper()}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with head_col2:
    if st.button("🚪 Sign Out", use_container_width=True):
        st.session_state.user = None
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# SIDEBAR MENU
with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)
    st.markdown(f"### **{user['first_name']}'s Workspace**")
    
    navigation = [
        "📊 Workspace & Data",
        "⚙️ Formula Lab",
        "📈 Add Dynamics (Charts)",
        "📁 File Vault",
        "📥 Export Center",
    ]
    if user["role"] == "master":
        navigation.append("👑 Overall Admin DI Portal")

    selected_page = st.radio("Navigation", navigation)

# =============================================================================
# PAGE 1: WORKSPACE & DATA
# =============================================================================
if selected_page == "📊 Workspace & Data":
    st.header("Workspace & Data Engine")
    
    file_upload = st.file_uploader(
        "Upload dataset (CSV, Excel, TSV, JSON)",
        type=SUPPORTED_EXTENSIONS,
    )

    if file_upload is not None:
        if st.button("Import & Load Dataset"):
            df_raw = load_dataframe(file_upload)
            st.session_state.raw_df = df_raw
            st.session_state.processed_df = clean_dataframe(df_raw)
            st.session_state.active_filename = file_upload.name
            
            save_file(user, file_upload, st.session_state.processed_df)
            save_project(
                user,
                st.session_state.raw_df,
                st.session_state.processed_df,
                st.session_state.active_filename,
                st.session_state.formula_logs,
                st.session_state.chart_config,
            )
            st.success(f"Loaded '{file_upload.name}' successfully!")
            st.rerun()

    if st.session_state.processed_df is not None:
        st.subheader(f"Active File: {st.session_state.active_filename}")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Rows", f"{len(st.session_state.processed_df):,}")
        m2.metric("Total Columns", len(st.session_state.processed_df.columns))
        m3.metric("Duplicates Removed", int(st.session_state.raw_df.duplicated().sum()) if st.session_state.raw_df is not None else 0)

        st.dataframe(st.session_state.processed_df, use_container_width=True)

        if st.button("💾 Save Project State to Admin DI"):
            save_project(
                user,
                st.session_state.raw_df,
                st.session_state.processed_df,
                st.session_state.active_filename,
                st.session_state.formula_logs,
                st.session_state.chart_config,
            )
            st.toast("Project saved instantly to overall Admin DI database!", icon="💾")
    else:
        st.info("No active dataset. Upload a file or restore from File Vault.")

# =============================================================================
# PAGE 2: FORMULA LAB
# =============================================================================
elif selected_page == "⚙️ Formula Lab":
    st.header("Formula Lab")
    df = st.session_state.processed_df

    if df is None:
        st.warning("Please upload or open a dataset first.")
    else:
        formula = st.selectbox("Formula Operation", SHEET_FORMULAS)
        cols = list(df.columns)
        
        if formula in ["SUM", "AVERAGE", "COUNT", "COUNTA", "MAX", "MIN", "UPPER", "LOWER", "TRIM"]:
            target_col = st.selectbox("Target Column", cols)
            if st.button("Run Formula"):
                res = apply_formula(df, formula, {"column": target_col})
                if isinstance(res, tuple) and res[0] == "column":
                    df[res[1]] = res[2]
                    st.session_state.processed_df = df
                    st.success(f"Applied {formula} on '{target_col}'!")
                else:
                    st.markdown(f"### Result of {formula}({target_col}): `{res}`")
                    st.session_state.formula_logs.append(f"{formula}({target_col}) = {res}")

# =============================================================================
# PAGE 3: ADD DYNAMICS (CHARTS)
# =============================================================================
elif selected_page == "📈 Add Dynamics (Charts)":
    st.header("Add Dynamics — Chart Builder")
    df = st.session_state.processed_df

    if df is None:
        st.warning("Please upload or open a dataset first.")
    else:
        chart_type = st.selectbox("Chart Type", ["Bar Chart", "Line Chart", "Area Chart"])
        cols = list(df.columns)
        num_cols = df.select_dtypes(include=["number"]).columns.tolist()

        x_col = st.selectbox("X-Axis (Category Column)", cols)
        y_col = st.selectbox("Y-Axis (Numeric Values)", num_cols if num_cols else cols)

        if st.button("Generate Dynamic Chart"):
            st.session_state.chart_config = {
                "type": chart_type,
                "x": x_col,
                "y": y_col,
            }
            st.success("Chart attached to workspace!")

        if st.session_state.chart_config:
            cfg = st.session_state.chart_config
            st.subheader(f"Dynamic {cfg['type']}: {cfg['y']} by {cfg['x']}")
            
            chart_data = df[[cfg['x'], cfg['y']]].dropna().set_index(cfg['x'])
            if cfg["type"] == "Bar Chart":
                st.bar_chart(chart_data)
            elif cfg["type"] == "Line Chart":
                st.line_chart(chart_data)
            elif cfg["type"] == "Area Chart":
                st.area_chart(chart_data)

# =============================================================================
# PAGE 4: FILE VAULT
# =============================================================================
elif selected_page == "📁 File Vault":
    st.header("Organization File Vault")
    saved_files = get_files(user)

    if not saved_files:
        st.info("No files stored in vault for your organization.")
    else:
        for fname, ftype, created, fjson in saved_files:
            col_a, col_b = st.columns([3, 1])
            col_a.markdown(f"**{fname}** (`.{ftype}`) — Saved on: {created}")
            if col_b.button(f"Load '{fname}'", key=f"btn_{fname}_{created}"):
                restored_df = dataframe_from_json(fjson)
                st.session_state.processed_df = restored_df
                st.session_state.raw_df = restored_df
                st.session_state.active_filename = fname
                st.success(f"Loaded {fname} from Vault!")
                st.rerun()

# =============================================================================
# PAGE 5: EXPORT CENTER
# =============================================================================
elif selected_page == "📥 Export Center":
    st.header("Export Center")
    df = st.session_state.processed_df

    if df is None:
        st.warning("No data available to export.")
    else:
        csv_data = df.to_csv(index=False).encode("utf-8")
        excel_data = make_excel(df)

        st.download_button(
            "📥 Download CSV Dataset",
            data=csv_data,
            file_name=f"{st.session_state.active_filename}_processed.csv",
            mime="text/csv",
        )

        st.download_button(
            "📥 Download Excel Workbook (.xlsx)",
            data=excel_data,
            file_name=f"{st.session_state.active_filename}_workbook.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

# =============================================================================
# PAGE 6: OVERALL ADMIN DI PORTAL (MASTER ONLY)
# =============================================================================
elif selected_page == "👑 Overall Admin DI Portal" and user["role"] == "master":
    st.header("👑 Overall Admin DI Portal")

    adm_tab1, adm_tab2, adm_tab3 = st.tabs(
        ["👥 Users Information Source", "✉️ Mail Source Page", "📜 System Activity"]
    )

    con = db()

    with adm_tab1:
        st.subheader("Overall Admin DI — Registered Users Source")
        users_df = pd.read_sql_query(
            "SELECT id, first_name, last_name, company_name, email, role, login_count, created_at, last_login FROM users",
            con,
        )
        st.dataframe(users_df, use_container_width=True)

    with adm_tab2:
        st.subheader("Overall Admin DI — Mail Source Logs")
        mails_df = pd.read_sql_query(
            "SELECT id, recipient_name, recipient_email, company_name, subject, sender_email, status, sent_at, body FROM emails_log ORDER BY id DESC",
            con,
        )
        st.dataframe(mails_df, use_container_width=True)

    with adm_tab3:
        st.subheader("System Activity Monitor")
        activity_df = pd.read_sql_query(
            "SELECT * FROM activity ORDER BY id DESC",
            con,
        )
        st.dataframe(activity_df, use_container_width=True)

    con.close()

# =============================================================================
# DI ASSISTANT DOCK
# =============================================================================
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("🤖 DI — David's Intelligence Assistant", expanded=False):
    for msg in st.session_state.chat_history:
        st.write(f"**{msg['sender']}**: {msg['text']}")

    di_input = st.text_input(
        "Ask DI something about your data or workspace...",
        placeholder="e.g., how many rows are in my dataset?",
        key="di_dock_input",
    )
    if st.button("Send to DI"):
        if di_input:
            st.session_state.chat_history.append({"sender": user["first_name"], "text": di_input})
            reply = di_reply(di_input, user, st.session_state.processed_df)
            st.session_state.chat_history.append({"sender": "DI", "text": reply})
            speak(reply)
            st.rerun()
