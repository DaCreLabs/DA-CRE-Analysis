import hashlib
import hmac
import io
import json
import os
import re
import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

# =============================================================================
# DACRE ANALYSIS ENGINE | DI = DAVID'S INTELLIGENCE
# Unified security foundation + High-End UI/UX
# =============================================================================

APP_NAME = "DACRE Analysis"
DI_NAME = "DI — David's Intelligence"
MASTER_USERNAME = "david"
MASTER_FULL_NAME = "David Emenike"


def get_master_passkey():
    env_value = os.getenv("DACRE_MASTER_PASSKEY")
    if env_value:
        return env_value
    try:
        secret_value = st.secrets.get("DACRE_MASTER_PASSKEY")
        if secret_value:
            return str(secret_value)
    except Exception:
        pass
    return ""


MASTER_PASSKEY = get_master_passkey()

BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "logo.png"
FAVICON_PATH = BASE_DIR / ".dacre_favicon.png"
DB_PATH = BASE_DIR / "dacre_platform.db"


# =============================================================================
# BRAND & FAVICON
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
        left = max(0, (crop.width - side) // 2)
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
# HIGH-END VISUAL SYSTEM & STYLING
# =============================================================================

st.markdown(
    """
    <style>
    /* Dark Radial Deep Ocean Theme */
    .stApp {
        background:
            radial-gradient(circle at 15% 0%, rgba(24,183,255,.12), transparent 28%),
            radial-gradient(circle at 90% 15%, rgba(255,193,7,.09), transparent 25%),
            linear-gradient(135deg, #050914, #091322 55%, #050914);
        color: #eef6ff;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #07101d, #050914);
        border-right: 1px solid rgba(24,183,255,.20);
    }

    /* Glassmorphism Cards */
    .dacre-hero {
        padding: 26px 30px;
        border-radius: 20px;
        border: 1px solid rgba(24,183,255,.35);
        background: linear-gradient(135deg, rgba(6,16,31,.92), rgba(10,28,47,.85));
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(8px);
        margin-bottom: 20px;
    }

    .gold-card {
        padding: 24px;
        border-radius: 20px;
        border: 1px solid rgba(255,193,7,.50);
        background: linear-gradient(145deg, #080704, #19140b);
        box-shadow: 0 0 30px rgba(255,193,7,.12);
        margin-bottom: 20px;
    }

    .metric-card {
        padding: 16px 20px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,.12);
        background: rgba(255,255,255,.03);
        backdrop-filter: blur(4px);
    }

    .badge {
        display: inline-block;
        padding: 4px 12px;
        margin: 2px;
        border-radius: 999px;
        border: 1px solid rgba(24,183,255,.30);
        background: rgba(24,183,255,.08);
        color: #18b7ff;
        font-size: 0.82rem;
        font-weight: 600;
    }

    .small-muted {
        color: #9db0c5;
        font-size: 0.88rem;
    }

    .success-glow {
        padding: 12px 16px;
        border-radius: 12px;
        border: 1px solid rgba(0,220,150,.35);
        background: rgba(0,220,150,.06);
        color: #00dc96;
    }

    /* Streamlit UI Tweaks */
    div.stButton > button {
        border-radius: 12px;
        border: 1px solid rgba(24,183,255,.40);
        background: linear-gradient(135deg, #0a2540, #0d3860);
        color: #ffffff;
        font-weight: 500;
        transition: all 0.25s ease;
    }
    div.stButton > button:hover {
        border-color: #18b7ff;
        box-shadow: 0 0 15px rgba(24,183,255,.40);
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def show_logo(width=210):
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=width)


# =============================================================================
# SECURE DATABASE LAYER (Context-Managed Contexts)
# =============================================================================

PBKDF2_ITERATIONS = 600_000
PBKDF2_ALGORITHM = "sha256"


def db():
    con = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=30)
    con.execute("PRAGMA foreign_keys = ON")
    con.execute("PRAGMA journal_mode = WAL")
    con.execute("PRAGMA busy_timeout = 30000")
    return con


def hash_password(value):
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac(
        PBKDF2_ALGORITHM,
        str(value).encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )
    return f"pbkdf2_{PBKDF2_ALGORITHM}${PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(value, stored_hash):
    if not stored_hash:
        return False, False

    if stored_hash.startswith("pbkdf2_sha256$"):
        try:
            _, iterations, salt_hex, digest_hex = stored_hash.split("$", 3)
            salt = bytes.fromhex(salt_hex)
            expected = bytes.fromhex(digest_hex)
            actual = hashlib.pbkdf2_hmac(
                "sha256",
                str(value).encode("utf-8"),
                salt,
                int(iterations),
            )
            return hmac.compare_digest(actual, expected), False
        except (ValueError, TypeError):
            return False, False

    legacy = hashlib.sha256(str(value).encode("utf-8")).hexdigest()
    if hmac.compare_digest(legacy, stored_hash):
        return True, True
    return False, False


def valid_password(value):
    value = str(value or "")
    return (
        len(value) >= 10
        and bool(re.search(r"[A-Z]", value))
        and bool(re.search(r"[a-z]", value))
        and bool(re.search(r"\d", value))
    )


def init_db():
    with db() as con:
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
        con.commit()


def ensure_master():
    if not MASTER_PASSKEY:
        return
    with db() as con:
        cur = con.cursor()
        row = cur.execute(
            "SELECT id FROM users WHERE username = ?", (MASTER_USERNAME,)
        ).fetchone()

        if not row:
            now = datetime.now().isoformat(timespec="seconds")
            cur.execute("""
                INSERT INTO users (
                    first_name, last_name, username, company_name, email,
                    password_hash, passkey_hash, role, login_count, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                "David", "Emenike", MASTER_USERNAME, "DACRE MASTER",
                "master@dacre.local", hash_password(MASTER_PASSKEY),
                hash_password(MASTER_PASSKEY), "master", 0, now
            ))
            con.commit()


init_db()
ensure_master()


def log_activity(username, company, action):
    with db() as con:
        con.execute("""
            INSERT INTO activity(username, company_name, action, created_at)
            VALUES (?, ?, ?, ?)
        """, (username, company, action, datetime.now().isoformat(timespec="seconds")))
        con.commit()


# =============================================================================
# AUTHENTICATION
# =============================================================================

def authenticate(username, password, passkey):
    username = str(username).strip().lower()

    with db() as con:
        row = con.execute("""
            SELECT first_name, last_name, username, company_name, email,
                   password_hash, passkey_hash, role
            FROM users
            WHERE lower(username) = lower(?)
        """, (username,)).fetchone()

        if not row:
            return None

        password_ok, password_legacy = verify_password(password, row[5])
        passkey_ok, passkey_legacy = verify_password(passkey, row[6])

        if not password_ok or not passkey_ok:
            return None

        now = datetime.now().isoformat(timespec="seconds")
        if password_legacy or passkey_legacy:
            con.execute("""
                UPDATE users
                SET password_hash = ?, passkey_hash = ?
                WHERE username = ?
            """, (hash_password(password), hash_password(passkey), row[2]))

        con.execute("""
            UPDATE users
            SET login_count = login_count + 1, last_login = ?
            WHERE username = ?
        """, (now, row[2]))
        con.commit()

    log_activity(row[2], row[3], "Signed in")

    return {
        "first_name": row[0],
        "last_name": row[1],
        "username": row[2],
        "company": row[3],
        "email": row[4],
        "role": row[7],
    }


def create_account(first, last, username, company, email, password, passkey):
    values = [first, last, username, company, email, password, passkey]
    if not all(str(v).strip() for v in values):
        return False, "Please complete every required field."

    username_clean = username.strip().lower()
    company_clean = company.strip()
    email_clean = email.strip().lower()

    if username_clean == MASTER_USERNAME:
        return False, "That username is reserved for Master David."

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email_clean):
        return False, "Please enter a valid email address."

    if not valid_password(password):
        return False, "Password must be at least 10 characters and include uppercase, lowercase, and a number."

    if len(passkey.strip()) < 8:
        return False, "Account Passkey must contain at least 8 characters."

    with db() as con:
        try:
            now = datetime.now().isoformat(timespec="seconds")
            cur = con.cursor()

            company_row = cur.execute(
                "SELECT id FROM companies WHERE lower(name) = lower(?)",
                (company_clean,),
            ).fetchone()

            if not company_row:
                cur.execute("""
                    INSERT INTO companies
                    (name, owner_username, admin_password_hash, created_at)
                    VALUES (?, ?, ?, ?)
                """, (company_clean, username_clean, hash_password(passkey), now))

            cur.execute("""
                INSERT INTO users
                (first_name, last_name, username, company_name, email,
                 password_hash, passkey_hash, role, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                first.strip(), last.strip(), username_clean, company_clean, email_clean,
                hash_password(password), hash_password(passkey), "company_admin", now
            ))

            con.commit()
            log_activity(username_clean, company_clean, "Created company account")
            return True, "Account created successfully."
        except sqlite3.IntegrityError:
            return False, "Username or email is already registered."


# =============================================================================
# DATA ENGINE
# =============================================================================

def load_dataframe(uploaded_file):
    ext = uploaded_file.name.rsplit(".", 1)[-1].lower()
    if ext == "csv":
        return pd.read_csv(uploaded_file)
    if ext == "tsv":
        return pd.read_csv(uploaded_file, sep="\t")
    if ext in ("xlsx", "xls"):
        return pd.read_excel(uploaded_file)
    if ext == "json":
        return pd.read_json(uploaded_file)
    raise ValueError(f"Unsupported file type: .{ext}")


def clean_dataframe(df):
    out = df.copy()
    out.columns = [
        re.sub(r"\s+", " ", str(col).strip()) if str(col).strip()
        else f"Column_{i + 1}"
        for i, col in enumerate(out.columns)
    ]

    out = out.dropna(axis=0, how="all").dropna(axis=1, how="all")

    for col in out.columns:
        if out[col].dtype == "object":
            series = out[col].astype(str).replace({"nan": ""}).str.strip()
            numeric_candidate = (
                series
                .str.replace(r"[\$€£₦,%]", "", regex=True)
                .str.replace(",", "", regex=False)
            )
            numeric = pd.to_numeric(numeric_candidate, errors="coerce")

            if numeric.notna().mean() >= 0.80 and series.ne("").any():
                out[col] = numeric
            else:
                out[col] = series

    return out.drop_duplicates().reset_index(drop=True)


def dataframe_to_json(df):
    if df is None:
        return ""
    return df.to_json(orient="split", date_format="iso")


def dataframe_from_json(value):
    if not value:
        return None
    try:
        return pd.read_json(io.StringIO(value), orient="split")
    except Exception:
        return None


def data_profile(df):
    if df is None:
        return None
    return {
        "Rows": len(df),
        "Columns": len(df.columns),
        "Duplicates": int(df.duplicated().sum()),
        "Missing Cells": int(df.isna().sum().sum()),
        "Numeric Columns": len(df.select_dtypes(include="number").columns),
        "Memory (KB)": round(df.memory_usage(deep=True).sum() / 1024, 1),
    }


def save_file(user, uploaded_file, df):
    with db() as con:
        con.execute("""
            INSERT INTO files
            (username, company_name, filename, file_type, file_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user["username"], user["company"], uploaded_file.name,
            uploaded_file.name.rsplit(".", 1)[-1].lower(),
            dataframe_to_json(df), datetime.now().isoformat(timespec="seconds"),
        ))
        con.commit()
    log_activity(user["username"], user["company"], f"Saved file: {uploaded_file.name}")


def get_files(user):
    with db() as con:
        if user["role"] in ("company_admin", "master"):
            rows = con.execute("""
                SELECT id, filename, file_type, created_at, file_json
                FROM files WHERE company_name = ? ORDER BY id DESC
            """, (user["company"],)).fetchall()
        else:
            rows = con.execute("""
                SELECT id, filename, file_type, created_at, file_json
                FROM files WHERE company_name = ? AND username = ? ORDER BY id DESC
            """, (user["company"], user["username"])).fetchall()
    return rows


def delete_file(file_id, user):
    with db() as con:
        if user["role"] in ("company_admin", "master"):
            con.execute("DELETE FROM files WHERE id = ? AND company_name = ?", (file_id, user["company"]))
        else:
            con.execute("DELETE FROM files WHERE id = ? AND company_name = ? AND username = ?", (file_id, user["company"], user["username"]))
        con.commit()
    log_activity(user["username"], user["company"], f"Deleted vault file ID {file_id}")


def save_project(user, raw_df, processed_df, filename, logs, chart_config=None):
    with db() as con:
        existing = con.execute("""
            SELECT id FROM projects WHERE username = ? AND company_name = ?
            ORDER BY id DESC LIMIT 1
        """, (user["username"], user["company"])).fetchone()

        payload = (
            user["username"], user["company"], "Main Workspace", filename or "",
            dataframe_to_json(raw_df), dataframe_to_json(processed_df),
            json.dumps(logs), json.dumps(chart_config or {}),
            datetime.now().isoformat(timespec="seconds"),
        )

        if existing:
            con.execute("""
                UPDATE projects
                SET project_name = ?, active_filename = ?, raw_json = ?,
                    processed_json = ?, formula_logs = ?, chart_config = ?,
                    updated_at = ?
                WHERE id = ?
            """, (payload[2], payload[3], payload[4], payload[5], payload[6], payload[7], payload[8], existing[0]))
        else:
            con.execute("""
                INSERT INTO projects
                (username, company_name, project_name, active_filename,
                 raw_json, processed_json, formula_logs, chart_config, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, payload)
        con.commit()


def restore_project(user):
    with db() as con:
        row = con.execute("""
            SELECT active_filename, raw_json, processed_json, formula_logs, chart_config
            FROM projects WHERE username = ? AND company_name = ? ORDER BY id DESC LIMIT 1
        """, (user["username"], user["company"])).fetchone()

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


# =============================================================================
# FORMULA ENGINE & SQL LAB
# =============================================================================

SHEET_FORMULAS = [
    "SUM", "AVERAGE", "COUNT", "COUNTA", "MAX", "MIN",
    "CONCATENATE", "UPPER", "LOWER", "TRIM"
]


def apply_formula(df, formula, options):
    formula = formula.upper()
    col = options.get("column")

    if formula == "SUM":
        return pd.to_numeric(df[col], errors="coerce").sum()
    if formula == "AVERAGE":
        return pd.to_numeric(df[col], errors="coerce").mean()
    if formula == "COUNT":
        return int(pd.to_numeric(df[col], errors="coerce").count())
    if formula == "COUNTA":
        return int(df[col].notna().sum())
    if formula == "MAX":
        return pd.to_numeric(df[col], errors="coerce").max()
    if formula == "MIN":
        return pd.to_numeric(df[col], errors="coerce").min()
    if formula == "CONCATENATE":
        first, second = options["first"], options["second"]
        sep, new_col = options.get("separator", " "), options["new_column"]
        result = df[first].fillna("").astype(str) + sep + df[second].fillna("").astype(str)
        return ("column", new_col, result)
    if formula in ("UPPER", "LOWER", "TRIM"):
        series = df[col].fillna("").astype(str)
        if formula == "UPPER":
            result = series.str.upper()
        elif formula == "LOWER":
            result = series.str.lower()
        else:
            result = series.str.strip()
        return ("column", col, result)
    return None


def run_sql_query(df, query):
    if df is None:
        raise ValueError("No active dataset.")

    query_clean = query.strip().rstrip(";")
    if not re.match(r"(?is)^\s*select\b", query_clean) or ";" in query_clean:
        raise ValueError("Only single SELECT queries are permitted in SQL Lab.")

    con = sqlite3.connect(":memory:")
    try:
        df.copy().to_sql("dataset", con, index=False, if_exists="replace")
        return pd.read_sql_query(query_clean, con)
    finally:
        con.close()


# =============================================================================
# EXCEL EXPORT WITH OPENPYXL
# =============================================================================

def openpyxl_ref(ws, col_idx, min_row, max_row):
    from openpyxl.chart.reference import Reference
    return Reference(ws, min_col=col_idx, max_col=col_idx, min_row=min_row, max_row=max_row)


def make_excel(processed_df, chart_df=None, chart_type="Bar Chart", x_col=None, y_col=None):
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        processed_df.to_excel(writer, sheet_name="Processed Data", index=False)

        if chart_df is not None:
            chart_df.to_excel(writer, sheet_name="Dynamic Chart Data", index=False)
            workbook = writer.book
            chart_sheet = workbook.create_sheet("Dynamic Chart")

            try:
                from openpyxl.chart import AreaChart, BarChart, LineChart, PieChart
                from openpyxl.chart.label import DataLabelList

                chart_data_sheet = workbook["Dynamic Chart Data"]
                if not x_col or not y_col:
                    raise ValueError("Chart columns are not configured.")

                x_idx = list(chart_df.columns).index(x_col) + 1
                y_idx = list(chart_df.columns).index(y_col) + 1
                max_row = len(chart_df) + 1

                if chart_type == "Pie Chart":
                    chart = PieChart()
                    labels = openpyxl_ref(chart_data_sheet, x_idx, 2, max_row)
                    data = openpyxl_ref(chart_data_sheet, y_idx, 1, max_row)
                    chart.add_data(data, titles_from_data=True)
                    chart.set_categories(labels)
                    chart.title = f"{y_col} by {x_col}"
                    chart.dataLabels = DataLabelList()
                    chart.dataLabels.showPercent = True
                else:
                    if chart_type == "Line Chart":
                        chart = LineChart()
                    elif chart_type == "Area Chart":
                        chart = AreaChart()
                    else:
                        chart = BarChart()
                        chart.type = "col"

                    data = openpyxl_ref(chart_data_sheet, y_idx, 1, max_row)
                    cats = openpyxl_ref(chart_data_sheet, x_idx, 2, max_row)
                    chart.add_data(data, titles_from_data=True)
                    chart.set_categories(cats)
                    chart.title = f"{y_col} by {x_col}"
                    chart.y_axis.title = y_col
                    chart.x_axis.title = x_col

                chart_sheet.add_chart(chart, "B2")
            except Exception:
                chart_sheet["A1"] = "Dynamic chart could not be embedded."
                chart_sheet["A2"] = "Use the Dynamic Chart Data sheet."

    output.seek(0)
    return output.getvalue()


# =============================================================================
# DI ASSISTANT
# =============================================================================

LANGUAGES = {
    "English": "en-NG",
    "Nigerian Pidgin": "en-NG",
    "Yoruba": "yo-NG",
    "Igbo": "ig-NG",
    "Hausa": "ha-NG",
    "French": "fr-FR",
    "German": "de-DE",
}


def di_reply(message, user, df):
    text = message.strip()
    low = text.lower()

    if not text:
        return "I am ready. Tell me what you want me to do."

    name = "Master David" if user["role"] == "master" else user["first_name"]
    profile = data_profile(df) if df is not None else None

    if any(x in low for x in ["hello", "hi", "good morning", "good day"]):
        return f"Good day {name}. DI is online and ready to work with your data."

    if "row count" in low or "how many rows" in low:
        return "No active dataset." if df is None else f"The active dataset contains {len(df):,} rows."

    if "column count" in low or "how many columns" in low:
        return "No active dataset." if df is None else f"The active dataset contains {len(df.columns):,} columns."

    if "profile" in low or "summary" in low:
        if not profile:
            return "There is no active dataset to profile."
        return f"Dataset profile: {profile['Rows']:,} rows, {profile['Columns']:,} columns, {profile['Duplicates']:,} duplicate rows, {profile['Missing Cells']:,} missing cells."

    if "clean" in low:
        return "Use Process & Clean Data. I will standardize headers, remove empty rows, normalize numbers, and drop duplicates."

    if "master" in low and user["role"] == "master":
        return "With all due respect, Master David, the sovereign DI portal is active."

    return f"DI received your request: '{text}'."


def speak(text, language="en-NG"):
    safe_text = json.dumps(str(text))
    safe_lang = json.dumps(language)
    components.html(
        f"""
        <script>
        const message = new SpeechSynthesisUtterance({safe_text});
        message.rate = 0.95;
        message.pitch = 0.82;
        message.lang = {safe_lang};
        if (window.speechSynthesis) {{
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(message);
        }}
        </script>
        """,
        height=0,
    )


# =============================================================================
# SESSION STATE & APP BOOTSTRAP
# =============================================================================

defaults = {
    "user": None,
    "page": "Workspace",
    "raw_df": None,
    "df": None,
    "active_filename": "",
    "formula_logs": [],
    "chart_config": {},
    "chat": [],
    "auth_mode": "Sign In",
    "language": "English",
    "last_clean_report": None,
    "last_sql_result": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def set_user(user):
    st.session_state.user = user
    restored = restore_project(user)
    st.session_state.raw_df = restored["raw"] if restored else None
    st.session_state.df = restored["processed"] if restored else None
    st.session_state.active_filename = restored["filename"] if restored else ""
    st.session_state.formula_logs = restored["logs"] if restored else []
    st.session_state.chart_config = restored["chart"] if restored else {}
    st.session_state.chat = []
    st.session_state.page = "Workspace"


# =============================================================================
# AUTHENTICATION UI
# =============================================================================

if st.session_state.user is None:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])

    with c2:
        show_logo(width=280)
        st.markdown(
            f"""
            <div class="dacre-hero">
                <h2>{APP_NAME}</h2>
                <p class="small-muted">{DI_NAME} — Enterprise Data & Analytics Engine</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        tab_signin, tab_signup = st.tabs(["🔒 Sign In", "📝 Create Company Account"])

        with tab_signin:
            with st.form("form_signin"):
                u = st.text_input("Username")
                p = st.text_input("Password", type="password")
                k = st.text_input("Passkey", type="password")
                sub = st.form_submit_button("Sign In to DACRE", use_container_width=True)

                if sub:
                    user = authenticate(u, p, k)
                    if user:
                        set_user(user)
                        st.rerun()
                    else:
                        st.error("Invalid credentials provided.")

        with tab_signup:
            with st.form("form_signup"):
                fn = st.text_input("First Name")
                ln = st.text_input("Last Name")
                un = st.text_input("Desired Username")
                cn = st.text_input("Company / Organization Name")
                em = st.text_input("Email Address")
                pw = st.text_input("Password (min 10 chars, uppercase, lowercase, digit)", type="password")
                pk = st.text_input("Account Passkey (min 8 chars)", type="password")
                sub_up = st.form_submit_button("Register Account", use_container_width=True)

                if sub_up:
                    ok, msg = create_account(fn, ln, un, cn, em, pw, pk)
                    if ok:
                        st.success(msg + " Please switch to the Sign In tab.")
                    else:
                        st.error(msg)
    st.stop()


# =============================================================================
# MAIN LOGGED-IN APPLICATION LAYOUT
# =============================================================================

user = st.session_state.user

# Sidebar Profile & Navigation
with st.sidebar:
    show_logo(width=180)
    st.markdown(
        f"""
        <div style="margin-top: 15px; margin-bottom: 20px;">
            <div style="font-weight:700; font-size:1.1rem; color:#eef6ff;">{user['first_name']} {user['last_name']}</div>
            <div class="small-muted">{user['company']} • <span class="badge">{user['role'].upper()}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    nav_options = ["Workspace", "SQL Lab", "Chart Studio", "Data Vault", "Export Center"]
    if user["role"] in ("company_admin", "master"):
        nav_options.append("Admin Console")

    st.session_state.page = st.radio("Navigation", nav_options, index=nav_options.index(st.session_state.page) if st.session_state.page in nav_options else 0)

    st.markdown("---")
    st.session_state.language = st.selectbox("DI Voice Locale", list(LANGUAGES.keys()))

    if st.button("🚪 Sign Out", use_container_width=True):
        st.session_state.user = None
        st.rerun()


# =============================================================================
# PAGE 1: WORKSPACE & DATA STUDIO
# =============================================================================

if st.session_state.page == "Workspace":
    st.markdown(
        f"""
        <div class="dacre-hero">
            <h1>Workspace & Data Studio</h1>
            <p class="small-muted">Ingest, clean, profile, and transform datasets with the DACRE engine.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    file_up = st.file_uploader("Upload Dataset (CSV, TSV, XLSX, JSON)", type=["csv", "tsv", "xlsx", "xls", "json"])

    if file_up:
        try:
            raw = load_dataframe(file_up)
            st.session_state.raw_df = raw
            st.session_state.df = raw.copy()
            st.session_state.active_filename = file_up.name
            save_file(user, file_up, raw)
            save_project(user, raw, raw, file_up.name, st.session_state.formula_logs)
            st.success(f"Successfully loaded and backed up '{file_up.name}'!")
        except Exception as e:
            st.error(f"Error reading file: {e}")

    df = st.session_state.df

    if df is not None:
        prof = data_profile(df)
        cols = st.columns(6)
        cols[0].metric("Rows", f"{prof['Rows']:,}")
        cols[1].metric("Columns", f"{prof['Columns']:,}")
        cols[2].metric("Duplicates", f"{prof['Duplicates']:,}")
        cols[3].metric("Missing Cells", f"{prof['Missing Cells']:,}")
        cols[4].metric("Numeric Cols", f"{prof['Numeric Columns']:,}")
        cols[5].metric("Memory (KB)", f"{prof['Memory (KB)']}")

        st.markdown("### Process & Standardize Data")
        if st.button("✨ Run Standard Data Cleaning"):
            cleaned = clean_dataframe(df)
            st.session_state.df = cleaned
            save_project(user, st.session_state.raw_df, cleaned, st.session_state.active_filename, st.session_state.formula_logs)
            st.success("Dataset cleaned: Stripped currency symbols, trimmed whitespace, and dropped empty rows/columns.")
            st.rerun()

        st.markdown("### Active Dataset Preview")
        st.dataframe(df, use_container_width=True, height=350)

        st.markdown("### Formula Engine")
        c1, c2 = st.columns([1, 2])
        with c1:
            formula_choice = st.selectbox("Select Formula", SHEET_FORMULAS)
            options = {}

            if formula_choice in ("SUM", "AVERAGE", "COUNT", "COUNTA", "MAX", "MIN", "UPPER", "LOWER", "TRIM"):
                options["column"] = st.selectbox("Target Column", df.columns)
            elif formula_choice == "CONCATENATE":
                options["first"] = st.selectbox("First Column", df.columns)
                options["second"] = st.selectbox("Second Column", df.columns)
                options["separator"] = st.text_input("Separator", " ")
                options["new_column"] = st.text_input("New Column Name", "Combined")

            if st.button("Apply Formula"):
                res = apply_formula(df, formula_choice, options)
                if isinstance(res, tuple) and res[0] == "column":
                    _, col_name, new_series = res
                    df[col_name] = new_series
                    st.session_state.df = df
                    st.session_state.formula_logs.append(f"Applied {formula_choice} to column '{col_name}'")
                    save_project(user, st.session_state.raw_df, df, st.session_state.active_filename, st.session_state.formula_logs)
                    st.success(f"Column '{col_name}' created/updated!")
                    st.rerun()
                elif res is not None:
                    st.session_state.formula_logs.append(f"{formula_choice} on {options.get('column')}: {res}")
                    st.info(f"Result of **{formula_choice}**: `{res}`")

        with c2:
            st.markdown("#### Formula Application Audit Log")
            if st.session_state.formula_logs:
                for log in reversed(st.session_state.formula_logs):
                    st.markdown(f"- `{log}`")
            else:
                st.caption("No formulas executed yet.")
    else:
        st.info("Upload a dataset or restore a project from the Data Vault to get started.")


# =============================================================================
# PAGE 2: SQL LAB
# =============================================================================

elif st.session_state.page == "SQL Lab":
    st.markdown(
        f"""
        <div class="dacre-hero">
            <h1>SQL Lab</h1>
            <p class="small-muted">Execute read-only SQL queries against your active dataset in real-time (`FROM dataset`).</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df = st.session_state.df
    if df is None:
        st.warning("Please upload a dataset in the Workspace first.")
    else:
        query = st.text_area("SQL Query", "SELECT * FROM dataset LIMIT 10;", height=120)
        if st.button("Run Query"):
            try:
                res = run_sql_query(df, query)
                st.session_state.last_sql_result = res
                st.success(f"Query executed successfully! Returned {len(res)} rows.")
            except Exception as e:
                st.error(f"SQL Execution Error: {e}")

        if st.session_state.last_sql_result is not None:
            st.dataframe(st.session_state.last_sql_result, use_container_width=True)


# =============================================================================
# PAGE 3: CHART STUDIO
# =============================================================================

elif st.session_state.page == "Chart Studio":
    st.markdown(
        f"""
        <div class="dacre-hero">
            <h1>Dynamic Chart Studio</h1>
            <p class="small-muted">Build charts that render dynamically in app and export natively into Excel.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df = st.session_state.df
    if df is None:
        st.warning("Please upload a dataset in the Workspace first.")
    else:
        c1, c2 = st.columns([1, 2])
        with c1:
            chart_type = st.selectbox("Chart Type", ["Bar Chart", "Line Chart", "Area Chart", "Pie Chart"])
            x_col = st.selectbox("X-Axis (Categories)", df.columns)
            y_col = st.selectbox("Y-Axis (Values)", df.select_dtypes(include="number").columns)

            agg_func = st.selectbox("Aggregation", ["Sum", "Mean", "Count", "Max", "Min"])

            if agg_func == "Sum":
                chart_df = df.groupby(x_col, as_index=False)[y_col].sum()
            elif agg_func == "Mean":
                chart_df = df.groupby(x_col, as_index=False)[y_col].mean()
            elif agg_func == "Count":
                chart_df = df.groupby(x_col, as_index=False)[y_col].count()
            elif agg_func == "Max":
                chart_df = df.groupby(x_col, as_index=False)[y_col].max()
            else:
                chart_df = df.groupby(x_col, as_index=False)[y_col].min()

            st.session_state.chart_config = {
                "chart_type": chart_type,
                "x_col": x_col,
                "y_col": y_col,
                "chart_df": chart_df,
            }
            save_project(user, st.session_state.raw_df, df, st.session_state.active_filename, st.session_state.formula_logs, st.session_state.chart_config)

        with c2:
            if chart_type == "Bar Chart":
                st.bar_chart(chart_df.set_index(x_col)[y_col])
            elif chart_type in ("Line Chart", "Area Chart"):
                st.line_chart(chart_df.set_index(x_col)[y_col])
            else:
                st.dataframe(chart_df, use_container_width=True)


# =============================================================================
# PAGE 4: DATA VAULT
# =============================================================================

elif st.session_state.page == "Data Vault":
    st.markdown(
        f"""
        <div class="dacre-hero">
            <h1>Data Vault</h1>
            <p class="small-muted">Isolated multi-tenant cloud storage for company datasets.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    files = get_files(user)
    if not files:
        st.info("No files stored in your vault yet.")
    else:
        for file_id, fname, ftype, created_at, fjson in files:
            cols = st.columns([3, 2, 1, 1])
            cols[0].markdown(f"**{fname}** (`.{ftype}`)")
            cols[1].caption(f"Uploaded: {created_at}")

            if cols[2].button("Load", key=f"load_{file_id}"):
                loaded_df = dataframe_from_json(fjson)
                st.session_state.raw_df = loaded_df
                st.session_state.df = loaded_df
                st.session_state.active_filename = fname
                save_project(user, loaded_df, loaded_df, fname, st.session_state.formula_logs)
                st.success(f"Loaded '{fname}' into Workspace.")
                st.rerun()

            if cols[3].button("Delete", key=f"del_{file_id}"):
                delete_file(file_id, user)
                st.success("File deleted.")
                st.rerun()


# =============================================================================
# PAGE 5: EXPORT CENTER
# =============================================================================

elif st.session_state.page == "Export Center":
    st.markdown(
        f"""
        <div class="dacre-hero">
            <h1>Export Center</h1>
            <p class="small-muted">Download complete workbooks featuring openpyxl dynamic chart embedding.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df = st.session_state.df
    if df is None:
        st.warning("No processed dataset available to export.")
    else:
        chart_cfg = st.session_state.chart_config
        chart_df = chart_cfg.get("chart_df")
        c_type = chart_cfg.get("chart_type", "Bar Chart")
        x_c = chart_cfg.get("x_col")
        y_c = chart_cfg.get("y_col")

        excel_data = make_excel(df, chart_df=chart_df, chart_type=c_type, x_col=x_c, y_col=y_c)

        st.download_button(
            label="📥 Download Fully Formatted Excel Workbook",
            data=excel_data,
            file_name=f"DACRE_Export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )


# =============================================================================
# PAGE 6: ADMIN CONSOLE
# =============================================================================

elif st.session_state.page == "Admin Console" and user["role"] in ("company_admin", "master"):
    st.markdown(
        f"""
        <div class="gold-card">
            <h2>👑 Admin Console</h2>
            <p class="small-muted">Manage company users, audit system activity, and view multi-tenant controls.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_users, tab_audit = st.tabs(["👥 Company Users", "📜 Activity Audit Log"])

    with tab_users:
        with db() as con:
            users_df = pd.read_sql_query(
                "SELECT first_name, last_name, username, email, role, login_count, created_at, last_login FROM users WHERE company_name = ?",
                con, params=(user["company"],)
            )
        st.dataframe(users_df, use_container_width=True)

    with tab_audit:
        with db() as con:
            logs_df = pd.read_sql_query(
                "SELECT username, action, created_at FROM activity WHERE company_name = ? ORDER BY id DESC LIMIT 100",
                con, params=(user["company"],)
            )
        st.dataframe(logs_df, use_container_width=True)


# =============================================================================
# PERSISTENT FLOATING DI ASSISTANT DOCK
# =============================================================================

st.markdown("<br><br><br>", unsafe_allow_html=True)
with st.expander("🤖 DI — David's Intelligence (Assistant & Voice Hub)", expanded=False):
    st.markdown(f"**Locale Active:** `{st.session_state.language}` ({LANGUAGES[st.session_state.language]})")

    chat_input = st.text_input("Ask DI a question or command...", key="di_input_box")
    if st.button("Send to DI"):
        if chat_input.strip():
            reply = di_reply(chat_input, user, st.session_state.df)
            st.session_state.chat.append(("user", chat_input))
            st.session_state.chat.append(("di", reply))
            speak(reply, LANGUAGES[st.session_state.language])

    for sender, msg in reversed(st.session_state.chat):
        if sender == "user":
            st.markdown(f"**You:** {msg}")
        else:
            st.markdown(f"**DI:** {msg}")
